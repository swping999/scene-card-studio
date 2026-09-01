from __future__ import annotations

from pathlib import Path
import shutil
import sysconfig


def bundled_skill_path() -> Path:
    candidates = (
        Path(sysconfig.get_path("data")) / "share" / "scene-card-studio" / "skill",
        Path(__file__).resolve().parents[2] / "skills" / "scene-card-studio",
    )
    for candidate in candidates:
        if (candidate / "SKILL.md").is_file():
            return candidate.resolve()
    raise FileNotFoundError(
        "The Scene Card Studio Codex Skill is not present in this installation; reinstall from a complete wheel or source checkout"
    )


def install_bundled_skill(target: Path) -> Path:
    source = bundled_skill_path()
    destination = target.expanduser().resolve()
    if destination.exists():
        raise FileExistsError(f"Refusing to overwrite existing Skill directory: {destination}")
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return destination
