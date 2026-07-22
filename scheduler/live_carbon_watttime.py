"""
WattTime v3 API client (https://www.watttime.org), used in place of the
modeled diurnal curve for US/Canada regions when the user supplies their
own WattTime login credentials.

*** Status: reachable but not fully verified. api.watttime.org was
blocked by this build environment's network policy for most of the
project; once the allowlist was updated, requests with fake credentials
confirmed the real request shapes used here: `GET /login` (note: NOT
under `/v3/`) with HTTP Basic Auth returns a real `403 Forbidden` for bad
credentials (not a redirect -- an earlier version of this client
mistakenly pointed at `/v3/login`, which 302-redirects to WattTime's docs
site instead of erroring, silently masking the bug until tested), and
`GET /v3/forecast` with a bad bearer token returns a real `401` complaining
the JWT is malformed -- confirming both endpoints and the auth handshake.
No real WattTime account was available in this build to obtain valid
credentials, so the *authenticated* forecast payload shape hasn't been
checked against real data. If it doesn't match, `fetch_live_forecast`
raises and the caller falls back to the modeled curve automatically.

Get free-tier credentials at https://www.watttime.org/get-the-data/, then
either export them:
    export WATTTIME_USERNAME=...
    export WATTTIME_PASSWORD=...
or add `watttime_username` / `watttime_password` to
.streamlit/secrets.toml.
"""

import os

import pandas as pd
import requests

LOGIN_URL = "https://api.watttime.org/login"  # NOT under /v3/ -- see module docstring
API_BASE = "https://api.watttime.org/v3"


def get_credentials() -> tuple[str, str] | None:
    username = os.environ.get("WATTTIME_USERNAME")
    password = os.environ.get("WATTTIME_PASSWORD")
    if username and password:
        return username, password
    try:
        import streamlit as st
        username = st.secrets.get("watttime_username")
        password = st.secrets.get("watttime_password")
        if username and password:
            return username, password
    except Exception:
        pass
    return None


def _login(username: str, password: str) -> str:
    response = requests.get(LOGIN_URL, auth=(username, password), timeout=15)
    response.raise_for_status()
    return response.json()["token"]


def fetch_live_forecast(region: str, username: str, password: str, hours_ahead: int = 48) -> pd.DataFrame:
    """
    Real-time + forecast average carbon intensity (co2_aoer signal -- the
    average, not marginal, operating emissions rate, for comparability
    with the other providers here) for one WattTime balancing-authority
    region. Raises on any failure so callers can fall back.
    """
    token = _login(username, password)
    response = requests.get(
        f"{API_BASE}/forecast",
        params={"region": region, "signal_type": "co2_aoer"},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()

    points = payload.get("data", payload if isinstance(payload, list) else [])
    if not points:
        raise ValueError(f"Empty forecast payload for WattTime region {region}")

    df = pd.DataFrame(points)
    df["point_time"] = pd.to_datetime(df["point_time"], utc=True)
    now = pd.Timestamp.now(tz="UTC")

    df["hours_from_now"] = ((df["point_time"] - now) / pd.Timedelta(hours=1)).round().astype(int)
    df = df[(df["hours_from_now"] >= 0) & (df["hours_from_now"] < hours_ahead)]
    if df.empty:
        raise ValueError(f"No forecast points within {hours_ahead}h for WattTime region {region}")

    return df.rename(columns={"value": "carbon_intensity_gco2_per_kwh"})[
        ["hours_from_now", "carbon_intensity_gco2_per_kwh"]
    ].sort_values("hours_from_now").reset_index(drop=True)


def hourly_forecast_with_fallback(
    region_row: pd.Series,
    modeled_forecast_fn,
    credentials: tuple[str, str] | None,
    hours_ahead: int = 48,
) -> tuple[pd.DataFrame, str]:
    region = region_row.get("watttime_region")
    if credentials and isinstance(region, str) and region:
        username, password = credentials
        try:
            return fetch_live_forecast(region, username, password, hours_ahead), "live:watttime"
        except Exception:
            pass
    return modeled_forecast_fn(region_row, hours_ahead=hours_ahead), "modeled"
