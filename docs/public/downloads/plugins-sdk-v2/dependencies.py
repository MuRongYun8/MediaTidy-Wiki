"""Validate dependency metadata as data, without importing a plugin or build backend."""
from __future__ import annotations

from pathlib import Path
import json
import re
import sys
import tomllib
from urllib.parse import urlsplit

SDK_NAMES = {"mt-plugin", "mediatidy-plugin-sdk"}


def normalized(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


class DependencyError(ValueError):
    """Only host-authored metadata diagnostics may cross the public boundary."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise DependencyError(message)


def read_metadata(root: Path, name: str) -> dict:
    try:
        return tomllib.loads((root / name).read_text("utf-8"))
    except tomllib.TOMLDecodeError as error:
        position = re.search(r"\(at line (\d+), column (\d+)\)", str(error))
        suffix = f" (line {position[1]}, column {position[2]})" if position else ""
        raise DependencyError(name + ": invalid TOML syntax" + suffix) from None
    except (OSError, UnicodeError):
        raise DependencyError(name + ": missing, unreadable or not UTF-8") from None


def validate_dependencies(root: Path) -> None:
    try:
        _validate_dependencies(root)
    except DependencyError:
        raise
    except (KeyError, TypeError, AttributeError, ValueError):
        raise DependencyError("pyproject.toml / uv.lock: invalid metadata structure or field type") from None


def _validate_dependencies(root: Path) -> None:
    require(sys.version_info[:2] == (3, 12), "Python 3.12 is required")
    project = read_metadata(root, "pyproject.toml")
    lock = read_metadata(root, "uv.lock")
    meta = project["project"]
    require(re.sub(r"\s+", "", meta["requires-python"]) in (">=3.12,<3.13", "==3.12.*"),
            "pyproject.toml: project.requires-python must select Python 3.12")
    require(not (root / "uv.toml").exists(), "uv.toml is unsupported; use pyproject.toml")
    tool = project.get("tool", {}).get("uv", {})
    require(not set(tool) - {"package", "dev-dependencies"}, "pyproject.toml: tool.uv contains unsupported sources or installation options")
    require(not tool.get("package", False), "pyproject.toml: tool.uv.package must be false")
    name = normalized(meta["name"])
    require(name not in SDK_NAMES, "pyproject.toml / uv.lock: host SDK cannot be replaced")
    dependencies = list(meta.get("dependencies", []))
    for group in meta.get("optional-dependencies", {}).values():
        dependencies.extend(group)
    dependencies.extend(tool.get("dev-dependencies", []))
    for group in project.get("dependency-groups", {}).values():
        dependencies.extend(dep for dep in group if isinstance(dep, str))
    for dep in dependencies:
        require(not any(char in dep for char in ("@", "://", "file:")), "pyproject.toml: URL/path dependencies are unsupported")
        match = re.match(r"^\s*([A-Za-z0-9][A-Za-z0-9._-]*)", dep)
        require(match is not None and normalized(match[1]) not in SDK_NAMES, "pyproject.toml / uv.lock: host SDK cannot be replaced")
    packages = lock.get("package", [])
    require(bool(packages), "uv.lock: package must contain the virtual project")
    roots = 0
    for package in packages:
        package_name = normalized(package["name"])
        require(package_name not in SDK_NAMES, "pyproject.toml / uv.lock: host SDK cannot be replaced")
        source = package.get("source", {})
        if source == {"virtual": "."}:
            require(package_name == name, "uv.lock: virtual project name must match pyproject.toml project.name")
            roots += 1
            continue
        require(source == {"registry": "https://pypi.org/simple"}, "uv.lock: package.source must use public PyPI")
        wheels = package.get("wheels", [])
        require(bool(wheels), "uv.lock: dependency has no prebuilt wheels")
        for artifact in [*wheels, *([package["sdist"]] if "sdist" in package else [])]:
            url = urlsplit(artifact["url"])
            require(url.scheme == "https" and url.netloc == "files.pythonhosted.org" and not url.query and not url.fragment,
                    "uv.lock: artifact URL must use files.pythonhosted.org without query or fragment")
            require(re.fullmatch(r"sha256:[a-f0-9]{64}", artifact["hash"]) is not None, "uv.lock: artifact.hash must be sha256 followed by 64 lowercase hexadecimal digits")
    require(roots == 1, "uv.lock: package must contain exactly one virtual project")


if __name__ == "__main__":
    try:
        validate_dependencies(Path(sys.argv[1]))
    except DependencyError as error:
        print("MT_DEPENDENCY_ERROR " + json.dumps({"message": str(error)}, ensure_ascii=True), flush=True)
        sys.exit(1)
    print("Python 3.12 / PyPI wheel lock checked")
