"""
Builds data/region_carbon_intensity.csv from real published national grid
carbon-intensity figures in Our World in Data's energy dataset
(https://github.com/owid/energy-data), which aggregates Ember / Energy
Institute Statistical Review of World Energy data.

This gives one real gCO2/kWh number per *country*, for the most recent
year available -- not a per-cloud-region figure (a zone-level feed like
Electricity Maps would be needed for that, and isn't reachable from this
environment). Where several regions in data/regions.py share a country
(e.g. the four US regions) they carry the same value; real intra-country
grid variation (e.g. Pacific Northwest hydro vs. Ohio Valley coal/gas) is
not captured. See data/README.md.

Usage (run as a module from the repo root, so `data.regions` resolves):
    uv run python -m data.fetch_carbon_intensity
"""

import datetime

import pandas as pd
import requests

from data.regions import REGIONS

OWID_ENERGY_DATA_URL = "https://raw.githubusercontent.com/owid/energy-data/master/owid-energy-data.csv"
REGION_TABLE_PATH = "data/region_carbon_intensity.csv"
RAW_CACHE_PATH = "data/sources/owid_carbon_intensity_by_country.csv"


def fetch_latest_country_carbon_intensity() -> pd.DataFrame:
    response = requests.get(OWID_ENERGY_DATA_URL, timeout=60)
    response.raise_for_status()

    with open(RAW_CACHE_PATH, "wb") as f:
        f.write(response.content)

    df = pd.read_csv(RAW_CACHE_PATH, usecols=["country", "year", "carbon_intensity_elec"])
    df = df.dropna(subset=["carbon_intensity_elec"])
    latest = df.sort_values("year").groupby("country", as_index=False).tail(1)
    return latest[["country", "year", "carbon_intensity_elec"]]


def build_region_table(path: str = REGION_TABLE_PATH) -> pd.DataFrame:
    regions = pd.DataFrame(REGIONS)
    latest = fetch_latest_country_carbon_intensity()

    merged = regions.merge(latest, on="country", how="left")
    missing = merged[merged["carbon_intensity_elec"].isna()]["country"].unique()
    if len(missing):
        raise ValueError(f"No OWID carbon-intensity data found for: {list(missing)}")

    merged["avg_carbon_intensity_gco2_per_kwh"] = merged["carbon_intensity_elec"].round(1)
    merged["source_year"] = merged["year"].astype(int)

    out_cols = [
        "region", "cloud", "location", "country",
        "avg_carbon_intensity_gco2_per_kwh", "diurnal_swing_pct",
        "grid_mix_note", "source_year",
    ]
    result = merged[out_cols]
    result.to_csv(path, index=False)
    return result


if __name__ == "__main__":
    updated = build_region_table()
    print(f"Wrote {REGION_TABLE_PATH} from OWID energy-data "
          f"(retrieved {datetime.date.today().isoformat()}):")
    print(updated.to_string(index=False))
