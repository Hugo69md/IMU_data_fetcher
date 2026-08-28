"""Assemble the Flux query sent to InfluxDB."""

from __future__ import annotations

from A_query.config import BUCKET, FIELDS, MEASUREMENT


def build_flux(
    start: str = "-24h",
    stop: str = "now()",
    every: str | None = "5s",
    fields: list[str] | None = None,
    pivot: bool = True,
) -> str:
    """Assemble the Flux query.

    `start` accepts a duration (-24h) or an RFC3339 timestamp
    (2026-08-01T00:00:00Z). The browser sent these as `v.timeRangeStart`
    and `v.timeRangeStop` — variables its time-picker injected. Standalone,
    we just write the values in directly.
    """
    fields = fields or FIELDS
    field_filter = " or ".join(f'r["_field"] == "{f}"' for f in fields)

    q = f'''from(bucket: "{BUCKET}")
  |> range(start: {start}, stop: {stop})
  |> filter(fn: (r) => r["_measurement"] == "{MEASUREMENT}")
  |> filter(fn: (r) => {field_filter})'''

    if every:
        # Mean per window. createEmpty:false drops windows with no data,
        # so you get gaps rather than rows of NaN.
        q += f'\n  |> aggregateWindow(every: {every}, fn: mean, createEmpty: false)'

    if pivot:
        # Long -> wide: one row per timestamp, one column per field.
        # The browser did NOT do this (the UI charts long format), but it is
        # what you want feeding pandas.
        q += '\n  |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")'

    return q
