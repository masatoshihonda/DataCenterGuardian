"""
Optional live carbon-intensity feed via the Electricity Maps v3 API
(https://api.electricitymap.org/v3), used in place of the synthetic
diurnal curve in scheduler/carbon.py when an API key is configured.

*** Status: real data, verified. api.electricitymap.org was blocked by
this project's build sandbox for most of development; once the
environment's network allowlist was updated, this client was confirmed
against a real trial API key with full-zone access -- `fetch_live_forecast`
successfully pulled real 24h forecasts for multiple zones (Sweden, Tokyo,
US-PJM among others) with the exact response shape assumed here. (An
earlier test with a different, more restricted key -- a Home Assistant
integration key scoped to a single zone/endpoint -- correctly failed
closed with a clear 401 rather than silently misbehaving, which is its
own useful confirmation that auth failures are handled safely.) If the
response shape ever drifts, `fetch_live_forecast` still raises and the
caller falls back to the modeled curve automatically -- it won't silently
return wrong numbers.

Get a key, then either export it:
    export ELECTRICITYMAPS_API_KEY=...
or add it to .streamlit/secrets.toml as `electricitymaps_api_key`.
"""

import os

import pandas as pd
import requests

API_BASE = "https://api.electricitymap.org/v3"
ENV_VAR_NAME = "ELECTRICITYMAPS_API_KEY"


def get_api_key() -> str | None:
    key = os.environ.get(ENV_VAR_NAME)
    if key:
        return key
    try:
        import streamlit as st
        return st.secrets.get("electricitymaps_api_key")
    except Exception:
        return None


def fetch_live_forecast(zone: str, api_key: str, hours_ahead: int = 48) -> pd.DataFrame:
    """
    Real-time + forecast carbon intensity for one Electricity Maps zone.
    Raises on any failure (network, auth, unexpected shape) so callers can
    fall back to the modeled curve -- never returns partial/guessed data.
    """
    response = requests.get(
        f"{API_BASE}/carbon-intensity/forecast",
        params={"zone": zone},
        headers={"auth-token": api_key},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()

    forecast = payload["forecast"]
    if not forecast:
        raise ValueError(f"Empty forecast payload for zone {zone}")

    df = pd.DataFrame(forecast)
    df["datetime"] = pd.to_datetime(df["datetime"])
    now = pd.Timestamp.now(tz=df["datetime"].dt.tz)

    df["hours_from_now"] = ((df["datetime"] - now) / pd.Timedelta(hours=1)).round().astype(int)
    df = df[(df["hours_from_now"] >= 0) & (df["hours_from_now"] < hours_ahead)]
    if df.empty:
        raise ValueError(f"No forecast points within {hours_ahead}h for zone {zone}")

    return df.rename(columns={"carbonIntensity": "carbon_intensity_gco2_per_kwh"})[
        ["hours_from_now", "carbon_intensity_gco2_per_kwh"]
    ].sort_values("hours_from_now").reset_index(drop=True)


def hourly_forecast_with_fallback(
    region_row: pd.Series,
    modeled_forecast_fn,
    api_key: str | None = None,
    hours_ahead: int = 48,
) -> tuple[pd.DataFrame, str]:
    """
    Tries the live Electricity Maps feed for this region's zone; falls
    back to the modeled diurnal curve (modeled_forecast_fn, i.e.
    scheduler.carbon.hourly_forecast) on any error or missing key.
    Returns (dataframe, "live" | "modeled") so callers/UI can show which
    one was actually used for a given region.
    """
    zone = region_row.get("electricitymaps_zone")
    if api_key and zone:
        try:
            return fetch_live_forecast(zone, api_key, hours_ahead), "live"
        except Exception:
            pass
    return modeled_forecast_fn(region_row, hours_ahead=hours_ahead), "modeled"
