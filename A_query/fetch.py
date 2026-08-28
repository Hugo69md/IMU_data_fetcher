"""Run a Flux query against InfluxDB and get a DataFrame back."""

from __future__ import annotations

import os

import certifi
import pandas as pd
from influxdb_client import InfluxDBClient


def fetch(flux: str) -> pd.DataFrame:
    """Send the query, get a DataFrame back. No CSV file in between."""
    with InfluxDBClient(
        url=os.environ["INFLUX_URL"],
        token=os.environ["INFLUX_TOKEN"],
        org=os.environ["INFLUX_ORG_ID"],
        ssl_ca_cert=certifi.where(),
        enable_gzip=True,
        timeout=120_000,               # milliseconds
    ) as client:
        df = client.query_api().query_data_frame(flux)

    # A Flux query yielding several tables comes back as a list of frames.
    if isinstance(df, list):
        df = pd.concat(df, ignore_index=True)

    # Bookkeeping columns InfluxDB adds; none carry information here.
    df = df.drop(columns=["result", "table", "_start", "_stop", "_measurement"],
                 errors="ignore")

    if "_time" in df.columns:
        df = df.rename(columns={"_time": "time"}).sort_values("time")

    return df.reset_index(drop=True)
