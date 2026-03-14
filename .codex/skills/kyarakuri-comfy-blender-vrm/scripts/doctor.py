from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib import error, request


REQUIRED_KEYS = ("comfyui_url", "blender_path", "workflow_dir", "output_dir")
COMFYUI_PROBES = ("/system_stats", "/queue")


@dataclass
class SettingResult:
    key: str
    raw_value: str
    resolved_value: str
    ok: bool
    detail: str
    next_action: str | None = None


@dataclass
class CheckResult:
    name: str
    ok: bool
    detail: str
    next_action: str | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the local ComfyUI and Blender setup for the kyarakuri-comfy-blender-vrm skill."
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to the config JSON file. Defaults to config/kyarakuri-comfy-blender-vrm.json under the repository root.",
    )
    return parser.parse_args()


def find_repo_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / "AGENTS.md").exists() and (candidate / "docs").is_dir():
            return candidate
    raise RuntimeError("Repository root not found from script location.")


def default_config_path(repo_root: Path) -> Path:
    return repo_root / "config" / "kyarakuri-comfy-blender-vrm.json"


def resolve_repo_path(value: str, repo_root: Path) -> Path:
    path = Path(value)
    if path.is_absolute():
        return path
    return (repo_root / path).resolve()


def load_config(config_path: Path) -> tuple[dict[str, Any] | None, CheckResult]:
    if not config_path.exists():
        return None, CheckResult(
            name="config",
            ok=False,
            detail=f"Config file not found: {config_path}",
            next_action="Create the config file or pass --config with a valid JSON path.",
        )

    try:
        raw_text = config_path.read_text(encoding="utf-8")
    except OSError as exc:
        return None, CheckResult(
            name="config",
            ok=False,
            detail=f"Config file could not be read: {exc}",
            next_action="Check file permissions and try again.",
        )

    try:
        payload = json.loads(raw_text)
    except json.JSONDecodeError as exc:
        return None, CheckResult(
            name="config",
            ok=False,
            detail=f"Config JSON is invalid at line {exc.lineno}, column {exc.colno}: {exc.msg}",
            next_action="Fix the JSON syntax and rerun doctor.",
        )

    if not isinstance(payload, dict):
        return None, CheckResult(
            name="config",
            ok=False,
            detail="Config JSON must be an object at the top level.",
            next_action="Rewrite the config as a JSON object with the required keys.",
        )

    return payload, CheckResult(
        name="config",
        ok=True,
        detail=f"Loaded config from {config_path}",
    )


def build_setting_results(config: dict[str, Any] | None, repo_root: Path) -> list[SettingResult]:
    results: list[SettingResult] = []
    source = config or {}

    for key in REQUIRED_KEYS:
        value = source.get(key)
        if value is None or (isinstance(value, str) and not value.strip()):
            results.append(
                SettingResult(
                    key=key,
                    raw_value="<missing>",
                    resolved_value="<missing>",
                    ok=False,
                    detail="Required setting is missing.",
                    next_action=f"Add '{key}' to the config file.",
                )
            )
            continue

        if not isinstance(value, str):
            results.append(
                SettingResult(
                    key=key,
                    raw_value=repr(value),
                    resolved_value="<invalid>",
                    ok=False,
                    detail="Setting must be a string.",
                    next_action=f"Rewrite '{key}' as a string value.",
                )
            )
            continue

        raw_value = value.strip()
        resolved_value = raw_value
        if key.endswith("_dir") or key == "blender_path":
            resolved_value = str(resolve_repo_path(raw_value, repo_root))

        results.append(
            SettingResult(
                key=key,
                raw_value=raw_value,
                resolved_value=resolved_value,
                ok=True,
                detail="Resolved successfully.",
            )
        )

    return results


def check_comfyui(url: str) -> CheckResult:
    normalized = url.rstrip("/")
    failures: list[str] = []

    for suffix in COMFYUI_PROBES:
        probe_url = f"{normalized}{suffix}"
        try:
            req = request.Request(probe_url, method="GET")
            with request.urlopen(req, timeout=5) as response:
                status = getattr(response, "status", 200)
                if 200 <= status < 400:
                    return CheckResult(
                        name="comfyui",
                        ok=True,
                        detail=f"Reachable via {probe_url} (HTTP {status}).",
                    )
                failures.append(f"{probe_url} returned HTTP {status}")
        except error.HTTPError as exc:
            failures.append(f"{probe_url} returned HTTP {exc.code}")
        except error.URLError as exc:
            failures.append(f"{probe_url} failed: {exc.reason}")
        except ValueError as exc:
            failures.append(f"{probe_url} failed: {exc}")

    detail = "; ".join(failures) if failures else "ComfyUI probe failed."
    return CheckResult(
        name="comfyui",
        ok=False,
        detail=detail,
        next_action="Start ComfyUI and confirm the configured URL is correct, for example http://127.0.0.1:8000.",
    )


