import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="ComputeMarket - Settlement & Verification Layer",
    page_icon="🔗",
    layout="wide"
)

# Sidebar
st.sidebar.title("ComputeMarket")
st.sidebar.info("""
ComputeMarket defines how AI compute is verified, settled, and energy-trusted
across data centers and healthcare infrastructure.

**Key Concepts:**
- Compute Work Unit (CWU)
- Energy-backed verification
- Settlement-grade telemetry
- Cross-boundary compute trust
""")

# Main content
st.title("ComputeMarket: Settlement & Verification Layer for AI Compute")

st.markdown("""
<div style="border-left: 4px solid #1A237E; padding: 15px; background-color: #f0f4ff; margin-bottom: 20px;">
    <h3 style="margin-top: 0; color: #1A237E;">Defining Verifiable, Settleable, Energy-Backed AI Compute</h3>
    <p style="margin-bottom: 0;">
        We're not making AI faster. We're making AI <strong>real</strong>—creating the conditions under which
        AI can exist at scale by defining how compute becomes contractible, auditable, and trustworthy.
    </p>
</div>
""", unsafe_allow_html=True)

# Create main tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "Compute Work Unit (CWU)",
    "Settlement Dashboard",
    "Market Intelligence",
    "Energy Trust Anchor"
])

with tab1:
    st.header("Compute Work Unit (CWU) Definition")

    st.markdown("""
    <div style="background-color: #e8f5e9; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="color: #2e7d32; margin-top: 0;">The New Primitive for AI Compute</h4>
        <p style="font-size: 1.1em; margin-bottom: 0;">
            A <strong>Compute Work Unit (CWU)</strong> is a completed computation task with verifiable energy backing—
            turning compute from "usage" into "contractible work."
        </p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("CWU Components")

        st.markdown("""
        **What CWU Includes:**
        - Job specification (task type, resource request)
        - Deadline & completion window
        - Job completion status (success/fail)
        - Energy consumed (kWh)
        - Interruption/migration history
        - Verifiable receipt with attestation

        **What CWU Explicitly Excludes:**
        - GPU-hour equivalence
        - SKU-level guarantees (e.g., H100 x8 NVLink)
        - Normalized performance benchmarks
        - Direct performance comparison
        """)

        st.info("**Design Philosophy:** We intentionally avoid defining 'equivalent performance.' The MVP focuses on proving that computation happened, not how fast it happened.")

    with col2:
        st.subheader("CWU Receipt Schema")

        # Sample CWU receipt
        cwu_receipt = {
            "cwu_id": "CWU-2025-001847",
            "job_id": "JOB-ML-TRAIN-8847",
            "status": "COMPLETED",
            "start_time": "2025-01-25T10:00:00Z",
            "end_time": "2025-01-25T14:32:18Z",
            "node_id": "dc-west-node-042",
            "rack_id": "RACK-W-12",
            "energy_kwh_it": 12.47,
            "pue_used": 1.25,
            "energy_kwh_facility": 15.59,
            "carbon_intensity_gco2_kwh": 142.3,
            "co2e_kg": 2.22,
            "meter_source": "PDU_RACK_LEVEL",
            "checkpoint_count": 8,
            "interruption_count": 0,
            "provider_signature": "0x7f8a...3d2e",
            "verifier_signature": "0x9b4c...1a7f",
            "timestamp": "2025-01-25T14:32:20Z"
        }

        st.json(cwu_receipt)

        st.success("This receipt proves: computation happened, energy was consumed, and the result is auditable.")

    # CWU Flow Diagram
    st.subheader("CWU Lifecycle")

    # Create a flow visualization
    stages = ["Job Submission", "Execution", "Energy Measurement", "Receipt Generation", "Settlement"]
    stage_descriptions = [
        "Client submits job spec with deadline",
        "Compute executed on verified node",
        "kWh measured via PDU/meter",
        "CWU receipt with signatures",
        "Contract fulfilled, payment cleared"
    ]

    fig_flow = go.Figure()

    for i, (stage, desc) in enumerate(zip(stages, stage_descriptions)):
        # Add stage boxes
        fig_flow.add_trace(go.Scatter(
            x=[i],
            y=[1],
            mode='markers+text',
            marker=dict(size=60, color='#1A237E', symbol='square'),
            text=[f"<b>{i+1}</b>"],
            textfont=dict(color='white', size=16),
            hovertext=f"<b>{stage}</b><br>{desc}",
            hoverinfo='text',
            showlegend=False
        ))

        # Add stage labels
        fig_flow.add_annotation(
            x=i, y=0.5,
            text=f"<b>{stage}</b>",
            showarrow=False,
            font=dict(size=11)
        )

        fig_flow.add_annotation(
            x=i, y=0.2,
            text=desc,
            showarrow=False,
            font=dict(size=9, color='gray')
        )

        # Add arrows between stages
        if i < len(stages) - 1:
            fig_flow.add_annotation(
                x=i + 0.5, y=1,
                ax=i + 0.2, ay=1,
                xref='x', yref='y',
                axref='x', ayref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowcolor='#3949AB'
            )

    fig_flow.update_layout(
        height=250,
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.5, 4.5]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.2, 1.5]),
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=20)
    )

    st.plotly_chart(fig_flow, use_container_width=True)

with tab2:
    st.header("Settlement Dashboard")

    # Key metrics
    metric_cols = st.columns(4)

    with metric_cols[0]:
        st.metric(
            label="CWUs Settled (24h)",
            value="1,247",
            delta="+18%"
        )

    with metric_cols[1]:
        st.metric(
            label="Total Energy Verified",
            value="4,832 kWh",
            delta="+12%"
        )

    with metric_cols[2]:
        st.metric(
            label="Settlement Success Rate",
            value="99.7%",
            delta="+0.2%"
        )

    with metric_cols[3]:
        st.metric(
            label="Avg Settlement Time",
            value="2.3 sec",
            delta="-0.4 sec",
            delta_color="inverse"
        )

    st.markdown("---")

    # Recent CWU settlements
    st.subheader("Recent CWU Settlements")

    # Generate sample settlement data
    np.random.seed(42)
    n_settlements = 20

    settlement_data = pd.DataFrame({
        "cwu_id": [f"CWU-{i:06d}" for i in range(n_settlements)],
        "job_type": np.random.choice(["ML Training", "Inference", "Fine-tuning", "Data Processing"], n_settlements),
        "provider": np.random.choice(["DC-West", "DC-East", "DC-Central", "Partner-A"], n_settlements),
        "buyer": np.random.choice(["HealthCorp", "FinanceAI", "ResearchLab", "TechStartup"], n_settlements),
        "energy_kwh": np.random.uniform(1, 50, n_settlements).round(2),
        "co2_kg": np.random.uniform(0.1, 5, n_settlements).round(2),
        "status": np.random.choice(["Settled", "Settled", "Settled", "Pending", "Verified"], n_settlements),
        "settlement_time": np.random.uniform(1, 5, n_settlements).round(1),
        "timestamp": [(datetime.now() - timedelta(hours=np.random.randint(0, 24))).strftime("%Y-%m-%d %H:%M") for _ in range(n_settlements)]
    })

    # Style the status column
    def style_status(val):
        if val == "Settled":
            return "background-color: #d4edda; color: #155724"
        elif val == "Pending":
            return "background-color: #fff3cd; color: #856404"
        elif val == "Verified":
            return "background-color: #d1ecf1; color: #0c5460"
        return ""

    styled_df = settlement_data.style.applymap(style_status, subset=["status"])

    st.dataframe(
        styled_df,
        column_config={
            "cwu_id": st.column_config.Column("CWU ID", width="small"),
            "energy_kwh": st.column_config.NumberColumn("Energy (kWh)", format="%.2f"),
            "co2_kg": st.column_config.NumberColumn("CO2 (kg)", format="%.2f"),
            "settlement_time": st.column_config.NumberColumn("Settlement (s)", format="%.1f")
        },
        height=400,
        use_container_width=True
    )

    # Settlement analytics
    st.subheader("Settlement Analytics")

    analytics_cols = st.columns(2)

    with analytics_cols[0]:
        # Settlements by provider
        provider_data = settlement_data.groupby("provider").agg({
            "cwu_id": "count",
            "energy_kwh": "sum"
        }).reset_index()
        provider_data.columns = ["Provider", "CWU Count", "Total Energy (kWh)"]

        fig_provider = px.bar(
            provider_data,
            x="Provider",
            y="CWU Count",
            color="Total Energy (kWh)",
            title="Settlements by Provider",
            color_continuous_scale="Blues"
        )
        fig_provider.update_layout(height=300)
        st.plotly_chart(fig_provider, use_container_width=True)

    with analytics_cols[1]:
        # Settlements by job type
        job_data = settlement_data.groupby("job_type").size().reset_index(name="count")

        fig_job = px.pie(
            job_data,
            values="count",
            names="job_type",
            title="Settlements by Job Type",
            hole=0.4
        )
        fig_job.update_layout(height=300)
        st.plotly_chart(fig_job, use_container_width=True)

with tab3:
    st.header("Market Intelligence")

    st.markdown("""
    <div style="background-color: #fff3e0; padding: 15px; border-radius: 10px; border-left: 4px solid #ff9800; margin-bottom: 20px;">
        <h4 style="color: #e65100; margin-top: 0;">Market Context</h4>
        <p style="margin-bottom: 0;">
            The AI compute market is evolving from GPU-hours to energy-backed settlement units.
            Traditional marketplaces assume the unit exists—we're defining that unit.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Market positioning
    st.subheader("Ecosystem Positioning")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### What We Are
        - **Settlement & Verification Layer** for AI compute
        - **Energy-backed Receipt Generator**
        - **Trust Layer** across organizational boundaries
        - **Clearing Engine** for compute markets

        ### What We Are NOT
        - A GPU marketplace
        - A cloud provider
        - An optimization-only SaaS
        - A price comparison tool
        """)

    with col2:
        st.markdown("""
        ### How We Integrate with Ecosystem

        | Layer | Player | Our Role |
        |-------|--------|----------|
        | Grid Control | Emerald AI | Consume their telemetry |
        | Internal Optimization | Chamber | Receive supply signals |
        | Procurement | Compute Exchange | Provide settlement |
        | Observability | Datadog | Integrate metrics |

        *Others optimize or source compute. We make it legally and economically real.*
        """)

    # Market trends visualization
    st.subheader("Market Trends")

    # Generate market data
    dates = pd.date_range(start="2024-01-01", end="2025-12-31", freq="M")
    market_data = pd.DataFrame({
        "date": dates,
        "traditional_gpu_hours": 100 - np.arange(len(dates)) * 2 + np.random.normal(0, 3, len(dates)),
        "cwu_settlements": np.arange(len(dates)) * 4 + np.random.normal(0, 5, len(dates)),
        "energy_backed_compute": np.arange(len(dates)) * 3 + np.random.normal(0, 4, len(dates))
    })

    # Ensure no negative values (only for numeric columns)
    numeric_cols = ["traditional_gpu_hours", "cwu_settlements", "energy_backed_compute"]
    market_data[numeric_cols] = market_data[numeric_cols].clip(lower=0)

    fig_market = go.Figure()

    fig_market.add_trace(go.Scatter(
        x=market_data["date"],
        y=market_data["traditional_gpu_hours"],
        name="Traditional GPU-Hours",
        line=dict(color="#e74c3c", dash="dash"),
        fill='tozeroy',
        fillcolor='rgba(231, 76, 60, 0.1)'
    ))

    fig_market.add_trace(go.Scatter(
        x=market_data["date"],
        y=market_data["cwu_settlements"],
        name="CWU-Based Settlements",
        line=dict(color="#27ae60", width=3),
        fill='tozeroy',
        fillcolor='rgba(39, 174, 96, 0.2)'
    ))

    fig_market.add_trace(go.Scatter(
        x=market_data["date"],
        y=market_data["energy_backed_compute"],
        name="Energy-Backed Compute",
        line=dict(color="#3498db", width=2),
        fill='tozeroy',
        fillcolor='rgba(52, 152, 219, 0.1)'
    ))

    fig_market.update_layout(
        title="Market Evolution: GPU-Hours to CWU Settlement",
        xaxis_title="Date",
        yaxis_title="Market Share Index",
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5)
    )

    st.plotly_chart(fig_market, use_container_width=True)

    # Customer pain points
    st.subheader("Customer Pain Points & Solutions")

    pain_data = [
        {"segment": "Healthcare", "pain": "AI outputs cannot be proven or audited", "severity": "Critical", "solution": "CWU receipts with full audit trail"},
        {"segment": "Financial Services", "pain": "GPU inference logs lack compliance", "severity": "Critical", "solution": "Settlement-grade telemetry"},
        {"segment": "Data Centers", "pain": "Power constraints and failure risks", "severity": "High", "solution": "Energy-backed verification"},
        {"segment": "Research Labs", "pain": "Cross-institution compute sharing", "severity": "Medium", "solution": "Boundary-crossing CWU settlements"},
        {"segment": "AI Startups", "pain": "Unpredictable GPU costs", "severity": "High", "solution": "Energy-based cost transparency"}
    ]

    pain_df = pd.DataFrame(pain_data)

    def color_severity(val):
        if val == "Critical":
            return "background-color: #f8d7da; color: #721c24"
        elif val == "High":
            return "background-color: #fff3cd; color: #856404"
        elif val == "Medium":
            return "background-color: #d1ecf1; color: #0c5460"
        return ""

    styled_pain = pain_df.style.applymap(color_severity, subset=["severity"])
    st.dataframe(styled_pain, use_container_width=True, height=250)

with tab4:
    st.header("Energy Trust Anchor")

    st.markdown("""
    <div style="background-color: #e3f2fd; padding: 20px; border-radius: 10px; margin-bottom: 20px;">
        <h4 style="color: #1565c0; margin-top: 0;">Why Energy is the Truth Anchor</h4>
        <p style="font-size: 1.05em;">
            <strong>Performance can be manipulated. Logs can be forged. Energy consumption cannot be faked at scale.</strong>
        </p>
        <p style="margin-bottom: 0;">
            If compute is backed by energy, it becomes verifiable.<br>
            If it's verifiable, it becomes settleable.<br>
            If it's settleable, markets and regulation can exist.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Energy measurement hierarchy
    st.subheader("Energy Measurement Hierarchy")

    measurement_cols = st.columns(2)

    with measurement_cols[0]:
        st.markdown("""
        ### Tier A: External Measurement (Strongest)

        | Source | Trust Level | Use Case |
        |--------|-------------|----------|
        | Facility Meter | Highest | DC-wide verification |
        | UPS / Branch Circuit | High | Zone-level audit |
        | Rack PDU | High | Rack-level settlement |
        | Server BMC (IPMI) | Medium | Node-level tracking |

        **Why Tier A is preferred:**
        - Independent of job executor
        - Auditable by third parties
        - Aligned with utility billing
        """)

    with measurement_cols[1]:
        st.markdown("""
        ### Tier B: GPU-Level Estimation (Reference)

        | Source | Trust Level | Limitation |
        |--------|-------------|------------|
        | NVML/DCGM | Lower | Host-controlled |
        | RAPL (CPU) | Lower | Environment-dependent |
        | Software Estimation | Lowest | Model-based only |

        **Use Tier B when:**
        - External meters unavailable
        - PoC/development phase
        - Same-organization compute
        """)

    # Energy formula
    st.subheader("Energy Calculation")

    st.markdown("""
    ```
    CWU Energy Calculation:

    E_IT,job = Σ P_IT(t) × Δt        # IT energy: power integrated over time
    E_facility = E_IT × PUE          # Include cooling/overhead
    CO2e = E_facility × CI_region    # Carbon footprint

    Where:
    - P_IT(t): Power draw at time t (Watts)
    - Δt: Sampling interval (typically 1-10 seconds)
    - PUE: Power Usage Effectiveness (1.1 - 1.6 typical)
    - CI_region: Carbon Intensity of regional grid (gCO2/kWh)
    ```
    """)

    # Real-time energy monitoring simulation
    st.subheader("Real-Time Energy Monitoring")

    # Generate simulated energy data
    time_points = 60
    timestamps = [datetime.now() - timedelta(minutes=time_points-i) for i in range(time_points)]

    energy_trace = pd.DataFrame({
        "timestamp": timestamps,
        "power_w": np.random.normal(350, 30, time_points) + np.sin(np.arange(time_points) * 0.1) * 50,
        "carbon_intensity": np.random.normal(150, 20, time_points)
    })
    energy_trace["energy_kwh"] = energy_trace["power_w"].cumsum() / 1000 / 60  # Cumulative kWh
    energy_trace["co2_g"] = energy_trace["power_w"] * energy_trace["carbon_intensity"] / 1000  # gCO2

    fig_energy = go.Figure()

    fig_energy.add_trace(go.Scatter(
        x=energy_trace["timestamp"],
        y=energy_trace["power_w"],
        name="Power Draw (W)",
        line=dict(color="#e74c3c", width=2)
    ))

    fig_energy.add_trace(go.Scatter(
        x=energy_trace["timestamp"],
        y=energy_trace["carbon_intensity"],
        name="Carbon Intensity (gCO2/kWh)",
        line=dict(color="#27ae60", width=2, dash="dash"),
        yaxis="y2"
    ))

    fig_energy.update_layout(
        title="Live Energy & Carbon Monitoring",
        xaxis_title="Time",
        yaxis=dict(title=dict(text="Power (W)", font=dict(color="#e74c3c"))),
        yaxis2=dict(title=dict(text="Carbon Intensity (gCO2/kWh)", font=dict(color="#27ae60")), overlaying="y", side="right"),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02)
    )

    st.plotly_chart(fig_energy, use_container_width=True)

    # Summary metrics
    energy_metrics = st.columns(4)

    with energy_metrics[0]:
        st.metric("Current Power", f"{energy_trace['power_w'].iloc[-1]:.0f} W")

    with energy_metrics[1]:
        st.metric("Cumulative Energy", f"{energy_trace['energy_kwh'].iloc[-1]:.2f} kWh")

    with energy_metrics[2]:
        st.metric("Avg Carbon Intensity", f"{energy_trace['carbon_intensity'].mean():.0f} gCO2/kWh")

    with energy_metrics[3]:
        total_co2 = energy_trace['co2_g'].sum() / 1000
        st.metric("Total CO2", f"{total_co2:.2f} kg")

