"""Author-side checker/packager. Never used to inspect uploads in the host."""
from __future__ import annotations
import argparse
import ast
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib
import zipfile

REQUIRED = ("plugin.py", "plugin.json", "pyproject.toml", "uv.lock")
EXCLUDED = {".git", ".venv", "__pycache__", "node_modules", ".mypy_cache", ".pytest_cache", ".env", "mt_plugin"}


def include_paths(root: Path, project: dict) -> list[str]:
    includes = project.get("tool", {}).get("mt-plugin", {}).get("include")
    if includes is None:
        return [*REQUIRED, *(name for name in ("ui", "prompts") if (root / name).exists())]
    if not isinstance(includes, list) or not includes:
        raise ValueError("pyproject.toml: tool.mt-plugin.include must be a non-empty list of file/directory paths")
    for index, name in enumerate(includes):
        location = f"pyproject.toml: tool.mt-plugin.include[{index}]"
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{location}: must be a non-empty path")
        if any(char in name for char in "*?[]{}"):
            raise ValueError(f"{location}: glob patterns are not supported; use a directory such as 'core' or 'ui' (collected recursively)")
        path = Path(name)
        if path.is_absolute() or ".." in path.parts or "\\" in name or ":" in name or "\x00" in name:
            raise ValueError(f"{location}: must be a relative path inside the project")
        if any(part in EXCLUDED or part.startswith(".env") for part in path.parts) or name == "release.json":
            raise ValueError(f"{location}: reserved development/host path cannot be included")
    return includes


def collect_files(root: Path, includes: list[str], manifest: dict) -> set[Path]:
    root = root.resolve()
    files: set[Path] = set()
    for index, name in enumerate(includes):
        location = f"pyproject.toml: tool.mt-plugin.include[{index}] ({name!r})"
        path = root / name
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root and parent.is_relative_to(root)):
            raise ValueError(f"{location}: symlinks cannot be packaged")
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"{location}: path escapes the project")
        if not path.exists():
            raise ValueError(f"{location}: path does not exist")
        candidates: list[Path] = [path] if path.is_file() else []
        if path.is_dir():
            for directory, subdirs, names in os.walk(path, followlinks=False):
                # Excluded environment/cache trees are never traversed.
                subdirs[:] = [d for d in subdirs if d not in EXCLUDED and not d.startswith(".env")]
                for subdir in subdirs:
                    if (Path(directory) / subdir).is_symlink():
                        raise ValueError(f"{location}: symlink directory cannot be packaged")
                candidates.extend(Path(directory) / file for file in names)
        for candidate in candidates:
            relative = candidate.relative_to(root)
            if any(part in EXCLUDED or part.startswith(".env") for part in relative.parts) or candidate.suffix in (".pyc", ".pyo"):
                continue
            if candidate.is_symlink() or not candidate.resolve().is_relative_to(root):
                raise ValueError(f"{location}: symlink file cannot be packaged")
            if relative.as_posix() == "release.json":
                raise ValueError(f"{location}: release.json is reserved for the host")
            if candidate.is_file():
                files.add(candidate)
    for name in REQUIRED:
        if root / name not in files:
            raise ValueError(f"pyproject.toml: tool.mt-plugin.include: required package file excluded: {name}")
    ui = manifest["ui"]
    for name in [*ui.get("assets", []), ui.get("icon"), ui.get("entry")]:
        if name and root / name not in files:
            raise ValueError(f"plugin.json: ui: declared resource is not packaged: {name}")
    if len(files) > 1000 or sum(file.stat().st_size for file in files) > 200 * 1024 * 1024:
        raise ValueError("Unpacked package exceeds 1000 files or 200 MiB")
    return files


