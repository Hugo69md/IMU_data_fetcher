"""Shared config for the Telegram delivery layer.

.env additions:
    TELEGRAM_BOT_TOKEN=<from @BotFather>
    TELEGRAM_BOT_NAME=<bot username>
    TELEGRAM_CHAT_ID=<printed by get_chat_id.py, added after first /start>
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
BOT_NAME = os.environ.get("TELEGRAM_BOT_NAME", "")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")  # unset until get_chat_id.py has been run

API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"
