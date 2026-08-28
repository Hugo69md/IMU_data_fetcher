"""Fetch telemetry from InfluxDB — same query the Data Explorer sent.

Setup:
    pip install 'influxdb-client[extra]' python-dotenv

.env (chmod 600), next to this file:
    INFLUX_URL=https://timedb.athena-system.com
    INFLUX_ORG_ID=dd36661177283a2d
    INFLUX_TOKEN=<generate in UI: Load Data -> API Tokens>

Run:
    python main.py
    python main.py --start -7d --every 1s
    python main.py --raw --start -30m      # no downsampling
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path

from A_query import build_flux, fetch
from B_telegram import build_caption, send_document


def main() -> None:
    p = argparse.ArgumentParser(description="Pull telemetry from InfluxDB")
    p.add_argument("--start", default="-12h", help="e.g. -24h, -7d, or RFC3339")
    p.add_argument("--stop", default="now()")
    p.add_argument("--every", default="5s", help="downsample window")
    p.add_argument("--raw", action="store_true", help="no downsampling")
    p.add_argument("--long", action="store_true", help="skip pivot (browser's format)")
    p.add_argument("--out", type=Path, default=None,
                    help="output path (default: telemetry_<UTC timestamp>.csv)")
    p.add_argument("--no-telegram", action="store_true", help="skip sending the CSV to the bot")
    args = p.parse_args()

    extraction_time = datetime.now(timezone.utc)
    out = args.out or Path(f"telemetry_{extraction_time:%Y%m%dT%H%M%SZ}.csv")

    flux = build_flux(
        start=args.start,
        stop=args.stop,
        every=None if args.raw else args.every,
        pivot=not args.long,
    )
    print(f"--- Flux ---\n{flux}\n")

    df = fetch(flux)
    print(df.head(10))
    print(f"\n{len(df)} rows x {df.shape[1]} cols")
    if "time" in df.columns and len(df):
        print(f"span: {df['time'].min()} -> {df['time'].max()}")

    df.to_csv(out, index=False)
    print(f"saved -> {out}")

    if not args.no_telegram:
        caption = build_caption(
            out,
            extraction_time=extraction_time,
            start=args.start,
            stop=args.stop,
            every="raw" if args.raw else args.every,
        )
        send_document(out, caption=caption)
        print("sent -> Telegram")


if __name__ == "__main__":
    main()
