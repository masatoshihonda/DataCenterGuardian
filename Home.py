import streamlit as st

# Set page configuration
st.set_page_config(
    page_title="Prefrontal™ | AI Infrastructure Governance and Cross-border Energy Optimization",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional styling
st.markdown("""
    <style>
    .main-title {
        font-size: 2.8rem;
        font-weight: 800;
        color: #1A237E;
        margin-bottom: 0.5rem;
        text-align: center;
        letter-spacing: -0.5px;
    }
    .platform-name {
        color: #3949AB; 
        font-weight: 900;
    }
    .subtitle {
        font-size: 1.25rem;
        color: #424242;
        text-align: center;
        margin-bottom: 0.5rem;
        font-weight: 400;
        max-width: 800px;
        margin-left: auto;
        margin-right: auto;
    }
    .value-proposition {
        background: linear-gradient(90deg, rgba(26,35,126,0.03) 0%, rgba(26,35,126,0.09) 50%, rgba(26,35,126,0.03) 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin: 2rem auto;
        max-width: 90%;
        text-align: center;
        border-left: 4px solid #3949AB;
        border-right: 4px solid #3949AB;
    }
    .value-text {
        font-size: 1.15rem;
        color: #37474F;
        line-height: 1.6;
        font-weight: 400;
    }
    .category-header {
        color: #1A237E;
        font-weight: 700;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #E0E0E0;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
    }
    .category-icon {
        margin-right: 10px;
        color: #3949AB;
    }
    .tool-card {
        background-color: white;
        border-radius: 10px;
        padding: 1.8rem;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
        border: 1px solid #F0F0F0;
        height: 100%;
        transition: transform 0.3s, box-shadow 0.3s;
    }
    .tool-card:hover {
        transform: translateY(-7px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    .tool-title {
        color: #1A237E;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.75rem;
        display: flex;
        align-items: center;
    }
    .tool-description {
        color: #455A64;
        font-size: 1rem;
        margin-bottom: 1.25rem;
        line-height: 1.6;
    }
    .key-feature {
        display: flex;
        align-items: center;
        margin: 8px 0;
        color: #455A64;
    }
    .feature-icon {
        color: #3949AB;
        margin-right: 8px;
        font-size: 14px;
    }
    .stat-highlight {
        background-color: rgba(57, 73, 171, 0.07);
        border-radius: 6px;
        padding: 0.15rem 0.5rem;
        margin: 0 0.2rem;
        font-weight: 600;
        color: #1A237E;
        display: inline-block;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding-top: 1.5rem;
        border-top: 1px solid #E0E0E0;
        color: #757575;
        font-size: 0.9rem;
    }
    .badge {
        font-size: 0.75rem;
        padding: 0.25rem 0.6rem;
        border-radius: 4px;
        margin-left: 0.8rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .badge-infra {
        background-color: rgba(76, 175, 80, 0.15);
        color: #2E7D32;
    }
    .badge-ai {
        background-color: rgba(33, 150, 243, 0.15);
        color: #1565C0;
    }
    .metrics-container {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin: 2rem 0;
    }
    .metric-item {
        text-align: center;
        padding: 1rem;
    }
    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1A237E;
        margin-bottom: 0.5rem;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #616161;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Change the primary button color to blue from red */
    .stButton > button {
        background-color: #1A237E !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:hover {
        background-color: #3949AB !important;
        color: white !important;
        border: none !important;
    }
    .stButton > button:active {
        background-color: #303F9F !important;
        color: white !important;
        border: none !important;
    }
    </style>
""", unsafe_allow_html=True)

# Main title and heading
st.markdown("<h1 class='main-title'><span class='platform-name'>Prefrontal™</span> | AI Infrastructure Governance and Cross-border Energy Optimization</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Agent-driven infrastructure governance and cross-border energy optimization for next-gen data centers</p>", unsafe_allow_html=True)

# Value proposition and problem statement
st.markdown("""
<div class="value-proposition">
    <p class="value-text">
        Modern GPU infrastructure lacks governance standards—Prefrontal™ is a <span class="stat-highlight">5+ patents pending</span> platform enabling GPUs to 
        <b>self-optimize</b>, <b>self-explain</b>, and <b>self-audit</b> across energy, health, and AI compliance layers.
    </p>
</div>
""", unsafe_allow_html=True)

# Problem statement
st.markdown("""
<div style="max-width: 90%; margin: 20px auto; padding: 15px; background-color: rgba(25,118,210,0.05); border-left: 3px solid #1976D2; border-radius: 4px;">
    <p style="margin: 0; color: #37474F; font-size: 1.05rem;">
        <span style="font-weight: 600; color: #1565C0;">The Problem:</span> 
        Today's GPU infrastructure is ungoverned with no standard to log, validate, or dynamically control inference outputs or 
        infrastructure-level risks. Existing hardware monitoring tools are insufficient, and compliance solutions don't address GPU workloads. 
        AI systems are scaling faster than the infrastructure that monitors them.
    </p>
</div>
""", unsafe_allow_html=True)

# Main content container
with st.container():
    # Section 1: GPU Infrastructure & Optimization
    st.markdown("<h2 class='category-header'><span class='category-icon'>🔧</span> GPU Infrastructure & Optimization</h2>", unsafe_allow_html=True)
    
    gpu_col1, gpu_col2 = st.columns(2)
    
    with gpu_col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">GreenGPU™ <span class="badge badge-infra">Infrastructure</span></div>
            <p class="tool-description">
                First-ever environmentally-aware GPU task scheduler that optimizes workloads across CO₂ emissions, 
                energy cost, and carbon credit ROI metrics.
            </p>
            <div class="key-feature"><span class="feature-icon">✓</span> Carbon-aware task scheduling</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Significant reduction in GPU carbon footprint</div>
            <div class="key-feature"><span class="feature-icon">✓</span> ESG compliance reporting automation</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch GreenGPU™", key="greengpu_btn", 
                     use_container_width=True, type="primary"):
            st.switch_page("pages/1_GreenGPU.py")
    
    with gpu_col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">GPU Health Monitor™ <span class="badge badge-infra">Infrastructure</span></div>
            <p class="tool-description">
                Breakthrough predictive analytics for GPU memory fragmentation and component reliability,
                going far beyond traditional hardware-only monitoring approaches.
            </p>
            <div class="key-feature"><span class="feature-icon">✓</span> Memory fragmentation analysis (patent-pending)</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Advanced failure prediction capabilities</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Proactive maintenance recommendations</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch GPU Health Monitor™", key="gpuhealth_btn", 
                     use_container_width=True, type="primary"):
            st.switch_page("pages/2_GPU_Health.py")
    
    # Spacer
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Section 2: AI Assurance & Trust Layer
    st.markdown("<h2 class='category-header'><span class='category-icon'>🛡️</span> AI Assurance & Trust Layer</h2>", unsafe_allow_html=True)
    
    ai_col1, ai_col2, ai_col3 = st.columns(3)
    
    with ai_col1:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">AgentGuard™ <span class="badge badge-ai">Trust</span></div>
            <p class="tool-description">
                Industry-first dynamic risk-based output control system with real-time 
                guardrails and automatic content moderation capabilities.
            </p>
            <div class="key-feature"><span class="feature-icon">✓</span> Real-time risk scoring and analysis</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Configurable moderation thresholds</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Regulatory compliance automation</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch AgentGuard™", key="agentguard_btn", 
                     use_container_width=True, type="primary"):
            st.switch_page("pages/3_AgentGuard.py")
    
    with ai_col2:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">TrustLog™ <span class="badge badge-ai">Trust</span></div>
            <p class="tool-description">
                Tamper-evident cryptographic logging for all AI outputs, enabling full 
                auditability and verification for high-stakes AI deployments.
            </p>
            <div class="key-feature"><span class="feature-icon">✓</span> Cryptographic verification (patent-pending)</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Chain-of-custody for AI assets</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Full regulatory audit trail</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch TrustLog™", key="trustlog_btn", 
                     use_container_width=True, type="primary"):
            st.switch_page("pages/4_TrustLog.py")
    
    with ai_col3:
        st.markdown("""
        <div class="tool-card">
            <div class="tool-title">EdgeSync™ <span class="badge badge-ai">Trust</span></div>
            <p class="tool-description">
                Patent-pending domain-restricted federated learning system that enables 
                cross-organization AI without compromising data sovereignty.
            </p>
            <div class="key-feature"><span class="feature-icon">✓</span> Domain-restricted inference</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Differential privacy guarantees</div>
            <div class="key-feature"><span class="feature-icon">✓</span> Cross-organizational knowledge sharing</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Launch EdgeSync™", key="edgesync_btn", 
                     use_container_width=True, type="primary"):
            st.switch_page("pages/5_EdgeSync.py")

    # Spacer before footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div class='footer'>
        <div style="margin-bottom: 10px;">© 2025 Prefrontal™ by Masatoshi Honda | AI Infrastructure Governance and Cross-border Energy Optimization</div>
        <div style="font-size: 0.8rem; color: #9E9E9E;">
            Certain core technologies presented in this platform are patent pending
        </div>
    </div>
    """, unsafe_allow_html=True)
