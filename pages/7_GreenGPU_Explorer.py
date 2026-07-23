import pandas as pd
import plotly.express as px
import streamlit as st

from scheduler import carbon, live_carbon, live_carbon_entsoe, live_carbon_watttime, pricing
from scheduler.optimizer import recommend
from telemetry.parse_dcgm_log import build_benchmark_profiles_csv

st.set_page_config(
    page_title="GreenGPU Explorer - Carbon & Cost-aware GPU Scheduling",
    page_icon="🌍",
    layout="wide",
)

st.sidebar.title("GreenGPU Explorer")
st.sidebar.info(
    """
KEHAI GreenGPU Explorer recommends **where** and **when** to run a GPU job
across cloud regions, trading off cost, CO2 and how long you're willing to
wait.

Workload power profiles come from real DCGM telemetry captured while running
the CUDA benchmarks in `gpu-benchmarks/cuda/` (compute-bound vs memory-bound),
so the same job shape isn't treated the same everywhere.
"""
)

st.title("🌍 KEHAI GreenGPU Explorer")
st.caption(
    "Compare where and when to run a GPU workload based on estimated cost, "
    "carbon intensity and completion deadline."
)

st.warning(
    "Estimated operational emissions based on public cloud pricing, published "
    "hardware specifications and regional grid-carbon data. Actual emissions "
    "may vary with server utilization, power usage effectiveness, cloud "
    "allocation and contractual pricing. These figures support relative "
    "comparison between candidates, not audited/exact emissions reporting."
)

with st.expander("🧪 Live carbon data"):
    st.caption(
        "**eu-west-2 (London) always tries a real live feed first, no key "
        "needed**: the UK's free Carbon Intensity API "
        "(api.carbonintensity.org.uk), verified against real responses -- "
        "true regional data (not a national average) with a real 24h "
        "forecast. Every other region defaults to a modeled day/night "
        "carbon curve shaped around a real published annual average (see "
        "data/README.md).\n\n"
        "**All four live providers are now verified with real data.** "
        "Electricity Maps confirmed real 24h forecasts across multiple "
        "zones; WattTime confirmed real data for us-west-1/CAISO_NORTH "
        "(a free account only gets that one region -- the others need a "
        "paid plan and correctly fall back to modeled); ENTSO-E confirmed "
        "a real generation mix for the EU zones, used to re-anchor the "
        "modeled curve's current value (it doesn't forecast -- see "
        "`scheduler/live_carbon_entsoe.py`). Any live fetch that still "
        "fails for any reason silently falls back to the modeled curve "
        "for that region -- check the 'carbon source' column below to "
        "see what was actually used for each row."
    )

    col_em, col_wt, col_entsoe = st.columns(3)

    with col_em:
        st.caption("[Electricity Maps](https://www.electricitymaps.com/free-tier) (any region) -- verified")
        api_key_input = st.text_input(
            "API key", value=live_carbon.get_api_key() or "", type="password", key="em_key",
        )
        electricitymaps_api_key = api_key_input or None

    with col_wt:
        st.caption(
            "[WattTime](https://www.watttime.org/get-the-data/) (US/Canada regions) "
            "-- verified for CAISO_NORTH (us-west-1) on a free account"
        )
        wt_creds = live_carbon_watttime.get_credentials()
        wt_username = st.text_input("Username", value=(wt_creds[0] if wt_creds else ""), key="wt_user")
        wt_password = st.text_input(
            "Password", value=(wt_creds[1] if wt_creds else ""), type="password", key="wt_pass",
        )
        watttime_credentials = (wt_username, wt_password) if wt_username and wt_password else None

    with col_entsoe:
        st.caption(
            "[ENTSO-E](https://transparency.entsoe.eu) (EU regions, current-value "
            "anchor only) -- verified"
        )
        entsoe_token_input = st.text_input(
            "Security token",
            value=live_carbon_entsoe.get_security_token() or "",
            type="password",
            key="entsoe_key",
        )
        entsoe_security_token = entsoe_token_input or None

