"""One-time setup: discover your Telegram chat_id.

Message the bot on Telegram first (search for it, tap Start / send anything),
then run this script — it reads that pending update and prints the chat_id
to add to .env as TELEGRAM_CHAT_ID.

Run:
    python3 B_telegram/get_chat_id.py
"""

from __future__ import annotations

import requests

from B_telegram.config import API_URL


def get_chat_id() -> int | None:
    resp = requests.get(f"{API_URL}/getUpdates", timeout=30)
    resp.raise_for_status()
    updates = resp.json()["result"]

    if not updates:
        return None

    return updates[-1]["message"]["chat"]["id"]


if __name__ == "__main__":
    chat_id = get_chat_id()
    if chat_id is None:
        print("No messages found yet — message the bot on Telegram first, then rerun this.")
    else:
        print(f"chat_id: {chat_id}")
        print(f"Add this to .env: TELEGRAM_CHAT_ID = {chat_id}")
