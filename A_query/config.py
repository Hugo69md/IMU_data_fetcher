"""Shared config for the InfluxDB query layer.

.env (chmod 600), next to the project root:
    INFLUX_URL=https://timedb.athena-system.com
    INFLUX_ORG_ID=dd36661177283a2d
    INFLUX_TOKEN=<generate in UI: Load Data -> API Tokens>
"""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")

BUCKET = "telemtryData"          # sic — typo is in the bucket name itself
MEASUREMENT = "mqtt_consumer"
FIELDS = ["accl", "roll", "speed", "pitch"]
