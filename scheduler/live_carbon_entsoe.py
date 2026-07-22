"""
ENTSO-E Transparency Platform client (https://transparency.entsoe.eu),
used to anchor the modeled diurnal curve to a real current measurement
for EU-region entries when the user supplies their own security token.

Unlike the other live-carbon clients here, ENTSO-E doesn't hand back a
ready-made "carbon intensity" number, and -- importantly -- document A75
("Actual generation per production type", processType A16 "Realised")
is exactly what it says: *actual* generation, only available for periods
that have already happened. There is no publicly available ENTSO-E feed
of a full future generation-by-fuel-type mix comparable to what
Electricity Maps or the UK Carbon Intensity API forecast, so this client
does NOT claim to forecast: it fetches the most recent actual generation
mix, converts it to gCO2/kWh via published emission-intensity factors
(`EMISSION_FACTORS_GCO2_PER_KWH`, lifecycle medians from IPCC AR5 WG3
Annex III Table A.III.2, 2014 -- the same reference most public carbon
calculators cite, not invented numbers), and uses that one real
observation to re-anchor the modeled day/night curve's mean -- keeping
the illustrative diurnal *shape* but replacing its baseline (the OWID
annual average) with what the grid is actually doing right now. This
doesn't account for cross-border imports/exports into the bidding zone,
only in-zone generation.

*** Status: reachable but not fully verified. web-api.tp.entsoe.eu was
blocked by this build environment's network policy for most of the
project; once the allowlist was updated, an unauthenticated request
(with the exact document/process/domain/period query parameters used
here) returned a real, well-formed XML "Authentication failed"
acknowledgement document -- confirming the request shape is right -- but
no ENTSO-E account was available in this build to obtain a real security
token, so the actual generation-data XML shape has not been checked
against a real response. If it doesn't parse as expected,
`fetch_current_carbon_intensity` raises and the caller falls back to the
plain modeled curve automatically.

Request a free token by emailing transparency@entsoe.eu from your
registered platform account (see their API docs), then either export it:
    export ENTSOE_SECURITY_TOKEN=...
or add `entsoe_security_token` to .streamlit/secrets.toml.
"""

import os
import xml.etree.ElementTree as ET

import pandas as pd
import requests

API_BASE = "https://web-api.tp.entsoe.eu/api"
LOOKBACK_HOURS = 6  # how far back to look for the most recent *reported* actual data

# IPCC AR5 WG3 Annex III (2014), Table A.III.2 -- lifecycle median gCO2eq/kWh
# by ENTSO-E PSR (production source) type code.
EMISSION_FACTORS_GCO2_PER_KWH = {
    "B01": 230,   # Biomass
    "B02": 1054,  # Fossil Brown coal/Lignite
    "B03": 490,   # Fossil Coal-derived gas
    "B04": 490,   # Fossil Gas
    "B05": 820,   # Fossil Hard coal
    "B06": 650,   # Fossil Oil
    "B07": 820,   # Fossil Oil shale
    "B08": 820,   # Fossil Peat
    "B09": 38,    # Geothermal
    "B10": 24,    # Hydro Pumped Storage
    "B11": 24,    # Hydro Run-of-river and poundage
    "B12": 24,    # Hydro Water Reservoir
    "B13": 17,    # Marine
    "B14": 12,    # Nuclear
    "B15": 100,   # Other renewable
    "B16": 45,    # Solar
    "B17": 700,   # Waste
    "B18": 12,    # Wind Offshore
    "B19": 11,    # Wind Onshore
    "B20": 500,   # Other
    "B25": 24,    # Energy storage
}

NS = {"ns": "urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0"}


def get_security_token() -> str | None:
    token = os.environ.get("ENTSOE_SECURITY_TOKEN")
    if token:
        return token
    try:
        import streamlit as st
        return st.secrets.get("entsoe_security_token")
    except Exception:
        return None


def fetch_current_carbon_intensity(bidding_zone: str, security_token: str) -> float:
    """
    Converts the most recent real actual-generation-by-fuel-type report
    for one ENTSO-E bidding zone into a single gCO2/kWh figure. Raises on
    any failure (network, auth, unexpected XML shape, no usable points).
    """
    now = pd.Timestamp.now(tz="UTC")
    period_start = (now - pd.Timedelta(hours=LOOKBACK_HOURS)).strftime("%Y%m%d%H00")
    period_end = now.strftime("%Y%m%d%H00")

    response = requests.get(
        API_BASE,
        params={
            "securityToken": security_token,
            "documentType": "A75",
            "processType": "A16",
            "outBiddingZone_Domain": bidding_zone,
            "periodStart": period_start,
            "periodEnd": period_end,
        },
        timeout=20,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)
    rows = []
    for timeseries in root.findall("ns:TimeSeries", NS):
        psr_type_el = timeseries.find("ns:MktPSRType/ns:psrType", NS)
        if psr_type_el is None or psr_type_el.text not in EMISSION_FACTORS_GCO2_PER_KWH:
            continue
        psr_type = psr_type_el.text

        period = timeseries.find("ns:Period", NS)
        if period is None:
            continue
        period_start_dt = pd.Timestamp(period.find("ns:timeInterval/ns:start", NS).text)
        resolution = period.find("ns:resolution", NS).text
        step = pd.Timedelta(resolution.replace("PT", "").replace("M", "min"))

        for point in period.findall("ns:Point", NS):
            position = int(point.find("ns:position", NS).text)
            quantity_mw = float(point.find("ns:quantity", NS).text)
            timestamp = period_start_dt + (position - 1) * step
            rows.append({"timestamp": timestamp, "psr_type": psr_type, "quantity_mw": quantity_mw})

    if not rows:
        raise ValueError(f"No usable generation-mix data for bidding zone {bidding_zone}")

    df = pd.DataFrame(rows)
    latest_timestamp = df["timestamp"].max()
    latest = df[df["timestamp"] == latest_timestamp]

    total_mw = latest["quantity_mw"].sum()
    if total_mw <= 0:
        raise ValueError(f"Zero total generation reported for bidding zone {bidding_zone}")

    weighted_emissions = (latest["quantity_mw"] * latest["psr_type"].map(EMISSION_FACTORS_GCO2_PER_KWH)).sum()
    return weighted_emissions / total_mw


def hourly_forecast_with_fallback(
    region_row: pd.Series,
    modeled_forecast_fn,
    security_token: str | None,
    hours_ahead: int = 48,
) -> tuple[pd.DataFrame, str]:
    """
    Re-anchors the modeled diurnal curve's mean to a real current
    ENTSO-E-derived measurement, keeping the illustrative day/night
    shape. Falls back to the plain modeled curve on any failure.
    """
    bidding_zone = region_row.get("entsoe_bidding_zone")
    modeled_df = modeled_forecast_fn(region_row, hours_ahead=hours_ahead)

    if not (security_token and isinstance(bidding_zone, str) and bidding_zone):
        return modeled_df, "modeled"

    try:
        live_now = fetch_current_carbon_intensity(bidding_zone, security_token)
    except Exception:
        return modeled_df, "modeled"

    modeled_mean = modeled_df["carbon_intensity_gco2_per_kwh"].mean()
    if modeled_mean <= 0:
        return modeled_df, "modeled"

    adjusted = modeled_df.copy()
    adjusted["carbon_intensity_gco2_per_kwh"] = (
        adjusted["carbon_intensity_gco2_per_kwh"] * (live_now / modeled_mean)
    )
    return adjusted, "live:entsoe (current, modeled shape)"
