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

from scheduler import carbon, live_carbon, pricing
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


def _region_carbon_curve(
    region_row: pd.Series, hours_ahead: int, electricitymaps_api_key: str | None
) -> tuple[pd.DataFrame, str]:
    """One curve per region covering the whole candidate window -- fetched
    (or modeled) once, then sliced per start-hour, instead of re-deriving
    it for every candidate start time."""
    if electricitymaps_api_key:
        return live_carbon.hourly_forecast_with_fallback(
            region_row, carbon.hourly_forecast, electricitymaps_api_key, hours_ahead
        )
    return carbon.hourly_forecast(region_row, hours_ahead=hours_ahead), "modeled"


def _avg_carbon_over_window(curve: pd.DataFrame, start_hour: int, span_hours: int) -> float:
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
    pricing_type: str = "On-Demand",
    instance_type: str | None = None,
    regions_df: pd.DataFrame | None = None,
    pricing_df: pd.DataFrame | None = None,
    overhead_factor: float = 1.4,
    start_hour_step: int = 2,
    electricitymaps_api_key: str | None = None,
) -> pd.DataFrame:
    if regions_df is None:
        regions_df = carbon.load_region_table()
    if pricing_df is None:
        pricing_df = pricing.load_pricing_table()

    weights = PREFERENCE_WEIGHTS[preference]
    system_power_w = estimate_system_power_w(gpu_power_w, gpu_count, overhead_factor)
    start_hours = _candidate_start_hours(deadline_hours, runtime_hours, start_hour_step)
    span_hours = max(1, int(np.ceil(runtime_hours)))
    hours_ahead = max(start_hours) + span_hours

    rows = []
    for _, region_row in regions_df.iterrows():
        region = region_row["region"]
        try:
            rate, used_instance_type = pricing.hourly_rate(
                pricing_df, region, gpu_model, pricing_type, instance_type
            )
        except ValueError:
            continue

        cost_usd = rate * gpu_count * runtime_hours
        energy_kwh = estimate_energy_kwh(system_power_w, runtime_hours)
        curve, carbon_source = _region_carbon_curve(region_row, hours_ahead, electricitymaps_api_key)

        for start_hour in start_hours:
            avg_carbon = _avg_carbon_over_window(curve, start_hour, span_hours)
            emissions_kg = estimate_emissions_kg(energy_kwh, avg_carbon)

            rows.append(
                {
                    "region": region,
                    "instance_type": used_instance_type,
                    "start_hours_from_now": start_hour,
                    "cost_usd": round(cost_usd, 2),
                    "energy_kwh": round(energy_kwh, 2),
                    "avg_carbon_intensity_gco2_per_kwh": round(avg_carbon, 1),
                    "emissions_kg_co2": round(emissions_kg, 3),
                    "carbon_data_source": carbon_source,
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
