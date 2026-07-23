"""
WattTime v3 API client (https://www.watttime.org), used in place of the
modeled diurnal curve for US/Canada regions when the user supplies their
own WattTime login credentials.

*** Status: real data, verified for CAISO_NORTH (us-west-1). A free
test account was self-registered via `register_account()` and, once its
email was confirmed, `fetch_live_forecast('CAISO_NORTH', ...)` returned
real 5-minute-resolution MOER data (`/v3/my-access` confirmed this free
account's only entitlement is CAISO_NORTH, exactly as the docs describe)
-- correctly converted from lbs/MWh to gCO2/kWh, values in the ~400-450
gCO2/kWh range with some brief near-zero dips (plausible: California's
marginal generator briefly becomes a near-zero-emission source at
times, e.g. curtailed solar). us-east-1/us-east-2/us-west-2 (PJM_DC,
PJM_OH, BPAT) still need an ANALYST/PRO subscription to verify -- on
this free account they correctly return 403 and fall back to modeled,
per the priority-chain design below.

Reading WattTime's official API docs (docs.watttime.org) caught real
bugs in an earlier version of this client before it could ship silently
wrong numbers:

- WattTime's signal is CO2 MOER (Marginal Operating Emissions Rate) in
  **lbs/MWh**, not gCO2/kWh like every other provider here. An earlier
  version requested a `co2_aoer` signal (average, not marginal) that
  never appears anywhere in WattTime's docs -- every documented example
  uses `co2_moer` -- and didn't convert units at all, which would have
  silently mixed lbs/MWh values into a gCO2/kWh column. Fixed to request
  `co2_moer` and convert (1 lb/MWh = 0.453592 gCO2/kWh).
- MOER (marginal) is a genuinely different quantity from the average
  grid intensity the other providers (Electricity Maps, UK Carbon
  Intensity, ENTSO-E) report: it answers "what's the incremental effect
  of adding one more MW of load right now", not "what's the average
  carbon intensity of all generation on the grid". WattTime doesn't
  expose an average-rate forecast on the free/preview tier (their
  average-rate "AOER" signal, where offered, is a historical/analyst
  product) -- so treat WattTime numbers here as directionally comparable
  to the other providers, not identical in kind.
- `/v3/forecast` and `/v3/historical` require an ANALYST/PRO
  subscription for most regions; the docs explicitly carve out
  `region=CAISO_NORTH` as always available for preview without a paid
  plan. So on a free account, only the region mapped to CAISO_NORTH
  (us-west-1 here) is expected to actually return data -- the others
  (PJM_DC, PJM_OH, BPAT) should correctly 403 and fall back to modeled
  until/unless a paid plan is added.
- The login endpoint is `/login`, not `/v3/login` (confirmed separately
  once api.watttime.org became reachable from this build environment --
  the versioned path silently 302-redirects to WattTime's docs site
  instead of erroring).

Get free-tier credentials by self-registering via `register_account()` or
at https://www.watttime.org/get-the-data/, then either export them:
    export WATTTIME_USERNAME=...
    export WATTTIME_PASSWORD=...
or add `watttime_username` / `watttime_password` to
.streamlit/secrets.toml.
"""

import os

import pandas as pd
import requests

REGISTER_URL = "https://api.watttime.org/register"
LOGIN_URL = "https://api.watttime.org/login"  # NOT under /v3/ -- see module docstring
API_BASE = "https://api.watttime.org/v3"

LBS_PER_MWH_TO_GRAMS_PER_KWH = 0.453592


def register_account(username: str, password: str, email: str, org: str | None = None) -> dict:
    """Self-serve registration -- no email verification required per WattTime's docs."""
    payload = {"username": username, "password": password, "email": email}
    if org:
        payload["org"] = org
    response = requests.post(REGISTER_URL, json=payload, timeout=15)
    response.raise_for_status()
    return response.json()


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
    Forecast CO2 MOER (marginal operating emissions rate) for one WattTime
    balancing-authority region, converted from lbs/MWh to gCO2/kWh.
    Raises on any failure so callers can fall back.
    """
    token = _login(username, password)
    horizon_hours = max(1, min(int(hours_ahead), 72))  # API caps this at 72
    response = requests.get(
        f"{API_BASE}/forecast",
        params={"region": region, "signal_type": "co2_moer", "horizon_hours": horizon_hours},
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()

    points = payload.get("data", [])
    if not points:
        raise ValueError(f"Empty forecast payload for WattTime region {region}")

    df = pd.DataFrame(points)
    df["point_time"] = pd.to_datetime(df["point_time"], utc=True)
    now = pd.Timestamp.now(tz="UTC")

    df["carbon_intensity_gco2_per_kwh"] = df["value"] * LBS_PER_MWH_TO_GRAMS_PER_KWH
    df["hours_from_now"] = ((df["point_time"] - now) / pd.Timedelta(hours=1)).round().astype(int)
    df = df[(df["hours_from_now"] >= 0) & (df["hours_from_now"] < hours_ahead)]
    if df.empty:
        raise ValueError(f"No forecast points within {hours_ahead}h for WattTime region {region}")

    return df[["hours_from_now", "carbon_intensity_gco2_per_kwh"]].sort_values(
        "hours_from_now"
    ).reset_index(drop=True)


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
