import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from utils.data_utils import get_gpu_health_data

# Page configuration
st.set_page_config(
    page_title="GPU Health - Monitoring and Forecasting",
    page_icon="🔍",
    layout="wide"
)

# Sidebar
st.sidebar.title("GPU Health")
st.sidebar.info("""
Monitor GPU health metrics with time-series forecasting and fragmentation analysis.
Get early warnings about potential hardware issues and optimize GPU lifecycle management.
""")

# Main content
st.title("GPU Health: Monitoring, Scoring, and Forecasting")

tab1, tab2, tab3 = st.tabs(["Health Overview", "Memory Fragmentation", "Predictive Maintenance"])

with tab1:
    st.header("GPU Health Overview")
    
    # GPU selection
    gpu_ids = [f"gpu-{i}" for i in range(1, 9)]
    selected_gpu = st.selectbox("Select GPU", options=gpu_ids)
    
    # Get health data
    health_data = get_gpu_health_data(selected_gpu)
    
    # Calculate overall health score
    current_score = health_data["health_score"].iloc[-1]
    prev_score = health_data["health_score"].iloc[-30]
    score_change = current_score - prev_score
    
    # Top status section with enhanced layout
    status_cols = st.columns([1, 1, 1])
    
    with status_cols[0]:
        st.markdown(f"**GPU Model:** NVIDIA A100 SXM4")
        st.markdown(f"**VRAM:** 80 GB HBM2e")
        st.markdown(f"**Driver:** 535.129.03")
    
    with status_cols[1]:
        # Calculate uptime
        current_uptime = np.random.randint(5, 60)
        total_uptime = np.random.randint(1000, 5000)
        
        st.markdown(f"**Current Uptime:** {current_uptime} days")
        st.markdown(f"**Total Uptime:** {total_uptime} hours")
        st.markdown(f"**Last Maintenance:** {(datetime.now() - timedelta(days=np.random.randint(10, 45))).strftime('%Y-%m-%d')}")
    
    with status_cols[2]:
        # Status indicator
        if current_score >= 75:
            status = "Healthy"
            status_color = "#2E7D32"  # Dark green
        elif current_score >= 50:
            status = "Monitor"
            status_color = "#FFA000"  # Amber
        else:
            status = "Warning"
            status_color = "#C62828"  # Dark red
        
        st.markdown(
            f"""
            <div style="background-color: {status_color}; padding: 10px; border-radius: 5px; text-align: center;">
                <h2 style="color: white; margin: 0; font-size: 1.5rem;">{status}</h2>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Health trend indicator
        trend_icon = "↗️" if score_change > 0 else "↘️" if score_change < 0 else "↔️"
        st.markdown(f"**Health Trend:** {trend_icon} {abs(score_change):.1f} points")
    
    # Horizontal divider
    st.markdown("<hr style='margin: 1rem 0; border-color: #E0E0E0;'>", unsafe_allow_html=True)
    
    # Enhanced health score gauge with better visual design
    gauge_cols = st.columns([2, 1])
    
    with gauge_cols[0]:
        st.subheader("GPU Health Score")
        
        # Create an enhanced gauge chart
        fig = go.Figure()
        
        # Add main gauge
        fig.add_trace(go.Indicator(
            mode="gauge+number+delta",
            value=current_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            delta={
                'reference': prev_score, 
                'increasing': {'color': 'green'}, 
                'decreasing': {'color': 'red'},
                'valueformat': '.1f'
            },
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#444"},
                'bar': {'color': "#2196F3" if current_score >= 50 else "#F44336"},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "#E0E0E0",
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(244, 67, 54, 0.3)'},  # Red with opacity
                    {'range': [40, 75], 'color': 'rgba(255, 152, 0, 0.3)'},  # Orange with opacity
                    {'range': [75, 100], 'color': 'rgba(76, 175, 80, 0.3)'}  # Green with opacity
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
            },
            title={'text': f"{selected_gpu} Health Status", 'font': {'size': 24}}
        ))
        
        # Add custom annotations for health ranges
        fig.add_annotation(
            x=0.15, y=0.2,
            text="Critical",
            showarrow=False,
            font={'color': '#C62828', 'size': 12}
        )
        
        fig.add_annotation(
            x=0.35, y=0.2,
            text="Warning",
            showarrow=False,
            font={'color': '#F57F17', 'size': 12}
        )
        
        fig.add_annotation(
            x=0.75, y=0.2,
            text="Healthy",
            showarrow=False,
            font={'color': '#388E3C', 'size': 12}
        )
        
        # Update layout for better appearance
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with gauge_cols[1]:
        st.subheader("Health Rating Explained")
        
        # Health score interpretation
        if current_score >= 75:
            health_description = "Excellent condition. The GPU is operating at optimal performance levels."
            recommended_action = "Continue regular monitoring."
        elif current_score >= 60:
            health_description = "Good condition. Minor signs of wear but functioning properly."
            recommended_action = "Monitor closely for changes in performance."
        elif current_score >= 50:
            health_description = "Fair condition. Some performance degradation detected."
            recommended_action = "Schedule diagnostic tests within 2 weeks."
        elif current_score >= 40:
            health_description = "Concerning condition. Significant performance issues detected."
            recommended_action = "Perform maintenance within 1 week."
        else:
            health_description = "Poor condition. Major issues affecting performance and reliability."
            recommended_action = "Immediate maintenance required."
        
        # Display interpretation with better formatting
        st.markdown(
            f"""
            <div style="background-color: rgba(33, 150, 243, 0.1); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #0D47A1;">Current Rating: {current_score:.1f}/100</h4>
                <p style="margin-bottom: 5px;">{health_description}</p>
            </div>
            
            <div style="background-color: rgba(0, 0, 0, 0.05); padding: 10px; border-radius: 5px;">
                <h4 style="margin-top: 0;">Recommended Action:</h4>
                <p style="margin-bottom: 0;">{recommended_action}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Enhanced component breakdown with better visualization
    st.subheader("Health Components Breakdown")
    
    # Two columns for components and radar chart
    component_cols = st.columns([3, 2])
    
    with component_cols[0]:
        # Create a grid layout for components
        component_grid = st.columns(2)
        
        component_scores = {
            "Memory Health": int(np.mean(health_data["memory_health"].tail(5))),
            "Temperature Stability": int(np.mean(health_data["temp_stability"].tail(5))),
            "Power Efficiency": int(np.mean(health_data["power_efficiency"].tail(5))),
            "Performance Consistency": int(np.mean(health_data["perf_consistency"].tail(5)))
        }
        
        # Add historical data for sparklines
        component_history = {
            "Memory Health": list(health_data["memory_health"].tail(14)),
            "Temperature Stability": list(health_data["temp_stability"].tail(14)),
            "Power Efficiency": list(health_data["power_efficiency"].tail(14)),
            "Performance Consistency": list(health_data["perf_consistency"].tail(14))
        }
        
        # Add component descriptions
        component_descriptions = {
            "Memory Health": "VRAM integrity and error rate",
            "Temperature Stability": "Thermal regulation efficiency",
            "Power Efficiency": "Energy consumption vs performance",
            "Performance Consistency": "Clock stability and throughput"
        }
        
        for i, (component, score) in enumerate(component_scores.items()):
            col_idx = i % 2
            with component_grid[col_idx]:
                # Create a card-like layout for each component
                # Define color based on score
                if score < 50:
                    color = "#F44336"  # Red
                    level = "Poor"
                elif score < 75:
                    color = "#FF9800"  # Orange
                    level = "Fair"
                else:
                    color = "#4CAF50"  # Green
                    level = "Good"
                
                # Create mini sparkline for trend
                history = component_history[component]
                spark_fig = go.Figure(go.Scatter(
                    y=history,
                    mode='lines',
                    line=dict(width=2, color=color)
                ))
                
                spark_fig.update_layout(
                    height=40,
                    width=120,
                    margin=dict(l=0, r=0, t=0, b=0),
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    yaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False,
                        range=[min(0, min(history)-5), 100]
                    ),
                    xaxis=dict(
                        showticklabels=False,
                        showgrid=False,
                        zeroline=False
                    ),
                    showlegend=False
                )
                
                # Card layout with HTML
                st.markdown(
                    f"""
                    <div style="border: 1px solid #E0E0E0; border-radius: 5px; padding: 10px; margin-bottom: 15px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: {color};">{component}</h4>
                            <span style="background-color: {color}20; color: {color}; padding: 2px 8px; border-radius: 10px; font-size: 0.8rem;">{level}</span>
                        </div>
                        <p style="color: #666; font-size: 0.8rem; margin: 5px 0;">{component_descriptions[component]}</p>
                        <div style="margin: 10px 0;">
                            <div style="width: 100%; background-color: #eee; border-radius: 5px; height: 8px;">
                                <div style="width: {score}%; height: 8px; border-radius: 5px; background-color: {color};"></div>
                            </div>
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-weight: bold;">{score}/100</span>
                            <span style="color: #666; font-size: 0.8rem;">14-day trend</span>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with component_cols[1]:
        # Create radar chart for component comparison
        categories = list(component_scores.keys())
        values = list(component_scores.values())
        # Close the loop for radar chart
        categories.append(categories[0])
        values.append(values[0])
        
        # Create radar plot
        radar_fig = go.Figure()
        
        # Add radar chart with better styling
        radar_fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(33, 150, 243, 0.2)',
            line=dict(color='#2196F3', width=2),
            name='Component Health'
        ))
        
        # Add threshold for reference
        threshold_values = [50] * len(categories)
        radar_fig.add_trace(go.Scatterpolar(
            r=threshold_values,
            theta=categories,
            fill='none',
            line=dict(color='#F44336', width=1, dash='dash'),
            name='Warning Threshold'
        ))
        
        # Update layout
        radar_fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=True,
            legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
            margin=dict(l=80, r=80, t=20, b=20),
            height=350
        )
        
        st.plotly_chart(radar_fig, use_container_width=True)
    
    # Enhanced health trend over time
    st.subheader("Health Score Trend & Analysis")
    
    # Two columns for trend chart and statistics
    trend_cols = st.columns([3, 1])
    
    with trend_cols[0]:
        # Create enhanced trend visualization with area fill and annotations
        trend_fig = go.Figure()
        
        # Add area for high health zone
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=[75] * len(health_data),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=[100] * len(health_data),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(76, 175, 80, 0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add area for warning zone
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=[50] * len(health_data),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=[75] * len(health_data),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(255, 152, 0, 0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add area for critical zone
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=[0] * len(health_data),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=[50] * len(health_data),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(244, 67, 54, 0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add main health score line
        trend_fig.add_trace(go.Scatter(
            x=health_data["timestamp"],
            y=health_data["health_score"],
            mode="lines+markers",
            name="Health Score",
            line=dict(color="#2196F3", width=3),
            connectgaps=True,
            marker=dict(size=6)
        ))
        
        # Add threshold lines with better styling
        trend_fig.add_shape(
            type="line",
            x0=health_data["timestamp"].min(),
            x1=health_data["timestamp"].max(),
            y0=75,
            y1=75,
            line=dict(color="#4CAF50", width=2, dash="dash")
        )
        
        trend_fig.add_shape(
            type="line",
            x0=health_data["timestamp"].min(),
            x1=health_data["timestamp"].max(),
            y0=50,
            y1=50,
            line=dict(color="#F44336", width=2, dash="dash")
        )
        
        # Add annotations for thresholds
        trend_fig.add_annotation(
            x=health_data["timestamp"].min(),
            y=75,
            text="Good Health Threshold",
            showarrow=False,
            xshift=70,
            yshift=10,
            font=dict(size=12, color="#4CAF50")
        )
        
        trend_fig.add_annotation(
            x=health_data["timestamp"].min(),
            y=50,
            text="Warning Threshold",
            showarrow=False,
            xshift=70,
            yshift=-10,
            font=dict(size=12, color="#F44336")
        )
        
        # Add events markers for significant changes
        # Find largest drops in health score
        health_diff = health_data["health_score"].diff().fillna(0)
        significant_drops = health_data.loc[health_diff < -5].index.tolist()
        
        for idx in significant_drops[:3]:  # Only show top 3 most significant drops
            event_date = health_data.loc[idx, "timestamp"]
            event_score = health_data.loc[idx, "health_score"]
            
            trend_fig.add_trace(go.Scatter(
                x=[event_date],
                y=[event_score],
                mode="markers",
                marker=dict(
                    symbol="triangle-down",
                    size=14,
                    color="#F44336",
                    line=dict(color="#FFFFFF", width=1)
                ),
                name="Significant Drop",
                showlegend=False,
                hovertemplate="<b>Significant Drop</b><br>Date: %{x}<br>Score: %{y:.1f}<extra></extra>"
            ))
        
        # Update layout for better appearance
        trend_fig.update_layout(
            title=f"{selected_gpu} Health Score History & Analysis",
            xaxis_title="Date",
            yaxis=dict(
                title="Health Score",
                range=[0, 100],
                tickmode="linear",
                tick0=0,
                dtick=25
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            height=350,
            hovermode="closest"
        )
        
        st.plotly_chart(trend_fig, use_container_width=True)
    
    with trend_cols[1]:
        # Add trend statistics and analysis
        st.markdown("#### Trend Statistics")
        
        # Calculate trend metrics
        trend_window = min(30, len(health_data))
        health_window = health_data["health_score"].tail(trend_window)
        
        avg_health = health_window.mean()
        min_health = health_window.min()
        max_health = health_window.max()
        volatility = health_window.std()
        
        # Calculate slope of trend (positive = improving, negative = declining)
        x = np.array(range(len(health_window))).reshape(-1, 1)
        y = health_window.values
        model = LinearRegression().fit(x, y)
        slope = model.coef_[0]
        
        # Trend direction
        if abs(slope) < 0.05:
            trend = "Stable"
            trend_color = "#2196F3"  # Blue
        elif slope > 0:
            trend = "Improving"
            trend_color = "#4CAF50"  # Green
        else:
            trend = "Declining"
            trend_color = "#F44336"  # Red
        
        # Display metrics with better formatting
        st.markdown(
            f"""
            <div style="background-color: rgba(33, 150, 243, 0.05); padding: 10px; border-radius: 5px; margin-bottom: 10px;">
                <table style="width: 100%;">
                    <tr>
                        <td><b>Avg Health:</b></td>
                        <td style="text-align: right;">{avg_health:.1f}</td>
                    </tr>
                    <tr>
                        <td><b>Range:</b></td>
                        <td style="text-align: right;">{min_health:.1f} - {max_health:.1f}</td>
                    </tr>
                    <tr>
                        <td><b>Volatility:</b></td>
                        <td style="text-align: right;">±{volatility:.1f}</td>
                    </tr>
                    <tr>
                        <td><b>30-Day Trend:</b></td>
                        <td style="text-align: right; color: {trend_color};">{trend}</td>
                    </tr>
                </table>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Add analysis of trend
        st.markdown("#### Health Analysis")
        
        if trend == "Improving":
            analysis = f"Health score is showing improvement over the past {trend_window} days. Continue current maintenance protocols."
        elif trend == "Stable":
            if avg_health >= 75:
                analysis = f"Health score is stable at good levels. Maintain regular monitoring protocols."
            elif avg_health >= 50:
                analysis = f"Health score is stable but below optimal levels. Consider proactive maintenance."
            else:
                analysis = f"Health score is stable at concerning levels. Maintenance advised."
        else:  # Declining
            if avg_health >= 75:
                analysis = f"Health score is declining from good levels. Monitor closely for acceleration."
            elif avg_health >= 50:
                analysis = f"Health score is declining and approaching warning levels. Schedule diagnostic tests."
            else:
                analysis = f"Health score is declining at already concerning levels. Urgent maintenance required."
        
        st.markdown(f"<p style='font-size: 0.95rem;'>{analysis}</p>", unsafe_allow_html=True)
        
        # Predict time to warning level
        if avg_health > 50 and slope < 0:
            weeks_to_warning = (avg_health - 50) / (-slope * 7)
            if weeks_to_warning < 52:  # Only show if less than a year
                st.markdown(
                    f"""
                    <div style="background-color: rgba(255, 152, 0, 0.1); padding: 10px; border-radius: 5px; margin-top: 10px;">
                        <p style="margin: 0; color: #FF9800;"><b>Forecast:</b> Warning level may be reached in {weeks_to_warning:.1f} weeks if current trend continues.</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Event log with enhanced styling
    st.subheader("Health Event Log")
    
    # Sample events with more detail
    events = [
        {"timestamp": (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"), "type": "Warning", "message": "Unusually high temperature detected", "details": "Peak temperature reached 87°C during benchmark test", "action": "Increased fan speed automatically"},
        {"timestamp": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"), "type": "Info", "message": "Scheduled memory test completed", "details": "No errors detected in VRAM integrity check", "action": "None required"},
        {"timestamp": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d %H:%M"), "type": "Warning", "message": "Memory fragmentation increasing", "details": "Fragmentation level reached 18.5%", "action": "Scheduled automatic defragmentation"},
        {"timestamp": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d %H:%M"), "type": "Error", "message": "Power fluctuation detected during operation", "details": "Voltage dropped below threshold for 25ms", "action": "System recovered automatically"},
        {"timestamp": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d %H:%M"), "type": "Info", "message": "Firmware updated to version 450.21", "details": "Security and performance improvements applied", "action": "System restarted successfully"}
    ]
    
    events_df = pd.DataFrame(events)
    
    # Add filter options
    event_filter_cols = st.columns([1, 2, 1])
    with event_filter_cols[0]:
        event_type_filter = st.multiselect(
            "Filter by Type",
            options=["Info", "Warning", "Error"],
            default=["Info", "Warning", "Error"]
        )
    
    with event_filter_cols[1]:
        event_search = st.text_input("Search in events", placeholder="Search by keyword...")
    
    with event_filter_cols[2]:
        event_timeframe = st.selectbox(
            "Timeframe",
            options=["Last 24 Hours", "Last 7 Days", "Last 30 Days", "All Time"]
        )
    
    # Apply filters (simulated)
    filtered_events = events_df[events_df["type"].isin(event_type_filter)]
    if event_search:
        filtered_events = filtered_events[filtered_events["message"].str.contains(event_search, case=False) | 
                                         filtered_events["details"].str.contains(event_search, case=False)]
    
    # Color-code events with enhanced styling
    def color_events(val):
        if val == "Error":
            return 'background-color: rgba(244, 67, 54, 0.2); color: #C62828;'
        elif val == "Warning":
            return 'background-color: rgba(255, 152, 0, 0.2); color: #EF6C00;'
        else:  # Info
            return 'background-color: rgba(33, 150, 243, 0.2); color: #1565C0;'
    
    # Display events with enhanced styling
    if not filtered_events.empty:
        st.dataframe(
            filtered_events.style.map(color_events, subset=['type']),
            column_config={
                "timestamp": st.column_config.Column(
                    "Time",
                    width="medium"
                ),
                "type": st.column_config.Column(
                    "Type",
                    width="small"
                ),
                "message": st.column_config.Column(
                    "Event",
                    width="large"
                ),
                "details": st.column_config.Column(
                    "Details",
                    width="large"
                ),
                "action": st.column_config.Column(
                    "Action Taken",
                    width="medium"
                )
            },
            hide_index=True,
            use_container_width=True
        )
    else:
        st.info("No events match your current filter criteria.")
    
    # Export button for log data
    st.download_button(
        label="Export Event Log",
        data=events_df.to_csv(index=False).encode("utf-8"),
        file_name=f"{selected_gpu}_event_log_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

with tab2:
    st.header("Memory Fragmentation Analysis")
    
    # Top section with explanation
    st.markdown("""
    <div style="background-color: rgba(33, 150, 243, 0.1); padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h4 style="margin-top: 0; color: #0D47A1;">About Memory Fragmentation</h4>
        <p style="margin-bottom: 0;">Memory fragmentation occurs when the GPU's VRAM becomes divided into small, non-contiguous blocks, reducing performance and availability for large allocations. Regular monitoring helps prevent performance degradation.</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Controls and GPU selection
    control_cols = st.columns([2, 1, 1])
    
    with control_cols[0]:
        # GPU selection for fragmentation analysis
        frag_gpu = st.selectbox("Select GPU for Memory Analysis", options=gpu_ids, key="frag_gpu")
    
    with control_cols[1]:
        time_range = st.selectbox(
            "Time Range",
            options=["Last 7 Days", "Last 30 Days", "Last 90 Days"],
            index=1
        )
    
    with control_cols[2]:
        refresh_button = st.button("🔄 Refresh Data", use_container_width=True)
    
    # Generate sample fragmentation data - enhanced with more realistic patterns
    if time_range == "Last 7 Days":
        days = 7
    elif time_range == "Last 30 Days":
        days = 30
    else:  # Last 90 Days
        days = 90
    
    timestamps = [datetime.now() - timedelta(days=i) for i in range(days)][::-1]
    
    # Create more realistic fragmentation pattern
    # Base trend with gradual increase
    base_trend = np.linspace(5, 25, days) 
    
    # Add weekly pattern (fragmentation rises during week, drops after weekend maintenance)
    week_pattern = np.zeros(days)
    for i in range(days):
        day_of_week = timestamps[i].weekday()  # 0=Monday, 6=Sunday
        if day_of_week == 6:  # Maintenance on Sunday
            week_pattern[i] = -5
        else:
            week_pattern[i] = day_of_week * 0.5  # Gradual increase through the week
    
    # Add occasional drops due to maintenance/defragmentation
    maintenance_drops = np.zeros(days)
    maintenance_dates = []
    
    for i in range(1, days):
        # Add random maintenance events (significant drops in fragmentation)
        if i % 14 == 0 or np.random.random() < 0.03:  # Scheduled or random maintenance
            drop_amount = np.random.uniform(4, 10)
            maintenance_drops[i] = -drop_amount
            maintenance_dates.append(timestamps[i])
    
    # Add recovery after maintenance (fragmentation builds back up)
    recovery_pattern = np.zeros(days)
    for i, date in enumerate(timestamps):
        for m_date in maintenance_dates:
            days_since = (date - m_date).days
            if 0 < days_since < 10:  # Recovery period
                recovery_pattern[i] += min(days_since * 0.5, 3)  # Gradual recovery
    
    # Random daily variations
    daily_variation = np.random.normal(0, 1.5, days)
    
    # Combine all patterns
    memory_fragmentation = np.clip(base_trend + week_pattern + maintenance_drops + recovery_pattern + daily_variation, 0, 100)
    
    # Create additional data for analysis
    # Memory allocation data (increases with fragmentation)
    allocation_attempts = [100 + int(frag * 1.5) for frag in memory_fragmentation]
    failed_allocations = [int(frag**1.5 / 10) for frag in memory_fragmentation]
    allocation_time_ms = [10 + int(frag**1.2) for frag in memory_fragmentation]
    
    # Create main dataframe
    frag_data = pd.DataFrame({
        "timestamp": timestamps,
        "fragmentation": memory_fragmentation,
        "allocation_attempts": allocation_attempts,
        "failed_allocations": failed_allocations,
        "allocation_time_ms": allocation_time_ms
    })
    
    # Add daily summary stats
    daily_frag_data = frag_data.copy()
    daily_frag_data["date"] = daily_frag_data["timestamp"].dt.date
    daily_summary = daily_frag_data.groupby("date").agg({
        "fragmentation": ["mean", "min", "max"],
        "failed_allocations": "sum"
    }).reset_index()
    
    daily_summary.columns = ["date", "avg_frag", "min_frag", "max_frag", "total_failures"]
    
    # Enhanced fragmentation trend visualization
    st.subheader("Memory Fragmentation Trend Analysis")
    
    frag_chart_tabs = st.tabs(["Line Chart", "Heatmap", "Daily Summary"])
    
    with frag_chart_tabs[0]:
        # Enhanced line chart with area fill and annotations
        fig = go.Figure()
        
        # Add colored zones for severity levels
        # Critical zone
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=[30] * len(frag_data),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=[100] * len(frag_data),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(244, 67, 54, 0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Warning zone
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=[15] * len(frag_data),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=[30] * len(frag_data),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(255, 152, 0, 0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Normal zone
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=[0] * len(frag_data),
            fill=None,
            mode='lines',
            line=dict(width=0),
            showlegend=False,
            hoverinfo='skip'
        ))
        
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=[15] * len(frag_data),
            fill='tonexty',
            mode='lines',
            line=dict(width=0),
            fillcolor='rgba(76, 175, 80, 0.1)',
            showlegend=False,
            hoverinfo='skip'
        ))
        
        # Add main fragmentation line
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=frag_data["fragmentation"],
            mode="lines+markers",
            name="Fragmentation Level",
            line=dict(color="#2196F3", width=3),
            connectgaps=True,
            marker=dict(size=6),
            hovertemplate="<b>%{x|%d %b, %H:%M}</b><br>Fragmentation: %{y:.1f}%<extra></extra>"
        ))
        
        # Add secondary axis with failed allocations
        fig.add_trace(go.Scatter(
            x=frag_data["timestamp"],
            y=frag_data["failed_allocations"],
            mode="lines",
            name="Failed Allocations",
            line=dict(color="#F44336", width=2, dash="dot"),
            yaxis="y2",
            hovertemplate="<b>%{x|%d %b, %H:%M}</b><br>Failed Allocations: %{y}<extra></extra>"
        ))
        
        # Add threshold lines with better styling
        fig.add_shape(
            type="line",
            x0=frag_data["timestamp"].min(),
            x1=frag_data["timestamp"].max(),
            y0=15,
            y1=15,
            line=dict(color="#FF9800", width=2, dash="dash")
        )
        
        fig.add_shape(
            type="line",
            x0=frag_data["timestamp"].min(),
            x1=frag_data["timestamp"].max(),
            y0=30,
            y1=30,
            line=dict(color="#F44336", width=2, dash="dash")
        )
        
        # Add annotations for thresholds
        fig.add_annotation(
            x=frag_data["timestamp"].min(),
            y=15,
            text="Warning Threshold",
            showarrow=False,
            xshift=70,
            yshift=10,
            font=dict(size=12, color="#FF9800")
        )
        
        fig.add_annotation(
            x=frag_data["timestamp"].min(),
            y=30,
            text="Critical Threshold",
            showarrow=False,
            xshift=70,
            yshift=10,
            font=dict(size=12, color="#F44336")
        )
        
        # Mark maintenance events
        for date in maintenance_dates:
            if date >= frag_data["timestamp"].min() and date <= frag_data["timestamp"].max():
                fig.add_shape(
                    type="line",
                    x0=date,
                    x1=date,
                    y0=0,
                    y1=100,
                    line=dict(color="#4CAF50", width=1, dash="dot")
                )
        
        # Update layout with dual Y-axis
        fig.update_layout(
            title=f"{frag_gpu} Memory Fragmentation Analysis",
            xaxis_title="Date",
            yaxis=dict(
                title="Fragmentation (%)",
                range=[0, max(35, max(frag_data["fragmentation"]) + 5)],
            ),
            yaxis2=dict(
                title="Failed Allocations",
                range=[0, max(frag_data["failed_allocations"]) * 1.2],
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            height=400,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with frag_chart_tabs[1]:
        # Create heatmap of fragmentation by day and hour
        frag_data["day"] = frag_data["timestamp"].dt.date
        frag_data["hour"] = frag_data["timestamp"].dt.hour
        
        # Group by day and hour
        if len(frag_data) > 24:  # Only create heatmap if enough data
            heatmap_data = frag_data.pivot_table(
                index="day", 
                columns="hour", 
                values="fragmentation",
                aggfunc="mean"
            ).fillna(0)
            
            # Create heatmap
            fig = px.imshow(
                heatmap_data,
                labels=dict(x="Hour of Day", y="Date", color="Fragmentation (%)"),
                x=heatmap_data.columns,
                y=heatmap_data.index,
                color_continuous_scale="RdYlGn_r",
                title="Memory Fragmentation Heatmap by Hour"
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            st.markdown("""
            <div style="background-color: rgba(0, 0, 0, 0.05); padding: 10px; border-radius: 5px;">
                <p style="margin: 0; font-size: 0.9rem;">
                    <strong>Interpret this heatmap:</strong> Darker red areas indicate higher fragmentation. Look for patterns in fragmentation levels by time of day and day of week to optimize maintenance scheduling.
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Insufficient data for heatmap visualization. Please select a longer time range.")
    
    with frag_chart_tabs[2]:
        # Daily summary statistics table and chart
        st.markdown("### Daily Fragmentation Summary")
        
        # Create range chart showing min, avg, max fragmentation by day
        fig = go.Figure()
        
        # Add range for each day
        fig.add_trace(go.Scatter(
            x=daily_summary["date"],
            y=daily_summary["min_frag"],
            name="Minimum",
            mode="lines",
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=daily_summary["date"],
            y=daily_summary["max_frag"],
            name="Range",
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            fillcolor="rgba(33, 150, 243, 0.2)",
            showlegend=False
        ))
        
        # Add average line
        fig.add_trace(go.Scatter(
            x=daily_summary["date"],
            y=daily_summary["avg_frag"],
            name="Average",
            mode="lines+markers",
            line=dict(color="#0D47A1", width=2),
            marker=dict(size=6, color="#0D47A1")
        ))
        
        # Add threshold lines
        fig.add_shape(
            type="line",
            x0=daily_summary["date"].min(),
            x1=daily_summary["date"].max(),
            y0=15,
            y1=15,
            line=dict(color="#FF9800", width=1, dash="dash")
        )
        
        fig.add_shape(
            type="line",
            x0=daily_summary["date"].min(),
            x1=daily_summary["date"].max(),
            y0=30,
            y1=30,
            line=dict(color="#F44336", width=1, dash="dash")
        )
        
        fig.update_layout(
            title="Daily Fragmentation Range",
            xaxis_title="Date",
            yaxis_title="Fragmentation (%)",
            yaxis=dict(range=[0, max(35, daily_summary["max_frag"].max())]),
            height=300,
            margin=dict(l=0, r=0, t=40, b=0),
            hovermode="x unified",
            hoverlabel=dict(bgcolor="white"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Display summary table
        with st.expander("View Daily Summary Table", expanded=False):
            # Format table for display
            display_summary = daily_summary.copy()
            display_summary["date"] = display_summary["date"].astype(str)
            display_summary = display_summary.rename(columns={
                "date": "Date",
                "avg_frag": "Avg Fragmentation (%)",
                "min_frag": "Min Fragmentation (%)",
                "max_frag": "Max Fragmentation (%)",
                "total_failures": "Failed Allocations"
            })
            
            # Round numeric columns
            for col in ["Avg Fragmentation (%)", "Min Fragmentation (%)", "Max Fragmentation (%)"]:
                display_summary[col] = display_summary[col].round(1)
            
            st.dataframe(display_summary, use_container_width=True)
    
    # Enhanced memory block visualization with detailed map
    st.subheader("Memory Block Visualization")
    
    # Create time point selector for block visualization
    time_points = ["Current State"]
    if time_range != "Last 7 Days":
        time_points.extend(["7 Days Ago", "14 Days Ago"])
    if time_range == "Last 90 Days":
        time_points.append("30 Days Ago")
    
    time_point_cols = st.columns([2, 1, 1])
    with time_point_cols[0]:
        selected_time = st.select_slider(
            "Select Time Point for Memory Map", 
            options=time_points
        )
    
    with time_point_cols[1]:
        simulated_total_memory = st.selectbox(
            "Memory Size",
            options=["16 GB", "24 GB", "32 GB", "80 GB"],
            index=2
        )
    
    with time_point_cols[2]:
        visualization_type = st.selectbox(
            "Visualization Type",
            options=["Block Map", "Treemap"],
            index=0
        )
    
    # Get current fragmentation percentage based on selected time point
    if selected_time == "Current State":
        current_frag = memory_fragmentation[-1]
        view_date = timestamps[-1]
    elif selected_time == "7 Days Ago":
        idx = max(0, len(memory_fragmentation) - 7)
        current_frag = memory_fragmentation[idx]
        view_date = timestamps[idx]
    elif selected_time == "14 Days Ago":
        idx = max(0, len(memory_fragmentation) - 14)
        current_frag = memory_fragmentation[idx]
        view_date = timestamps[idx]
    else:  # 30 Days Ago
        idx = max(0, len(memory_fragmentation) - 30)
        current_frag = memory_fragmentation[idx]
        view_date = timestamps[idx]
    
    # Add viewer state information
    st.markdown(f"""
    <div style="background-color: rgba(0, 0, 0, 0.05); padding: 10px; border-radius: 5px; margin-bottom: 15px;">
        <p style="margin: 0; font-size: 0.9rem;">
            <strong>Viewing memory state for:</strong> {frag_gpu} at {view_date.strftime('%Y-%m-%d %H:%M')} 
            | Fragmentation: {current_frag:.1f}% | {simulated_total_memory} Memory
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Generate memory blocks with more detailed categories
    np.random.seed(int(current_frag) + hash(selected_time) % 1000)  # Consistent but different seed for each view
    total_blocks = 100
    
    # Number of fragments depends on fragmentation level
    num_fragments = int(current_frag * 1.5 + 10)
    
    # Generate memory blocks
    blocks = []
    used_size = 0
    
    # Different allocation types
    allocation_types = [
        "Model Weights", 
        "Activation Cache", 
        "Tensor Data", 
        "Kernel Buffers", 
        "Free"
    ]
    
    allocation_colors = {
        "Model Weights": "#1976D2",  # Blue
        "Activation Cache": "#7B1FA2",  # Purple
        "Tensor Data": "#388E3C",  # Green
        "Kernel Buffers": "#F57F17",  # Orange
        "Free": "#E0E0E0"  # Light grey
    }
    
    # Create a more fragmented layout if fragmentation is high
    if current_frag > 20:
        # Many smaller blocks
        while len(blocks) < num_fragments and used_size < 95:
            # Block size inversely relates to fragmentation
            block_size = np.random.exponential(10 / (current_frag/10 + 1))
            block_size = max(0.2, min(block_size, 8))  # Cap size between 0.2 and 8
            
            if used_size + block_size > 95:
                block_size = 95 - used_size
            
            # Determine block type
            if np.random.random() < 0.15:  # 15% chance of free block when fragmented
                block_type = "Free"
            else:
                block_type = np.random.choice(allocation_types[:-1], p=[0.4, 0.3, 0.2, 0.1])
            
            blocks.append({
                "start": used_size,
                "size": block_size,
                "status": block_type
            })
            
            used_size += block_size
    else:
        # Fewer, larger blocks with less fragmentation
        while used_size < 85:
            # Larger blocks
            block_size = np.random.exponential(15 / (current_frag/20 + 1))
            block_size = max(1, min(block_size, 20))  # Cap size between 1 and 20
            
            if used_size + block_size > 85:
                block_size = 85 - used_size
            
            # Determine block type - fewer free blocks in middle
            if np.random.random() < 0.05:  # Only 5% chance of free block
                block_type = "Free"
            else:
                block_type = np.random.choice(allocation_types[:-1], p=[0.5, 0.2, 0.2, 0.1])
            
            blocks.append({
                "start": used_size,
                "size": block_size,
                "status": block_type
            })
            
            used_size += block_size
    
    # Add free space at the end (always a larger contiguous block)
    blocks.append({
        "start": used_size,
        "size": 100 - used_size,
        "status": "Free"
    })
    
    # Create additional small free blocks scattered throughout (for realism)
    for _ in range(int(current_frag / 3)):
        insert_at = np.random.uniform(0, used_size)
        # Find containing block
        for i, block in enumerate(blocks):
            if block["start"] <= insert_at < block["start"] + block["size"]:
                if block["status"] != "Free" and block["size"] > 1:
                    # Split this block
                    original_end = block["start"] + block["size"]
                    split_point = insert_at + np.random.uniform(0.2, 0.8)
                    if split_point < original_end - 0.3:
                        # Resize original block
                        original_size = block["size"]
                        block["size"] = split_point - block["start"]
                        
                        # Insert free block
                        free_size = min(np.random.uniform(0.2, 0.8), original_end - split_point)
                        
                        # Insert new free block
                        blocks.append({
                            "start": split_point,
                            "size": free_size,
                            "status": "Free"
                        })
                        
                        # Add remainder block if space left
                        if split_point + free_size < original_end:
                            blocks.append({
                                "start": split_point + free_size,
                                "size": original_end - (split_point + free_size),
                                "status": block["status"]  # Same type as original
                            })
                break
    
    # Sort blocks by start position
    blocks.sort(key=lambda x: x["start"])
    
    # Calculate actual fragmentation metrics
    free_blocks = [block for block in blocks if block["status"] == "Free"]
    num_free_blocks = len(free_blocks)
    total_free = sum(block["size"] for block in free_blocks)
    largest_free = max(block["size"] for block in free_blocks) if free_blocks else 0
    computed_fragmentation = (1 - largest_free / total_free) * 100 if total_free > 0 else 0
    
    # Create DataFrame for visualization
    memory_blocks = pd.DataFrame(blocks)
    memory_blocks["end"] = memory_blocks["start"] + memory_blocks["size"]
    memory_blocks["y"] = 1
    
    # Different visualization options
    if visualization_type == "Block Map":
        # Create a more reliable memory block visualization using rectangles instead of timeline
        fig = go.Figure()
        
        # Add rectangles for each block
        for i, block in enumerate(blocks):
            fig.add_shape(
                type="rect",
                x0=block["start"],
                x1=block["start"] + block["size"],
                y0=0,
                y1=1,
                fillcolor=allocation_colors[block["status"]],
                line=dict(width=1, color="white"),
                layer="below"
            )
            
            # Add hover text for larger blocks
            if block["size"] > 2:
                fig.add_trace(go.Scatter(
                    x=[(block["start"] + block["start"] + block["size"])/2],
                    y=[0.5],
                    text=[block["status"]],
                    mode="text",
                    showlegend=False,
                    hoverinfo="text",
                    hovertext=f"{block['status']}: {block['size']:.1f}%"
                ))
        
        # Add legend manually since shapes don't show up in legend
        for status, color in allocation_colors.items():
            fig.add_trace(go.Scatter(
                x=[None], y=[None],
                mode="markers",
                marker=dict(size=10, color=color),
                name=status,
                showlegend=True
            ))
            
        # Update layout for better appearance
        fig.update_layout(
            title="Memory Block Allocation Map",
            xaxis_title="Memory Address Space (%)",
            xaxis=dict(range=[0, 100]),
            yaxis=dict(visible=False),
            height=250,
            margin=dict(l=0, r=0, t=40, b=0),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Treemap visualization
        # Format data for treemap
        treemap_data = []
        for block in blocks:
            end_pos = block["start"] + block["size"]
            treemap_data.append({
                "type": block["status"],
                "size": block["size"],
                "address": f"{block['start']:.1f} - {end_pos:.1f}%"
            })
        
        treemap_df = pd.DataFrame(treemap_data)
        
        # Group by type for treemap representation
        grouped_treemap = treemap_df.groupby("type").agg({
            "size": "sum"
        }).reset_index()
        
        # Create treemap with better formatting
        fig = px.treemap(
            grouped_treemap,
            path=["type"],
            values="size",
            color="type",
            color_discrete_map=allocation_colors,
            title="Memory Allocation by Type"
        )
        
        fig.update_traces(
            textinfo="label+value+percent root",
            hovertemplate="<b>%{label}</b><br>Size: %{value:.1f}%<br>Percentage: %{percentRoot:.1%}<extra></extra>"
        )
        
        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show blocks in tabular form too
        with st.expander("View Detailed Block Information", expanded=False):
            # Format block data for display
            block_data_display = memory_blocks[["start", "end", "size", "status"]].copy()
            block_data_display.columns = ["Start (%)", "End (%)", "Size (%)", "Allocation Type"]
            
            # Round for better display
            block_data_display["Start (%)"] = block_data_display["Start (%)"].round(1)
            block_data_display["End (%)"] = block_data_display["End (%)"].round(1)
            block_data_display["Size (%)"] = block_data_display["Size (%)"].round(1)
            
            # Style dataframe - highlight free blocks and very small blocks
            def color_status(val):
                if val == "Free":
                    return 'background-color: rgba(76, 175, 80, 0.1); color: #2E7D32;'
                return ''
            
            def color_small_blocks(val):
                if val < 1.0:
                    return 'background-color: rgba(244, 67, 54, 0.1); color: #C62828;'
                return ''
            
            styled_blocks = block_data_display.copy().style.map(
                color_status, subset=["Allocation Type"]
            ).map(
                color_small_blocks, subset=["Size (%)"]
            )
            
            st.dataframe(styled_blocks, use_container_width=True)
    
    # Fragmentation metrics with improved visualization
    st.subheader("Memory Fragmentation Metrics")
    
    # Display metrics in 3-column layout with explanations
    metrics_cols = st.columns(3)
    
    with metrics_cols[0]:
        # Create a gauge for fragmentation
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=current_frag,
            domain={'x': [0, 1], 'y': [0, 1]},
            gauge={
                'axis': {'range': [0, 50], 'tickwidth': 1},
                'bar': {'color': "#2196F3"},
                'bgcolor': "white",
                'steps': [
                    {'range': [0, 15], 'color': 'rgba(76, 175, 80, 0.3)'},
                    {'range': [15, 30], 'color': 'rgba(255, 152, 0, 0.3)'},
                    {'range': [30, 50], 'color': 'rgba(244, 67, 54, 0.3)'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 30
                }
            },
            title={'text': "Current Fragmentation"}
        ))
        
        fig.update_layout(height=200, margin=dict(l=20, r=20, t=30, b=20))
        st.plotly_chart(fig, use_container_width=True)
        
        # Fragmentation severity
        severity = "Low" if current_frag < 15 else ("High" if current_frag >= 30 else "Moderate")
        severity_color = "#4CAF50" if severity == "Low" else ("#F44336" if severity == "High" else "#FF9800")
        
        st.markdown(f"""
        <div style="text-align: center; margin-top: -15px;">
            <p style="color: {severity_color}; font-weight: bold; font-size: 1.1em;">{severity} Severity</p>
        </div>
        """, unsafe_allow_html=True)
    
    with metrics_cols[1]:
        # Memory blocks visualization
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric(
                label="Free Memory Blocks",
                value=f"{num_free_blocks}",
                delta=None,
                help="Number of non-contiguous free blocks in memory"
            )
            
            st.metric(
                label="Free Memory",
                value=f"{total_free:.1f}%",
                delta=None,
                help="Total percentage of free memory available"
            )
        
        with col2:
            st.metric(
                label="Largest Contiguous Block",
                value=f"{largest_free:.1f}%",
                delta=None,
                help="Size of the largest contiguous free memory block"
            )
            
            # Calculate a usability score based on fragmentation metrics
            usability = 100 - min(100, (num_free_blocks * 2) + (computed_fragmentation * 0.8))
            usability = max(0, usability)
            
            st.metric(
                label="Memory Usability",
                value=f"{usability:.0f}/100",
                delta=None,
                help="Overall usability score based on fragmentation level and block distribution"
            )
    
    with metrics_cols[2]:
        # Impact assessment and forecasting
        
        # Calculate impact on performance
        if current_frag < 10:
            perf_impact = "Minimal"
            perf_impact_pct = "< 1%"
            perf_color = "#4CAF50"
        elif current_frag < 20:
            perf_impact = "Slight"
            perf_impact_pct = "1-3%"
            perf_color = "#8BC34A"
        elif current_frag < 30:
            perf_impact = "Moderate"
            perf_impact_pct = "3-8%"
            perf_color = "#FF9800"
        else:
            perf_impact = "Significant"
            perf_impact_pct = "> 8%"
            perf_color = "#F44336"
        
        st.markdown(f"""
        <div style="border: 1px solid #E0E0E0; border-radius: 5px; padding: 12px; margin-bottom: 15px;">
            <h4 style="margin-top: 0; margin-bottom: 10px;">Performance Impact</h4>
            <div style="display: flex; align-items: center; margin-bottom: 10px;">
                <span style="color: {perf_color}; font-weight: bold; font-size: 1.2em; margin-right: 10px;">{perf_impact}</span>
                <span style="color: #666;">({perf_impact_pct} degradation)</span>
            </div>
            <p style="margin-bottom: 0; font-size: 0.9em; color: #555;">Based on memory allocation pattern analysis and failed allocation rate.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Days until critical calculation
        if current_frag < 30:
            # Calculate trend from last 7 days or all available data
            data_window = min(7, len(memory_fragmentation))
            if data_window > 1:
                start_frag = memory_fragmentation[-data_window]
                daily_increase = (current_frag - start_frag) / data_window
                
                if daily_increase > 0:
                    days_to_critical = int((30 - current_frag) / daily_increase)
                    if days_to_critical < 30:
                        st.markdown(f"""
                        <div style="background-color: rgba(255, 152, 0, 0.1); border-radius: 5px; padding: 12px;">
                            <h4 style="margin-top: 0; margin-bottom: 10px; color: #E65100;">Critical Level Forecast</h4>
                            <p style="margin-bottom: 0;">At current rate, memory fragmentation may reach critical levels in <strong>{days_to_critical} days</strong>.</p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div style="background-color: rgba(76, 175, 80, 0.1); border-radius: 5px; padding: 12px;">
                            <h4 style="margin-top: 0; margin-bottom: 10px; color: #2E7D32;">Stable Forecast</h4>
                            <p style="margin-bottom: 0;">At current rate, memory fragmentation will remain below critical levels for at least 30 days.</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="background-color: rgba(76, 175, 80, 0.1); border-radius: 5px; padding: 12px;">
                        <h4 style="margin-top: 0; margin-bottom: 10px; color: #2E7D32;">Improving Trend</h4>
                        <p style="margin-bottom: 0;">Fragmentation is currently decreasing or stable. Continue regular monitoring.</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background-color: rgba(244, 67, 54, 0.1); border-radius: 5px; padding: 12px;">
                <h4 style="margin-top: 0; margin-bottom: 10px; color: #C62828;">Critical Level Alert</h4>
                <p style="margin-bottom: 0;">Memory fragmentation is already at critical levels. Immediate defragmentation recommended.</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Recommendation and action section
    st.subheader("Memory Management Recommendations")
    
    # Generate specific recommendations based on fragmentation
    if current_frag >= 30:
        st.markdown("""
        <div style="border-left: 4px solid #F44336; padding: 15px; background-color: rgba(244, 67, 54, 0.05); margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #C62828;">Critical: Immediate Action Required</h4>
            <ul style="margin-bottom: 0;">
                <li><strong>Schedule memory defragmentation immediately</strong> to prevent performance degradation</li>
                <li>Consider restarting GPU processes to release fragmented memory</li>
                <li>Analyze workload patterns to identify causes of fragmentation</li>
                <li>Monitor allocation failures and performance metrics closely</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    elif current_frag >= 15:
        st.markdown("""
        <div style="border-left: 4px solid #FF9800; padding: 15px; background-color: rgba(255, 152, 0, 0.05); margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #E65100;">Warning: Proactive Maintenance Recommended</h4>
            <ul style="margin-bottom: 0;">
                <li>Schedule memory defragmentation within the next week</li>
                <li>Review memory allocation patterns in workloads</li>
                <li>Consider implementing automated memory compaction for long-running tasks</li>
                <li>Monitor for increased allocation failures</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="border-left: 4px solid #4CAF50; padding: 15px; background-color: rgba(76, 175, 80, 0.05); margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #2E7D32;">Good: Healthy Memory State</h4>
            <ul style="margin-bottom: 0;">
                <li>Memory fragmentation is at acceptable levels</li>
                <li>Continue regular monitoring and scheduled maintenance</li>
                <li>No immediate action required</li>
                <li>Consider implementing a regular defragmentation schedule (e.g., weekly) for preventive maintenance</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # Action buttons (simulated)
    action_cols = st.columns(3)
    
    with action_cols[0]:
        defrag_button = st.button("Run Defragmentation", use_container_width=True, type="primary")
        if defrag_button:
            st.success("✅ Defragmentation process initiated. This may take several minutes.")
    
    with action_cols[1]:
        analyze_button = st.button("Analyze Allocation Patterns", use_container_width=True)
        if analyze_button:
            st.info("📊 Analysis started. Results will be available in the detailed report.")
    
    with action_cols[2]:
        report_button = st.button("Generate Detailed Report", use_container_width=True)
        if report_button:
            st.info("📄 Generating comprehensive memory fragmentation report...")
            
            # Simulate report generation
            with st.spinner("Processing data..."):
                time.sleep(0.5)  # Simulate processing delay
            
            st.download_button(
                label="Download Memory Analysis Report",
                data="This would be a PDF or HTML report in a real implementation",
                file_name=f"{frag_gpu}_memory_analysis_{datetime.now().strftime('%Y%m%d')}.pdf",
                mime="application/pdf"
            )

with tab3:
    st.header("Predictive Maintenance")
    
    # Introduction and explanation
    st.markdown("""
    <div style="background-color: rgba(33, 150, 243, 0.1); padding: 15px; border-radius: 5px; margin-bottom: 20px;">
        <h4 style="margin-top: 0; color: #0D47A1;">About Predictive Maintenance</h4>
        <p style="margin-bottom: 0;">
            Our predictive models analyze historical GPU health data to forecast future behavior, detect potential failures before they occur,
            and provide targeted maintenance recommendations to extend hardware lifespan and prevent costly downtime.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Control and configuration section
    control_cols = st.columns([2, 1, 1])
    
    with control_cols[0]:
        # GPU selection for prediction
        pred_gpu = st.selectbox("Select GPU for Prediction", options=gpu_ids, key="pred_gpu")
    
    with control_cols[1]:
        prediction_range = st.selectbox(
            "Forecast Horizon",
            options=["30 Days", "60 Days", "90 Days"],
            index=0
        )
    
    with control_cols[2]:
        model_type = st.selectbox(
            "Model Type",
            options=["Standard", "Conservative", "Aggressive"],
            index=0,
            help="Standard: balanced prediction, Conservative: emphasizes stability, Aggressive: emphasizes early warning"
        )
    
    # Convert prediction range to days
    if prediction_range == "30 Days":
        prediction_days = 30
    elif prediction_range == "60 Days":
        prediction_days = 60
    else:  # 90 Days
        prediction_days = 90
    
    # Apply model confidence factor based on selection
    if model_type == "Conservative":
        confidence_factor = 0.7  # Less aggressive degradation prediction
    elif model_type == "Aggressive":
        confidence_factor = 1.3  # More aggressive degradation prediction
    else:  # Standard
        confidence_factor = 1.0  # Balanced prediction
    
    # Tabs for different predictive analytics
    prediction_tabs = st.tabs(["Health Score Forecast", "Failure Analysis", "Maintenance Planning"])
    
    with prediction_tabs[0]:
        st.subheader("GPU Health Score Forecast")
        
        # Get historical data
        pred_data = get_gpu_health_data(pred_gpu)
        
        # Prepare data for prediction with enhanced modeling
        X = np.array(range(len(pred_data))).reshape(-1, 1)
        y = pred_data["health_score"].values
        
        # Normalize data
        scaler_X = StandardScaler()
        scaler_y = StandardScaler()
        
        X_scaled = scaler_X.fit_transform(X)
        y_scaled = scaler_y.fit_transform(y.reshape(-1, 1)).flatten()
        
        # Train simple linear model
        model = LinearRegression()
        model.fit(X_scaled, y_scaled)
        
        # Predict future values
        future_X = np.array(range(len(pred_data), len(pred_data) + prediction_days)).reshape(-1, 1)
        future_X_scaled = scaler_X.transform(future_X)
        future_y_scaled = model.predict(future_X_scaled)
        
        # Apply confidence factor to predictions (affects slope of prediction)
        if confidence_factor != 1.0:
            # Get the linear trend direction
            trend_direction = np.sign(future_y_scaled[-1] - future_y_scaled[0])
            
            # Adjust prediction based on trend and confidence factor
            adjustment = np.linspace(0, (confidence_factor - 1.0) * trend_direction * 0.5, len(future_y_scaled))
            future_y_scaled = future_y_scaled - adjustment
        
        # Transform back to original scale
        future_y = scaler_y.inverse_transform(future_y_scaled.reshape(-1, 1)).flatten()
        
        # Add some realistic noise to predictions
        noise_level = 2.0  # Standard deviation of noise
        noise = np.random.normal(0, noise_level, len(future_y))
        noise_cumulative = np.cumsum(noise) * 0.3  # Cumulative to make it smoother and scaled down
        future_y = future_y + noise_cumulative
        
        # Clip predicted values to valid range
        future_y = np.clip(future_y, 0, 100)
        
        # Generate prediction intervals
        prediction_std = noise_level * np.sqrt(np.arange(len(future_y)) + 1)  # Increasing uncertainty with time
        upper_bound = np.clip(future_y + prediction_std * 1.96, 0, 100)  # 95% confidence interval
        lower_bound = np.clip(future_y - prediction_std * 1.96, 0, 100)  # 95% confidence interval
        
        # Future dates
        current_date = pred_data["timestamp"].iloc[-1]
        future_dates = [current_date + timedelta(days=i+1) for i in range(prediction_days)]
        
        # Create enhanced visualization
        fig = go.Figure()
        
        # Add confidence interval
        fig.add_trace(go.Scatter(
            x=future_dates + future_dates[::-1],
            y=list(upper_bound) + list(lower_bound)[::-1],
            fill='toself',
            fillcolor='rgba(33, 150, 243, 0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name="95% Confidence Interval"
        ))
        
        # Historical data
        fig.add_trace(go.Scatter(
            x=pred_data["timestamp"],
            y=pred_data["health_score"],
            mode="lines",
            name="Historical Health Score",
            line=dict(color="#1976D2", width=3)
        ))
        
        # Prediction data with better styling
        fig.add_trace(go.Scatter(
            x=future_dates,
            y=future_y,
            mode="lines",
            name="Predicted Health Score",
            line=dict(color="#F44336", width=3, dash="dash")
        ))
        
        # Add warning and critical thresholds
        fig.add_shape(
            type="line",
            x0=pred_data["timestamp"].min(),
            x1=future_dates[-1],
            y0=50,
            y1=50,
            line=dict(color="#FF9800", width=2, dash="dash")
        )
        
        fig.add_annotation(
            x=pred_data["timestamp"].min(),
            y=50,
            text="Warning Threshold",
            showarrow=False,
            xshift=70,
            yshift=10,
            font=dict(size=12, color="#FF9800")
        )
        
        fig.add_shape(
            type="line",
            x0=pred_data["timestamp"].min(),
            x1=future_dates[-1],
            y0=25,
            y1=25,
            line=dict(color="#F44336", width=2, dash="dash")
        )
        
        fig.add_annotation(
            x=pred_data["timestamp"].min(),
            y=25,
            text="Critical Threshold",
            showarrow=False,
            xshift=70,
            yshift=10,
            font=dict(size=12, color="#F44336")
        )
        
        # Add vertical line at current date
        fig.add_shape(
            type="line", 
            x0=current_date, 
            y0=0, 
            x1=current_date, 
            y1=100, 
            line=dict(color="#4CAF50", width=2, dash="solid")
        )
        
        # Add annotation for today
        fig.add_annotation(
            x=current_date,
            y=95,
            text="Today",
            showarrow=True,
            arrowhead=1,
            ax=0,
            ay=-40,
            font=dict(color="#4CAF50")
        )
        
        # Detect threshold crossings and mark them
        warning_threshold = 50
        critical_threshold = 25
        
        warning_cross_idx = None
        for i, score in enumerate(future_y):
            if score < warning_threshold:
                warning_cross_idx = i
                break
                
        if warning_cross_idx is not None:
            warning_date = future_dates[warning_cross_idx]
            fig.add_shape(
                type="line", 
                x0=warning_date, 
                y0=0, 
                x1=warning_date, 
                y1=100, 
                line=dict(color="#FF9800", width=2, dash="dot")
            )
            
            fig.add_annotation(
                x=warning_date,
                y=85,
                text=f"Warning Level<br>{warning_date.strftime('%Y-%m-%d')}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40,
                font=dict(color="#FF9800")
            )
        
        critical_cross_idx = None
        for i, score in enumerate(future_y):
            if score < critical_threshold:
                critical_cross_idx = i
                break
                
        if critical_cross_idx is not None:
            critical_date = future_dates[critical_cross_idx]
            fig.add_shape(
                type="line", 
                x0=critical_date, 
                y0=0, 
                x1=critical_date, 
                y1=100, 
                line=dict(color="#F44336", width=2, dash="dot")
            )
            
            fig.add_annotation(
                x=critical_date,
                y=75,
                text=f"Critical Level<br>{critical_date.strftime('%Y-%m-%d')}",
                showarrow=True,
                arrowhead=1,
                ax=0,
                ay=-40,
                font=dict(color="#F44336")
            )
        
        # Update layout with better styling
        fig.update_layout(
            title=f"{pred_gpu} Health Score Forecast ({prediction_range})",
            xaxis_title="Date",
            yaxis=dict(
                title="Health Score",
                range=[0, 100],
                tickmode="linear",
                tick0=0,
                dtick=25
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            height=450,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Health forecast analysis
        analysis_cols = st.columns(3)
        
        with analysis_cols[0]:
            # Final health score
            final_score = future_y[-1]
            score_change = final_score - pred_data["health_score"].iloc[-1]
            
            score_color = "#4CAF50" if final_score >= 75 else ("#FF9800" if final_score >= 50 else "#F44336")
            
            st.markdown(
                f"""
                <div style="border: 1px solid {score_color}30; border-radius: 5px; padding: 15px; text-align: center;">
                    <h4 style="margin-top: 0; margin-bottom: 5px; color: {score_color};">Projected Health Score</h4>
                    <div style="font-size: 2rem; font-weight: bold; color: {score_color};">{final_score:.1f}</div>
                    <div style="color: {'#4CAF50' if score_change >= 0 else '#F44336'};">
                        {'+' if score_change >= 0 else ''}{score_change:.1f} points
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with analysis_cols[1]:
            # Time to threshold - compute string representations for display
            days_to_warning_text = "Not within forecast"
            if warning_cross_idx is not None:
                days_to_warning = warning_cross_idx + 1
                days_to_warning_text = f"In {days_to_warning} days"
            
            days_to_critical_text = "Not within forecast"
            if critical_cross_idx is not None:
                days_to_critical = critical_cross_idx + 1
                days_to_critical_text = f"In {days_to_critical} days"
            
            st.markdown(
                f"""
                <div style="border: 1px solid #E0E0E0; border-radius: 5px; padding: 15px;">
                    <h4 style="margin-top: 0; margin-bottom: 10px;">Threshold Timeline</h4>
                    <table style="width: 100%;">
                        <tr>
                            <td><b>Warning Level:</b></td>
                            <td style="text-align: right; color: {'#FF9800' if warning_cross_idx is not None else '#4CAF50'};">
                                {days_to_warning_text}
                            </td>
                        </tr>
                        <tr>
                            <td><b>Critical Level:</b></td>
                            <td style="text-align: right; color: {'#F44336' if critical_cross_idx is not None else '#4CAF50'};">
                                {days_to_critical_text}
                            </td>
                        </tr>
                    </table>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with analysis_cols[2]:
            # Health trend analysis
            health_trend_slope = (future_y[-1] - future_y[0]) / len(future_y)
            
            if health_trend_slope > 0.05:
                trend_desc = "Improving"
                trend_color = "#4CAF50"
                confidence = "High" if abs(health_trend_slope) > 0.2 else "Medium"
            elif health_trend_slope < -0.05:
                trend_desc = "Declining"
                trend_color = "#F44336"
                confidence = "High" if abs(health_trend_slope) > 0.2 else "Medium"
            else:
                trend_desc = "Stable"
                trend_color = "#2196F3"
                confidence = "Medium"
            
            st.markdown(
                f"""
                <div style="border: 1px solid #E0E0E0; border-radius: 5px; padding: 15px;">
                    <h4 style="margin-top: 0; margin-bottom: 10px;">Trend Analysis</h4>
                    <div style="margin-bottom: 10px;">
                        <span style="font-weight: bold; color: {trend_color};">{trend_desc}</span>
                        <span style="color: #666; margin-left: 10px; font-size: 0.9em;">(Confidence: {confidence})</span>
                    </div>
                    <p style="margin-bottom: 0; font-size: 0.9em;">
                        {f"Health score changing by {abs(health_trend_slope):.2f} points/day" if abs(health_trend_slope) > 0.01 else "Health score relatively stable"}
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        # Maintenance advisory
        if warning_cross_idx is not None:
            # days_to_warning is already an integer here
            days_to_warning = warning_cross_idx + 1
            
            if days_to_warning <= 7:
                st.warning(
                    f"⚠️ **Urgent Maintenance Advisory**: Health score predicted to drop below warning threshold in {days_to_warning} days. "
                    f"Schedule maintenance immediately to prevent performance degradation."
                )
            elif days_to_warning <= 14:
                st.warning(
                    f"⚠️ **Maintenance Advisory**: Health score predicted to drop below warning threshold in {days_to_warning} days. "
                    f"Plan maintenance within the next week."
                )
            else:
                st.info(
                    f"ℹ️ **Maintenance Notice**: Health score predicted to drop below warning threshold in {days_to_warning} days. "
                    f"Consider scheduling preventive maintenance."
                )
        else:
            st.success(
                f"✅ **Healthy Forecast**: GPU health score predicted to remain above warning threshold for the entire {prediction_range} forecast period."
            )
    
    with prediction_tabs[1]:
        st.subheader("Failure Probability Analysis")
        
        # Generate component-specific failure probabilities
        components = [
            {"name": "Memory Subsystem", "current_health": 88, "failure_risk": "Low"},
            {"name": "Core Clock Stability", "current_health": 92, "failure_risk": "Low"},
            {"name": "Power Delivery", "current_health": 76, "failure_risk": "Medium"},
            {"name": "Cooling System", "current_health": 65, "failure_risk": "Medium"},
            {"name": "PCI-E Interface", "current_health": 95, "failure_risk": "Low"},
            {"name": "CUDA Cores", "current_health": 91, "failure_risk": "Low"},
            {"name": "Tensor Cores", "current_health": 85, "failure_risk": "Low"}
        ]
        
        # Adjust component health based on the model's confidence factor
        for comp in components:
            if comp["current_health"] < 80 and confidence_factor > 1.0:
                # More aggressive model means lower health scores for at-risk components
                comp["current_health"] = max(10, comp["current_health"] - (confidence_factor - 1.0) * 15)
            elif comp["current_health"] < 80 and confidence_factor < 1.0:
                # More conservative model means higher health scores for at-risk components
                comp["current_health"] = min(90, comp["current_health"] + (1.0 - confidence_factor) * 15)
        
        # Recalculate failure risk based on adjusted health
        for comp in components:
            if comp["current_health"] >= 85:
                comp["failure_risk"] = "Low"
            elif comp["current_health"] >= 65:
                comp["failure_risk"] = "Medium"
            else:
                comp["failure_risk"] = "High"
        
        # Create component health dataframe
        component_df = pd.DataFrame(components)
        
        # Calculate overall failure probability over time
        # Base failure probability on component health, weighted by importance
        component_weights = {
            "Memory Subsystem": 0.25,
            "Core Clock Stability": 0.15,
            "Power Delivery": 0.20,
            "Cooling System": 0.15,
            "PCI-E Interface": 0.05,
            "CUDA Cores": 0.10,
            "Tensor Cores": 0.10
        }
        
        # Calculate initial failure probability
        initial_failure_prob = 0
        for comp in components:
            comp_failure_prob = max(0, (100 - comp["current_health"]) / 100)
            weighted_prob = comp_failure_prob * component_weights[comp["name"]]
            initial_failure_prob += weighted_prob
        
        # Scale to percentage and apply confidence factor
        initial_failure_prob = min(0.9, initial_failure_prob) * 100 * confidence_factor
        
        # Project future failure probability (increases over time)
        failure_prob = [initial_failure_prob]
        for i in range(1, prediction_days):
            # Failure probability increases more quickly as time passes
            # Add some random variations for realism
            daily_increase = 0.1 + 0.01 * i + np.random.normal(0, 0.03)
            failure_prob.append(min(95, failure_prob[-1] + daily_increase))
        
        # Create future dates array for plotting
        future_dates = [current_date + timedelta(days=i+1) for i in range(prediction_days)]
        
        # Calculate failure probability for each component over time
        component_probs = {}
        for comp in components:
            base_prob = max(0, (100 - comp["current_health"]) / 100)
            comp_probs = []
            for i in range(prediction_days):
                # Components degrade at different rates based on their current health
                daily_factor = 1.0 + (0.005 * i) * (1.0 - comp["current_health"] / 100)
                comp_probs.append(min(0.95, base_prob * daily_factor) * 100)
            component_probs[comp["name"]] = comp_probs
        
        # Visualization controls
        failure_analysis_tabs = st.tabs(["Overall Failure Risk", "Component Comparison", "Risk Assessment"])
        
        with failure_analysis_tabs[0]:
            # Enhanced overall failure probability visualization
            fig = go.Figure()
            
            # Add colored risk zones
            # High risk zone
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=[60] * len(future_dates),
                fill=None,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=[100] * len(future_dates),
                fill='tonexty',
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(244, 67, 54, 0.1)',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Medium risk zone
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=[30] * len(future_dates),
                fill=None,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=[60] * len(future_dates),
                fill='tonexty',
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(255, 152, 0, 0.1)',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Low risk zone
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=[0] * len(future_dates),
                fill=None,
                mode='lines',
                line=dict(width=0),
                showlegend=False,
                hoverinfo='skip'
            ))
            
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=[30] * len(future_dates),
                fill='tonexty',
                mode='lines',
                line=dict(width=0),
                fillcolor='rgba(76, 175, 80, 0.1)',
                showlegend=False,
                hoverinfo='skip'
            ))
            
            # Add main failure probability line
            fig.add_trace(go.Scatter(
                x=future_dates,
                y=failure_prob,
                mode="lines+markers",
                name="Failure Probability",
                line=dict(color="#F44336", width=3),
                marker=dict(size=6),
                hovertemplate="<b>%{x|%d %b}</b><br>Probability: %{y:.1f}%<extra></extra>"
            ))
            
            # Add threshold lines with better styling
            fig.add_shape(
                type="line",
                x0=future_dates[0],
                x1=future_dates[-1],
                y0=30,
                y1=30,
                line=dict(color="#FF9800", width=2, dash="dash")
            )
            
            fig.add_shape(
                type="line",
                x0=future_dates[0],
                x1=future_dates[-1],
                y0=60,
                y1=60,
                line=dict(color="#F44336", width=2, dash="dash")
            )
            
            # Add annotations for thresholds
            fig.add_annotation(
                x=future_dates[0],
                y=30,
                text="Medium Risk Threshold",
                showarrow=False,
                xshift=85,
                yshift=10,
                font=dict(size=12, color="#FF9800")
            )
            
            fig.add_annotation(
                x=future_dates[0],
                y=60,
                text="High Risk Threshold",
                showarrow=False,
                xshift=75,
                yshift=10,
                font=dict(size=12, color="#F44336")
            )
            
            # Detect threshold crossings and mark them
            medium_risk_idx = None
            for i, prob in enumerate(failure_prob):
                if prob > 30:
                    medium_risk_idx = i
                    break
                    
            if medium_risk_idx is not None:
                medium_risk_date = future_dates[medium_risk_idx]
                fig.add_shape(
                    type="line", 
                    x0=medium_risk_date, 
                    y0=0, 
                    x1=medium_risk_date, 
                    y1=100, 
                    line=dict(color="#FF9800", width=2, dash="dot")
                )
                
                fig.add_annotation(
                    x=medium_risk_date,
                    y=40,
                    text=f"Medium Risk<br>{medium_risk_date.strftime('%Y-%m-%d')}",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=-20,
                    font=dict(color="#FF9800")
                )
            
            high_risk_idx = None
            for i, prob in enumerate(failure_prob):
                if prob > 60:
                    high_risk_idx = i
                    break
                    
            if high_risk_idx is not None:
                high_risk_date = future_dates[high_risk_idx]
                fig.add_shape(
                    type="line", 
                    x0=high_risk_date, 
                    y0=0, 
                    x1=high_risk_date, 
                    y1=100, 
                    line=dict(color="#F44336", width=2, dash="dot")
                )
                
                fig.add_annotation(
                    x=high_risk_date,
                    y=70,
                    text=f"High Risk<br>{high_risk_date.strftime('%Y-%m-%d')}",
                    showarrow=True,
                    arrowhead=1,
                    ax=0,
                    ay=-20,
                    font=dict(color="#F44336")
                )
            
            # Update layout
            fig.update_layout(
                title=f"{pred_gpu} Failure Probability Forecast",
                xaxis_title="Date",
                yaxis=dict(
                    title="Failure Probability (%)",
                    range=[0, 100],
                    tickmode="linear",
                    tick0=0,
                    dtick=20
                ),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                ),
                margin=dict(l=0, r=0, t=40, b=0),
                height=400,
                hovermode="x unified"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk level and projection
            risk_cols = st.columns(3)
            
            with risk_cols[0]:
                current_risk = failure_prob[0]
                final_risk = failure_prob[-1]
                
                if current_risk < 10:
                    risk_level = "Minimal"
                    risk_color = "#4CAF50"
                elif current_risk < 30:
                    risk_level = "Low"
                    risk_color = "#8BC34A"
                elif current_risk < 60:
                    risk_level = "Medium"
                    risk_color = "#FF9800"
                else:
                    risk_level = "High"
                    risk_color = "#F44336"
                
                st.markdown(
                    f"""
                    <div style="border: 1px solid {risk_color}30; border-radius: 5px; padding: 15px; text-align: center;">
                        <h4 style="margin-top: 0; margin-bottom: 5px; color: {risk_color};">Current Risk Level</h4>
                        <div style="font-size: 1.8rem; font-weight: bold; color: {risk_color};">{risk_level}</div>
                        <div style="color: #666;">{current_risk:.1f}% probability</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with risk_cols[1]:
                # Time to risk thresholds
                days_to_medium = "N/A"
                if medium_risk_idx is not None:
                    days_to_medium = medium_risk_idx + 1
                
                days_to_high = "N/A"
                if high_risk_idx is not None:
                    days_to_high = high_risk_idx + 1
                
                st.markdown(
                    f"""
                    <div style="border: 1px solid #E0E0E0; border-radius: 5px; padding: 15px;">
                        <h4 style="margin-top: 0; margin-bottom: 10px;">Risk Timeline</h4>
                        <table style="width: 100%;">
                            <tr>
                                <td><b>Medium Risk:</b></td>
                                <td style="text-align: right; color: {'#FF9800' if days_to_medium != 'N/A' else '#4CAF50'};">
                                    {f"In {days_to_medium} days" if days_to_medium != 'N/A' else "Not within forecast"}
                                </td>
                            </tr>
                            <tr>
                                <td><b>High Risk:</b></td>
                                <td style="text-align: right; color: {'#F44336' if days_to_high != 'N/A' else '#4CAF50'};">
                                    {f"In {days_to_high} days" if days_to_high != 'N/A' else "Not within forecast"}
                                </td>
                            </tr>
                            <tr>
                                <td><b>Final Risk Level:</b></td>
                                <td style="text-align: right;">
                                    {final_risk:.1f}%
                                </td>
                            </tr>
                        </table>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with risk_cols[2]:
                # Primary risk factors
                # Sort components by risk level (convert to numeric for sorting)
                risk_mapping = {"High": 3, "Medium": 2, "Low": 1}
                component_df["risk_numeric"] = component_df["failure_risk"].map(risk_mapping)
                top_risk_components = component_df.sort_values(by=["risk_numeric", "current_health"], ascending=[False, True]).head(3)
                
                st.markdown(
                    f"""
                    <div style="border: 1px solid #E0E0E0; border-radius: 5px; padding: 15px;">
                        <h4 style="margin-top: 0; margin-bottom: 10px;">Primary Risk Factors</h4>
                        <ul style="margin-bottom: 0; padding-left: 20px;">
                    """,
                    unsafe_allow_html=True
                )
                
                for _, comp in top_risk_components.iterrows():
                    risk_color = "#F44336" if comp["failure_risk"] == "High" else ("#FF9800" if comp["failure_risk"] == "Medium" else "#4CAF50")
                    st.markdown(
                        f"""
                        <li style="margin-bottom: 5px;">
                            <span style="font-weight: bold;">{comp["name"]}</span>
                            <span style="color: {risk_color}; margin-left: 5px;">({comp["failure_risk"]} Risk)</span>
                        </li>
                        """,
                        unsafe_allow_html=True
                    )
                
                st.markdown("</ul></div>", unsafe_allow_html=True)
            
            # MTBF (Mean Time Between Failure) projection
            if current_risk > 5:
                # Calculate MTBF in days based on failure probability
                # Higher probability = lower MTBF
                base_mtbf = 730  # ~2 years for a healthy GPU
                mtbf_days = int(base_mtbf * (1 - (current_risk / 100)) * (1 - (final_risk / 200)))
                mtbf_lower = int(mtbf_days * 0.8)  # Lower bound
                mtbf_upper = int(mtbf_days * 1.2)  # Upper bound
                
                st.markdown(
                    f"""
                    <div style="background-color: rgba(0, 0, 0, 0.05); padding: 15px; border-radius: 5px; margin-top: 15px;">
                        <h4 style="margin-top: 0; margin-bottom: 10px;">MTBF Projection</h4>
                        <p>
                            Estimated Mean Time Between Failures: <strong>{mtbf_days} days</strong> 
                            <span style="color: #666;">(range: {mtbf_lower} - {mtbf_upper} days)</span>
                        </p>
                        <p style="font-size: 0.9em; color: #666; margin-bottom: 0;">
                            This projection is based on current failure probability and degradation rate. 
                            Regular maintenance can significantly extend this estimate.
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        with failure_analysis_tabs[1]:
            # Component-level comparison visualization
            st.markdown("#### Component Failure Probability Comparison")
            
            # Create a line chart comparing all components
            fig = go.Figure()
            
            # Add all component probability lines
            for comp_name, probs in component_probs.items():
                # Get current risk level for color
                comp_risk = next((c["failure_risk"] for c in components if c["name"] == comp_name), "Low")
                if comp_risk == "High":
                    line_color = "#F44336"
                elif comp_risk == "Medium":
                    line_color = "#FF9800"
                else:
                    line_color = "#2196F3"
                
                fig.add_trace(go.Scatter(
                    x=future_dates,
                    y=probs,
                    mode="lines",
                    name=comp_name,
                    line=dict(color=line_color, width=2),
                    hovertemplate="<b>%{x|%d %b}</b><br>%{y:.1f}%<extra>" + comp_name + "</extra>"
                ))
            
            # Add threshold lines
            fig.add_shape(
                type="line",
                x0=future_dates[0],
                x1=future_dates[-1],
                y0=30,
                y1=30,
                line=dict(color="#FF9800", width=1, dash="dash")
            )
            
            fig.add_shape(
                type="line",
                x0=future_dates[0],
                x1=future_dates[-1],
                y0=60,
                y1=60,
                line=dict(color="#F44336", width=1, dash="dash")
            )
            
            # Update layout
            fig.update_layout(
                title="Component Failure Probability Over Time",
                xaxis_title="Date",
                yaxis=dict(
                    title="Failure Probability (%)",
                    range=[0, 100]
                ),
                height=350,
                margin=dict(l=0, r=0, t=40, b=0),
                hovermode="x unified",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Component health radar chart
            st.markdown("#### Component Health Assessment")
            
            # Create metrics for all components
            component_cols = st.columns(len(components))
            
            for i, comp in enumerate(components):
                with component_cols[i]:
                    # Set color based on health
                    if comp["current_health"] >= 85:
                        color = "#4CAF50"  # Green
                    elif comp["current_health"] >= 65:
                        color = "#FF9800"  # Orange
                    else:
                        color = "#F44336"  # Red
                    
                    st.markdown(
                        f"""
                        <div style="border: 1px solid {color}30; border-radius: 5px; padding: 10px; text-align: center;">
                            <div style="font-size: 0.8rem; font-weight: bold; margin-bottom: 5px; height: 35px; display: flex; align-items: center; justify-content: center;">
                                {comp["name"]}
                            </div>
                            <div style="font-size: 1.5rem; font-weight: bold; color: {color};">
                                {int(comp["current_health"])}
                            </div>
                            <div style="font-size: 0.8rem; color: {color};">
                                {comp["failure_risk"]} Risk
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Create radar chart of component health
            radar_data = pd.DataFrame({
                'component': [comp["name"] for comp in components],
                'health': [comp["current_health"] for comp in components],
                'risk': [comp["failure_risk"] for comp in components]
            })
            
            # Add the first component again to close the loop
            radar_data = pd.concat([radar_data, radar_data.iloc[[0]]], ignore_index=True)
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=radar_data['health'],
                theta=radar_data['component'],
                fill='toself',
                name='Component Health',
                line_color='#2196F3',
                fillcolor='rgba(33, 150, 243, 0.2)'
            ))
            
            # Add threshold rings
            fig.add_trace(go.Scatterpolar(
                r=[65] * len(radar_data),
                theta=radar_data['component'],
                fill=None,
                mode='lines',
                line=dict(color='#FF9800', width=1, dash='dash'),
                name='Warning Threshold'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[85] * len(radar_data),
                theta=radar_data['component'],
                fill=None,
                mode='lines',
                line=dict(color='#4CAF50', width=1, dash='dash'),
                name='Optimal Threshold'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )
                ),
                showlegend=True,
                height=400,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with failure_analysis_tabs[2]:
            st.markdown("#### Risk Assessment Matrix")
            
            # Create a risk assessment matrix visualization
            # Calculate impact and likelihood for each component
            for comp in components:
                # Impact based on importance of the component
                comp["impact"] = component_weights[comp["name"]] * 10  # Scale to 1-10
                
                # Likelihood based on health score and risk
                likelihood_map = {"Low": 3, "Medium": 6, "High": 9}
                comp["likelihood"] = likelihood_map[comp["failure_risk"]]
                
                # Overall risk score
                comp["risk_score"] = comp["impact"] * comp["likelihood"]
            
            # Create scatter plot for risk matrix
            fig = go.Figure()
            
            # Create colored zones for risk levels
            # High risk zone (red)
            fig.add_shape(
                type="rect",
                x0=6, y0=6,
                x1=10, y1=10,
                fillcolor="rgba(244, 67, 54, 0.2)",
                line=dict(width=0),
            )
            
            # Medium risk zone (orange)
            fig.add_shape(
                type="rect",
                x0=3, y0=6,
                x1=6, y1=10,
                fillcolor="rgba(255, 152, 0, 0.2)",
                line=dict(width=0),
            )
            
            fig.add_shape(
                type="rect",
                x0=6, y0=3,
                x1=10, y1=6,
                fillcolor="rgba(255, 152, 0, 0.2)",
                line=dict(width=0),
            )
            
            # Low risk zone (green)
            fig.add_shape(
                type="rect",
                x0=0, y0=0,
                x1=3, y1=10,
                fillcolor="rgba(76, 175, 80, 0.2)",
                line=dict(width=0),
            )
            
            fig.add_shape(
                type="rect",
                x0=3, y0=0,
                x1=10, y1=3,
                fillcolor="rgba(76, 175, 80, 0.2)",
                line=dict(width=0),
            )
            
            fig.add_shape(
                type="rect",
                x0=3, y0=3,
                x1=6, y1=6,
                fillcolor="rgba(255, 235, 59, 0.2)",  # Yellow for medium-low
                line=dict(width=0),
            )
            
            # Add component points
            for comp in components:
                # Set color based on risk level
                if comp["risk_score"] >= 40:
                    marker_color = "#F44336"  # Red
                elif comp["risk_score"] >= 20:
                    marker_color = "#FF9800"  # Orange
                else:
                    marker_color = "#4CAF50"  # Green
                
                fig.add_trace(go.Scatter(
                    x=[comp["likelihood"]],
                    y=[comp["impact"]],
                    mode="markers+text",
                    name=comp["name"],
                    marker=dict(
                        size=comp["risk_score"] * 0.8,
                        color=marker_color,
                        line=dict(color='black', width=1)
                    ),
                    text=[comp["name"]],
                    textposition="top center",
                    hovertemplate=
                    "<b>%{text}</b><br>" +
                    "Likelihood: %{x}<br>" +
                    "Impact: %{y}<br>" +
                    "Risk Score: " + str(comp["risk_score"]) +
                    "<extra></extra>"
                ))
            
            # Update layout
            fig.update_layout(
                title="Component Risk Assessment Matrix",
                xaxis=dict(
                    title="Likelihood",
                    range=[0, 10],
                    tickmode="array",
                    tickvals=[1, 3, 5, 7, 9],
                    ticktext=["Very Low", "Low", "Medium", "High", "Very High"]
                ),
                yaxis=dict(
                    title="Impact",
                    range=[0, 10],
                    tickmode="array",
                    tickvals=[1, 3, 5, 7, 9],
                    ticktext=["Minimal", "Low", "Medium", "High", "Critical"]
                ),
                height=500,
                showlegend=False,
                hovermode="closest"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Risk assessment explanation
            st.markdown(
                """
                <div style="background-color: rgba(0, 0, 0, 0.05); padding: 15px; border-radius: 5px; margin-top: 10px;">
                    <h4 style="margin-top: 0;">How to Interpret the Risk Matrix</h4>
                    <p style="margin-bottom: 10px;">
                        The risk assessment matrix plots each component based on two factors:
                    </p>
                    <ul>
                        <li><strong>Likelihood:</strong> Probability of component failure based on health metrics</li>
                        <li><strong>Impact:</strong> Severity of consequences if the component fails</li>
                    </ul>
                    <p style="margin-bottom: 0;">
                        Bubble size indicates overall risk score (Likelihood × Impact). Components in the upper-right 
                        quadrant require immediate attention, while those in the lower-left are less critical.
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Highest risk components
            top_risk = sorted(components, key=lambda x: x["risk_score"], reverse=True)[:3]
            
            st.markdown("#### Priority Risk Components")
            
            for comp in top_risk:
                risk_color = "#F44336" if comp["risk_score"] >= 40 else ("#FF9800" if comp["risk_score"] >= 20 else "#4CAF50")
                st.markdown(
                    f"""
                    <div style="border-left: 4px solid {risk_color}; padding: 10px 15px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h5 style="margin: 0; color: {risk_color};">{comp["name"]}</h5>
                            <span style="font-weight: bold; color: {risk_color};">Risk Score: {comp["risk_score"]:.1f}</span>
                        </div>
                        <p style="margin: 5px 0 0 0; font-size: 0.9em;">
                            Current Health: {comp["current_health"]}/100 | 
                            Impact Level: {comp["impact"]:.1f}/10 | 
                            Failure Likelihood: {comp["likelihood"]}/10
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    with prediction_tabs[2]:
        st.subheader("GPU Maintenance Planning")
        
        # Get recommendations based on health predictions
        # Use the results from health score prediction
        
        # Create a maintenance schedule visualization based on predicted health
        st.markdown("#### Maintenance Schedule Projection")
        
        # Create a timeline visualization for maintenance
        today = current_date
        schedule_end = today + timedelta(days=prediction_days)
        
        # Determine maintenance events based on health prediction
        maintenance_events = []
        
        # First, check for urgent maintenance
        if current_score < 50:
            maintenance_events.append({
                "task": "Urgent Maintenance",
                "start": today,
                "end": today + timedelta(days=3),
                "description": "Immediate maintenance required due to current low health score",
                "type": "urgent"
            })
        
        # Check for scheduled maintenance based on warning threshold
        elif warning_cross_idx is not None:
            scheduled_date = future_dates[max(0, warning_cross_idx - 5)]  # Schedule before it reaches warning
            maintenance_events.append({
                "task": "Scheduled Maintenance",
                "start": scheduled_date,
                "end": scheduled_date + timedelta(days=5),
                "description": f"Preventive maintenance before health score drops below warning threshold",
                "type": "scheduled"
            })
        
        # Add routine maintenance regardless
        routine_date = today + timedelta(days=max(30, prediction_days // 2))
        if routine_date < schedule_end:
            # Ensure it doesn't overlap with other maintenance
            overlaps = False
            for event in maintenance_events:
                if event["start"] <= routine_date <= event["end"]:
                    overlaps = True
                    break
            
            if not overlaps:
                maintenance_events.append({
                    "task": "Routine Maintenance",
                    "start": routine_date,
                    "end": routine_date + timedelta(days=2),
                    "description": "Regular maintenance to prevent issues and maintain optimal performance",
                    "type": "routine"
                })
        
        # Add firmware updates (simulated)
        firmware_date = today + timedelta(days=15)
        if firmware_date < schedule_end:
            # Ensure it doesn't overlap with other maintenance
            overlaps = False
            for event in maintenance_events:
                if event["start"] <= firmware_date <= event["end"]:
                    overlaps = True
                    break
            
            if not overlaps:
                maintenance_events.append({
                    "task": "Firmware Update",
                    "start": firmware_date,
                    "end": firmware_date + timedelta(days=1),
                    "description": "Update GPU firmware to latest version for security and stability improvements",
                    "type": "update"
                })
        
        # Create a Gantt chart for maintenance schedule
        if maintenance_events:
            # Create a DataFrame for the Gantt chart
            schedule_df = pd.DataFrame(maintenance_events)
            schedule_df["delta"] = schedule_df["end"] - schedule_df["start"]
            schedule_df["days"] = schedule_df["delta"].dt.days
            
            # Map types to colors
            color_map = {
                "urgent": "#F44336",
                "scheduled": "#FF9800",
                "routine": "#4CAF50",
                "update": "#2196F3"
            }
            
            # Make color column
            schedule_df["color"] = schedule_df["type"].map(color_map)
            
            # Create Gantt chart
            fig = go.Figure()
            
            # Add health score prediction line on secondary y-axis
            # Combine historical and future data
            all_dates = list(pred_data["timestamp"]) + future_dates
            all_scores = list(pred_data["health_score"]) + list(future_y)
            
            fig.add_trace(go.Scatter(
                x=all_dates,
                y=all_scores,
                mode="lines",
                name="Health Score",
                line=dict(color="#9C27B0", width=2),
                opacity=0.7,
                yaxis="y2"
            ))
            
            # Add horizontal warning line
            fig.add_shape(
                type="line",
                x0=today,
                x1=schedule_end,
                y0=50,
                y1=50,
                line=dict(color="#FF9800", width=1, dash="dash"),
                yref="y2"
            )
            
            # Add maintenance blocks
            for i, row in schedule_df.iterrows():
                fig.add_trace(go.Bar(
                    x=[row["days"]],
                    y=[row["task"]],
                    orientation="h",
                    base=[(row["start"] - today).days],
                    marker=dict(color=row["color"]),
                    name=row["task"],
                    hovertemplate=
                    "<b>%{y}</b><br>" +
                    "Start: " + row["start"].strftime("%Y-%m-%d") + "<br>" +
                    "Duration: %{x} days<br>" +
                    row["description"] +
                    "<extra></extra>",
                    width=0.6
                ))
            
            # Update layout with dual y-axis
            fig.update_layout(
                title="Maintenance Schedule with Health Forecast",
                xaxis=dict(
                    title="Days from Today",
                    range=[0, prediction_days]
                ),
                yaxis=dict(
                    title="",
                    categoryorder="array",
                    categoryarray=schedule_df["task"].tolist()
                ),
                yaxis2=dict(
                    title=dict(
                        text="Health Score",
                        font=dict(color="#9C27B0")
                    ),
                    tickfont=dict(color="#9C27B0"),
                    overlaying="y",
                    side="right",
                    range=[0, 100]
                ),
                height=300,
                barmode="overlay",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="center",
                    x=0.5
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Display maintenance tasks in a more friendly format
            st.markdown("#### Maintenance Action Items")
            
            for i, event in enumerate(maintenance_events):
                event_color = color_map[event["type"]]
                event_icon = "🔴" if event["type"] == "urgent" else ("🟠" if event["type"] == "scheduled" else ("🟢" if event["type"] == "routine" else "🔵"))
                
                st.markdown(
                    f"""
                    <div style="border: 1px solid {event_color}40; border-radius: 5px; padding: 15px; margin-bottom: 10px;">
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <h4 style="margin: 0; color: {event_color};">{event_icon} {event["task"]}</h4>
                            <span style="color: #666;">
                                {event["start"].strftime("%Y-%m-%d")} - {event["end"].strftime("%Y-%m-%d")}
                            </span>
                        </div>
                        <p style="margin: 10px 0 15px 0;">{event["description"]}</p>
                        
                        <details>
                            <summary style="cursor: pointer; color: #2196F3;">View recommended actions</summary>
                            <div style="padding: 10px 0 0 15px;">
                    """,
                    unsafe_allow_html=True
                )
                
                # Generate specific recommendations based on event type and component risks
                if event["type"] == "urgent":
                    recs = [
                        "Perform full diagnostic scan on all components",
                        f"Check {top_risk[0]['name']} for immediate issues (highest risk component)",
                        "Run memory consistency verification and repair",
                        "Check thermal paste and cooling system",
                        "Verify power delivery stability",
                        "Consider temporary reallocation of critical workloads"
                    ]
                elif event["type"] == "scheduled":
                    recs = [
                        "Perform targeted diagnostic of declining components",
                        "Schedule downtime of 4-6 hours for maintenance",
                        "Run memory defragmentation",
                        "Clean cooling components and verify airflow",
                        "Check for firmware updates",
                        "Validate performance benchmarks before and after maintenance"
                    ]
                elif event["type"] == "routine":
                    recs = [
                        "Run standard diagnostic suite",
                        "Check memory fragmentation levels",
                        "Verify temperature profiles under load",
                        "Update monitoring thresholds if needed",
                        "Document performance metrics for trend analysis"
                    ]
                else:  # update
                    recs = [
                        "Backup current firmware before updating",
                        "Verify compatibility with current drivers",
                        "Schedule short downtime (30-60 min) for update",
                        "Run validation tests after update",
                        "Monitor for any anomalies for 24 hours post-update"
                    ]
                
                for rec in recs:
                    st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
                
                st.markdown(
                    """
                            </div>
                        </details>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.info("No maintenance activities required within the forecast period. Continue regular monitoring.")
        
        # Advanced maintenance recommendations based on component-specific issues
        st.markdown("#### Component-Specific Maintenance Recommendations")
        
        # Get the top 3 components that need attention
        top_maintenance_components = component_df.sort_values(by="current_health").head(3)
        
        for _, comp in top_maintenance_components.iterrows():
            if comp["current_health"] < 60:
                severity = "Critical"
                color = "#F44336"  # Red
            elif comp["current_health"] < 75:
                severity = "Important"
                color = "#FF9800"  # Orange
            else:
                severity = "Recommended"
                color = "#2196F3"  # Blue
            
            st.markdown(
                f"""
                <div style="border-left: 4px solid {color}; padding: 15px; margin-bottom: 15px;">
                    <h4 style="margin-top: 0; color: {color};">{comp["name"]} ({severity})</h4>
                    <p style="margin-bottom: 10px;">Current Health: {comp["current_health"]}/100</p>
                """,
                unsafe_allow_html=True
            )
            
            # Generate component-specific recommendations
            if comp["name"] == "Memory Subsystem":
                recs = [
                    "Run complete memory diagnostic scan",
                    "Perform advanced memory defragmentation",
                    "Check for memory leak issues in running applications",
                    "Verify memory bandwidth performance under load"
                ]
            elif comp["name"] == "Cooling System":
                recs = [
                    "Clean heatsink and fan components",
                    "Replace thermal paste between GPU die and heatsink",
                    "Verify fan speed control is responding properly",
                    "Check for airflow obstructions in the chassis"
                ]
            elif comp["name"] == "Power Delivery":
                recs = [
                    "Test power supply stability under varying loads",
                    "Check for voltage fluctuations during high performance tasks",
                    "Verify all power connectors are secure",
                    "Consider power limiting to reduce stress on degraded components"
                ]
            elif comp["name"] == "Core Clock Stability":
                recs = [
                    "Run stability test with varying clock frequencies",
                    "Reset overclocking to factory defaults if applied",
                    "Update GPU drivers to latest stable version",
                    "Monitor for anomalies in performance benchmarks"
                ]
            elif comp["name"] == "PCI-E Interface":
                recs = [
                    "Check physical connection in PCI-E slot",
                    "Run bandwidth tests to verify interface performance",
                    "Clean connection contacts if accessible",
                    "Verify motherboard firmware is up to date"
                ]
            else:
                recs = [
                    "Run diagnostic tests specific to this component",
                    "Check for driver-related issues",
                    "Monitor performance metrics under load",
                    "Consider firmware updates if available"
                ]
            
            for rec in recs:
                st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Long-term maintenance strategy based on overall health trends
        st.markdown("#### Long-term Maintenance Strategy")
        
        # Determine long-term strategy based on current health and prediction
        if current_score >= 75 and min(future_y) >= 60:
            # Healthy GPU with good forecast
            strategy_type = "Standard Maintenance"
            strategy_color = "#4CAF50"
            strategy_icon = "✓"
            strategy_desc = "The GPU is in good health with a positive forecast. Focus on preventive maintenance to maintain optimal performance."
            strategy_interval = "Every 90 days"
            strategy_duration = "2-3 hours"
        elif current_score >= 60 and min(future_y) >= 40:
            # Moderate health with acceptable forecast
            strategy_type = "Enhanced Monitoring"
            strategy_color = "#2196F3"
            strategy_icon = "ℹ"
            strategy_desc = "The GPU shows signs of wear but remains functional. Increase monitoring frequency and implement regular maintenance."
            strategy_interval = "Every 45-60 days"
            strategy_duration = "3-4 hours"
        elif current_score >= 40 or min(future_y) >= 25:
            # Poor health but not critical
            strategy_type = "Intensive Care"
            strategy_color = "#FF9800"
            strategy_icon = "⚠"
            strategy_desc = "The GPU is showing significant degradation. Implement aggressive maintenance schedule and consider workload reduction."
            strategy_interval = "Every 30 days"
            strategy_duration = "4-6 hours"
        else:
            # Critical condition
            strategy_type = "End-of-Life Planning"
            strategy_color = "#F44336"
            strategy_icon = "⛔"
            strategy_desc = "The GPU is approaching end-of-life condition. Perform critical maintenance while planning for replacement."
            strategy_interval = "Every 14-21 days"
            strategy_duration = "6-8 hours"
        
        st.markdown(
            f"""
            <div style="background-color: {strategy_color}10; border: 1px solid {strategy_color}30; border-radius: 5px; padding: 20px; margin-top: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h3 style="margin: 0; color: {strategy_color};">{strategy_icon} {strategy_type}</h3>
                    <span style="background-color: {strategy_color}20; color: {strategy_color}; padding: 5px 10px; border-radius: 15px;">
                        Interval: {strategy_interval}
                    </span>
                </div>
                
                <p style="margin-bottom: 15px;">{strategy_desc}</p>
                
                <table style="width: 100%; border-collapse: collapse; margin-bottom: 15px;">
                    <tr style="border-bottom: 1px solid {strategy_color}30;">
                        <td style="padding: 8px 0;"><b>Maintenance Duration:</b></td>
                        <td style="text-align: right;">{strategy_duration}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid {strategy_color}30;">
                        <td style="padding: 8px 0;"><b>Monitoring Frequency:</b></td>
                        <td style="text-align: right;">{"Daily" if strategy_type in ["Intensive Care", "End-of-Life Planning"] else "Weekly"}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;"><b>Resource Allocation:</b></td>
                        <td style="text-align: right;">{"High" if strategy_type in ["Intensive Care", "End-of-Life Planning"] else "Moderate" if strategy_type == "Enhanced Monitoring" else "Low"}</td>
                    </tr>
                </table>
            """,
            unsafe_allow_html=True
        )
        
        # Strategy-specific recommendations
        if strategy_type == "Standard Maintenance":
            strategy_recs = [
                "Implement quarterly maintenance schedule with automated diagnostics",
                "Monitor health scores weekly and establish baseline for normal variations",
                "Keep firmware and drivers updated to latest stable releases",
                "Document maintenance activities and performance benchmarks for trend analysis"
            ]
        elif strategy_type == "Enhanced Monitoring":
            strategy_recs = [
                "Increase diagnostic depth and frequency of maintenance sessions",
                "Implement automated health checks twice weekly with alert thresholds",
                "Consider load balancing to reduce stress on declining components",
                "Prepare contingency plans for potential failure scenarios",
                "Verify cooling and power delivery systems are operating optimally"
            ]
        elif strategy_type == "Intensive Care":
            strategy_recs = [
                "Implement bi-weekly maintenance with full diagnostic suite",
                "Consider underclocking to reduce thermal and power stress",
                "Redirect high-intensity workloads to other GPUs when possible",
                "Prepare migration plan for critical workloads in case of failure",
                "Allocate budget for potential replacement within 3-6 months",
                "Maintain detailed performance logs to identify degradation patterns"
            ]
        else:  # End-of-Life Planning
            strategy_recs = [
                "Begin immediate migration of critical workloads to alternate GPUs",
                "Implement strict performance limits to extend remaining lifespan",
                "Schedule replacement within 1-3 months",
                "Maintain frequent (weekly) maintenance sessions focused on critical components",
                "Document failure patterns to inform future GPU management strategies",
                "Consider salvage options for non-critical workloads or spare parts"
            ]
        
        for rec in strategy_recs:
            st.markdown(f"<li>{rec}</li>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Maintenance scheduling tools
        maintenance_cols = st.columns(2)
        
        with maintenance_cols[0]:
            st.button("Generate Maintenance Plan PDF", use_container_width=True)
        
        with maintenance_cols[1]:
            st.button("Add to Maintenance Calendar", use_container_width=True)
        
        # Return on Investment (ROI) calculation for maintenance
        st.markdown("#### Maintenance ROI Calculator")
        
        # Calculate maintenance impact on GPU lifespan
        current_mtbf = 730  # ~2 years base MTBF for GPU
        
        # Adjust based on current health score
        adjusted_mtbf = current_mtbf * (current_score / 100)
        
        # Calculate improvement with maintenance
        mtbf_with_maintenance = adjusted_mtbf * 1.5  # Assume 50% improvement with proper maintenance
        
        # Calculate financial impact
        gpu_cost = 10000  # Assume high-end GPU cost
        daily_value = gpu_cost / current_mtbf  # Daily depreciation
        maintenance_cost = 500  # Cost per maintenance session
        
        # Calculate ROI
        lifespan_extension = mtbf_with_maintenance - adjusted_mtbf
        financial_benefit = lifespan_extension * daily_value
        maintenance_sessions = prediction_days / 90  # Quarterly maintenance
        total_maintenance_cost = maintenance_sessions * maintenance_cost
        net_benefit = financial_benefit - total_maintenance_cost
        roi_percent = (net_benefit / total_maintenance_cost) * 100 if total_maintenance_cost > 0 else 0
        
        st.markdown(
            f"""
            <div style="background-color: rgba(0, 0, 0, 0.05); padding: 20px; border-radius: 5px; margin-top: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                    <h4 style="margin: 0;">Maintenance Value Analysis</h4>
                    <span style="background-color: #E0E0E0; padding: 5px 10px; border-radius: 15px; font-size: 0.9em;">
                        ROI: {roi_percent:.1f}%
                    </span>
                </div>
                
                <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                    <div style="flex: 1; margin-right: 10px;">
                        <div style="background-color: white; padding: 15px; border-radius: 5px; height: 100%;">
                            <h5 style="margin-top: 0; color: #666;">Without Maintenance</h5>
                            <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 5px;">{adjusted_mtbf:.0f} days</div>
                            <div style="font-size: 0.9rem; color: #666;">Estimated remaining lifespan</div>
                        </div>
                    </div>
                    <div style="flex: 1; margin-left: 10px;">
                        <div style="background-color: white; padding: 15px; border-radius: 5px; height: 100%;">
                            <h5 style="margin-top: 0; color: #666;">With Maintenance</h5>
                            <div style="font-size: 1.5rem; font-weight: bold; margin-bottom: 5px; color: #2196F3;">{mtbf_with_maintenance:.0f} days</div>
                            <div style="font-size: 0.9rem; color: #666;">Projected extended lifespan</div>
                        </div>
                    </div>
                </div>
                
                <table style="width: 100%; border-collapse: collapse;">
                    <tr style="border-bottom: 1px solid #E0E0E0;">
                        <td style="padding: 8px 0;"><b>Lifespan Extension:</b></td>
                        <td style="text-align: right;">{lifespan_extension:.0f} days</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E0E0E0;">
                        <td style="padding: 8px 0;"><b>Financial Benefit:</b></td>
                        <td style="text-align: right;">${financial_benefit:.2f}</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #E0E0E0;">
                        <td style="padding: 8px 0;"><b>Maintenance Cost:</b></td>
                        <td style="text-align: right;">${total_maintenance_cost:.2f}</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 0;"><b>Net Benefit:</b></td>
                        <td style="text-align: right; font-weight: bold; color: {"#4CAF50" if net_benefit > 0 else "#F44336"};">${net_benefit:.2f}</td>
                    </tr>
                </table>
                
                <p style="font-size: 0.9em; color: #666; margin-top: 15px; margin-bottom: 0;">
                    Note: This analysis is based on industry averages and specific GPU characteristics. 
                    Actual results may vary based on workload intensity and environmental factors.
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
