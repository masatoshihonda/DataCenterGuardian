"""
Candidate generation and ranking for the KEHAI GreenGPU Explorer.

For every (region, start time) candidate within the user's deadline window,
estimate cost and CO2, then rank by a weighted score. This mirrors the
integer-programming-style tradeoff in carbon-aware CDN scheduling papers
(where/when to place a workload), just applied to cloud GPU jobs instead of
content delivery.
"""

import numpy as np
import pandas as pd

from scheduler import carbon, pricing
from scheduler.estimator import (
    estimate_emissions_kg,
    estimate_energy_kwh,
    estimate_system_power_w,
)

PREFERENCE_WEIGHTS = {
    "Cheapest": {"cost": 1.0, "carbon": 0.0},
    "Balanced": {"cost": 0.5, "carbon": 0.5},
    "Greenest": {"cost": 0.0, "carbon": 1.0},
}
DELAY_WEIGHT = 0.1  # small nudge toward sooner starts among near-ties


def _candidate_start_hours(deadline_hours: float, runtime_hours: float, step_hours: int = 2) -> list[int]:
    last_start = deadline_hours - runtime_hours
    if last_start < 0:
        # Can't fit before the deadline: only "start now" is feasible.
        return [0]
    starts = list(range(0, int(last_start) + 1, step_hours))
    if not starts:
        starts = [0]
    return starts


def _avg_carbon_over_window(region_row: pd.Series, start_hour: int, runtime_hours: float) -> float:
    span_hours = max(1, int(np.ceil(runtime_hours)))
    curve = carbon.hourly_forecast(region_row, hours_ahead=start_hour + span_hours)
    window = curve[
        (curve["hours_from_now"] >= start_hour)
        & (curve["hours_from_now"] < start_hour + span_hours)
    ]
    return float(window["carbon_intensity_gco2_per_kwh"].mean())


def recommend(
    gpu_power_w: float,
    gpu_count: int,
    runtime_hours: float,
    deadline_hours: float,
    gpu_model: str,
    preference: str = "Balanced",
    regions_df: pd.DataFrame | None = None,
    pricing_df: pd.DataFrame | None = None,
    overhead_factor: float = 1.4,
    start_hour_step: int = 2,
) -> pd.DataFrame:
    if regions_df is None:
        regions_df = carbon.load_region_table()
    if pricing_df is None:
        pricing_df = pricing.load_pricing_table()

    weights = PREFERENCE_WEIGHTS[preference]
    system_power_w = estimate_system_power_w(gpu_power_w, gpu_count, overhead_factor)
    start_hours = _candidate_start_hours(deadline_hours, runtime_hours, start_hour_step)

    rows = []
    for _, region_row in regions_df.iterrows():
        region = region_row["region"]
        try:
            rate = pricing.hourly_rate(pricing_df, region, gpu_model)
        except ValueError:
            continue

        cost_usd = rate * gpu_count * runtime_hours
        energy_kwh = estimate_energy_kwh(system_power_w, runtime_hours)

        for start_hour in start_hours:
            avg_carbon = _avg_carbon_over_window(region_row, start_hour, runtime_hours)
            emissions_kg = estimate_emissions_kg(energy_kwh, avg_carbon)

            rows.append(
                {
                    "region": region,
                    "start_hours_from_now": start_hour,
                    "cost_usd": round(cost_usd, 2),
                    "energy_kwh": round(energy_kwh, 2),
                    "avg_carbon_intensity_gco2_per_kwh": round(avg_carbon, 1),
                    "emissions_kg_co2": round(emissions_kg, 3),
                }
            )

    candidates = pd.DataFrame(rows)
    if candidates.empty:
        return candidates

    def normalize(series: pd.Series) -> pd.Series:
        span = series.max() - series.min()
        if span == 0:
            return pd.Series(0.0, index=series.index)
        return (series - series.min()) / span

    norm_cost = normalize(candidates["cost_usd"])
    norm_carbon = normalize(candidates["emissions_kg_co2"])
    norm_delay = normalize(candidates["start_hours_from_now"])

    candidates["score"] = (
        weights["cost"] * norm_cost
        + weights["carbon"] * norm_carbon
        + DELAY_WEIGHT * norm_delay
    )

    candidates = candidates.sort_values("score").reset_index(drop=True)
    candidates.insert(0, "rank", candidates.index + 1)
    return candidates
