"""On-demand GPU pricing lookup and job cost calculation."""

import pandas as pd

GPU_PRICING_CSV = "data/gpu_pricing.csv"


def load_pricing_table(path: str = GPU_PRICING_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def hourly_rate(pricing: pd.DataFrame, region: str, gpu_model: str) -> float:
    match = pricing[(pricing["region"] == region) & (pricing["gpu_model"] == gpu_model)]
    if match.empty:
        raise ValueError(f"No pricing for {gpu_model} in {region}")
    return float(match["hourly_usd_per_gpu"].iloc[0])


def job_cost_usd(hourly_usd_per_gpu: float, gpu_count: int, runtime_hours: float) -> float:
    return hourly_usd_per_gpu * gpu_count * runtime_hours