# GPU TDP reference used to scale an observed power-draw pattern from one GPU
# model to another (illustrative, from published spec sheets).
GPU_TDP_W = {
    "L40S": 350,
    "A100_80GB": 400,
    "H100_80GB": 700,
}


@st.cache_data
def load_benchmark_profiles() -> pd.DataFrame:
    try:
        return pd.read_csv("data/benchmark_profiles.csv")
    except FileNotFoundError:
        return build_benchmark_profiles_csv()


@st.cache_data
def load_reference_tables():
    return carbon.load_region_table(), pricing.load_pricing_table()


profiles = load_benchmark_profiles()
regions_df, pricing_df = load_reference_tables()

st.subheader("1. Measured workload power profiles (from real CUDA/DCGM runs)")
col_chart, col_table = st.columns([2, 1])

with col_chart:
    fig = px.bar(
        profiles,
        x="workload",
        y=["avg_power_w", "peak_power_w"],
        barmode="group",
        labels={"value": "Power (W)", "workload": "Workload", "variable": "Metric"},
        title="Compute-bound vs memory-bound power draw (NVIDIA L40S)",
    )
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.dataframe(
        profiles[["workload", "avg_power_w", "peak_power_w", "avg_gpu_util_pct"]],
        hide_index=True,
        use_container_width=True,
    )
    st.caption(
        "Same GPU, same wall-clock time, ~3x difference in average power draw "
        "-> workload shape changes the CO2 estimate, not just GPU-hours."
    )

st.subheader("2. Describe your job")

input_cols = st.columns(5)

with input_cols[0]:
    workload_choice = st.selectbox(
        "Workload profile",
        options=list(profiles["workload"]) + ["Custom power draw"],
    )
    if workload_choice == "Custom power draw":
        custom_power_w = st.number_input("Power draw per GPU (W)", min_value=10, max_value=1000, value=300)
        benchmarked_power_w = float(custom_power_w)
        benchmarked_tdp_w = float(custom_power_w)
    else:
        row = profiles[profiles["workload"] == workload_choice].iloc[0]
        benchmarked_power_w = float(row["avg_power_w"])
        benchmarked_tdp_w = float(row["power_limit_w"])

with input_cols[1]:
    gpu_model = st.selectbox("Target GPU model (for pricing)", options=list(GPU_TDP_W.keys()), index=0)
    gpu_count = st.number_input("Number of GPUs", min_value=1, max_value=64, value=4)

with input_cols[2]:
    runtime_hours = st.number_input("Runtime (hours)", min_value=0.5, max_value=72.0, value=6.0, step=0.5)
    deadline_choice = st.selectbox("Deadline", options=["Now", "Within 24 hours", "Within 48 hours"])
    deadline_hours = {"Now": 0, "Within 24 hours": 24, "Within 48 hours": 48}[deadline_choice]

with input_cols[3]:
    preference = st.select_slider("Priority", options=["Cheapest", "Balanced", "Greenest"], value="Balanced")

with input_cols[4]:
    pricing_type = st.radio("Pricing", options=["On-Demand", "Spot"], horizontal=True)
    instance_options = ["Any (cheapest real SKU)"] + sorted(
        pricing_df.loc[pricing_df["gpu_model"] == gpu_model, "instance_type"].unique()
    )
    instance_choice = st.selectbox("Instance type", options=instance_options)
    instance_type = None if instance_choice == "Any (cheapest real SKU)" else instance_choice

if pricing_type == "Spot":
    st.caption(
        "Spot prices are real AWS spot quotes from the catalog snapshot, but spot "
        "capacity can be reclaimed with short notice and prices fluctuate "
        "continuously -- treat this as directional, not a locked-in rate."
    )

# Scale the observed power-draw pattern to the target GPU's TDP so a
# memory-bound profile measured on an L40S still gives a sensible estimate
# when the user is pricing out an A100 or H100.
scale_factor = GPU_TDP_W[gpu_model] / benchmarked_tdp_w if benchmarked_tdp_w else 1.0
scaled_gpu_power_w = benchmarked_power_w * scale_factor

