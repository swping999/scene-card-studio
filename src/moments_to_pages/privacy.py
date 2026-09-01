from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


def build_upload_consent(
    manifest: dict[str, Any],
    *,
    manifest_sha256: str,
    provider: str,
    purpose: str,
    user_confirmed: bool,
) -> dict[str, Any]:
    if not user_confirmed:
        raise ValueError("Explicit user consent is required before creating an upload record")
    if not provider.strip():
        raise ValueError("provider is required")
    if not purpose.strip():
        raise ValueError("purpose is required")
    readiness = manifest.get("direction_readiness")
    if isinstance(readiness, dict) and readiness.get("generation_ready") is not True:
        raise ValueError(
            "Semantic Scene Card direction is incomplete; finish the fields listed in direction_readiness before recording upload consent"
        )
    if isinstance(readiness, dict) and manifest.get("generation_ready") is not True:
        raise ValueError("The automatic route is unresolved; select a Narrative System explicitly before recording upload consent")
    files = manifest.get("privacy", {}).get("files", [])
    if not files:
        raise ValueError("Manifest contains no upload file list")
    return {
        "schema_version": "1.0",
        "manifest_sha256": manifest_sha256,
        "provider": provider.strip(),
        "purpose": purpose.strip(),
        "files": files,
        "user_explicitly_consented": True,
        "consented_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "scope": "Only the listed files may be uploaded to the named provider for the stated purpose.",
    }


def validate_upload_consent(record: dict[str, Any], manifest: dict[str, Any], manifest_sha256: str) -> None:
    if record.get("manifest_sha256") != manifest_sha256:
        raise ValueError("Upload consent does not match the current manifest")
    if record.get("user_explicitly_consented") is not True:
        raise ValueError("Upload consent is not explicit")
    if record.get("files") != manifest.get("privacy", {}).get("files"):
        raise ValueError("Upload consent file list does not match the manifest")
    for field in ("provider", "purpose", "consented_at"):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError(f"Upload consent {field} is required")
