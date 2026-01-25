import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="ComputeMarket - Settlement & Verification Layer",
    page_icon="https://em-content.zobj.net/source/apple/391/chart-increasing_1f4c8.png",
    layout="wide"
)

# Modern CSS theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --dark-gradient: linear-gradient(135deg, #0c1445 0%, #1a1a2e 50%, #16213e 100%);
        --accent-pink: #f093fb;
        --accent-green: #00d9a5;
        --accent-blue: #667eea;
    }

    .stApp {
        background: var(--dark-gradient);
        font-family: 'Inter', sans-serif;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, rgba(12, 20, 69, 0.95) 0%, rgba(26, 26, 46, 0.95) 100%);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: rgba(255, 255, 255, 0.8);
    }

    .page-header {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 1rem;
    }

    .page-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.2) 0%, rgba(240, 147, 251, 0.1) 100%);
        border: 1px solid rgba(240, 147, 251, 0.3);
        padding: 0.4rem 1.2rem;
        border-radius: 50px;
        font-size: 0.8rem;
        color: #f0abfc;
        font-weight: 500;
        margin-bottom: 1rem;
    }

    .page-title {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #f0abfc 50%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.75rem;
    }

    .page-subtitle {
        font-size: 1.1rem;
        color: rgba(255, 255, 255, 0.7);
        max-width: 700px;
        margin: 0 auto;
        line-height: 1.6;
    }

    .info-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .info-card-title {
        color: #a78bfa;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }

    .info-card-text {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1rem;
        line-height: 1.6;
        margin: 0;
    }

    .glass-panel {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 1.5rem;
        margin-bottom: 1rem;
    }

    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }

    .metric-value {
        font-size: 1.8rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00d9a5 0%, #667eea 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .metric-label {
        font-size: 0.85rem;
        color: rgba(255, 255, 255, 0.5);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-top: 0.25rem;
    }

    .partner-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1rem 1.25rem;
        margin-bottom: 0.75rem;
        border-left: 3px solid;
    }

    .partner-card.blue { border-left-color: #667eea; }
    .partner-card.green { border-left-color: #00d9a5; }
    .partner-card.orange { border-left-color: #ff9a56; }
    .partner-card.purple { border-left-color: #a78bfa; }

    .partner-name {
        color: #ffffff;
        font-weight: 600;
        font-size: 0.95rem;
        margin-bottom: 0.25rem;
    }

    .partner-desc {
        color: rgba(255, 255, 255, 0.6);
        font-size: 0.85rem;
        margin: 0;
    }

    .stTabs [data-baseweb="tab-list"] {
        background: rgba(255, 255, 255, 0.03);
        border-radius: 12px;
        padding: 0.5rem;
        gap: 0.5rem;
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent;
        border-radius: 8px;
        color: rgba(255, 255, 255, 0.6);
        font-weight: 500;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
        color: #ffffff;
    }

    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
    }

    .stMarkdown p {
        color: rgba(255, 255, 255, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("""
<div style="padding: 1rem 0;">
    <h3 style="color: #f0abfc; margin-bottom: 1rem;">ComputeMarket</h3>
    <p style="color: rgba(255,255,255,0.7); font-size: 0.9rem; line-height: 1.6;">
        Defines how AI compute is verified, settled, and energy-trusted
        across data centers and healthcare infrastructure.
    </p>
    <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
        <p style="color: rgba(255,255,255,0.5); font-size: 0.8rem; margin-bottom: 0.5rem;">KEY CONCEPTS</p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0.3rem 0;">&#8226; Compute Work Unit (CWU)</p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0.3rem 0;">&#8226; Energy-backed verification</p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0.3rem 0;">&#8226; Settlement-grade telemetry</p>
        <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem; margin: 0.3rem 0;">&#8226; Cross-boundary compute trust</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Page header
st.markdown("""
<div class="page-header">
    <div class="page-badge">Settlement Layer</div>
    <h1 class="page-title">ComputeMarket</h1>
    <p class="page-subtitle">
        We're not making AI faster. We're making AI <strong>real</strong>—defining how compute becomes
        verifiable, settleable, and energy-trusted.
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
    st.markdown("<h2 style='color: #ffffff; font-size: 1.5rem;'>Compute Work Unit (CWU) Definition</h2>", unsafe_allow_html=True)

    st.markdown("""
    <div class="info-card" style="background: linear-gradient(135deg, rgba(0, 217, 165, 0.1) 0%, rgba(0, 217, 165, 0.05) 100%); border-color: rgba(0, 217, 165, 0.2);">
        <h4 class="info-card-title" style="color: #00d9a5;">The New Primitive for AI Compute</h4>
        <p class="info-card-text">
            A <strong style="color: #00d9a5;">Compute Work Unit (CWU)</strong> is a completed computation task with verifiable energy backing—
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
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(255,255,255,0.02)',
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
        title=dict(text="Market Evolution: GPU-Hours to CWU Settlement", font=dict(color="white")),
        xaxis=dict(title="Date", gridcolor="rgba(255,255,255,0.1)", color="rgba(255,255,255,0.7)"),
        yaxis=dict(title="Market Share Index", gridcolor="rgba(255,255,255,0.1)", color="rgba(255,255,255,0.7)"),
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="center", x=0.5, font=dict(color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="rgba(255,255,255,0.8)")
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
        title=dict(text="Live Energy & Carbon Monitoring", font=dict(color="white")),
        xaxis=dict(title="Time", gridcolor="rgba(255,255,255,0.1)", color="rgba(255,255,255,0.7)"),
        yaxis=dict(title=dict(text="Power (W)", font=dict(color="#f87171")), gridcolor="rgba(255,255,255,0.1)", color="rgba(255,255,255,0.7)"),
        yaxis2=dict(title=dict(text="Carbon Intensity (gCO2/kWh)", font=dict(color="#00d9a5")), overlaying="y", side="right", color="rgba(255,255,255,0.7)"),
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, font=dict(color="white")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,0.02)",
        font=dict(color="rgba(255,255,255,0.8)")
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
st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
st.markdown("""
<div style="border-top: 1px solid rgba(255,255,255,0.1); padding-top: 2rem;">
    <h2 style="color: #ffffff; font-size: 1.5rem; margin-bottom: 0.5rem;">Traction & Partnerships</h2>
    <p style="color: rgba(255,255,255,0.6); margin-bottom: 1.5rem;">Strong Early Traction with Public Institutions & Regulated Industries</p>
</div>
""", unsafe_allow_html=True)

traction_col1, traction_col2 = st.columns(2)

with traction_col1:
    st.markdown("""
    <div class="partner-card blue">
        <p class="partner-name">Government of British Columbia</p>
        <p class="partner-desc">Public university consortium - Active PoCs around distributed research computing</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="partner-card orange">
        <p class="partner-name">Global Relay (Canada)</p>
        <p class="partner-desc">Financial compliance - PoCs on verifiable computation and auditability</p>
    </div>
    """, unsafe_allow_html=True)

with traction_col2:
    st.markdown("""
    <div class="partner-card green">
        <p class="partner-name">AIST (Japan)</p>
        <p class="partner-desc">World's largest quantum-AI data center - Use cases spanning quantum, AI, and energy</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="partner-card purple">
        <p class="partner-name">StrangeWorks + Hitachi</p>
        <p class="partner-desc">Joint proposals to energy infrastructure players</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<p style="margin-top: 1rem; font-style: italic; color: rgba(255,255,255,0.5); text-align: center;">
    As quantum, edge, and distributed computing blur boundaries of jurisdiction, responsibility, and execution,
    markets are not discovered—they are continuously created.
</p>
""", unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="margin-top: 3rem; padding-top: 2rem; border-top: 1px solid rgba(255,255,255,0.1); text-align: center;">
    <p style="color: rgba(255,255,255,0.6); font-size: 0.95rem; margin-bottom: 0.5rem;">
        <strong style="color: #f0abfc;">ComputeMarket</strong> — Defining how AI compute becomes verifiable, settleable, and trustworthy.
    </p>
    <p style="color: rgba(255,255,255,0.4); font-size: 0.8rem;">
        Part of the Prefrontal platform | Patent-pending technology
    </p>
</div>
""", unsafe_allow_html=True)
