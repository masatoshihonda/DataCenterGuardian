"""
Energy and CO2 estimation for a GPU job.

Energy = observed/estimated per-GPU power draw x GPU count x runtime,
inflated by an overhead factor for the rest of the system (CPU, memory,
cooling/PUE) that isn't visible to a single-GPU power reading.

CO2 = Energy x regional grid carbon intensity at the chosen start time.
"""

from dataclasses import dataclass

DEFAULT_OVERHEAD_FACTOR = 1.4  # system + cooling overhead on top of raw GPU power draw


@dataclass
class JobEstimate:
    region: str
    start_hours_from_now: float
    gpu_power_w: float
    system_power_w: float
    energy_kwh: float
    carbon_intensity_gco2_per_kwh: float
    emissions_kg_co2: float
    cost_usd: float


def estimate_system_power_w(gpu_power_w: float, gpu_count: int, overhead_factor: float = DEFAULT_OVERHEAD_FACTOR) -> float:
    return gpu_power_w * gpu_count * overhead_factor


def estimate_energy_kwh(system_power_w: float, runtime_hours: float) -> float:
    return (system_power_w * runtime_hours) / 1000.0


def estimate_emissions_kg(energy_kwh: float, carbon_intensity_gco2_per_kwh: float) -> float:
    return (energy_kwh * carbon_intensity_gco2_per_kwh) / 1000.0
