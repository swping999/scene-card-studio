from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

from moments_to_pages import __version__

ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", ".venv", "dist", "build"}
TEXT_SUFFIXES = {".gitignore", ".json", ".md", ".py", ".toml", ".yaml", ".yml"}


def _repository_text_files():
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(part in SKIP_PARTS for part in path.parts):
            continue
        if path.name == ".gitignore" or path.suffix in TEXT_SUFFIXES:
            yield path


def test_all_local_markdown_links_resolve():
    missing = []
    checked = 0
    markdown_files = [path for path in _repository_text_files() if path.suffix == ".md"]
    for markdown in markdown_files:
        text = markdown.read_text(errors="replace")
        for raw_target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            target = raw_target.strip().split()[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            local_target = target.split("#", 1)[0]
            if not local_target:
                continue
            checked += 1
            if not (markdown.parent / local_target).resolve().exists():
                missing.append(f"{markdown.relative_to(ROOT)} -> {target}")
    assert checked >= 100
    assert not missing, "Missing local Markdown links:\n" + "\n".join(missing)


def test_public_version_is_consistent():
    pyproject = (ROOT / "pyproject.toml").read_text()
    english = (ROOT / "README.md").read_text()
    chinese = (ROOT / "README.zh-CN.md").read_text()
    assert f'version = "{__version__}"' in pyproject
    assert f"releases/tag/v{__version__}" in english
    assert f"releases/tag/v{__version__}" in chinese
    assert f"## [{__version__}]" in (ROOT / "CHANGELOG.md").read_text()


def test_public_text_has_no_local_user_paths_or_high_confidence_credentials():
    credential_pattern = re.compile(
        r"sk-(?:proj-)?[A-Za-z0-9_-]{20,}"
        r"|gh[pousr]_[A-Za-z0-9]{20,}"
        r"|github_pat_[A-Za-z0-9_]{20,}"
        r"|AKIA[0-9A-Z]{16}"
        r"|-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
        r"|xox[baprs]-[A-Za-z0-9-]{10,}"
    )
    local_path_pattern = re.compile(
        "/" + r"(?:Users|home)/[^/\s]+" + "|" + "/var/" + "folders/"
    )
    findings = []
    for path in _repository_text_files():
        text = path.read_text(errors="replace")
        if credential_pattern.search(text) or local_path_pattern.search(text):
            findings.append(str(path.relative_to(ROOT)))
    assert not findings, f"Potential private path or credential in: {', '.join(findings)}"


def test_gallery_scene_cards_and_manifests_are_reproducible():
    for gallery_name, expected_count in (("v0.4-gallery", 13), ("v0.6-gallery", 12)):
        gallery = ROOT / "examples/cases" / gallery_name
        subprocess.run(
            [sys.executable, str(gallery / "build_evidence.py"), "--check"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
        index = json.loads((gallery / "evidence/index.json").read_text())
        assert len(index["cases"]) == expected_count
        for case in index["cases"]:
            story_path = gallery / "evidence" / case["story"]
            manifest_path = gallery / "evidence" / case["prompt_manifest"]
            story = json.loads(story_path.read_text())
            manifest = json.loads(manifest_path.read_text())
            assert len(story) == 1
            assert manifest["generation_ready"] is True
            assert manifest["source_mode"] == "single-photo"
            assert manifest["prompts"][0]["reference_output"]["sha256"]
