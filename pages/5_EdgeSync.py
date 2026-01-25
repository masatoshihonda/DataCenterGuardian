import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="EdgeSync - AI System Monitoring Dashboard",
    page_icon="🔄",
    layout="wide"
)

# Custom CSS for more professional look
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        font-weight: 700;
        color: #0A2647;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        color: #144272;
        letter-spacing: 0.5px;
        font-size: 1.2rem;
        font-weight: 500;
        margin-bottom: 1.5rem;
    }
    .card {
        border-radius: 8px;
        padding: 20px;
        background-color: #FFFFFF;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border: 1px solid #EBEEF2;
    }
    .status-indicator {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 5px;
    }
    .status-active {
        background-color: #4CAF50;
    }
    .status-inactive {
        background-color: #F44336;
    }
    .status-syncing {
        background-color: #2196F3;
        animation: pulse 1.5s infinite;
    }
    .node-card {
        border-left: 4px solid #2196F3;
        padding: 15px;
        margin-bottom: 15px;
        background-color: rgba(33, 150, 243, 0.05);
    }
    @keyframes pulse {
        0% {
            opacity: 1;
        }
        50% {
            opacity: 0.4;
        }
        100% {
            opacity: 1;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Main title and description
st.markdown("<h1 class='main-header'>EdgeSync × Confidentiality-Aware Federated AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>This demo simulates domain-restricted inference and knowledge distillation-based model sync.</p>", unsafe_allow_html=True)

# Create a layout for the main content
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### Federated Inference")
    
    # Node selection
    location = st.selectbox(
        "Select Location", 
        ["Hospital A", "Hospital B"]
    )
    
    # Domain selection
    domain = st.selectbox(
        "Select Domain", 
        ["cardiology", "oncology", "general"]
    )
    
    # Input text area
    user_input = st.text_area(
        "Inference Input",
        "Enter your medical query here...",
        height=150
    )
    
    # Create columns for buttons
    button_cols = st.columns([1, 1])
    
    with button_cols[0]:
        run_inference = st.button("Run Federated Inference", type="primary", use_container_width=True)
    
    with button_cols[1]:
        sync_button = st.button("Distill & Sync Output", use_container_width=True)
    
    # Display domain access information
    st.markdown("#### Domain Access Status")
    
    # Create a table for domain access information
    domain_data = {
        "Domain": ["cardiology", "oncology", "general"],
        "Hospital A": ["Full Access", "Full Access", "Full Access"],
        "Hospital B": ["Restricted", "Full Access", "Full Access"]
    }
    
    domain_df = pd.DataFrame(domain_data)
    
    # Style the table
    def highlight_restricted(val):
        if val == "Restricted":
            return 'background-color: rgba(244, 67, 54, 0.1); color: #C62828;'
        elif val == "Full Access":
            return 'background-color: rgba(76, 175, 80, 0.1); color: #2E7D32;'
        return ''
    
    styled_domains = domain_df.style.map(highlight_restricted)
    st.dataframe(styled_domains, use_container_width=True)
    
    # Process inference
    if run_inference:
        st.markdown("#### Inference Results")
        
        # Show a warning for restricted domain
        if domain == "cardiology" and location == "Hospital B":
            st.warning("⚠️ **Access Denied**: Cardiology domain is restricted in Hospital B node. Access request logged.")
            
            # Show audit log
            st.markdown("""
            <div style="background-color: rgba(244, 67, 54, 0.05); padding: 10px; border-radius: 5px; font-family: monospace; font-size: 0.85rem; margin-top: 10px;">
                [AUDIT] [{}] - Restricted domain access attempt: User requested cardiology inference at Hospital B
            </div>
            """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)
        else:
            # Show a loading spinner
            with st.spinner("Running federated inference..."):
                time.sleep(1.5)  # Simulate processing time
            
            # Reverse the input as a simple "model output"
            output = user_input[::-1]
            
            # Display the result
            st.success("✅ Inference completed successfully")
            
            st.markdown("""
            <div class="card">
                <h4 style="margin-top: 0;">Model Output:</h4>
                <p style="background-color: #f9f9f9; padding: 10px; border-radius: 5px;">{}</p>
                <p style="font-size: 0.8rem; color: #777; margin-bottom: 0;">
                    Processed by {} / {} federated node
                </p>
            </div>
            """.format(output, location, domain), unsafe_allow_html=True)
            
            # Show audit log
            st.markdown("""
            <div style="background-color: rgba(33, 150, 243, 0.05); padding: 10px; border-radius: 5px; font-family: monospace; font-size: 0.85rem; margin-top: 10px;">
                [INFO] [{}] - Inference completed: {} characters processed in {} domain at {}
            </div>
            """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), len(user_input), domain, location), unsafe_allow_html=True)
    
    # Process sync
    if sync_button:
        st.markdown("#### Knowledge Sync Status")
        
        # Show a loading spinner
        with st.spinner("Syncing knowledge across federated nodes..."):
            time.sleep(2.0)  # Simulate processing time
        
        # Display sync log
        st.info("🔄 Knowledge distillation and model sync in progress")
        
        # Create a progress bar
        sync_progress = st.progress(0)
        
        # Simulate progress
        for i in range(101):
            sync_progress.progress(i)
            time.sleep(0.02)
        
        st.success("✅ Knowledge sync completed successfully")
        
        # Show sync details
        st.markdown("""
        <div style="background-color: rgba(76, 175, 80, 0.05); padding: 15px; border-radius: 5px; margin-top: 10px;">
            <h4 style="margin-top: 0; color: #2E7D32;">Sync Report</h4>
            <ul style="margin-bottom: 0;">
                <li>Knowledge distilled from {} domain models</li>
                <li>Privacy-preserving gradient updates applied</li>
                <li>Differential privacy ε = 2.1 maintained</li>
                <li>Model performance variance: ±1.2%</li>
            </ul>
        </div>
        """.format(domain), unsafe_allow_html=True)

