import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Prefrontal | AI Infrastructure Governance",
    page_icon="https://em-content.zobj.net/source/apple/391/brain_1f9e0.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with clean white theme
st.markdown("""
<style>
    /* Import modern font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* Root variables for theming */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --bg-primary: #ffffff;
        --bg-secondary: #f8f9fc;
        --bg-card: #ffffff;
        --text-primary: #1a1a2e;
        --text-secondary: #64748b;
        --border-color: #e2e8f0;
        --accent-blue: #667eea;
        --accent-purple: #764ba2;
        --accent-pink: #f093fb;
        --accent-green: #10b981;
        --accent-orange: #f59e0b;
    }

    /* Global styles */
    .stApp {
        background: var(--bg-secondary);
        font-family: 'Inter', sans-serif;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--border-color);
    }

    [data-testid="stSidebar"] .stMarkdown {
        color: var(--text-secondary);
    }

    /* Hero section */
    .hero-container {
        text-align: center;
        padding: 3rem 2rem;
        margin-bottom: 2rem;
        background: #ffffff;
        border-radius: 24px;
        border: 1px solid var(--border-color);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }

    .hero-badge {
        display: inline-block;
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-size: 0.85rem;
        color: #667eea;
        font-weight: 600;
        letter-spacing: 0.5px;
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #1a1a2e 0%, #667eea 50%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 1rem;
        line-height: 1.1;
        letter-spacing: -1px;
    }

    .hero-subtitle {
        font-size: 1.3rem;
        color: var(--text-secondary);
        max-width: 700px;
        margin: 0 auto 2rem;
        line-height: 1.6;
        font-weight: 400;
    }

    /* Stats bar */
    .stats-container {
        display: flex;
        justify-content: center;
        gap: 3rem;
        margin: 2rem 0;
        flex-wrap: wrap;
    }

    .stat-item {
        text-align: center;
    }

    .stat-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .stat-label {
        font-size: 0.85rem;
        color: var(--text-secondary);
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 0.25rem;
    }

    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        margin: 2.5rem 0 1.5rem;
        padding-bottom: 1rem;
        border-bottom: 1px solid var(--border-color);
    }

    .section-icon {
        width: 44px;
        height: 44px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 1rem;
        font-size: 1.3rem;
    }

    .section-icon.infra {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .section-icon.trust {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(102, 126, 234, 0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .section-icon.market {
        background: linear-gradient(135deg, rgba(240, 147, 251, 0.1) 0%, rgba(240, 147, 251, 0.05) 100%);
        border: 1px solid rgba(240, 147, 251, 0.2);
    }

    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
        margin: 0;
    }

    /* Modern cards */
    .glass-card {
        background: #ffffff;
        border-radius: 20px;
        border: 1px solid var(--border-color);
        padding: 1.75rem;
        height: 100%;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }

    .glass-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 20px 40px -15px rgba(102, 126, 234, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }

    .card-icon {
        width: 50px;
        height: 50px;
        border-radius: 14px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        margin-bottom: 1.25rem;
    }

    .card-icon.green {
        background: linear-gradient(135deg, rgba(16, 185, 129, 0.15) 0%, rgba(16, 185, 129, 0.05) 100%);
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .card-icon.blue {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.15) 0%, rgba(102, 126, 234, 0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .card-icon.purple {
        background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(139, 92, 246, 0.05) 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
    }

    .card-icon.pink {
        background: linear-gradient(135deg, rgba(236, 72, 153, 0.15) 0%, rgba(236, 72, 153, 0.05) 100%);
        border: 1px solid rgba(236, 72, 153, 0.2);
    }

    .card-icon.orange {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.15) 0%, rgba(245, 158, 11, 0.05) 100%);
        border: 1px solid rgba(245, 158, 11, 0.2);
    }

    .card-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }

    .card-badge {
        font-size: 0.65rem;
        padding: 0.25rem 0.6rem;
        border-radius: 20px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .badge-infra {
        background: rgba(16, 185, 129, 0.1);
        color: #059669;
        border: 1px solid rgba(16, 185, 129, 0.2);
    }

    .badge-trust {
        background: rgba(102, 126, 234, 0.1);
        color: #667eea;
        border: 1px solid rgba(102, 126, 234, 0.2);
    }

    .badge-market {
        background: rgba(236, 72, 153, 0.1);
        color: #db2777;
        border: 1px solid rgba(236, 72, 153, 0.2);
    }

    .card-description {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
        margin-bottom: 1.25rem;
    }

    .card-features {
        list-style: none;
        padding: 0;
        margin: 0;
    }

    .card-feature {
        display: flex;
        align-items: center;
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-bottom: 0.6rem;
    }

    .feature-check {
        width: 20px;
        height: 20px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-right: 0.75rem;
        font-size: 0.7rem;
    }

    .feature-check.green {
        background: rgba(16, 185, 129, 0.15);
        color: #059669;
    }

    .feature-check.blue {
        background: rgba(102, 126, 234, 0.15);
        color: #667eea;
    }

    .feature-check.pink {
        background: rgba(236, 72, 153, 0.15);
        color: #db2777;
    }

    /* Highlight card */
    .highlight-card {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
        border: 1px solid rgba(102, 126, 234, 0.15);
        border-radius: 20px;
        padding: 2rem;
        position: relative;
        overflow: hidden;
    }

    .highlight-quote {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--text-primary);
        font-style: italic;
        margin-bottom: 1rem;
        line-height: 1.4;
    }

    .highlight-text {
        color: var(--text-secondary);
        font-size: 0.95rem;
        line-height: 1.6;
    }

    /* Problem statement */
    .problem-card {
        background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(239, 68, 68, 0.02) 100%);
        border: 1px solid rgba(239, 68, 68, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }

    .problem-label {
        color: #dc2626;
        font-weight: 600;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.75rem;
    }

    .problem-text {
        color: var(--text-secondary);
        font-size: 1rem;
        line-height: 1.7;
        margin: 0;
    }

    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25) !important;
    }

    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.35) !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        padding: 3rem 0 2rem;
        margin-top: 3rem;
        border-top: 1px solid var(--border-color);
    }

    .footer-text {
        color: var(--text-secondary);
        font-size: 0.85rem;
    }

    .footer-brand {
        color: var(--text-primary);
        font-weight: 600;
    }

    /* Force all text to be properly colored */
    h1, h2, h3, h4, h5, h6,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4,
    [data-testid="stHeader"], [data-testid="stSubheader"] {
        color: #1a1a2e !important;
    }

    .stMarkdown, .stMarkdown p, .stMarkdown li {
        color: #64748b !important;
    }

    .stMarkdown strong, .stMarkdown b {
        color: #1a1a2e !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        .hero-subtitle {
            font-size: 1.1rem;
        }
        .stats-container {
            gap: 1.5rem;
        }
        .stat-value {
            font-size: 2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# Hero Section
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">5+ Patents Pending</div>
    <h1 class="hero-title">Prefrontal</h1>
    <p class="hero-subtitle">
        Agent-driven infrastructure governance and cross-border energy optimization
        for next-generation AI data centers
    </p>
    <div class="stats-container">
        <div class="stat-item">
            <div class="stat-value">6</div>
            <div class="stat-label">Core Modules</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">3</div>
            <div class="stat-label">Patent Domains</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">4+</div>
            <div class="stat-label">Enterprise Partners</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Problem Statement
st.markdown("""
<div class="problem-card">
    <div class="problem-label">The Challenge</div>
    <p class="problem-text">
        Today's GPU infrastructure is ungoverned with no standard to log, validate, or dynamically control
        inference outputs or infrastructure-level risks. Existing hardware monitoring tools are insufficient,
        and compliance solutions don't address GPU workloads. AI systems are scaling faster than the
        infrastructure that monitors them.
    </p>
</div>
""", unsafe_allow_html=True)

# Section 1: GPU Infrastructure & Optimization
st.markdown("""
<div class="section-header">
    <div class="section-icon infra">&#9881;</div>
    <h2 class="section-title">GPU Infrastructure & Optimization</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon green">&#127793;</div>
        <div class="card-title">
            GreenGPU
            <span class="card-badge badge-infra">Infrastructure</span>
        </div>
        <p class="card-description">
            First-ever environmentally-aware GPU task scheduler that optimizes workloads
            across CO2 emissions, energy cost, and carbon credit ROI metrics.
        </p>
        <ul class="card-features">
            <li class="card-feature">
                <span class="feature-check green">&#10003;</span>
                Carbon-aware task scheduling
            </li>
            <li class="card-feature">
                <span class="feature-check green">&#10003;</span>
                Significant reduction in GPU carbon footprint
            </li>
            <li class="card-feature">
                <span class="feature-check green">&#10003;</span>
                ESG compliance reporting automation
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch GreenGPU", key="greengpu_btn", use_container_width=True):
        st.switch_page("pages/1_GreenGPU.py")

with col2:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon blue">&#128737;</div>
        <div class="card-title">
            GPU Health Monitor
            <span class="card-badge badge-infra">Infrastructure</span>
        </div>
        <p class="card-description">
            Breakthrough predictive analytics for GPU memory fragmentation and component reliability,
            going far beyond traditional hardware-only monitoring approaches.
        </p>
        <ul class="card-features">
            <li class="card-feature">
                <span class="feature-check green">&#10003;</span>
                Memory fragmentation analysis (patent-pending)
            </li>
            <li class="card-feature">
                <span class="feature-check green">&#10003;</span>
                Advanced failure prediction capabilities
            </li>
            <li class="card-feature">
                <span class="feature-check green">&#10003;</span>
                Proactive maintenance recommendations
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch GPU Health Monitor", key="gpuhealth_btn", use_container_width=True):
        st.switch_page("pages/2_GPU_Health.py")

st.markdown("""
<div class="glass-card">
    <div class="card-icon green">&#127757;</div>
    <div class="card-title">
        GreenGPU Explorer
        <span class="card-badge badge-infra">Infrastructure</span>
    </div>
    <p class="card-description">
        Carbon- and cost-aware recommender for cloud GPU jobs: given a workload, deadline
        and GPU count, ranks candidate regions and start times by estimated cost and CO2,
        using workload power profiles measured from real CUDA/DCGM benchmark runs.
    </p>
    <ul class="card-features">
        <li class="card-feature">
            <span class="feature-check green">&#10003;</span>
            Workload-aware power estimates from measured GPU telemetry
        </li>
        <li class="card-feature">
            <span class="feature-check green">&#10003;</span>
            Region and start-time ranking by cost / carbon / balanced priority
        </li>
        <li class="card-feature">
            <span class="feature-check green">&#10003;</span>
            Deadline-constrained scheduling, no live infrastructure access required
        </li>
    </ul>
</div>
""", unsafe_allow_html=True)
if st.button("Launch GreenGPU Explorer", key="greengpu_explorer_btn", use_container_width=True):
    st.switch_page("pages/7_GreenGPU_Explorer.py")

# Section 2: AI Assurance & Trust Layer
st.markdown("""
<div class="section-header">
    <div class="section-icon trust">&#128737;</div>
    <h2 class="section-title">AI Assurance & Trust Layer</h2>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon purple">&#128274;</div>
        <div class="card-title">
            AgentGuard
            <span class="card-badge badge-trust">Trust</span>
        </div>
        <p class="card-description">
            Industry-first dynamic risk-based output control system with real-time
            guardrails and automatic content moderation capabilities.
        </p>
        <ul class="card-features">
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Real-time risk scoring
            </li>
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Configurable thresholds
            </li>
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Regulatory compliance
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch AgentGuard", key="agentguard_btn", use_container_width=True):
        st.switch_page("pages/3_AgentGuard.py")

with col2:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon blue">&#128220;</div>
        <div class="card-title">
            TrustLog
            <span class="card-badge badge-trust">Trust</span>
        </div>
        <p class="card-description">
            Tamper-evident cryptographic logging for all AI outputs, enabling full
            auditability and verification for high-stakes AI deployments.
        </p>
        <ul class="card-features">
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Cryptographic verification
            </li>
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Chain-of-custody for AI
            </li>
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Full regulatory audit trail
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch TrustLog", key="trustlog_btn", use_container_width=True):
        st.switch_page("pages/4_TrustLog.py")

with col3:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon orange">&#128279;</div>
        <div class="card-title">
            EdgeSync
            <span class="card-badge badge-trust">Trust</span>
        </div>
        <p class="card-description">
            Patent-pending domain-restricted federated learning system that enables
            cross-organization AI without compromising data sovereignty.
        </p>
        <ul class="card-features">
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Domain-restricted inference
            </li>
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Differential privacy
            </li>
            <li class="card-feature">
                <span class="feature-check blue">&#10003;</span>
                Cross-org knowledge sharing
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch EdgeSync", key="edgesync_btn", use_container_width=True):
        st.switch_page("pages/5_EdgeSync.py")

# Section 3: Compute Settlement & Market Infrastructure
st.markdown("""
<div class="section-header">
    <div class="section-icon market">&#128279;</div>
    <h2 class="section-title">Compute Settlement & Market Infrastructure</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("""
    <div class="glass-card">
        <div class="card-icon pink">&#128200;</div>
        <div class="card-title">
            ComputeMarket
            <span class="card-badge badge-market">Settlement</span>
        </div>
        <p class="card-description">
            Industry-first settlement and verification layer for AI compute. Defines how computation
            becomes verifiable, settleable, and energy-trusted across data centers and healthcare infrastructure.
        </p>
        <ul class="card-features">
            <li class="card-feature">
                <span class="feature-check pink">&#10003;</span>
                Compute Work Unit (CWU) - new primitive for compute trading
            </li>
            <li class="card-feature">
                <span class="feature-check pink">&#10003;</span>
                Energy-backed verification and receipts
            </li>
            <li class="card-feature">
                <span class="feature-check pink">&#10003;</span>
                Settlement-grade telemetry for cross-boundary trust
            </li>
            <li class="card-feature">
                <span class="feature-check pink">&#10003;</span>
                Healthcare & financial compliance ready
            </li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Launch ComputeMarket", key="computemarket_btn", use_container_width=True):
        st.switch_page("pages/6_ComputeMarket.py")

with col2:
    st.markdown("""
    <div class="highlight-card">
        <p class="highlight-quote">"We're not making AI faster.<br>We're making AI <em>real</em>."</p>
        <p class="highlight-text">
            Energy is the only non-fungible truth in AI compute. If compute is backed by energy,
            it becomes verifiable. If it's verifiable, markets and regulation can exist.
        </p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p class="footer-text">
        <span class="footer-brand">Prefrontal</span> by Masatoshi Honda |
        AI Infrastructure Governance and Cross-border Energy Optimization
    </p>
    <p class="footer-text" style="margin-top: 0.5rem; font-size: 0.8rem;">
        Certain core technologies presented in this platform are patent pending
    </p>
</div>
""", unsafe_allow_html=True)
