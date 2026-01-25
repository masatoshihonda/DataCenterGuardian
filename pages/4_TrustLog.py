import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta
import hashlib
import time
import base64
from utils.data_utils import get_sample_trustlog_data

# Page configuration
st.set_page_config(
    page_title="TrustLog - AI Output Logging",
    page_icon="📝",
    layout="wide"
)

# Sidebar
st.sidebar.title("TrustLog")
st.sidebar.info("""
TrustLog provides cryptographic verification of AI outputs.
This tool helps you track outputs across models and verify their integrity.
""")

# Main content
st.title("TrustLog: AI Output Logging & Verification")

tab1, tab2, tab3 = st.tabs(["Output Log", "Signature Verification", "Visualization"])

with tab1:
    st.header("AI Output Log")
    
    # Get sample data
    logs_df = get_sample_trustlog_data()
    
    # Advanced filtering section
    with st.expander("Advanced Filtering Options", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            model_filter = st.multiselect("Filter by Model", 
                                         options=logs_df["model"].unique(), 
                                         default=logs_df["model"].unique(),
                                         placeholder="Select models...")
            
            content_filter = st.multiselect("Content Type", 
                                           options=logs_df["content_type"].unique(), 
                                           default=logs_df["content_type"].unique(),
                                           placeholder="Select content types...")
        
        with col2:
            user_filter = st.multiselect("Filter by User", 
                                        options=logs_df["user"].unique(), 
                                        default=logs_df["user"].unique(),
                                        placeholder="Select users...")
            
            verification_status = st.multiselect("Verification Status", 
                                              options=logs_df["verification_status"].unique(), 
                                              default=logs_df["verification_status"].unique(),
                                              placeholder="Select status...")
        
        with col3:
            date_range = st.date_input(
                "Date Range",
                value=(datetime.now() - timedelta(days=7), datetime.now()),
                max_value=datetime.now()
            )
            
            min_risk, max_risk = st.slider(
                "Risk Score Range", 
                min_value=0, 
                max_value=100, 
                value=(0, 100)
            )
    
    # Apply filters
    filtered_df = logs_df[
        logs_df["model"].isin(model_filter) &
        logs_df["user"].isin(user_filter) &
        logs_df["content_type"].isin(content_filter) &
        logs_df["verification_status"].isin(verification_status) &
        (logs_df["risk_score"] >= min_risk) &
        (logs_df["risk_score"] <= max_risk)
    ]
    
    if len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= start_date) &
            (filtered_df["timestamp"].dt.date <= end_date)
        ]
    
    # Table search and pagination
    search_term = st.text_input("Search in Log Data", placeholder="Type to search...")
    
    if search_term:
        search_mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
        filtered_df = filtered_df[search_mask]
    
    # Display data with metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Outputs", len(filtered_df))
    with col2:
        st.metric("Unique Models", filtered_df["model"].nunique())
    with col3:
        st.metric("Unique Users", filtered_df["user"].nunique())
    with col4:
        verified_pct = (filtered_df["verification_status"] == "Verified").mean() * 100
        st.metric("Verified Outputs", f"{verified_pct:.1f}%")
    
    # Display data with styling
    st.markdown("### Log Entries")
    
    # Function to color verification status
    def highlight_verification(s):
        if s == 'Verified':
            return 'background-color: #d4edda; color: #155724'
        elif s == 'Failed':
            return 'background-color: #f8d7da; color: #721c24'
        else:
            return 'background-color: #fff3cd; color: #856404'
    
    # Function to color risk scores
    def highlight_risk(val):
        if val < 40:
            return f'background-color: #d4edda; color: #155724'
        elif val < 70:
            return f'background-color: #fff3cd; color: #856404'
        else:
            return f'background-color: #f8d7da; color: #721c24'
    
    # Apply styling
    styled_df = filtered_df.style.applymap(highlight_verification, subset=['verification_status'])\
                                .applymap(highlight_risk, subset=['risk_score'])
    
    st.dataframe(styled_df, height=400, use_container_width=True)
    
    # Export options
    col1, col2 = st.columns([1, 3])
    with col1:
        st.download_button(
            label="Export as CSV",
            data=filtered_df.to_csv(index=False).encode('utf-8'),
            file_name=f"trustlog_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        st.caption(f"Showing {len(filtered_df)} of {len(logs_df)} total log entries. Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

with tab2:
    st.header("Signature Verification")
    
    # Informational callout about verification
    st.info("""
    **How AI Output Verification Works**
    
    Each AI output is cryptographically signed with a unique key. The verification process 
    ensures the output hasn't been tampered with since generation. This maintains a 
    reliable audit trail of AI system outputs.
    """)
    
    # Verification methods
    verification_method = st.radio(
        "Verification Method",
        ["Paste Output with Signature", "Upload Signed Document", "Verify by Output ID"]
    )
    
    if verification_method == "Paste Output with Signature":
        st.markdown("### Verify Text with Embedded Signature")
        
        # Example format helper
        with st.expander("Example Format"):
            st.code("""
This is the AI generated content that needs to be verified.
It can span multiple lines and contain any text content.

Signature: a1b2c3d4e5
            """, language="text")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            output_text = st.text_area(
                "Paste AI output with signature", 
                height=200,
                placeholder="Paste the complete output including the signature line..."
            )
            
            # Format detector and helper
            if output_text and "Signature:" not in output_text:
                st.warning("⚠️ No signature detected. Make sure the text includes a 'Signature:' line at the end.")
        
        with col2:
            st.markdown("### Verification Options")
            verification_key = st.text_input("Enter verification key", type="password")
            
            # Key selection from presets
            st.markdown("**Or select a preset key:**")
            preset_key = st.selectbox(
                "Known verification keys",
                ["", "model-gpt4-key", "model-claude2-key", "model-llama2-key"],
                index=0
            )
            
            if preset_key and not verification_key:
                verification_key = preset_key
                
            verify_button = st.button("Verify Signature", type="primary", use_container_width=True)
            
        # Verification process
        if verify_button and output_text:
            with st.spinner("Verifying signature..."):
                # Add slight delay to simulate processing
                time.sleep(1.5)
                
                # Example verification logic
                if verification_key:
                    output_parts = output_text.rsplit("Signature:", 1)
                    if len(output_parts) == 2:
                        content, signature = output_parts
                        # Simple hash check for demonstration
                        expected_hash = hashlib.sha256((content + verification_key).encode()).hexdigest()[:10]
                        
                        # Show verification results in a nice formatted box
                        if signature.strip() == expected_hash:
                            st.markdown("""
                            <div style="padding: 1rem; border-radius: 0.5rem; background-color: #d4edda; color: #155724; margin: 1rem 0;">
                                <h3 style="margin-top: 0;">✅ Signature Verified</h3>
                                <p>The output is authentic and has not been modified since generation.</p>
                                <ul>
                                    <li><strong>Verification Time:</strong> {}</li>
                                    <li><strong>Content Length:</strong> {} characters</li>
                                    <li><strong>Signature:</strong> {}</li>
                                </ul>
                            </div>
                            """.format(
                                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                len(content),
                                signature.strip()
                            ), unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style="padding: 1rem; border-radius: 0.5rem; background-color: #f8d7da; color: #721c24; margin: 1rem 0;">
                                <h3 style="margin-top: 0;">❌ Invalid Signature</h3>
                                <p>The output may have been tampered with or the wrong verification key was used.</p>
                                <p>Please check that you have the correct verification key and that the full output including signature was pasted.</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.error("❌ No signature found in the text. Format should include 'Signature:' followed by the signature.")
                else:
                    st.warning("Please enter a verification key.")
    
    elif verification_method == "Upload Signed Document":
        st.markdown("### Verify Document")
        
        uploaded_file = st.file_uploader("Upload signed document", type=["txt", "json", "pdf"])
        
        col1, col2 = st.columns([2, 1])
        with col1:
            verification_key = st.text_input("Enter verification key", type="password")
        with col2:
            file_format = st.selectbox("File Format", ["Automatic Detection", "TrustLog Standard", "Legacy Format"])
        
        if uploaded_file:
            file_info = f"**File:** {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)"
            st.markdown(file_info)
            
            verify_button = st.button("Verify Document", type="primary")
            
            if verify_button:
                if verification_key:
                    with st.spinner("Verifying document integrity..."):
                        # Simulate verification process
                        time.sleep(1.5)
                        
                        # Success outcome for demo
                        st.success("✅ Document verified! The content is authentic and has not been modified.")
                        
                        # Display document details in a more structured way
                        st.markdown("### Document Verification Details")
                        
                        col1, col2 = st.columns(2)
                        with col1:
                            st.markdown("**Document Information**")
                            st.markdown(f"- **Filename:** {uploaded_file.name}")
                            st.markdown(f"- **Size:** {uploaded_file.size / 1024:.2f} KB")
                            st.markdown(f"- **Type:** {uploaded_file.type}")
                            
                        with col2:
                            st.markdown("**Verification Information**")
                            st.markdown(f"- **Verification Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            st.markdown(f"- **Status:** VERIFIED")
                            st.markdown(f"- **Verification Method:** {file_format}")
                        
                        # Show document preview option
                        st.markdown("### Document Preview")
                        if uploaded_file.type in ["text/plain", "application/json"]:
                            try:
                                content = uploaded_file.getvalue().decode()
                                st.code(content[:500] + ("..." if len(content) > 500 else ""), language="text")
                            except:
                                st.warning("Unable to preview document content.")
                        else:
                            st.info("Preview not available for this file type.")
                else:
                    st.warning("Please enter a verification key to verify the document.")
    
    else:  # Verify by Output ID
        st.markdown("### Verify by Output ID")
        
        col1, col2 = st.columns([2, 1])
        with col1:
            output_id = st.text_input("Enter Output ID", placeholder="e.g., OUT-12345-6789")
        with col2:
            model = st.selectbox("Select Model", ["Any Model", "GPT-4", "Llama-2", "Claude-2", "Falcon-180B"])
        
        verify_id_button = st.button("Look Up and Verify", type="primary")
        
        if verify_id_button and output_id:
            with st.spinner(f"Looking up output ID {output_id}..."):
                time.sleep(1.5)
                
                # For demo purposes, show a found result
                st.success(f"✅ Output {output_id} found and verified!")
                
                # Display a sample verification result
                verification_time = datetime.now()
                sample_output = """The analysis of recent market trends suggests that renewable energy investments 
                have outperformed fossil fuel investments by an average of 18.3% over the last fiscal quarter.
                
                Key factors contributing to this performance include:
                1. Favorable policy changes in major markets
                2. Decreasing production costs for solar and wind technologies
                3. Increased corporate commitments to renewable energy procurement"""
                
                st.markdown("### Verification Result")
                st.markdown(f"**Output ID:** {output_id}")
                st.markdown(f"**Verification Date:** {verification_time.strftime('%Y-%m-%d %H:%M:%S')}")
                st.markdown(f"**Generated By:** {model if model != 'Any Model' else 'GPT-4'}")
                st.markdown(f"**User:** {'user_' + output_id[-2:]}")
                st.markdown("**Status:** Verified ✓")
                
                st.markdown("### Output Content")
                st.text_area("Original Content", value=sample_output, height=150, disabled=True)
                
                # Verification history
                st.markdown("### Verification History")
                history_data = {
                    "Date": [
                        (verification_time - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                        verification_time.strftime("%Y-%m-%d %H:%M")
                    ],
                    "Verifier": ["system", "manual"],
                    "Status": ["Verified", "Verified"],
                    "Notes": ["Automatic verification at generation", "Manual verification requested"]
                }
                st.dataframe(pd.DataFrame(history_data), use_container_width=True)

with tab3:
    st.header("Output Analytics")
    
    # Get sample data
    logs_df = get_sample_trustlog_data()
    
    # Analysis controls
    with st.expander("Analysis Settings", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            time_period = st.selectbox(
                "Time Period",
                ["Last 7 Days", "Last 30 Days", "Last Quarter", "Year to Date", "Custom Range"]
            )
            
            if time_period == "Custom Range":
                date_range = st.date_input(
                    "Custom Date Range",
                    value=(datetime.now() - timedelta(days=30), datetime.now()),
                    max_value=datetime.now()
                )
        
        with col2:
            models_to_include = st.multiselect(
                "Models to Include",
                options=logs_df["model"].unique(),
                default=logs_df["model"].unique()
            )
            
            group_by = st.selectbox(
                "Group Analysis By",
                ["Day", "Week", "Month", "Model", "Content Type", "User"]
            )
        
        with col3:
            chart_type = st.selectbox(
                "Chart Type",
                ["Bar Chart", "Line Chart", "Area Chart", "Pie Chart", "Scatter Plot"]
            )
            
            include_metrics = st.checkbox("Include Summary Metrics", value=True)
    
    # Filter data based on selections
    filtered_df = logs_df.copy()
    
    if time_period == "Last 7 Days":
        cutoff_date = datetime.now() - timedelta(days=7)
        filtered_df = filtered_df[filtered_df["timestamp"] >= cutoff_date]
    elif time_period == "Last 30 Days":
        cutoff_date = datetime.now() - timedelta(days=30)
        filtered_df = filtered_df[filtered_df["timestamp"] >= cutoff_date]
    elif time_period == "Last Quarter":
        cutoff_date = datetime.now() - timedelta(days=90)
        filtered_df = filtered_df[filtered_df["timestamp"] >= cutoff_date]
    elif time_period == "Year to Date":
        # Uses the start of the current year
        current_year = datetime.now().year
        cutoff_date = datetime(current_year, 1, 1)
        filtered_df = filtered_df[filtered_df["timestamp"] >= cutoff_date]
    elif time_period == "Custom Range" and len(date_range) == 2:
        start_date, end_date = date_range
        filtered_df = filtered_df[
            (filtered_df["timestamp"].dt.date >= start_date) &
            (filtered_df["timestamp"].dt.date <= end_date)
        ]
    
    # Filter by selected models
    filtered_df = filtered_df[filtered_df["model"].isin(models_to_include)]
    
    # Display summary metrics
    if include_metrics:
        st.markdown("### Summary Metrics")
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            total_outputs = len(filtered_df)
            st.metric(
                "Total Outputs", 
                f"{total_outputs:,}",
                delta=f"{int(total_outputs * 0.08):,}" if total_outputs > 0 else "0"
            )
        
        with metric_col2:
            if "verification_status" in filtered_df.columns:
                verified_pct = (filtered_df["verification_status"] == "Verified").mean() * 100
                st.metric(
                    "Verification Rate", 
                    f"{verified_pct:.1f}%",
                    delta=f"{verified_pct - 75:.1f}%" if not pd.isna(verified_pct) else "0%"
                )
        
        with metric_col3:
            if "risk_score" in filtered_df.columns:
                avg_risk = filtered_df["risk_score"].mean()
                st.metric(
                    "Avg. Risk Score", 
                    f"{avg_risk:.1f}", 
                    delta=f"{avg_risk - 50:.1f}" if not pd.isna(avg_risk) else "0",
                    delta_color="inverse"
                )
        
        with metric_col4:
            if "output_length" in filtered_df.columns:
                avg_length = filtered_df["output_length"].mean()
                st.metric(
                    "Avg. Output Length", 
                    f"{avg_length:.0f} chars"
                )
    
    # Main visualizations row
    st.markdown("### Model & Time Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Outputs by Model visualization
        model_counts = filtered_df.groupby("model").size().reset_index(name="count")
        
        if chart_type == "Pie Chart":
            fig1 = px.pie(
                model_counts,
                values="count",
                names="model",
                title="AI Outputs by Model",
                color="model",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig1.update_traces(textposition='inside', textinfo='percent+label')
        else:
            fig1 = px.bar(
                model_counts,
                x="model",
                y="count",
                color="model",
                title="AI Outputs by Model",
                color_discrete_sequence=px.colors.qualitative.Bold
            )
            fig1.update_layout(xaxis_title="Model", yaxis_title="Number of Outputs")
        
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        # Output Trends visualization
        if group_by == "Day":
            time_grouped = filtered_df.groupby(filtered_df["timestamp"].dt.date).size().reset_index(name="count")
            time_grouped.columns = ["date", "count"]
            x_col = "date"
            title = "Daily Output Trend"
        elif group_by == "Week":
            filtered_df["week"] = filtered_df["timestamp"].dt.isocalendar().week
            filtered_df["year"] = filtered_df["timestamp"].dt.isocalendar().year
            filtered_df["week_label"] = filtered_df.apply(lambda x: f"{x['year']}-W{x['week']:02d}", axis=1)
            time_grouped = filtered_df.groupby("week_label").size().reset_index(name="count")
            x_col = "week_label"
            title = "Weekly Output Trend"
        elif group_by == "Month":
            filtered_df["month"] = filtered_df["timestamp"].dt.strftime("%Y-%m")
            time_grouped = filtered_df.groupby("month").size().reset_index(name="count")
            x_col = "month"
            title = "Monthly Output Trend"
        else:
            time_grouped = filtered_df.groupby(filtered_df["timestamp"].dt.date).size().reset_index(name="count")
            time_grouped.columns = ["date", "count"]
            x_col = "date"
            title = "Daily Output Trend"
            
        if chart_type == "Line Chart" or chart_type == "Area Chart":
            fig2 = px.line(
                time_grouped,
                x=x_col,
                y="count",
                markers=True,
                title=title
            )
            if chart_type == "Area Chart":
                fig2.update_traces(fill='tozeroy')
        elif chart_type == "Bar Chart":
            fig2 = px.bar(
                time_grouped,
                x=x_col,
                y="count",
                title=title
            )
        else:
            fig2 = px.line(
                time_grouped,
                x=x_col,
                y="count",
                markers=True,
                title=title
            )
            
        fig2.update_layout(xaxis_title="Time Period", yaxis_title="Number of Outputs")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Bottom row visualizations
    st.markdown("### Content & Risk Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        # Content Type Analysis
        content_type_counts = filtered_df.groupby("content_type").size().reset_index(name="count")
        
        fig3 = px.pie(
            content_type_counts,
            values="count",
            names="content_type",
            title="Output Content Types",
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig3.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        # Risk Score Distribution
        if "risk_score" in filtered_df.columns:
            # Create bins for risk scores
            filtered_df["risk_bin"] = pd.cut(
                filtered_df["risk_score"], 
                bins=[0, 20, 40, 60, 80, 100],
                labels=["Very Low (0-20)", "Low (21-40)", "Medium (41-60)", "High (61-80)", "Very High (81-100)"]
            )
            
            risk_counts = filtered_df.groupby("risk_bin").size().reset_index(name="count")
            
            fig4 = px.bar(
                risk_counts,
                x="risk_bin",
                y="count",
                color="risk_bin",
                title="Risk Score Distribution",
                color_discrete_map={
                    "Very Low (0-20)": "#4CAF50",    # Green
                    "Low (21-40)": "#8BC34A",        # Light Green
                    "Medium (41-60)": "#FFEB3B",     # Yellow
                    "High (61-80)": "#FF9800",       # Orange
                    "Very High (81-100)": "#F44336"  # Red
                }
            )
            fig4.update_layout(xaxis_title="Risk Level", yaxis_title="Number of Outputs")
            st.plotly_chart(fig4, use_container_width=True)
            
            # Also show a heat map of risk by model and content type
            pivot = pd.pivot_table(
                filtered_df, 
                values="risk_score", 
                index=["model"], 
                columns=["content_type"], 
                aggfunc="mean"
            ).round(1)
            
            if not pivot.empty:
                st.markdown("### Risk Score Heat Map (by Model & Content Type)")
                fig5 = px.imshow(
                    pivot,
                    text_auto=True,
                    color_continuous_scale="RdYlGn_r",
                    title="Average Risk Score by Model and Content Type"
                )
                fig5.update_layout(height=300)
                st.plotly_chart(fig5, use_container_width=True)
        else:
            # If no risk score column, show output length distribution
            if "output_length" in filtered_df.columns:
                fig4 = px.histogram(
                    filtered_df,
                    x="output_length",
                    nbins=20,
                    title="Output Length Distribution",
                    color_discrete_sequence=["#1E88E5"]
                )
                fig4.update_layout(xaxis_title="Output Length (chars)", yaxis_title="Count")
                st.plotly_chart(fig4, use_container_width=True)
    
    # Export options for analyzed data
    with st.expander("Export Analysis Data"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.download_button(
                "Download Filtered Data (CSV)",
                filtered_df.to_csv(index=False).encode("utf-8"),
                file_name=f"trustlog_analysis_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        
        with col2:
            st.download_button(
                "Download Summary Report (JSON)",
                data=pd.Series({
                    "total_outputs": total_outputs,
                    "time_period": time_period,
                    "models_included": models_to_include,
                    "verification_rate": verified_pct if "verification_status" in filtered_df.columns else None,
                    "avg_risk_score": avg_risk if "risk_score" in filtered_df.columns else None,
                    "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }).to_json().encode("utf-8"),
                file_name=f"trustlog_summary_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
