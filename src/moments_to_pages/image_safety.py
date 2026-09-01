from __future__ import annotations

from pathlib import Path


MAX_RASTER_BYTES = 50 * 1024 * 1024
MAX_RASTER_PIXELS = 80_000_000


def validate_raster_path(path: Path) -> None:
    if not path.exists() or not path.is_file():
        raise FileNotFoundError(f"Image file does not exist: {path}")
    size = path.stat().st_size
    if size <= 0:
        raise ValueError(f"Image file is empty: {path}")
    if size > MAX_RASTER_BYTES:
        raise ValueError(
            f"Image file exceeds the {MAX_RASTER_BYTES // (1024 * 1024)} MiB safety limit: {path}"
        )


def validate_raster_dimensions(width: int, height: int, path: Path) -> None:
    if width <= 0 or height <= 0:
        raise ValueError(f"Image has invalid dimensions: {path}")
    if width * height > MAX_RASTER_PIXELS:
        raise ValueError(
            f"Image exceeds the {MAX_RASTER_PIXELS:,}-pixel safety limit: {path}"
        )