# Traction section
st.markdown("---")
st.header("Traction & Partnerships")

st.subheader("Strong Early Traction with Public Institutions & Regulated Industries")

traction_col1, traction_col2 = st.columns(2)

with traction_col1:
    st.markdown("""
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #1A237E; margin-bottom: 15px;">
        <strong>Government of British Columbia</strong><br>
        <span style="color: #666;">Public university consortium - Active PoCs around distributed research computing</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #f57c00; margin-bottom: 15px;">
        <strong>Global Relay (Canada)</strong><br>
        <span style="color: #666;">Financial compliance - PoCs on verifiable computation and auditability</span>
    </div>
    """, unsafe_allow_html=True)

with traction_col2:
    st.markdown("""
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #2e7d32; margin-bottom: 15px;">
        <strong>AIST (Japan)</strong><br>
        <span style="color: #666;">World's largest quantum-AI data center - Use cases spanning quantum, AI, and energy</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: white; padding: 15px; border-radius: 8px; border-left: 4px solid #7b1fa2; margin-bottom: 15px;">
        <strong>StrangeWorks + Hitachi</strong><br>
        <span style="color: #666;">Joint proposals to energy infrastructure players</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<p style="margin-top: 10px; font-style: italic; color: #666;">
    As quantum, edge, and distributed computing blur boundaries of jurisdiction, responsibility, and execution,
    markets are not discovered—they are continuously created.
</p>
""", unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9em;">
    <p><strong>ComputeMarket</strong> — Defining how AI compute becomes verifiable, settleable, and trustworthy.</p>
    <p style="font-size: 0.8em;">Part of the Prefrontal™ platform | Patent-pending technology</p>
</div>
""", unsafe_allow_html=True)
