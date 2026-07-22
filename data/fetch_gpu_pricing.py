"""
Builds data/gpu_pricing.csv from real on-demand AWS GPU VM pricing, sourced
from the SkyPilot project's public cloud-instance-catalog mirror
(https://github.com/skypilot-org/skypilot-catalog), which is scraped
directly from AWS's own pricing API and kept up to date for the
SkyPilot scheduler project.

Azure's public Retail Prices API (prices.azure.com) is the more obvious
"no auth needed" source and was the original plan, but it isn't reachable
from this sandbox's network egress policy. The Azure VM catalog available
through the same SkyPilot mirror also turned out to only cover a handful
of US regions and doesn't list our benchmarked L40S GPU at all -- Azure's
own H100/A100 SKU rollout is itself US-heavy today. AWS's public catalog
gives real prices for L40S, A100-80GB and H100 across a broad, genuinely
global set of regions, so data/regions.py and this MVP now compare AWS
regions instead of Azure ones.

Each (region, GPU model) price is the median of "price per GPU" (list
price divided by GPU count) across every real AWS instance type in that
region offering that accelerator -- e.g. g6e.xlarge through g6e.48xlarge
for L40S -- not a single cherry-picked SKU.

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
    df["price_per_gpu_usd"] = df["Price"] / df["AcceleratorCount"]
    return df


def build_gpu_pricing_table(path: str = GPU_PRICING_PATH) -> pd.DataFrame:
    region_codes = {r["region"] for r in REGIONS}
    prices = fetch_aws_gpu_prices()
    prices = prices[prices["Region"].isin(region_codes)]

    summary = (
        prices.groupby(["Region", "AcceleratorName"])["price_per_gpu_usd"]
        .agg(hourly_usd_per_gpu="median", n_instance_types_sampled="count")
        .reset_index()
    )
    summary["gpu_model"] = summary["AcceleratorName"].map(ACCELERATOR_TO_GPU_MODEL)
    summary["hourly_usd_per_gpu"] = summary["hourly_usd_per_gpu"].round(2)
    summary = summary.rename(columns={"Region": "region"})

    result = summary[["region", "gpu_model", "hourly_usd_per_gpu", "n_instance_types_sampled"]]
    result = result.sort_values(["region", "gpu_model"]).reset_index(drop=True)
    result.to_csv(path, index=False)
    return result


if __name__ == "__main__":
    updated = build_gpu_pricing_table()
    print(f"Wrote {GPU_PRICING_PATH} from the public AWS instance-pricing catalog:")
    print(updated.to_string(index=False))

    missing_regions = {r["region"] for r in REGIONS} - set(updated["region"].unique())
    if missing_regions:
        print(f"\nNote: no GPU pricing found at all for: {sorted(missing_regions)}")
