"""Send a file to the configured Telegram chat."""

from __future__ import annotations

from pathlib import Path

import requests

from B_telegram.config import API_URL, CHAT_ID


def send_document(file_path: Path, caption: str | None = None) -> None:
    if not CHAT_ID:
        raise RuntimeError(
            "TELEGRAM_CHAT_ID is not set. Message the bot on Telegram, then run "
            "`python3 B_telegram/get_chat_id.py` and add the printed value to .env."
        )

    data = {"chat_id": CHAT_ID}
    if caption:
        data["caption"] = caption

    with open(file_path, "rb") as f:
        resp = requests.post(
            f"{API_URL}/sendDocument",
            data=data,
            files={"document": (Path(file_path).name, f)},
            timeout=120,
        )
    resp.raise_for_status()
