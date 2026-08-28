"""Build the Telegram caption for a telemetry extraction."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

TELEGRAM_FILE_LIMIT_MB = 50
WARNING_THRESHOLD_PCT = 80


def build_caption(file_path: Path, extraction_time: datetime, start: str, stop: str, every: str) -> str:
    size_mb = file_path.stat().st_size / (1024 * 1024)
    pct = size_mb / TELEGRAM_FILE_LIMIT_MB * 100

    lines = [
        f"Extraction date: {extraction_time:%Y-%m-%d %H:%M UTC}",
        f"Range: {start} -> {stop} | every {every}",
        f"Size: {size_mb:.1f}MB is {pct:.1f}% / {TELEGRAM_FILE_LIMIT_MB}MB",
    ]

    if pct >= WARNING_THRESHOLD_PCT:
        lines.append(f"WARNING: file is at {pct:.1f}% of the {TELEGRAM_FILE_LIMIT_MB}MB Telegram limit")

    return "\n".join(lines)
