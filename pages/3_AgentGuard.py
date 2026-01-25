import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from utils.data_utils import get_sample_risk_data, get_risk_threshold_data
from utils.visualization import create_gauge_chart

# Page configuration
st.set_page_config(
    page_title="AgentGuard - Risk-Based Output Control",
    page_icon="🛡️",
    layout="wide"
)

# Sidebar
st.sidebar.title("AgentGuard")
st.sidebar.info("""
AgentGuard dynamically controls AI output modes based on risk scores.
Configure thresholds, review risk assessments, and manage output modes.
""")

# Main content
st.title("AgentGuard: Output Mode Control Based on Risk Scores")

tab1, tab2, tab3 = st.tabs(["Risk Dashboard", "Control Settings", "Agent Logs"])

with tab1:
    st.header("Risk Score Dashboard")
    
    # Top section with system status and filters
    status_col1, status_col2, status_col3 = st.columns([1, 2, 1])
    
    with status_col1:
        st.markdown("<h3 style='text-align: center; color: #0A2647;'>System Status</h3>", unsafe_allow_html=True)
        
        # System status indicator
        status_value = "ACTIVE"
        status_color = "#2E7D32"  # Green
        
        st.markdown(
            f"""
            <div style="background-color: {status_color}; padding: 10px; border-radius: 5px; text-align: center;">
                <h2 style="color: white; margin: 0;">{status_value}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Time of last update
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    with status_col2:
        st.markdown("<h3 style='text-align: center; color: #0A2647;'>Quick Filters</h3>", unsafe_allow_html=True)
        
        quick_col1, quick_col2 = st.columns(2)
        with quick_col1:
            model_filter = st.selectbox(
                "Model",
                options=["All Models", "GPT-4", "Llama-2", "Claude-2", "Falcon-180B"],
                index=0
            )
        
        with quick_col2:
            time_filter = st.selectbox(
                "Time Range",
                options=["Last Hour", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
                index=1
            )
    
    with status_col3:
        # System controls
        st.markdown("<h3 style='text-align: center; color: #0A2647;'>Actions</h3>", unsafe_allow_html=True)
        
        emergency_button = st.button("🚨 Emergency Lockdown", use_container_width=True)
        refresh_button = st.button("🔄 Refresh Data", use_container_width=True)
    
    # Horizontal divider
    st.markdown("<hr style='margin: 1rem 0; border-color: #EBEEF2;'>", unsafe_allow_html=True)
    
    # System-wide Risk Score Gauge
    gauge_col1, gauge_col2 = st.columns([2, 1])
    
    with gauge_col1:
        st.subheader("System-wide Risk Score")
        
        # Calculate current risk based on time and model filter (simulated)
        current_risk = 72  # Example value
        
        # Create gauge chart for risk level using utility function
        fig = create_gauge_chart(
            value=current_risk,
            title="Current System Risk Level",
            min_val=0,
            max_val=100,
            threshold=90
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with gauge_col2:
        st.subheader("Risk Interpretation")
        
        # Determine risk level
        if current_risk < 40:
            risk_level = "Low"
            risk_color = "green"
            risk_action = "Normal Operation"
        elif current_risk < 70:
            risk_level = "Medium"
            risk_color = "orange"
            risk_action = "Increased Monitoring"
        elif current_risk < 90:
            risk_level = "High"
            risk_color = "red"
            risk_action = "Enhanced Verification"
        else:
            risk_level = "Critical"
            risk_color = "darkred"
            risk_action = "Emergency Protocols"
        
        # Display risk level with colored indicator
        st.markdown(
            f"""
            <div style="padding: 15px; border-radius: 5px; margin-bottom: 20px; background-color: {risk_color}25; border-left: 5px solid {risk_color};">
                <h2 style="color: {risk_color}; margin: 0;">{risk_level.upper()} RISK</h2>
                <p style="margin: 5px 0 0 0;">Current Action: {risk_action}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Risk factors
        st.markdown("**Contributing Risk Factors:**")
        
        # Dynamic risk factors based on current score
        risk_factors = [
            "Multiple high-risk outputs detected" if current_risk > 60 else "Normal output patterns",
            "Unusual user behavior patterns" if current_risk > 50 else "Standard user behavior",
            "Elevated prompt complexity" if current_risk > 40 else "Normal prompt complexity"
        ]
        
        for factor in risk_factors:
            st.markdown(f"- {factor}")
    
    # Component metrics with enhanced visualization
    st.subheader("Risk Component Breakdown")
    
    # Risk components with descriptions and thresholds
    risk_components = [
        {
            "name": "Content Risk",
            "score": 65,
            "description": "Measures potential harm in AI outputs",
            "change": -12,
            "threshold": 75
        },
        {
            "name": "Model Vulnerability",
            "score": 45,
            "description": "Susceptibility to prompt injection/jailbreak",
            "change": 8,
            "threshold": 60
        },
        {
            "name": "User Trust Score",
            "score": 80,
            "description": "Reliability score of current user",
            "change": -5,
            "threshold": 40
        },
        {
            "name": "Request Complexity",
            "score": 70,
            "description": "Complexity of current request",
            "change": 15,
            "threshold": 85
        }
    ]
    
    # Display metrics and progress bars
    comp_col1, comp_col2 = st.columns(2)
    
    for i, component in enumerate(risk_components):
        # Alternate between columns
        with comp_col1 if i % 2 == 0 else comp_col2:
            # Metric with delta
            st.metric(
                label=component["name"],
                value=f"{component['score']}/100",
                delta=f"{component['change']}%" if component['change'] != 0 else None,
                delta_color="inverse"  # Lower is better for risk scores
            )
            
            # Description
            st.caption(component["description"])
            
            # Progress bar with color based on score
            if component["score"] < 40:
                bar_color = "green"
            elif component["score"] < 70:
                bar_color = "orange"
            else:
                bar_color = "red"
            
            # Create progress bar with custom color
            st.markdown(
                f"""
                <div style="margin-bottom: 20px;">
                    <div style="width: 100%; background-color: #f0f0f0; border-radius: 3px; height: 8px;">
                        <div style="width: {component['score']}%; background-color: {bar_color}; height: 8px; border-radius: 3px;"></div>
                    </div>
                    <div style="display: flex; justify-content: space-between; font-size: 12px; color: #666;">
                        <span>Low</span>
                        <span>Medium</span>
                        <span>High</span>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # Risk trend over time
    st.subheader("Risk Score Trend")
    
    # Get sample risk data
    risk_df = get_sample_risk_data()
    
    # Plot trend
    fig = px.line(
        risk_df,
        x="timestamp",
        y="risk_score",
        color="model",
        line_shape="spline",
        title="Risk Score Trend by Model"
    )
    
    # Add threshold line
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="High Risk Threshold")
    fig.add_hline(y=40, line_dash="dash", line_color="orange", annotation_text="Medium Risk Threshold")
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    st.header("Output Control Settings")
    
    # Top status display
    config_status_cols = st.columns([3, 1])
    with config_status_cols[0]:
        st.markdown(
            """
            <div style="border-left: 4px solid #0A2647; padding-left: 10px; margin-bottom: 20px;">
                <p style="margin: 0; color: #555;">Current Configuration Mode: <strong>Custom</strong></p>
                <p style="margin: 0; font-size: 12px; color: #777;">Last modified: 2023-05-01 14:32:18</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with config_status_cols[1]:
        template_selector = st.selectbox(
            "Load Template",
            options=["Custom Configuration", "Default Safe Mode", "High Security", "Balanced", "Development Mode"]
        )
        
        if template_selector != "Custom Configuration":
            st.button("Apply Template", use_container_width=True)
    
    # Risk threshold settings with visualization
    st.subheader("Risk Thresholds Configuration")
    
    threshold_data = get_risk_threshold_data()
    
    # Add tabs for different configuration aspects
    config_tabs = st.tabs(["Threshold Settings", "Response Actions", "Advanced Settings"])
    
    with config_tabs[0]:  # Threshold Settings Tab
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Model selector with better styling
            st.markdown("### Select Model to Configure")
            selected_model = st.selectbox(
                "Select AI Model",
                options=threshold_data["model"].unique(),
                help="Configure risk thresholds for specific AI models"
            )
            
            # Filter for selected model
            model_thresholds = threshold_data[threshold_data["model"] == selected_model].reset_index(drop=True)
            
            # Display current thresholds with visual elements
            st.markdown("### Current Threshold Configuration")
            
            # Visual representation of thresholds
            thresholds = {
                "Low": [0, 40],
                "Medium": [40, 70],
                "High": [70, 90],
                "Critical": [90, 100]
            }
            
            # Draw threshold visualization
            col_heights = {
                "Low": 40,
                "Medium": 30,
                "High": 20,
                "Critical": 10
            }
            
            st.markdown(
                """
                <style>
                .threshold-container {
                    display: flex;
                    width: 100%;
                    height: 50px;
                    margin: 15px 0;
                    border-radius: 4px;
                    overflow: hidden;
                }
                .threshold-segment {
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    color: white;
                    font-weight: bold;
                    position: relative;
                }
                .segment-label {
                    position: absolute;
                    bottom: -25px;
                    font-size: 12px;
                    color: #333;
                }
                </style>
                
                <div class="threshold-container">
                    <div class="threshold-segment" style="background-color: #4CAF50; width: 40%;">
                        Low Risk
                        <div class="segment-label">0-40</div>
                    </div>
                    <div class="threshold-segment" style="background-color: #FFC107; width: 30%;">
                        Medium Risk
                        <div class="segment-label">40-70</div>
                    </div>
                    <div class="threshold-segment" style="background-color: #FF5722; width: 20%;">
                        High Risk
                        <div class="segment-label">70-90</div>
                    </div>
                    <div class="threshold-segment" style="background-color: #D32F2F; width: 10%;">
                        Critical
                        <div class="segment-label">90-100</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Threshold adjustment with more descriptive labels
            st.markdown("### Adjust Risk Thresholds")
            st.markdown("Drag the sliders to adjust thresholds between risk levels.")
            
            # Compact sliders with better descriptions
            medium_threshold = st.slider(
                "Medium Risk Threshold",
                min_value=20,
                max_value=60,
                value=40,
                help="Outputs with risk scores above this will be classified as medium risk"
            )
            
            high_threshold = st.slider(
                "High Risk Threshold",
                min_value=medium_threshold + 10,
                max_value=90,
                value=70,
                help="Outputs with risk scores above this will be classified as high risk"
            )
            
            critical_threshold = st.slider(
                "Critical Risk Threshold",
                min_value=high_threshold + 5,
                max_value=100,
                value=90,
                help="Outputs with risk scores above this will be classified as critical risk"
            )
            
            # Dynamically generated threshold ranges after adjustments
            st.markdown("### Updated Risk Level Ranges")
            st.markdown(f"- **Low Risk:** 0-{medium_threshold}")
            st.markdown(f"- **Medium Risk:** {medium_threshold}-{high_threshold}")
            st.markdown(f"- **High Risk:** {high_threshold}-{critical_threshold}")
            st.markdown(f"- **Critical Risk:** {critical_threshold}-100")
        
        with col2:
            # Show the resulting risk distribution
            st.markdown("### Risk Distribution Preview")
            
            # Create sample data to show distribution impact
            risk_scores = np.random.normal(50, 20, 1000)
            risk_scores = np.clip(risk_scores, 0, 100)
            
            # Create histogram for risk distribution
            risk_hist = px.histogram(
                risk_scores, 
                nbins=20,
                labels={"value": "Risk Score", "count": "Frequency"},
                title="Sample Risk Distribution",
                opacity=0.7
            )
            
            # Add threshold lines
            risk_hist.add_vline(x=medium_threshold, line_dash="dash", line_color="#FFC107")
            risk_hist.add_vline(x=high_threshold, line_dash="dash", line_color="#FF5722")
            risk_hist.add_vline(x=critical_threshold, line_dash="dash", line_color="#D32F2F")
            
            # Add threshold annotations
            risk_hist.add_annotation(x=medium_threshold/2, y=0, text="Low", showarrow=False, yshift=10)
            risk_hist.add_annotation(x=(medium_threshold + high_threshold)/2, y=0, text="Medium", showarrow=False, yshift=10)
            risk_hist.add_annotation(x=(high_threshold + critical_threshold)/2, y=0, text="High", showarrow=False, yshift=10)
            risk_hist.add_annotation(x=(critical_threshold + 100)/2, y=0, text="Critical", showarrow=False, yshift=10)
            
            risk_hist.update_layout(height=300)
            st.plotly_chart(risk_hist, use_container_width=True)
            
            # Impact stats based on thresholds
            low_pct = (risk_scores < medium_threshold).mean() * 100
            medium_pct = ((risk_scores >= medium_threshold) & (risk_scores < high_threshold)).mean() * 100
            high_pct = ((risk_scores >= high_threshold) & (risk_scores < critical_threshold)).mean() * 100
            critical_pct = (risk_scores >= critical_threshold).mean() * 100
            
            st.markdown("### Impact on Outputs")
            st.markdown(f"- **Low Risk:** {low_pct:.1f}% of outputs")
            st.markdown(f"- **Medium Risk:** {medium_pct:.1f}% of outputs")
            st.markdown(f"- **High Risk:** {high_pct:.1f}% of outputs")
            st.markdown(f"- **Critical Risk:** {critical_pct:.1f}% of outputs")
    
    with config_tabs[1]:  # Response Actions Tab
        st.markdown("### Configure Response Actions")
        st.markdown("Define what actions should be taken for each risk level.")
        
        response_col1, response_col2 = st.columns(2)
        
        with response_col1:
            # Low risk response
            st.markdown(
                """
                <div style="padding: 10px; border-left: 4px solid #4CAF50; margin-bottom: 20px;">
                    <h4 style="margin: 0; color: #4CAF50;">Low Risk Actions</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            low_action = st.selectbox(
                "Primary Action for Low Risk",
                options=["Allow All Output", "Log Only", "Sample Review"],
                index=0
            )
            
            low_notification = st.checkbox("Send notifications for low risk events", value=False)
            low_logging = st.checkbox("Enable detailed logging for low risk events", value=True)
        
        with response_col2:
            # Medium risk response
            st.markdown(
                """
                <div style="padding: 10px; border-left: 4px solid #FFC107; margin-bottom: 20px;">
                    <h4 style="margin: 0; color: #FFC107;">Medium Risk Actions</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            medium_action = st.selectbox(
                "Primary Action for Medium Risk",
                options=["Allow with Warning", "Require User Confirmation", "Add Disclaimers", "Log & Review"],
                index=0
            )
            
            medium_notification = st.checkbox("Send notifications for medium risk events", value=True)
            medium_logging = st.checkbox("Enable detailed logging for medium risk events", value=True)
        
        response_col3, response_col4 = st.columns(2)
        
        with response_col3:
            # High risk response
            st.markdown(
                """
                <div style="padding: 10px; border-left: 4px solid #FF5722; margin-bottom: 20px;">
                    <h4 style="margin: 0; color: #FF5722;">High Risk Actions</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            high_action = st.selectbox(
                "Primary Action for High Risk",
                options=["Require Human Review", "Limit Output Scope", "Apply Strong Filters", "Allow Only Safe Content"],
                index=0
            )
            
            high_notification = st.checkbox("Send notifications for high risk events", value=True)
            high_alert = st.checkbox("Trigger security alert for high risk events", value=False)
        
        with response_col4:
            # Critical risk response
            st.markdown(
                """
                <div style="padding: 10px; border-left: 4px solid #D32F2F; margin-bottom: 20px;">
                    <h4 style="margin: 0; color: #D32F2F;">Critical Risk Actions</h4>
                </div>
                """, 
                unsafe_allow_html=True
            )
            
            critical_action = st.selectbox(
                "Primary Action for Critical Risk", 
                options=["Block Output", "System Shutdown", "Report to Admin", "Switch to Safe Mode"],
                index=0
            )
            
            critical_notification = st.checkbox("Send notifications for critical risk events", value=True)
            critical_alert = st.checkbox("Trigger security alert for critical risk events", value=True)
    
    with config_tabs[2]:  # Advanced Settings Tab
        st.markdown("### Advanced Guard Configuration")
        
        adv_col1, adv_col2 = st.columns(2)
        
        with adv_col1:
            st.markdown("#### Risk Assessment Factors")
            st.markdown("Configure the weight of different risk factors in the overall assessment.")
            
            st.slider("Content Risk Weight", 0, 100, 30, help="Weight of content-based risk assessment")
            st.slider("User Trust Weight", 0, 100, 20, help="Weight of user trust factors in risk assessment")
            st.slider("Context Risk Weight", 0, 100, 25, help="Weight of contextual risk factors")
            st.slider("Model Vulnerability Weight", 0, 100, 25, help="Weight of model-specific vulnerabilities")
        
        with adv_col2:
            st.markdown("#### Automation Settings")
            
            auto_adjust = st.checkbox("Enable automatic threshold adjustments", value=False)
            if auto_adjust:
                st.selectbox(
                    "Adjustment Frequency",
                    options=["Hourly", "Daily", "Weekly", "Monthly"]
                )
                st.slider("Maximum Adjustment (%)", 0, 50, 10)
            
            # Additional advanced settings
            st.markdown("#### Notification Rules")
            notify_roles = st.multiselect(
                "Notify Roles",
                options=["Admin", "Security Team", "Model Managers", "All Users"],
                default=["Admin", "Security Team"]
            )
    
    # Save button with enhanced styling
    st.markdown("### Save Configuration")
    save_cols = st.columns([1, 1, 2])
    
    with save_cols[0]:
        if st.button("Save Configuration", type="primary", use_container_width=True):
            st.success("✅ Configuration saved successfully!")
    
    with save_cols[1]:
        export_config = st.button("Export as JSON", use_container_width=True)
        if export_config:
            st.info("Configuration exported successfully!")
    
    with save_cols[2]:
        st.markdown(
            """
            <div style="border: 1px solid #e0e0e0; border-radius: 5px; padding: 10px; margin-top: 8px;">
                <span style="font-size: 14px; color: #555;">Changes will be applied to <strong>all sessions</strong> immediately after saving.</span>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    # Output mode control
    st.subheader("Output Mode Control")
    
    override_col1, override_col2 = st.columns(2)
    
    with override_col1:
        st.write("Manual Override")
        
        override_model = st.selectbox(
            "Select Model for Override",
            options=threshold_data["model"].unique()
        )
        
        override_mode = st.radio(
            "Select Forced Mode",
            options=["Normal Operation", "Safe Mode", "Strict Mode", "Development Mode", "Emergency Lockdown"]
        )
        
        st.button("Apply Override")
    
    with override_col2:
        st.write("Scheduled Mode Changes")
        
        scheduled_model = st.selectbox(
            "Select Model",
            options=threshold_data["model"].unique(),
            key="scheduled_model"
        )
        
        scheduled_mode = st.selectbox(
            "Select Mode",
            options=["Safe Mode", "Strict Mode", "Normal Operation", "Development Mode"]
        )
        
        start_time = st.time_input("Start Time")
        end_time = st.time_input("End Time", value=(datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time())
        
        schedule_date = st.date_input("Schedule Date")
        
        create_schedule = st.button("Create Schedule")
        if create_schedule:
            st.success(f"✅ Schedule created for {scheduled_model} to enter {scheduled_mode} from {start_time} to {end_time} on {schedule_date}")

with tab3:
    st.header("Agent Activity Logs")

    # Tabs for different log views
    log_tabs = st.tabs(["Log Viewer", "Statistics", "Alerts History"])
    
    with log_tabs[0]:  # Log Viewer tab
        # Advanced filters section
        with st.expander("Advanced Filtering Options", expanded=True):
            filter_cols = st.columns([1, 1, 1, 1])
            
            with filter_cols[0]:
                log_model_filter = st.multiselect(
                    "Filter by Model",
                    options=["GPT-4", "Llama-2", "Claude-2", "Falcon-180B"],
                    default=["GPT-4", "Llama-2", "Claude-2", "Falcon-180B"]
                )
            
            with filter_cols[1]:
                log_risk_filter = st.multiselect(
                    "Filter by Risk Level",
                    options=["Low", "Medium", "High", "Critical"],
                    default=["Low", "Medium", "High", "Critical"]
                )
            
            with filter_cols[2]:
                log_action_filter = st.multiselect(
                    "Filter by Action Taken",
                    options=["Allowed", "Modified", "Blocked", "Reviewed"],
                    default=["Allowed", "Modified", "Blocked", "Reviewed"]
                )
            
            with filter_cols[3]:
                log_date_filter = st.date_input(
                    "Date Range",
                    value=[datetime.now() - timedelta(days=7), datetime.now()],
                    max_value=datetime.now()
                )
            
            # Additional filters in a second row
            filter_cols2 = st.columns([2, 2, 1])
            
            with filter_cols2[0]:
                log_user_filter = st.multiselect(
                    "Filter by User",
                    options=["user_1", "user_2", "user_3", "user_4", "user_5"],
                    default=[]
                )
            
            with filter_cols2[1]:
                log_request_filter = st.multiselect(
                    "Filter by Request Type",
                    options=["Text Generation", "Code Generation", "Translation", "Summarization"],
                    default=[]
                )
            
            with filter_cols2[2]:
                min_risk, max_risk = st.slider(
                    "Risk Score Range", 
                    min_value=0, 
                    max_value=100, 
                    value=(0, 100)
                )
        
        # Search functionality for logs
        log_search = st.text_input("Search in logs...", placeholder="Enter search terms")
        
        # Create sample agent logs data with more fields
        agent_logs = pd.DataFrame({
            "timestamp": pd.date_range(start="2023-01-01", periods=100, freq="H")[::-1],
            "model": np.random.choice(["GPT-4", "Llama-2", "Claude-2", "Falcon-180B"], 100),
            "user_id": np.random.choice(["user_1", "user_2", "user_3", "user_4", "user_5"], 100),
            "risk_score": np.random.randint(10, 100, 100),
            "action_taken": np.random.choice(["Allowed", "Modified", "Blocked", "Reviewed"], 100),
            "request_type": np.random.choice(["Text Generation", "Code Generation", "Translation", "Summarization"], 100),
            "input_tokens": np.random.randint(10, 500, 100),
            "output_tokens": np.random.randint(50, 2000, 100),
            "processing_time": np.random.uniform(0.1, 5.0, 100).round(2),
            "log_id": [f"LOG-{i:05d}" for i in range(100)],
            "session_id": [f"SES-{i//5:04d}" for i in range(100)],
        })
        
        # Add risk level based on risk score
        def get_risk_level(score):
            if score < 40:
                return "Low"
            elif score < 70:
                return "Medium"
            elif score < 90:
                return "High"
            else:
                return "Critical"
        
        agent_logs["risk_level"] = agent_logs["risk_score"].apply(get_risk_level)
        
        # Add request snippet for display
        request_snippets = [
            "Generate a summary of the quarterly report...",
            "Translate the following text to Spanish...",
            "Write a function that calculates the factorial...",
            "Explain the concept of quantum computing...",
            "Create a list of 10 marketing strategies..."
        ]
        agent_logs["request_snippet"] = [np.random.choice(request_snippets) for _ in range(100)]
        
        # Apply filters
        filtered_logs = agent_logs.copy()
        
        # Apply model filter
        if log_model_filter:
            filtered_logs = filtered_logs[filtered_logs["model"].isin(log_model_filter)]
        
        # Apply risk level filter
        if log_risk_filter:
            filtered_logs = filtered_logs[filtered_logs["risk_level"].isin(log_risk_filter)]
        
        # Apply action filter
        if log_action_filter:
            filtered_logs = filtered_logs[filtered_logs["action_taken"].isin(log_action_filter)]
        
        # Apply user filter if any selected
        if log_user_filter:
            filtered_logs = filtered_logs[filtered_logs["user_id"].isin(log_user_filter)]
        
        # Apply request type filter if any selected
        if log_request_filter:
            filtered_logs = filtered_logs[filtered_logs["request_type"].isin(log_request_filter)]
        
        # Apply date filter
        if len(log_date_filter) == 2:
            start_date, end_date = log_date_filter
            filtered_logs = filtered_logs[
                (filtered_logs["timestamp"].dt.date >= start_date) &
                (filtered_logs["timestamp"].dt.date <= end_date)
            ]
        
        # Apply risk score range filter
        filtered_logs = filtered_logs[
            (filtered_logs["risk_score"] >= min_risk) &
            (filtered_logs["risk_score"] <= max_risk)
        ]
        
        # Apply search term if provided
        if log_search:
            # Convert all columns to string for searching
            search_mask = filtered_logs.astype(str).apply(
                lambda row: row.str.contains(log_search, case=False).any(), 
                axis=1
            )
            filtered_logs = filtered_logs[search_mask]
        
        # Show summary metrics for filtered logs
        metric_cols = st.columns(4)
        with metric_cols[0]:
            st.metric("Total Records", len(filtered_logs))
        with metric_cols[1]:
            if not filtered_logs.empty:
                avg_risk = filtered_logs["risk_score"].mean()
                st.metric("Avg. Risk Score", f"{avg_risk:.1f}")
            else:
                st.metric("Avg. Risk Score", "N/A")
        with metric_cols[2]:
            if not filtered_logs.empty:
                blocked_pct = (filtered_logs["action_taken"] == "Blocked").mean() * 100
                st.metric("Blocked Rate", f"{blocked_pct:.1f}%")
            else:
                st.metric("Blocked Rate", "N/A")
        with metric_cols[3]:
            if not filtered_logs.empty:
                critical_pct = (filtered_logs["risk_level"] == "Critical").mean() * 100
                st.metric("Critical Rate", f"{critical_pct:.1f}%")
            else:
                st.metric("Critical Rate", "N/A")
        
        # Styled dataframe for better visualization
        if not filtered_logs.empty:
            # Define style function to color risk levels
            def style_risk_level(val):
                color_map = {
                    "Low": "background-color: #d4edda; color: #155724",
                    "Medium": "background-color: #fff3cd; color: #856404",
                    "High": "background-color: #ffe4d1; color: #ff5722",
                    "Critical": "background-color: #f8d7da; color: #721c24"
                }
                return color_map.get(val, "")
            
            # Define style function to color actions
            def style_action(val):
                color_map = {
                    "Allowed": "color: green",
                    "Modified": "color: orange",
                    "Blocked": "color: red",
                    "Reviewed": "color: blue"
                }
                return color_map.get(val, "")
            
            # Apply styling
            styled_logs = filtered_logs.style.\
                applymap(style_risk_level, subset=["risk_level"]).\
                applymap(style_action, subset=["action_taken"])
            
            # Display the styled dataframe
            st.dataframe(
                styled_logs,
                height=400,
                use_container_width=True
            )
            
            # Log detail view for selected entry
            st.subheader("Log Entry Details")
            
            # Log entry selection
            selected_log_id = st.selectbox(
                "Select Log ID for Details",
                options=filtered_logs["log_id"].tolist(),
                format_func=lambda x: f"{x} - {filtered_logs[filtered_logs['log_id'] == x]['timestamp'].values[0]}"
            )
            
            # Display details of the selected log
            if selected_log_id:
                log_entry = filtered_logs[filtered_logs["log_id"] == selected_log_id].iloc[0]
                
                # Create two columns for details
                detail_col1, detail_col2 = st.columns(2)
                
                with detail_col1:
                    st.markdown("#### Session Information")
                    st.markdown(f"**Log ID:** {log_entry['log_id']}")
                    st.markdown(f"**Session ID:** {log_entry['session_id']}")
                    st.markdown(f"**Timestamp:** {log_entry['timestamp']}")
                    st.markdown(f"**Model:** {log_entry['model']}")
                    st.markdown(f"**User ID:** {log_entry['user_id']}")
                    st.markdown(f"**Request Type:** {log_entry['request_type']}")
                
                with detail_col2:
                    st.markdown("#### Risk Assessment")
                    
                    # Risk level with color indicator
                    risk_color_map = {
                        "Low": "#4CAF50",
                        "Medium": "#FFC107",
                        "High": "#FF5722",
                        "Critical": "#D32F2F"
                    }
                    risk_color = risk_color_map.get(log_entry["risk_level"], "#777777")
                    
                    st.markdown(
                        f"""
                        <div style="display: flex; align-items: center; margin-bottom: 10px;">
                            <div style="width: 12px; height: 12px; border-radius: 50%; background-color: {risk_color}; margin-right: 8px;"></div>
                            <div><strong>Risk Level:</strong> {log_entry['risk_level']} ({log_entry['risk_score']})</div>
                        </div>
                        """, 
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(f"**Action Taken:** {log_entry['action_taken']}")
                    st.markdown(f"**Input Tokens:** {log_entry['input_tokens']}")
                    st.markdown(f"**Output Tokens:** {log_entry['output_tokens']}")
                    st.markdown(f"**Processing Time:** {log_entry['processing_time']}s")
                
                # Request and response details
                st.markdown("#### Request Content")
                st.text_area("Input Prompt", value=log_entry["request_snippet"], height=100, disabled=True)
                
                # Response simulation based on action taken
                response_content = ""
                if log_entry["action_taken"] == "Blocked":
                    response_content = "[Content blocked due to high risk assessment]"
                elif log_entry["action_taken"] == "Modified":
                    response_content = "[Modified content with potentially harmful elements removed]"
                else:
                    response_content = "This is a simulated response for the AI model based on the input prompt..."
                
                st.markdown("#### Response Content")
                st.text_area("Model Output", value=response_content, height=150, disabled=True)
        else:
            st.warning("No logs match the current filter criteria.")
        
        # Export options
        export_col1, export_col2 = st.columns(2)
        with export_col1:
            st.download_button(
                label="Export Filtered Logs (CSV)",
                data=filtered_logs.to_csv(index=False).encode('utf-8'),
                file_name=f"agentguard_logs_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with export_col2:
            st.download_button(
                label="Export as JSON",
                data=filtered_logs.to_json(orient="records").encode('utf-8'),
                file_name=f"agentguard_logs_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json",
                use_container_width=True
            )
    
    with log_tabs[1]:  # Statistics tab
        st.subheader("Log Statistics & Trends")
        
        # Time period selector for statistics
        stat_period = st.selectbox(
            "Statistics Time Period",
            options=["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"],
            index=1
        )
        
        # Display metrics over time
        st.markdown("### Risk Score Distribution Over Time")
        
        # Filter data based on selected time period
        if stat_period == "Last 24 Hours":
            stat_data = agent_logs[agent_logs["timestamp"] >= datetime.now() - timedelta(days=1)]
            time_group = "H"  # Group by hour
        elif stat_period == "Last 7 Days":
            stat_data = agent_logs[agent_logs["timestamp"] >= datetime.now() - timedelta(days=7)]
            time_group = "D"  # Group by day
        elif stat_period == "Last 30 Days":
            stat_data = agent_logs[agent_logs["timestamp"] >= datetime.now() - timedelta(days=30)]
            time_group = "D"  # Group by day
        else:
            stat_data = agent_logs.copy()
            time_group = "W"  # Group by week
        
        # Create time-based visualizations
        if not stat_data.empty:
            # Risk level distribution over time
            risk_over_time = stat_data.groupby([pd.Grouper(key="timestamp", freq=time_group), "risk_level"]).size().reset_index(name="count")
            
            # Stacked area chart of risk levels
            risk_time_fig = px.area(
                risk_over_time,
                x="timestamp",
                y="count",
                color="risk_level",
                title="Risk Level Distribution Over Time",
                color_discrete_map={
                    "Low": "#4CAF50",
                    "Medium": "#FFC107",
                    "High": "#FF5722",
                    "Critical": "#D32F2F"
                }
            )
            st.plotly_chart(risk_time_fig, use_container_width=True)
            
            # Actions taken over time
            st.markdown("### Actions Taken Over Time")
            actions_over_time = stat_data.groupby([pd.Grouper(key="timestamp", freq=time_group), "action_taken"]).size().reset_index(name="count")
            
            action_time_fig = px.line(
                actions_over_time,
                x="timestamp",
                y="count",
                color="action_taken",
                title="Actions Taken Over Time",
                markers=True
            )
            st.plotly_chart(action_time_fig, use_container_width=True)
            
            # Risk distribution by model
            st.markdown("### Risk Distribution by Model")
            
            stats_cols = st.columns(2)
            
            with stats_cols[0]:
                model_risk = stat_data.groupby("model")["risk_score"].mean().reset_index()
                model_risk.columns = ["model", "avg_risk_score"]
                
                model_bar = px.bar(
                    model_risk,
                    x="model",
                    y="avg_risk_score",
                    title="Average Risk Score by Model",
                    color="avg_risk_score",
                    color_continuous_scale="RdYlGn_r"
                )
                st.plotly_chart(model_bar, use_container_width=True)
            
            with stats_cols[1]:
                # Request type distribution
                request_dist = stat_data.groupby("request_type").size().reset_index(name="count")
                
                request_pie = px.pie(
                    request_dist,
                    values="count",
                    names="request_type",
                    title="Request Type Distribution",
                    hole=0.4
                )
                st.plotly_chart(request_pie, use_container_width=True)
        else:
            st.warning("No data available for the selected time period.")
    
    with log_tabs[2]:  # Alerts History tab
        st.subheader("Historical Alerts")
        
        # Alert filter options
        alert_cols = st.columns([2, 1, 1])
        with alert_cols[0]:
            alert_severity = st.multiselect(
                "Filter by Severity",
                options=["Critical", "High", "Medium", "Low"],
                default=["Critical", "High"]
            )
        
        with alert_cols[1]:
            alert_status = st.multiselect(
                "Filter by Status",
                options=["Active", "Resolved", "In Progress", "Ignored"],
                default=["Active", "In Progress"]
            )
        
        with alert_cols[2]:
            alert_date_range = st.date_input(
                "Date Range",
                value=[datetime.now() - timedelta(days=30), datetime.now()],
                max_value=datetime.now()
            )
        
        # Create sample alert data
        alerts_data = []
        
        # Generate 20 sample alerts
        for i in range(20):
            # Determine severity with higher chance of critical/high for recent dates
            if i < 5:
                severity = np.random.choice(["Critical", "High"], 1)[0]
                status = np.random.choice(["Active", "In Progress"], 1)[0]
                days_ago = np.random.randint(0, 7)
            else:
                severity = np.random.choice(["Critical", "High", "Medium", "Low"], 1, 
                                        p=[0.1, 0.3, 0.4, 0.2])[0]
                status = np.random.choice(["Active", "Resolved", "In Progress", "Ignored"], 1)[0]
                days_ago = np.random.randint(0, 30)
            
            alert_time = datetime.now() - timedelta(days=days_ago, 
                                                  hours=np.random.randint(0, 24),
                                                  minutes=np.random.randint(0, 60))
            
            # Alert triggers based on severity
            if severity == "Critical":
                trigger = np.random.choice([
                    "Multiple blocked outputs in succession",
                    "Extreme risk score detected",
                    "Emergency lockdown triggered",
                    "Security policy violation"
                ])
            elif severity == "High":
                trigger = np.random.choice([
                    "High risk content detected",
                    "Unusual user behavior pattern",
                    "Risk threshold exceeded",
                    "Multiple warnings in short period"
                ])
            elif severity == "Medium":
                trigger = np.random.choice([
                    "Risk score approaching threshold",
                    "Unusual request pattern",
                    "Content warning triggered",
                    "Model performance issue"
                ])
            else:
                trigger = np.random.choice([
                    "Risk assessment notification",
                    "Periodic review required",
                    "Minor content warning",
                    "System information"
                ])
            
            alerts_data.append({
                "alert_id": f"ALT-{i+1:03d}",
                "timestamp": alert_time,
                "severity": severity,
                "status": status,
                "trigger": trigger,
                "model": np.random.choice(["GPT-4", "Llama-2", "Claude-2", "Falcon-180B"]),
                "related_logs": np.random.randint(1, 10),
                "assigned_to": "" if status in ["Active", "Ignored"] else np.random.choice(["admin", "moderator", "security"])
            })
        
        # Convert to dataframe
        alerts_df = pd.DataFrame(alerts_data)
        
        # Filter alerts
        filtered_alerts = alerts_df.copy()
        
        # Apply severity filter
        if alert_severity:
            filtered_alerts = filtered_alerts[filtered_alerts["severity"].isin(alert_severity)]
        
        # Apply status filter
        if alert_status:
            filtered_alerts = filtered_alerts[filtered_alerts["status"].isin(alert_status)]
        
        # Apply date filter
        if len(alert_date_range) == 2:
            start_date, end_date = alert_date_range
            filtered_alerts = filtered_alerts[
                (filtered_alerts["timestamp"].dt.date >= start_date) &
                (filtered_alerts["timestamp"].dt.date <= end_date)
            ]
        
        # Sort by timestamp descending
        filtered_alerts = filtered_alerts.sort_values("timestamp", ascending=False)
        
        # Display alerts
        if not filtered_alerts.empty:
            # Summary metrics for alerts
            alert_metrics = st.columns(4)
            with alert_metrics[0]:
                active_count = (filtered_alerts["status"] == "Active").sum()
                st.metric("Active Alerts", active_count)
            
            with alert_metrics[1]:
                critical_count = (filtered_alerts["severity"] == "Critical").sum()
                st.metric("Critical Alerts", critical_count)
            
            with alert_metrics[2]:
                resolved_count = (filtered_alerts["status"] == "Resolved").sum()
                st.metric("Resolved", resolved_count)
            
            with alert_metrics[3]:
                newest_alert = filtered_alerts["timestamp"].max()
                time_since = datetime.now() - newest_alert
                if time_since.days > 0:
                    time_str = f"{time_since.days}d ago"
                elif time_since.seconds // 3600 > 0:
                    time_str = f"{time_since.seconds // 3600}h ago"
                else:
                    time_str = f"{time_since.seconds // 60}m ago"
                st.metric("Latest Alert", time_str)
            
            # Create expandable cards for each alert
            for i, alert in filtered_alerts.iterrows():
                # Determine card color based on severity
                if alert["severity"] == "Critical":
                    card_color = "#D32F2F"
                elif alert["severity"] == "High":
                    card_color = "#FF5722"
                elif alert["severity"] == "Medium":
                    card_color = "#FFC107"
                else:
                    card_color = "#4CAF50"
                
                # Determine status badge color
                if alert["status"] == "Active":
                    status_color = "#D32F2F"
                elif alert["status"] == "In Progress":
                    status_color = "#2196F3"
                elif alert["status"] == "Resolved":
                    status_color = "#4CAF50"
                else:
                    status_color = "#9E9E9E"
                
                # Format timestamp
                time_str = alert["timestamp"].strftime("%Y-%m-%d %H:%M")
                
                # Create card
                with st.expander(f"{alert['alert_id']} - {alert['severity']} Alert - {alert['trigger']} - {time_str}"):
                    # Two columns for alert details
                    alert_detail_cols = st.columns([3, 2])
                    
                    with alert_detail_cols[0]:
                        st.markdown(
                            f"""
                            <div style="border-left: 4px solid {card_color}; padding-left: 10px;">
                                <h4 style="margin: 0;">{alert['trigger']}</h4>
                                <p style="color: #666; margin: 5px 0;">{alert['timestamp'].strftime("%Y-%m-%d %H:%M:%S")}</p>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                        
                        st.markdown(f"**Alert ID:** {alert['alert_id']}")
                        st.markdown(f"**Affected Model:** {alert['model']}")
                        st.markdown(f"**Related Logs:** {alert['related_logs']}")
                        
                        if alert["assigned_to"]:
                            st.markdown(f"**Assigned To:** {alert['assigned_to']}")
                        
                        # Action buttons
                        action_cols = st.columns(3)
                        with action_cols[0]:
                            if alert["status"] != "Resolved":
                                st.button(f"Resolve #{alert['alert_id']}", key=f"resolve_{i}")
                        
                        with action_cols[1]:
                            if alert["status"] == "Active":
                                st.button(f"Assign #{alert['alert_id']}", key=f"assign_{i}")
                        
                        with action_cols[2]:
                            st.button(f"View Logs #{alert['alert_id']}", key=f"logs_{i}")
                    
                    with alert_detail_cols[1]:
                        # Status badge
                        st.markdown(
                            f"""
                            <div style="background-color: {status_color}; color: white; padding: 4px 8px; border-radius: 4px; display: inline-block; margin-bottom: 10px;">
                                {alert['status']}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        
                        # Additional details
                        st.markdown("#### Alert Details")
                        
                        # Simulated alert details
                        if alert["severity"] in ["Critical", "High"]:
                            st.markdown("- Multiple high-risk outputs detected in sequence")
                            st.markdown("- Unusual pattern of API calls detected")
                            st.markdown(f"- Risk threshold exceeded by {np.random.randint(10, 50)}%")
                        
                        # Alert timeline
                        st.markdown("#### Alert Timeline")
                        timeline_data = {
                            "Time": [
                                (alert["timestamp"] - timedelta(minutes=np.random.randint(0, 5))).strftime("%H:%M:%S"),
                                alert["timestamp"].strftime("%H:%M:%S"),
                                (alert["timestamp"] + timedelta(minutes=np.random.randint(1, 10))).strftime("%H:%M:%S") if alert["status"] != "Active" else ""
                            ],
                            "Event": [
                                "High risk output detected",
                                f"{alert['severity']} alert triggered",
                                "Alert acknowledged" if alert["status"] != "Active" else ""
                            ]
                        }
                        # Filter out empty events
                        timeline_df = pd.DataFrame(timeline_data)
                        timeline_df = timeline_df[timeline_df["Event"] != ""]
                        
                        st.dataframe(timeline_df, hide_index=True)
        else:
            st.info("No alerts match the current filter criteria.")
