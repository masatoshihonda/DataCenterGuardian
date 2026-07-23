"""
Builds data/gpu_pricing.csv from real AWS GPU VM pricing, at real
instance-type granularity with both on-demand and spot prices, sourced
from the SkyPilot project's public cloud-instance-catalog mirror
(https://github.com/skypilot-org/skypilot-catalog), itself scraped from
AWS's own pricing API.

Azure's public Retail Prices API (prices.azure.com) was the original plan
(no auth needed) but isn't reachable from this sandbox's network egress
policy. The Azure VM catalog available through the same SkyPilot mirror
also only covers a handful of US regions and doesn't list our benchmarked
L40S GPU at all. AWS's public catalog gives real prices for L40S,
A100-80GB and H100 across a genuinely global region set, so
data/regions.py compares AWS regions instead of Azure ones.

Each row is one real (region, instance type) combination -- not a
collapsed median -- so the app can show e.g. "g6e.xlarge" next to
"g6e.48xlarge" as genuinely different SKUs with different $/GPU. On-demand
price is constant across a region's availability zones in AWS's own
pricing model; spot price is real and does vary by AZ, so
`hourly_usd_per_gpu_spot` here is the mean across the AZs this catalog
sampled for that instance type (spot prices also fluctuate over time --
this is a snapshot, not a live quote).

Usage (run as a module from the repo root, so `data.regions` resolves):
    uv run python -m data.fetch_gpu_pricing
"""

import pandas as pd
import requests

from data.regions import REGIONS

AWS_VM_CATALOG_URL = "https://raw.githubusercontent.com/skypilot-org/skypilot-catalog/master/catalogs/v7/aws/vms.csv"
GPU_PRICING_PATH = "data/gpu_pricing.csv"
RAW_CACHE_PATH = "data/sources/aws_gpu_vm_prices_raw.csv"

ACCELERATOR_TO_GPU_MODEL = {
    "L40S": "L40S",
    "A100-80GB": "A100_80GB",
    "H100": "H100_80GB",
}


def fetch_aws_gpu_prices() -> pd.DataFrame:
    response = requests.get(AWS_VM_CATALOG_URL, timeout=60)
    response.raise_for_status()

    with open(RAW_CACHE_PATH, "wb") as f:
        f.write(response.content)

    df = pd.read_csv(RAW_CACHE_PATH)
    df = df.dropna(subset=["AcceleratorName", "Price", "AcceleratorCount"])
    df = df[df["AcceleratorName"].isin(ACCELERATOR_TO_GPU_MODEL)]
    df["price_per_gpu_ondemand_usd"] = df["Price"] / df["AcceleratorCount"]
    df["price_per_gpu_spot_usd"] = df["SpotPrice"] / df["AcceleratorCount"]
    return df


def build_gpu_pricing_table(path: str = GPU_PRICING_PATH) -> pd.DataFrame:
    region_codes = {r["region"] for r in REGIONS}
    prices = fetch_aws_gpu_prices()
    prices = prices[prices["Region"].isin(region_codes)]

    # Collapse per-availability-zone duplicates: on-demand price is the
    # same across AZs in a region, spot price genuinely varies by AZ.
    summary = (
        prices.groupby(["Region", "AcceleratorName", "InstanceType", "AcceleratorCount", "vCPUs", "MemoryGiB"])
        .agg(
            hourly_usd_per_gpu_ondemand=("price_per_gpu_ondemand_usd", "mean"),
            hourly_usd_per_gpu_spot=("price_per_gpu_spot_usd", "mean"),
            n_availability_zones=("price_per_gpu_ondemand_usd", "count"),
        )
        .reset_index()
    )
    summary["gpu_model"] = summary["AcceleratorName"].map(ACCELERATOR_TO_GPU_MODEL)
    summary["hourly_usd_per_gpu_ondemand"] = summary["hourly_usd_per_gpu_ondemand"].round(3)
    summary["hourly_usd_per_gpu_spot"] = summary["hourly_usd_per_gpu_spot"].round(3)
    summary = summary.rename(columns={
        "Region": "region",
        "InstanceType": "instance_type",
        "AcceleratorCount": "gpu_count_per_instance",
        "vCPUs": "vcpus",
        "MemoryGiB": "memory_gib",
    })

    out_cols = [
        "region", "gpu_model", "instance_type", "gpu_count_per_instance",
        "vcpus", "memory_gib", "hourly_usd_per_gpu_ondemand",
        "hourly_usd_per_gpu_spot", "n_availability_zones",
    ]
    result = summary[out_cols].sort_values(
        ["region", "gpu_model", "hourly_usd_per_gpu_ondemand"]
    ).reset_index(drop=True)
    result.to_csv(path, index=False)
    return result


if __name__ == "__main__":
    updated = build_gpu_pricing_table()
    print(f"Wrote {GPU_PRICING_PATH} from the public AWS instance-pricing catalog:")
    print(updated.to_string(index=False))

    missing_regions = {r["region"] for r in REGIONS} - set(updated["region"].unique())
    if missing_regions:
        print(f"\nNote: no GPU pricing found at all for: {sorted(missing_regions)}")
