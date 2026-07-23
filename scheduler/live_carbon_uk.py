"""
UK National Grid ESO Carbon Intensity API client
(https://api.carbonintensity.org.uk) -- free, no API key, and (unlike
scheduler/live_carbon.py's Electricity Maps client) this one has been
verified against real responses: it was unreachable from this sandbox
until the environment's network allowlist was updated mid-project, and
once it opened up, real requests below were used to confirm both the
national forecast and the regional-forecast response shapes.

Coverage is Great Britain only, at true DNO-region granularity (18
regions incl. England/Scotland/Wales/GB aggregates) with a real 24h
forecast per region -- this is the closest thing in this project to
the "regional + real-time" carbon data the whole live_carbon.py effort
was aiming for, just scoped to one country. It's used for eu-west-2
(London), whose regionid is 13 ("UKPN London") -- confirmed by listing
/regional and matching by shortname.

No auth, so there's no key to configure -- this is always attempted for
eu-west-2 if network access allows it, no user action required.
"""

import pandas as pd
import requests

API_BASE = "https://api.carbonintensity.org.uk"
LONDON_REGION_ID = 13


def fetch_regional_forecast(region_id: int = LONDON_REGION_ID, hours_ahead: int = 24) -> pd.DataFrame:
    """
    Real DNO-region forecast, in 30-minute steps, up to 24h ahead (this
    endpoint doesn't offer 48h for individual regions, only for the
    national/GB figure). Raises on any failure so callers can fall back.
    """
    response = requests.get(
        f"{API_BASE}/regional/intensity/{pd.Timestamp.now(tz='UTC').strftime('%Y-%m-%dT%H:%MZ')}/fw24h/regionid/{region_id}",
        timeout=15,
    )
    response.raise_for_status()
    payload = response.json()

    points = payload["data"]["data"]
    if not points:
        raise ValueError(f"Empty regional forecast for regionid {region_id}")

    df = pd.DataFrame(
        {
            "from": pd.to_datetime([p["from"] for p in points], utc=True),
            "carbon_intensity_gco2_per_kwh": [p["intensity"]["forecast"] for p in points],
        }
    )

    now = pd.Timestamp.now(tz="UTC")
    df["hours_from_now"] = ((df["from"] - now) / pd.Timedelta(hours=1)).round().astype(int)
    df = df[(df["hours_from_now"] >= 0) & (df["hours_from_now"] < hours_ahead)]
    if df.empty:
        raise ValueError(f"No forecast points within {hours_ahead}h for regionid {region_id}")

    return df[["hours_from_now", "carbon_intensity_gco2_per_kwh"]].sort_values(
        "hours_from_now"
    ).reset_index(drop=True)


def hourly_forecast_with_fallback(
    region_row: pd.Series,
    modeled_forecast_fn,
    hours_ahead: int = 48,
) -> tuple[pd.DataFrame, str]:
    """
    Only applies to the region(s) this API actually covers (currently
    just eu-west-2 / London, via region_row["uk_carbon_intensity_regionid"]).
    Falls back to the modeled curve on any error, or if this region has
    no UK regionid mapped -- so it's always safe to call for every region.

    Note this API only forecasts 24h ahead per-region (vs. the 48h this
    app models elsewhere); hours 24-48 fall back to the modeled curve
    even when the live 0-24h portion succeeds, and the two segments are
    concatenated. The returned source label reflects that split.
    """
    region_id = region_row.get("uk_carbon_intensity_regionid")
    if pd.isna(region_id):
        return modeled_forecast_fn(region_row, hours_ahead=hours_ahead), "modeled"

    try:
        live_df = fetch_regional_forecast(int(region_id), hours_ahead=min(hours_ahead, 24))
    except Exception:
        return modeled_forecast_fn(region_row, hours_ahead=hours_ahead), "modeled"

    if hours_ahead <= 24:
        return live_df, "live:uk-carbon-intensity"

    modeled_df = modeled_forecast_fn(region_row, hours_ahead=hours_ahead)
    modeled_tail = modeled_df[modeled_df["hours_from_now"] >= 24]
    combined = pd.concat([live_df, modeled_tail], ignore_index=True)
    return combined, "live:uk-carbon-intensity+modeled"