def check(root: Path, manifest: dict) -> None:
    assert sys.version_info[:2] == (3, 12), "Use Python 3.12"
    assert manifest["sdkVersion"] == "2" and manifest["entry"] == "plugin.py:Plugin"
    assert manifest["ui"]["mode"] in ("python", "react") and manifest["ui"]["version"] == "2"
    assert manifest["ui"].get("entry", "") == ("ui/remoteEntry.js" if manifest["ui"]["mode"] == "react" else ""), "Invalid UI entry"
    methods = json.loads(Path(__file__).with_name("methods.json").read_text("utf-8"))["methods"]
    permissions = {m["permission"] for m in methods if m["permission"]} | {"organize.submit"}
    assert set(manifest.get("permissions", [])) <= permissions, "Unknown host permission"
    # Check declarations without executing arbitrary author code during this step.
    tree = ast.parse((root / "plugin.py").read_text("utf-8"))
    plugin = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "Plugin")
    registered: set[tuple[str, str]] = set()
    for node in plugin.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and isinstance(decorator.func, ast.Name) and decorator.func.id in ("action", "query", "continuation"):
                    pair = (decorator.func.id, ast.literal_eval(decorator.args[0]))
                    assert pair not in registered, "Duplicate handler"
                    registered.add(pair)
    expected = {("continuation" if a.get("kind") == "continuation" else "action", a["id"]) for a in manifest["actions"]}
    expected |= {("query", q["id"]) for q in manifest.get("queries", [])}
    assert len(expected) == len(manifest["actions"]) + len(manifest.get("queries", [])), "Duplicate declaration"
    if expected != registered:
        from .worker import HandlerMismatch
        raise HandlerMismatch(expected, registered)
    from .schema import validate_schema_definition, validate
    validate_schema_definition(manifest.get("configSchema"))
    config_schema = manifest.get("configSchema")
    if config_schema and config_schema.get("type") == "object":
        for index, field in enumerate(manifest.get("config", [])):
            key = field["key"]
            if key not in config_schema.get("properties", {}) and not config_schema.get("additionalProperties", False):
                raise ValueError(f"plugin.json: config[{index}].key: {key!r} is not declared in configSchema.properties")
            if "default" in field:
                try:
                    validate(config_schema.get("properties", {}).get(key), field["default"])
                except ValueError as error:
                    raise ValueError(f"plugin.json: config[{index}].default: does not satisfy configSchema.properties.{key}") from error
    for item in [*manifest["actions"], *manifest.get("queries", [])]:
        validate_schema_definition(item.get("inputSchema"))
        validate_schema_definition(item.get("outputSchema"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["pack", "check"], nargs="?", default="pack")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest = json.loads((root / "plugin.json").read_text("utf-8"))
    project = tomllib.loads((root / "pyproject.toml").read_text("utf-8"))
    includes = include_paths(root, project)
    check(root, manifest)
    uv = shutil.which("uv")
    assert uv, "Install uv==0.6.7 for reproducible dependency locking"
    assert subprocess.check_output([uv, "--version"], text=True).startswith("uv 0.6.7 "), "Use uv==0.6.7"
    subprocess.run([uv, "lock", "--python", sys.executable, "--no-sources", "--index-url", "https://pypi.org/simple"], cwd=root, check=True)
    from .dependencies import validate_dependencies
    validate_dependencies(root)
    # Import in an isolated child: author checks may execute author code, but never
    # call lifecycle hooks. The host's inspection path only reads package data.
    subprocess.run([sys.executable, "-I", "-B", "-c",
                    "import sys,json;from pathlib import Path;sys.path.insert(0,sys.argv[1]);"
                    "from mt_plugin.worker import load_plugin;root=Path(sys.argv[2]);"
                    "load_plugin(root,json.loads((root/'plugin.json').read_text('utf-8')))",
                    str(Path(__file__).resolve().parent.parent), str(root)], cwd=root, check=True, timeout=30)
    # Full Python type checking occurs locally; runtime installations omit these tools.
    env = {**os.environ, "MYPYPATH": str(Path(__file__).resolve().parent.parent)}
    subprocess.run([sys.executable, "-m", "mypy", "--check-untyped-defs", "--follow-imports=silent", "--ignore-missing-imports", "plugin.py"], cwd=root, env=env, check=True)
    if manifest["ui"]["mode"] == "react":
        node, npm = shutil.which("node"), shutil.which("npm.cmd" if os.name == "nt" else "npm")
        assert node and npm, "React authors need Node 22.12+ and npm"
        version = subprocess.check_output([node, "-p", "process.versions.node"], text=True).strip()
        major, minor, *_ = map(int, version.split("."))
        assert major > 22 or major == 22 and minor >= 12, "Node 22.12+ required"
        subprocess.run([npm, "run", "build"], cwd=root / "frontend", check=True)
        assert (root / manifest["ui"]["entry"]).is_file(), "React build must produce ui/remoteEntry.js"
    files = collect_files(root, includes, manifest)
    if args.command == "check":
        print("Entry, schemas, types and dependency lock checked")
        return
    output = (args.output or root / "dist" / f'{manifest["id"]}-{manifest["version"]}.zip').resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(dir=output.parent, prefix="mt-pack-", suffix=".zip", delete=False) as temp:
        candidate_output = Path(temp.name)
    try:
        with zipfile.ZipFile(candidate_output, "w", zipfile.ZIP_DEFLATED) as archive:
            for file in sorted(files):
                assert file.resolve().is_relative_to(root) and not file.is_symlink(), "Package file changed"
                archive.write(file, file.relative_to(root).as_posix())
        assert candidate_output.stat().st_size <= 40 * 1024 * 1024, "ZIP exceeds 40 MiB"
        os.replace(candidate_output, output)
    finally:
        candidate_output.unlink(missing_ok=True)
    print(output)


if __name__ == "__main__":
    main()
