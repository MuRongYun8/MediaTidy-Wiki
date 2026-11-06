"""Strict, offline fixtures for testing trusted plugin handlers.

This transport checks the public contract; it does not emulate MT's business
services, filesystem permissions, task execution or lifecycle implementation.
"""
from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from typing import Any, Callable, Mapping

from .core import SDKError

Fixture = Any | Callable[[dict[str, Any]], Any]


def _validate(schema: dict, value: Any, path: str, code: str) -> None:
    def fail(reason: str, location: str = path) -> None:
        raise SDKError(reason, code, path=location)

    if schema.get('anyOf'):
        for variant in schema['anyOf']:
            try:
                _validate(variant, value, path, code)
                return
            except SDKError:
                pass
        fail('Value does not match any contract variant')

    kind = schema.get('type')
    if 'enum' in schema and value not in schema['enum']:
        fail('Value is not in the contract enum')
    valid_type = {
        'object': isinstance(value, dict), 'array': isinstance(value, list),
        'string': isinstance(value, str), 'boolean': type(value) is bool,
        'integer': type(value) is int, 'number': type(value) in (int, float), 'null': value is None,
    }
    if kind and not valid_type.get(kind, False):
        fail('Value does not match the contract type')
    if kind == 'object':
        properties = schema.get('properties', {})
        for key in schema.get('required', []):
            if key not in value:
                fail('Required field is missing', f'{path}.{key}')
        for key, item in value.items():
            if key not in properties and not schema.get('additionalProperties', False):
                fail('Unknown contract field', f'{path}.{key}')
            _validate(properties.get(key, {}), item, f'{path}.{key}', code)
    if kind == 'array':
        if len(value) < schema.get('minItems', 0) or len(value) > schema.get('maxItems', 10000):
            fail('Array exceeds contract bounds')
        for index, item in enumerate(value):
            _validate(schema.get('items', {}), item, f'{path}[{index}]', code)
    if kind == 'string' and (len(value) < schema.get('minLength', 0) or len(value) > schema.get('maxLength', len(value))):
        fail('String exceeds contract bounds')
    if kind in ('number', 'integer') and (value < schema.get('minimum', float('-inf')) or value > schema.get('maximum', float('inf'))):
        fail('Number exceeds contract bounds')


class ContractTransport:
    """A Context-compatible transport with explicit responses and injected errors.

    Pass a manifest to check declarations, granted capabilities to check grants,
    and resources to check root/profile IDs. Omitted grants/resources do not
    pretend to verify authority; real authorization remains a host integration test.
    Unconfigured methods fail rather than accessing a real service.
    """
    def __init__(self, responses: Mapping[str, Fixture] | None = None, *,
                 manifest: Mapping[str, Any] | None = None, grants: Mapping[str, Any] | None = None,
                 invocation_mode: str = 'action'):
        contract = json.loads(Path(__file__).with_name('methods.json').read_text('utf-8'))
        self.methods = {method['name']: method for method in contract['methods']}
        self.responses = dict(responses or {})
        self.manifest, self.grants = manifest, grants
        self.invocation_mode = invocation_mode
        self.calls: list[tuple[str, dict[str, Any]]] = []
        self.counts: dict[str, int] = {}

    def call(self, invocation: str, name: str, value: dict[str, Any]) -> Any:
        definition = self.methods.get(name)
        if definition is None:
            raise SDKError('Unknown SDK method', 'PERMISSION_DENIED')
        mode = 'action' if self.invocation_mode == 'continuation' else self.invocation_mode
        if mode not in definition['contexts']:
            raise SDKError('Method is unavailable in this invocation mode', 'CONTEXT_DENIED', path='runtime.invocationMode')
        permission = definition['permission']
        if permission and self.manifest is not None and permission not in self.manifest.get('permissions', []):
            raise SDKError('Capability is not declared', 'PERMISSION_DENIED', path='manifest.permissions')
        if permission and self.grants is not None and permission not in self.grants.get('capabilities', []):
            raise SDKError('Capability is not granted', 'PERMISSION_DENIED', path='grants.capabilities')
        try:
            json.dumps(value, allow_nan=False)
        except (ValueError, TypeError):
            raise SDKError('Request is not valid JSON', 'INVALID_ARGUMENT', path='input') from None
        _validate(definition['input'], value, 'input', 'INVALID_ARGUMENT')
        if self.grants is not None:
            if name in ('files.list', 'files.stat', 'files.scan', 'files.search'):
                roots = self.grants.get('roots', [])
                if not any(root.get('id') == value.get('rootId') and root.get('read') for root in roots):
                    raise SDKError('Root is not granted for reading', 'PERMISSION_DENIED', path='input.rootId')
            if name == 'organize.manual.run' and value.get('profileId') not in self.grants.get('profileIds', []):
                raise SDKError('Organize profile is not granted', 'PERMISSION_DENIED', path='input.profileId')
        self.counts[name] = self.counts.get(name, 0) + 1
        if self.counts[name] > definition['limit']:
            raise SDKError('Per-run call limit exceeded', 'QUOTA_EXCEEDED')
        if name not in self.responses:
            raise SDKError('No offline response fixture configured', 'FIXTURE_MISSING')
        self.calls.append((name, deepcopy(value)))
        response = self.responses[name]
        if isinstance(response, SDKError):
            raise response
        result = response(deepcopy(value)) if callable(response) else deepcopy(response)
        if isinstance(result, SDKError):
            raise result
        try:
            json.dumps(result, allow_nan=False)
        except (ValueError, TypeError):
            raise SDKError('Fixture response is not valid JSON', 'INVALID_RESPONSE', path='output') from None
        _validate(definition['output'], result, 'output', 'INVALID_RESPONSE')
        return result