def check_blender(path_value: str, repo_root: Path) -> CheckResult:
    path = resolve_repo_path(path_value, repo_root)

    if not path.exists():
        return CheckResult(
            name="blender_path",
            ok=False,
            detail=f"Blender executable was not found: {path}",
            next_action="Update 'blender_path' in the config to the installed blender executable.",
        )

    if path.is_dir():
        return CheckResult(
            name="blender_path",
            ok=False,
            detail=f"Blender path points to a directory, not a file: {path}",
            next_action="Point 'blender_path' to blender.exe instead of the installation directory.",
        )

    return CheckResult(
        name="blender_path",
        ok=True,
        detail=f"Found Blender executable: {path}",
    )


def check_workflow_dir(path_value: str, repo_root: Path) -> CheckResult:
    path = resolve_repo_path(path_value, repo_root)

    if not path.exists():
        return CheckResult(
            name="workflow_dir",
            ok=False,
            detail=f"Workflow directory was not found: {path}",
            next_action="Create the workflow directory and place workflow JSON files there, or update 'workflow_dir'.",
        )

    if not path.is_dir():
        return CheckResult(
            name="workflow_dir",
            ok=False,
            detail=f"Workflow path is not a directory: {path}",
            next_action="Replace 'workflow_dir' with a directory path that contains workflow JSON files.",
        )

    return CheckResult(
        name="workflow_dir",
        ok=True,
        detail=f"Found workflow directory: {path}",
    )


def check_output_dir(path_value: str, repo_root: Path) -> CheckResult:
    path = resolve_repo_path(path_value, repo_root)

    if path.exists() and not path.is_dir():
        return CheckResult(
            name="output_dir",
            ok=False,
            detail=f"Output path exists but is not a directory: {path}",
            next_action="Replace the file with a directory or update 'output_dir'.",
        )

    if path.is_dir():
        return CheckResult(
            name="output_dir",
            ok=True,
            detail=f"Found output directory: {path}",
        )

    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError as exc:
        return CheckResult(
            name="output_dir",
            ok=False,
            detail=f"Output directory could not be created: {exc}",
            next_action="Check the parent directory permissions or update 'output_dir'.",
        )

    return CheckResult(
        name="output_dir",
        ok=True,
        detail=f"Created output directory: {path}",
    )


def print_setting_results(results: list[SettingResult]) -> None:
    print("Resolved settings:")
    for result in results:
        status = "OK" if result.ok else "FAIL"
        print(f"- [{status}] {result.key}")
        print(f"  raw: {result.raw_value}")
        print(f"  resolved: {result.resolved_value}")
        print(f"  detail: {result.detail}")
        if result.next_action:
            print(f"  next: {result.next_action}")


def print_check_results(results: list[CheckResult]) -> None:
    print("Checks:")
    for result in results:
        status = "OK" if result.ok else "FAIL"
        print(f"- [{status}] {result.name}: {result.detail}")
        if result.next_action:
            print(f"  next: {result.next_action}")


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root(Path(__file__).resolve())
    config_path = args.config.resolve() if args.config else default_config_path(repo_root)

    config, config_result = load_config(config_path)
    setting_results = build_setting_results(config, repo_root)

    print("kyarakuri-prepare-environment")
    print(f"Repository root: {repo_root}")
    print(f"Config path: {config_path}")
    print()
    print_check_results([config_result])
    print()
    print_setting_results(setting_results)
    print()

    checks: list[CheckResult] = []
    settings_by_key = {result.key: result for result in setting_results}

    comfyui_setting = settings_by_key["comfyui_url"]
    if comfyui_setting.ok:
        checks.append(check_comfyui(comfyui_setting.raw_value))
    else:
        checks.append(
            CheckResult(
                name="comfyui",
                ok=False,
                detail="ComfyUI check skipped because 'comfyui_url' is missing or invalid.",
                next_action="Fix 'comfyui_url' and rerun doctor.",
            )
        )

    blender_setting = settings_by_key["blender_path"]
    if blender_setting.ok:
        checks.append(check_blender(blender_setting.raw_value, repo_root))
    else:
        checks.append(
            CheckResult(
                name="blender_path",
                ok=False,
                detail="Blender check skipped because 'blender_path' is missing or invalid.",
                next_action="Fix 'blender_path' and rerun doctor.",
            )
        )

    workflow_setting = settings_by_key["workflow_dir"]
    if workflow_setting.ok:
        checks.append(check_workflow_dir(workflow_setting.raw_value, repo_root))
    else:
        checks.append(
            CheckResult(
                name="workflow_dir",
                ok=False,
                detail="Workflow directory check skipped because 'workflow_dir' is missing or invalid.",
                next_action="Fix 'workflow_dir' and rerun doctor.",
            )
        )

    output_setting = settings_by_key["output_dir"]
    if output_setting.ok:
        checks.append(check_output_dir(output_setting.raw_value, repo_root))
    else:
        checks.append(
            CheckResult(
                name="output_dir",
                ok=False,
                detail="Output directory check skipped because 'output_dir' is missing or invalid.",
                next_action="Fix 'output_dir' and rerun doctor.",
            )
        )

    print_check_results(checks)
    print()

    failures = 0
    if not config_result.ok:
        failures += 1
    failures += sum(1 for result in setting_results if not result.ok)
    failures += sum(1 for result in checks if not result.ok)

    passed = 1 + len(setting_results) + len(checks) - failures
    total = 1 + len(setting_results) + len(checks)

    print(f"Summary: {passed}/{total} checks passed.")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