st.caption(
    f"Using {benchmarked_power_w:.0f} W measured average power, scaled to "
    f"{scaled_gpu_power_w:.0f} W/GPU for {gpu_model} (TDP-ratio scaling)."
)

if st.button("Find best region & start time", type="primary"):
    candidates = recommend(
        gpu_power_w=scaled_gpu_power_w,
        gpu_count=int(gpu_count),
        runtime_hours=float(runtime_hours),
        deadline_hours=float(deadline_hours),
        gpu_model=gpu_model,
        preference=preference,
        pricing_type=pricing_type,
        instance_type=instance_type,
        regions_df=regions_df,
        pricing_df=pricing_df,
        electricitymaps_api_key=electricitymaps_api_key,
        watttime_credentials=watttime_credentials,
        entsoe_security_token=entsoe_security_token,
    )

    if candidates.empty:
        st.error(
            f"No {pricing_type} pricing available for {gpu_model}"
            + (f" on {instance_type}" if instance_type else "")
            + " in any modeled region."
        )
    else:
        st.subheader("3. Recommendation")

        best = candidates.iloc[0]
        now_baseline = candidates[candidates["start_hours_from_now"] == 0].sort_values("cost_usd").iloc[0]

        metric_cols = st.columns(5)
        metric_cols[0].metric("Recommended region", best["region"])
        start_label = "Now" if best["start_hours_from_now"] == 0 else f"in {int(best['start_hours_from_now'])}h"
        metric_cols[1].metric("Start", start_label)
        metric_cols[2].metric("Instance type", best["instance_type"])
        metric_cols[3].metric("Estimated cost", f"${best['cost_usd']:.2f}")
        metric_cols[4].metric("Estimated CO2", f"{best['emissions_kg_co2']:.2f} kg")

        if now_baseline["emissions_kg_co2"] > 0 and best["emissions_kg_co2"] < now_baseline["emissions_kg_co2"]:
            reduction_pct = (
                (now_baseline["emissions_kg_co2"] - best["emissions_kg_co2"])
                / now_baseline["emissions_kg_co2"]
                * 100
            )
            st.success(
                f"Vs. running now in the cheapest region right now "
                f"({now_baseline['region']}, {now_baseline['emissions_kg_co2']:.2f} kg CO2): "
                f"**{reduction_pct:.0f}% lower estimated emissions**."
            )

        st.markdown("#### Top candidates")
        display_cols = [
            "rank", "region", "instance_type", "start_hours_from_now", "cost_usd",
            "energy_kwh", "avg_carbon_intensity_gco2_per_kwh", "emissions_kg_co2",
            "carbon_data_source", "score",
        ]
        st.dataframe(
            candidates[display_cols].head(15).rename(columns={
                "instance_type": "instance",
                "start_hours_from_now": "start (h from now)",
                "cost_usd": "cost (USD)",
                "energy_kwh": "energy (kWh)",
                "avg_carbon_intensity_gco2_per_kwh": "avg carbon (gCO2/kWh)",
                "emissions_kg_co2": "emissions (kg CO2)",
                "carbon_data_source": "carbon source",
            }),
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("#### Cost vs. carbon tradeoff across all candidates")
        scatter = px.scatter(
            candidates,
            x="cost_usd",
            y="emissions_kg_co2",
            color="region",
            size="start_hours_from_now",
            hover_data=["start_hours_from_now", "avg_carbon_intensity_gco2_per_kwh"],
            labels={"cost_usd": "Cost (USD)", "emissions_kg_co2": "Emissions (kg CO2)"},
        )
        st.plotly_chart(scatter, use_container_width=True)

        csv = candidates[display_cols].to_csv(index=False)
        st.download_button("Download candidates as CSV", csv, file_name="greengpu_explorer_candidates.csv")
