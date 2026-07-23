"""
Parses real nvidia-smi/DCGM power-monitoring logs captured while running the
CUDA benchmarks in gpu-benchmarks/cuda/ (sustained_gemm.cu = compute-bound,
laplace3d = memory-bound) into per-workload power profiles.

This is what makes KEHAI's carbon/cost estimates workload-aware instead of a
flat "GPU count x TDP" guess: a compute-bound job and a memory-bound job on
the same GPU can draw very different average power for the same wall-clock
time.

Log format is the output of:
    dcgmi dmon -e 155,203,204,100 -d 200 -c 40
grouped under "=== DCGM log: <label> ===" section headers, one row per GPU
per sample:
    GPU <id>   <power_W>   <gputl_pct>   <mcutl_pct>   <smclk_mhz>
"""

import re
from dataclasses import dataclass

import pandas as pd

SECTION_RE = re.compile(r"^===\s*DCGM log:\s*(.+?)\s*===\s*$")
ROW_RE = re.compile(
    r"^GPU\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\d+)\s+(\d+)\s*$"
)
GPU_INFO_RE = re.compile(r"^([^,]+),\s*([\d.]+)\s*W\s*$")


@dataclass
class WorkloadProfile:
    workload: str
    gpu_model: str
    power_limit_w: float
    avg_power_w: float
    peak_power_w: float
    min_power_w: float
    avg_gpu_util_pct: float
    sample_count: int
    benchmarked_gpu_id: int


def _read_gpu_info(lines: list[str]) -> tuple[str, float]:
    """Reads the `nvidia-smi --query-gpu=name,power.limit` header line."""
    for line in lines:
        match = GPU_INFO_RE.match(line.strip())
        if match:
            return match.group(1).strip(), float(match.group(2))
    return "Unknown GPU", 0.0


def parse_dcgm_log(path: str) -> pd.DataFrame:
    """Parses a dcgm dmon capture into a long-form per-sample DataFrame."""
    with open(path) as f:
        lines = f.readlines()

    gpu_model, power_limit_w = _read_gpu_info(lines)

    rows = []
    current_section = None
    sample_index = 0

    for raw_line in lines:
        line = raw_line.rstrip("\n")

        section_match = SECTION_RE.match(line.strip())
        if section_match:
            current_section = section_match.group(1)
            sample_index = 0
            continue

        if current_section is None:
            continue

        row_match = ROW_RE.match(line.strip())
        if not row_match:
            continue

        gpu_id, power_w, gputl, mcutl, smclk = row_match.groups()
        gpu_id = int(gpu_id)

        if gpu_id == 0:
            sample_index += 1

        rows.append(
            {
                "workload": current_section,
                "gpu_id": gpu_id,
                "power_w": float(power_w),
                "gputl_pct": int(gputl),
                "mcutl_pct": int(mcutl),
                "smclk_mhz": int(smclk),
                "sample_index": sample_index,
                "gpu_model": gpu_model,
                "power_limit_w": power_limit_w,
            }
        )

    return pd.DataFrame(rows)


def summarize_workload_profiles(samples: pd.DataFrame, benchmarked_gpu_id: int = 0) -> pd.DataFrame:
    """
    Reduces per-sample telemetry to one power/utilization profile per workload
    label, using only the GPU the benchmark actually ran on (utilization on
    the other GPUs in the node is idle background noise, not signal).
    """
    subset = samples[samples["gpu_id"] == benchmarked_gpu_id]

    profiles = []
    for workload, group in subset.groupby("workload", sort=False):
        profiles.append(
            WorkloadProfile(
                workload=workload,
                gpu_model=group["gpu_model"].iloc[0],
                power_limit_w=group["power_limit_w"].iloc[0],
                avg_power_w=round(group["power_w"].mean(), 1),
                peak_power_w=round(group["power_w"].max(), 1),
                min_power_w=round(group["power_w"].min(), 1),
                avg_gpu_util_pct=round(group["gputl_pct"].mean(), 1),
                sample_count=len(group),
                benchmarked_gpu_id=benchmarked_gpu_id,
            )
        )

    return pd.DataFrame([p.__dict__ for p in profiles])


def build_benchmark_profiles_csv(
    log_path: str = "gpu-benchmarks/cuda/dcgm_power_comparison.log",
    output_path: str = "data/benchmark_profiles.csv",
) -> pd.DataFrame:
    samples = parse_dcgm_log(log_path)
    profiles = summarize_workload_profiles(samples)
    profiles.to_csv(output_path, index=False)
    return profiles


if __name__ == "__main__":
    result = build_benchmark_profiles_csv()
    print(result.to_string(index=False))