with col2:
    st.markdown("### Network Status")
    
    # Display node status
    st.markdown("""
    <div class="card">
        <h4 style="margin-top: 0;">Active Federated Nodes</h4>
        <div style="margin-bottom: 15px;">
            <span class="status-indicator status-active"></span> Hospital A <span style="font-size: 0.8rem; color: #666; margin-left: 10px;">Last sync: 5m ago</span>
        </div>
        <div>
            <span class="status-indicator status-active"></span> Hospital B <span style="font-size: 0.8rem; color: #666; margin-left: 10px;">Last sync: 17m ago</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display sync history
    st.markdown("#### Sync History")
    
    # Create sample sync history data
    sync_history = [
        {"time": "10:15 AM", "node": "Hospital A", "domains": "cardiology, general", "status": "Completed"},
        {"time": "09:47 AM", "node": "Hospital B", "domains": "oncology, general", "status": "Completed"},
        {"time": "08:30 AM", "node": "Hospital A", "domains": "oncology", "status": "Completed"},
        {"time": "Yesterday", "node": "Hospital B", "domains": "general", "status": "Completed"},
        {"time": "Yesterday", "node": "Hospital A", "domains": "cardiology, oncology", "status": "Completed"}
    ]
    
    for sync in sync_history:
        st.markdown(f"""
        <div class="node-card">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <strong>{sync["node"]}</strong>
                <span style="color: #666; font-size: 0.9em;">{sync["time"]}</span>
            </div>
            <div style="font-size: 0.9em;">Domains: {sync["domains"]}</div>
            <div style="font-size: 0.8em; color: #4CAF50; margin-top: 5px;">{sync["status"]}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display confidentiality settings
    st.markdown("#### Confidentiality Settings")
    
    # Sample confidentiality settings
    settings = {
        "Hospital A": {
            "cardiology": "Full model access",
            "oncology": "Full model access",
            "general": "Full model access"
        },
        "Hospital B": {
            "cardiology": "Inference blocked",
            "oncology": "Full model access",
            "general": "Full model access"
        }
    }
    
    # Show current location settings
    st.markdown(f"""
    <div class="card">
        <h4 style="margin-top: 0;">{location} Settings</h4>
        <table style="width: 100%;">
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 8px 0;"><strong>cardiology</strong></td>
                <td style="text-align: right; color: {'#F44336' if settings[location]['cardiology'] == 'Inference blocked' else '#4CAF50'};">
                    {settings[location]['cardiology']}
                </td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 8px 0;"><strong>oncology</strong></td>
                <td style="text-align: right; color: {'#F44336' if settings[location]['oncology'] == 'Inference blocked' else '#4CAF50'};">
                    {settings[location]['oncology']}
                </td>
            </tr>
            <tr>
                <td style="padding: 8px 0;"><strong>general</strong></td>
                <td style="text-align: right; color: {'#F44336' if settings[location]['general'] == 'Inference blocked' else '#4CAF50'};">
                    {settings[location]['general']}
                </td>
            </tr>
        </table>
    </div>
    """, unsafe_allow_html=True)
    
    # Additional metrics/stats
    st.markdown("#### Federated Metrics")
    
    # Create two columns for the metrics
    metric_cols = st.columns(2)
    
    with metric_cols[0]:
        st.metric(
            label="Total Inferences",
            value="1,247",
            delta="+23 today"
        )
        
        st.metric(
            label="Privacy Budget (ε)",
            value="2.1/3.0",
            delta="69% used",
            delta_color="off"
        )
    
    with metric_cols[1]:
        st.metric(
            label="Syncs Today",
            value="8",
            delta="+3 vs. avg."
        )
        
        st.metric(
            label="Model Drift",
            value="1.2%",
            delta="-0.3%",
            delta_color="inverse"
        )