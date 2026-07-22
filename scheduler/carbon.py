"""
Regional grid carbon intensity lookup and a synthetic hourly forecast.

Real deployments should replace `load_region_table()` / `hourly_forecast()`
with a live feed (e.g. the Electricity Maps API) that returns actual
day-ahead carbon intensity per region. Here we shape a diurnal sine curve
around each region's illustrative annual average so the MVP can demonstrate
*why* time-shifting a job changes its footprint, without claiming those
numbers are measured.
"""

import numpy as np
import pandas as pd

REGION_CARBON_CSV = "data/region_carbon_intensity.csv"


def load_region_table(path: str = REGION_CARBON_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def hourly_forecast(region_row: pd.Series, hours_ahead: int = 48, start_hour_utc: int = 0) -> pd.DataFrame:
    """
    Builds an hour-by-hour carbon intensity curve for one region, lowest
    around 04:00 local-ish (night, less demand / more wind) and highest
    around 16:00 (afternoon/evening peak demand).
    """
    avg = region_row["avg_carbon_intensity_gco2_per_kwh"]
    swing = avg * (region_row["diurnal_swing_pct"] / 100.0)

    hours = np.arange(hours_ahead)
    hour_of_day = (start_hour_utc + hours) % 24

    # Trough at hour 4, peak at hour 16 -> shift cosine accordingly.
    phase = (hour_of_day - 4) / 24.0 * 2 * np.pi
    intensity = avg - (swing / 2) * np.cos(phase)

    return pd.DataFrame(
        {
            "hours_from_now": hours,
            "hour_of_day": hour_of_day,
            "carbon_intensity_gco2_per_kwh": np.round(intensity, 1),
        }
    )
