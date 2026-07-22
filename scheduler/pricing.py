"""
Real, instance-type-level GPU pricing lookup (on-demand and spot) and job
cost calculation. See data/fetch_gpu_pricing.py for how the table is built.
"""

import pandas as pd

GPU_PRICING_CSV = "data/gpu_pricing.csv"
PRICING_TYPES = {
    "On-Demand": "hourly_usd_per_gpu_ondemand",
    "Spot": "hourly_usd_per_gpu_spot",
}


def load_pricing_table(path: str = GPU_PRICING_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def available_instance_types(pricing: pd.DataFrame, region: str, gpu_model: str, pricing_type: str = "On-Demand") -> pd.DataFrame:
    price_col = PRICING_TYPES[pricing_type]
    rows = pricing[(pricing["region"] == region) & (pricing["gpu_model"] == gpu_model)]
    rows = rows.dropna(subset=[price_col])
    return rows.sort_values(price_col)


def hourly_rate(
    pricing: pd.DataFrame,
    region: str,
    gpu_model: str,
    pricing_type: str = "On-Demand",
    instance_type: str | None = None,
) -> tuple[float, str]:
    """
    Returns (hourly_usd_per_gpu, instance_type_used). If instance_type is
    None, picks the cheapest real instance type available for that
    region/GPU/pricing-type combination.
    """
    price_col = PRICING_TYPES[pricing_type]
    rows = pricing[(pricing["region"] == region) & (pricing["gpu_model"] == gpu_model)]
    if instance_type is not None:
        rows = rows[rows["instance_type"] == instance_type]
    rows = rows.dropna(subset=[price_col])

    if rows.empty:
        raise ValueError(
            f"No {pricing_type} pricing for {gpu_model} in {region}"
            + (f" on {instance_type}" if instance_type else "")
        )

    best = rows.sort_values(price_col).iloc[0]
    return float(best[price_col]), str(best["instance_type"])


def job_cost_usd(hourly_usd_per_gpu: float, gpu_count: int, runtime_hours: float) -> float:
    return hourly_usd_per_gpu * gpu_count * runtime_hours
