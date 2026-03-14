from __future__ import annotations

import importlib
import sys
from pathlib import Path


DEFAULT_CONFIG = "comfy-blender-vrm.json"


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").exists() and (candidate / "docs").is_dir():
            return candidate
    raise RuntimeError("Repository root not found from compatibility wrapper location.")


def canonical_scripts_dir(repo_root: Path) -> Path:
    return repo_root / ".codex" / "skills" / "kyarakuri-comfy-blender-vrm" / "scripts"


def inject_default_config(arguments: list[str], repo_root: Path) -> list[str]:
    if "--config" in arguments:
        return arguments
    return [*arguments, "--config", str(repo_root / "config" / DEFAULT_CONFIG)]


def run_canonical_main(module_name: str) -> int:
    repo_root = find_repo_root(Path(__file__).resolve())
    scripts_dir = canonical_scripts_dir(repo_root)
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    forwarded_args = inject_default_config(list(sys.argv[1:]), repo_root)
    original_argv = sys.argv[:]
    try:
        sys.argv = [sys.argv[0], *forwarded_args]
        module = importlib.import_module(module_name)
        result = module.main()
    finally:
        sys.argv = original_argv

    return int(result) if isinstance(result, int) else 0
