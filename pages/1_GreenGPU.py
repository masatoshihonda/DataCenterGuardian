import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from utils.data_utils import get_gpu_emission_data, get_gpu_temperature_data

# Page configuration
st.set_page_config(
    page_title="GreenGPU - Eco-friendly GPU Assignment",
    page_icon="🌱",
    layout="wide"
)

# Sidebar
st.sidebar.title("GreenGPU")
st.sidebar.info("""
GreenGPU optimizes GPU task assignment based on environmental factors like CO2 emissions and temperature.
Schedule workloads during periods of lower environmental impact.
""")

# Main content
st.title("GreenGPU: Environmentally-Aware GPU Task Assignment")

tab1, tab2, tab3 = st.tabs(["Dashboard", "Task Scheduler", "Carbon Impact"])

with tab1:
    st.header("Environmental Metrics Dashboard")
    
    # Top metrics
    metric_cols = st.columns(4)
    
    with metric_cols[0]:
        st.metric(
            label="Current CO2 Intensity",
            value="183 g/kWh",
            delta="-15 g/kWh",
            delta_color="inverse"
        )
    
    with metric_cols[1]:
        st.metric(
            label="Avg GPU Temperature",
            value="67.3 °C",
            delta="+2.1 °C"
        )
    
    with metric_cols[2]:
        st.metric(
            label="Power Usage",
            value="4.2 kW",
            delta="+0.3 kW"
        )
    
    with metric_cols[3]:
        st.metric(
            label="Carbon Efficiency",
            value="82%",
            delta="+5%"
        )
    
    # GPU status overview
    st.subheader("GPU Fleet Status")
    
    # Generate sample GPU data
    gpu_count = 8
    gpu_data = pd.DataFrame({
        "gpu_id": [f"gpu-{i}" for i in range(1, gpu_count + 1)],
        "status": np.random.choice(["Active", "Idle", "Maintenance", "Cooling"], gpu_count, p=[0.5, 0.3, 0.1, 0.1]),
        "temperature": np.random.normal(65, 10, gpu_count).round(1),
        "power_draw": np.random.normal(180, 40, gpu_count).round(1),
        "utilization": np.random.uniform(0, 100, gpu_count).round(1),
        "memory_used": np.random.uniform(0, 32, gpu_count).round(1),
        "memory_total": np.random.choice([16, 24, 32, 40, 80], gpu_count),
        "tasks_completed": np.random.randint(10, 500, gpu_count),
        "carbon_rating": np.random.choice(["A+", "A", "B", "C", "D"], gpu_count, p=[0.1, 0.3, 0.3, 0.2, 0.1]),
        "task_type": np.random.choice(["Training", "Inference", "Data Processing", "Fine-tuning", "None"], gpu_count),
        "co2_per_hour": np.random.uniform(0.1, 0.8, gpu_count).round(2)
    })
    
    # Add memory utilization percentage
    gpu_data["memory_pct"] = (gpu_data["memory_used"] / gpu_data["memory_total"] * 100).round(1)
    
    # Create three columns for better layout
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Improved heatmap-style visualization for GPU utilization with temperature color coding
        st.markdown("### GPU Utilization & Temperature Status")
        
        # Create a more detailed and visually appealing heatmap-bar chart
        fig = go.Figure()
        
        # Add background reference rectangles for utilization zones
        fig.add_shape(
            type="rect",
            x0=0, y0=-0.5,
            x1=30, y1=gpu_count-0.5,
            fillcolor="rgba(0, 128, 0, 0.1)",
            line=dict(width=0),
            layer="below"
        )
        
        fig.add_shape(
            type="rect",
            x0=30, y0=-0.5,
            x1=70, y1=gpu_count-0.5,
            fillcolor="rgba(255, 165, 0, 0.1)",
            line=dict(width=0),
            layer="below"
        )
        
        fig.add_shape(
            type="rect",
            x0=70, y0=-0.5,
            x1=100, y1=gpu_count-0.5,
            fillcolor="rgba(255, 0, 0, 0.1)",
            line=dict(width=0),
            layer="below"
        )
        
        # Sort GPUs by temperature for better visualization
        gpu_data_sorted = gpu_data.sort_values(by="temperature", ascending=False)
        
        for i, row in gpu_data_sorted.reset_index().iterrows():
            # Determine color gradient based on temperature
            temp = row["temperature"]
            if temp < 50:
                color = "rgb(0, 180, 0)"  # Cool green
                temp_status = "Cool"
            elif temp < 65:
                color = "rgb(180, 180, 0)"  # Warm yellow
                temp_status = "Normal"
            elif temp < 80:
                color = "rgb(255, 120, 0)"  # Hot orange
                temp_status = "Warm"
            else:
                color = "rgb(255, 0, 0)"  # Critical red
                temp_status = "Hot"
            
            # Status indicator
            status = row["status"]
            if status == "Active":
                status_icon = "🟢"
            elif status == "Idle":
                status_icon = "⚪"
            elif status == "Maintenance":
                status_icon = "🟠"
            else:  # Cooling
                status_icon = "❄️"
            
            # Add GPU utilization bar
            fig.add_trace(go.Bar(
                x=[row["utilization"]],
                y=[row["gpu_id"]],
                orientation='h',
                marker=dict(
                    color=color,
                    line=dict(color='rgba(0, 0, 0, 0.5)', width=1)
                ),
                name=row["gpu_id"],
                text=[f"{row['utilization']}%"],
                textposition='auto',
                hovertemplate=f"""
                <b>{row['gpu_id']}</b> ({status_icon} {status})<br>
                <b>Temperature:</b> {temp}°C ({temp_status})<br>
                <b>Utilization:</b> {row['utilization']}%<br>
                <b>Memory:</b> {row['memory_used']}/{row['memory_total']} GB ({row['memory_pct']}%)<br>
                <b>Power Draw:</b> {row['power_draw']}W<br>
                <b>Carbon Rating:</b> {row['carbon_rating']}<br>
                <b>CO₂ Emission:</b> {row['co2_per_hour']} kg/hour<br>
                <b>Current Task:</b> {row['task_type']}
                <extra></extra>
                """
            ))
            
            # Add temperature indicator as small markers to the right of the bars
            fig.add_trace(go.Scatter(
                x=[100 + 2],  # Position just outside the bar
                y=[row["gpu_id"]],
                mode='markers+text',
                marker=dict(
                    symbol='circle',
                    size=20,
                    color=color,
                    line=dict(color='rgba(0, 0, 0, 0.5)', width=1)
                ),
                text=[f"{temp}°C"],
                textposition="middle right",
                textfont=dict(size=10, color="white"),
                hoverinfo='skip',
                showlegend=False
            ))
        
        # Update layout for a more professional look
        fig.update_layout(
            title=dict(
                text="GPU Utilization & Temperature",
                font=dict(size=18),
                x=0.5,
                xanchor='center'
            ),
            xaxis=dict(
                title="Utilization (%)",
                range=[0, 115],  # Extended range to accommodate temperature indicators
                tickvals=[0, 25, 50, 75, 100],
                ticktext=["0%", "25%", "50%", "75%", "100%"],
                showgrid=True,
                gridcolor='rgba(0, 0, 0, 0.1)'
            ),
            yaxis=dict(
                title="GPU ID",
                autorange="reversed"  # To show highest temps at top
            ),
            barmode='stack',
            height=400,
            margin=dict(l=0, r=80, t=50, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(255, 255, 255, 0.95)',
            showlegend=False,
            annotations=[
                dict(
                    x=15, y=gpu_count,
                    xref="x", yref="y",
                    text="Low Utilization",
                    showarrow=False,
                    font=dict(size=10, color="green")
                ),
                dict(
                    x=50, y=gpu_count,
                    xref="x", yref="y",
                    text="Moderate Utilization",
                    showarrow=False,
                    font=dict(size=10, color="orange")
                ),
                dict(
                    x=85, y=gpu_count,
                    xref="x", yref="y",
                    text="High Utilization",
                    showarrow=False,
                    font=dict(size=10, color="red")
                )
            ]
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Add a small explanation for the color coding
        st.markdown("""
        <div style="display: flex; justify-content: center; gap: 20px; margin-top: -15px; font-size: 0.85rem; color: #666;">
            <div><span style="color: rgb(0, 180, 0);">●</span> &lt;50°C (Cool)</div>
            <div><span style="color: rgb(180, 180, 0);">●</span> 50-64°C (Normal)</div>
            <div><span style="color: rgb(255, 120, 0);">●</span> 65-79°C (Warm)</div>
            <div><span style="color: rgb(255, 0, 0);">●</span> ≥80°C (Hot)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.subheader("Carbon Ratings")
        
        rating_counts = gpu_data.groupby("carbon_rating").size().reset_index(name="count")
        
        fig = px.pie(
            rating_counts,
            values="count",
            names="carbon_rating",
            title="GPU Carbon Efficiency Ratings",
            color="carbon_rating",
            color_discrete_map={
                "A+": "#1e8449",
                "A": "#2ecc71",
                "B": "#f4d03f",
                "C": "#e67e22",
                "D": "#e74c3c"
            }
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # CO2 Intensity and Temperature Trend
    st.subheader("CO2 Intensity and Temperature Trend")
    
    # Get sample data
    co2_data = get_gpu_emission_data()
    temp_data = get_gpu_temperature_data()
    
    # Create figure with secondary y-axis
    fig = go.Figure()
    
    # Add CO2 intensity line
    fig.add_trace(go.Scatter(
        x=co2_data["timestamp"],
        y=co2_data["co2_intensity"],
        name="CO2 Intensity (g/kWh)",
        line=dict(color="green", width=2)
    ))
    
    # Add temperature line
    fig.add_trace(go.Scatter(
        x=temp_data["timestamp"],
        y=temp_data["avg_temperature"],
        name="Avg Temperature (°C)",
        line=dict(color="red", width=2, dash="dash"),
        yaxis="y2"
    ))
    
    # Update layout for dual y-axis
    fig.update_layout(
        title="CO2 Intensity vs. GPU Temperature",
        xaxis_title="Time",
        yaxis=dict(
            title="CO2 Intensity (g/kWh)",
            title_font=dict(color="green"),
            tickfont=dict(color="green")
        ),
        yaxis2=dict(
            title="Temperature (°C)",
            title_font=dict(color="red"),
            tickfont=dict(color="red"),
            anchor="x",
            overlaying="y",
            side="right"
        ),
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

with tab2:
    st.header("Task Scheduler")
    
    # Create tabs for the task scheduler
    scheduler_tabs = st.tabs(["Schedule New Task", "Current Tasks", "Task History"])
    
    with scheduler_tabs[0]:
        st.markdown("""
        <div style="border-left: 4px solid #0050B3; padding: 10px; background-color: #f0f7ff; margin-bottom: 20px;">
            <h3 style="margin-top: 0; margin-bottom: 5px; color: #0050B3;">Green Scheduling</h3>
            <p style="margin: 0;">Schedule your GPU tasks to run during low-carbon intensity periods to reduce environmental impact.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced task scheduler form with more inputs and better organization
        col1, col2, col3 = st.columns([1.5, 1.5, 1])
        
        with col1:
            st.markdown("### Task Details")
            
            task_name = st.text_input("Task Name", "My GPU Task", help="Enter a descriptive name for your task")
            
            task_type = st.selectbox(
                "Task Type",
                options=["Training", "Inference", "Fine-tuning", "Data Processing", "Benchmarking", "Hyperparameter Tuning"],
                help="Select the type of computational task"
            )
            
            model_name = st.text_input(
                "Model Name (if applicable)", 
                placeholder="e.g., ResNet50, BERT-base, Custom CNN",
                help="Specify the AI model being used"
            )
            
            framework = st.selectbox(
                "Framework",
                options=["PyTorch", "TensorFlow", "JAX", "MXNet", "ONNX", "Custom"],
                help="Select the deep learning framework"
            )
            
            estimated_duration = st.slider(
                "Estimated Duration (hours)", 
                min_value=1, 
                max_value=48, 
                value=4,
                help="Estimate how long the task will take to run"
            )
            
            memory_required = st.slider(
                "Memory Required (GB)",
                min_value=2,
                max_value=80,
                value=16,
                step=2,
                help="Estimated GPU memory required for this task"
            )
        
        with col2:
            st.markdown("### Scheduling Options")
            
            priority = st.select_slider(
                "Priority",
                options=["Low", "Medium", "High", "Critical"],
                value="Medium",
                help="Higher priority tasks are scheduled sooner"
            )
            
            optimization_goal = st.selectbox(
                "Optimization Goal",
                options=[
                    "Minimize CO₂ Emissions (Eco-friendly)",
                    "Balance Emissions and Speed",
                    "Maximize Performance (Fastest execution)",
                    "Minimize Cost (Budget-friendly)"
                ],
                index=0,
                help="What is most important for this task?"
            )
            
            # Dynamic options based on optimization goal
            if "Minimize CO₂" in optimization_goal:
                st.markdown("""
                <div style="background-color: #d4edda; border-left: 4px solid #28a745; padding: 10px; margin: 10px 0;">
                    <p style="margin: 0; color: #155724;">🌱 <strong>Eco Mode:</strong> Task will be scheduled during low carbon intensity periods</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Delay allowance
            allow_delay = st.checkbox(
                "Allow Flexible Scheduling", 
                value=True,
                help="Allow the scheduler to delay the task for better environmental impact"
            )
            
            if allow_delay:
                delay_cols = st.columns(2)
                with delay_cols[0]:
                    min_delay = st.number_input(
                        "Minimum Delay (hours)",
                        min_value=0,
                        max_value=12,
                        value=0,
                        help="Minimum acceptable delay before task starts"
                    )
                
                with delay_cols[1]:
                    max_delay = st.number_input(
                        "Maximum Delay (hours)",
                        min_value=min_delay,
                        max_value=72,
                        value=min(min_delay + 6, 72),
                        help="Maximum acceptable delay before task must start"
                    )
                
                deadline = st.date_input(
                    "Completion Deadline",
                    value=datetime.now().date() + timedelta(days=1),
                    min_value=datetime.now().date(),
                    help="Task must complete by this date"
                )
            
            # GPU preferences
            preferred_gpus = st.multiselect(
                "Preferred GPU Models (optional)",
                options=["NVIDIA A100", "NVIDIA V100", "NVIDIA T4", "NVIDIA RTX A6000", "AMD MI250", "Any Available"],
                default=["Any Available"],
                help="Specific GPU models to use, if available"
            )
        
        with col3:
            st.markdown("### Resource Planning")
            
            # Estimated energy usage based on duration and GPU type
            energy_per_hour = 2.5  # kWh
            if task_type == "Training" or task_type == "Hyperparameter Tuning":
                energy_per_hour = 3.2
            elif task_type == "Inference":
                energy_per_hour = 1.8
                
            total_energy = energy_per_hour * estimated_duration
            
            # Current CO2 intensity (g/kWh)
            current_co2 = 183
            optimal_co2 = 120
            
            # Calculate emissions
            current_emissions = round((current_co2 * total_energy / 1000), 2)  # kg CO2
            optimal_emissions = round((optimal_co2 * total_energy / 1000), 2)  # kg CO2
            potential_savings = round((current_emissions - optimal_emissions), 2)
            savings_percentage = round((potential_savings / current_emissions * 100), 1)
            
            # Display energy and carbon metrics
            st.markdown("#### Estimated Resources")
            
            # Energy usage
            st.metric(
                "Energy Usage",
                f"{total_energy:.1f} kWh",
                delta=None,
                help="Estimated energy consumption for this task"
            )
            
            # CO2 emissions if run now
            st.metric(
                "CO₂ Emissions (Immediate)",
                f"{current_emissions} kg",
                delta=None,
                help="Carbon emissions if task runs immediately"
            )
            
            # CO2 emissions if optimized
            st.metric(
                "CO₂ Emissions (Optimized)",
                f"{optimal_emissions} kg",
                delta=f"-{savings_percentage}%",
                delta_color="inverse",
                help="Carbon emissions if task runs during low-carbon period"
            )
            
            # Cost estimate
            energy_cost = total_energy * 0.12  # Assume $0.12 per kWh
            st.metric(
                "Estimated Cost",
                f"${energy_cost:.2f}",
                delta=None,
                help="Approximate cost based on energy usage"
            )
            
            # Submit button with more prominence
            st.markdown("<br>", unsafe_allow_html=True)
            schedule_button = st.button("Schedule Task", type="primary", use_container_width=True)
        
        # Show CO2 savings calculator only if allow_delay is checked
        if allow_delay:
            st.markdown("### CO₂ Savings Calculator")
            
            savings_cols = st.columns(2)
            
            with savings_cols[0]:
                # Visualization showing potential CO2 savings
                fig = go.Figure()
                
                # Add bars for immediate vs. optimized emissions
                fig.add_trace(go.Bar(
                    x=["Immediate Execution", "Green Scheduling"],
                    y=[current_emissions, optimal_emissions],
                    text=[f"{current_emissions} kg", f"{optimal_emissions} kg"],
                    textposition="auto",
                    marker_color=["#e74c3c", "#2ecc71"],
                    name="CO₂ Emissions"
                ))
                
                # Add annotation for savings
                fig.add_annotation(
                    x=1.5,
                    y=(current_emissions + optimal_emissions) / 2,
                    text=f"Save {potential_savings} kg CO₂<br>({savings_percentage}% reduction)",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowwidth=2,
                    arrowcolor="#3498db",
                    font=dict(size=12, color="#3498db"),
                    ax=-40,
                    ay=0
                )
                
                fig.update_layout(
                    title="Potential Carbon Savings",
                    xaxis_title=None,
                    yaxis_title="CO₂ Emissions (kg)",
                    height=300,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            with savings_cols[1]:
                # Equivalency metrics to make the savings more tangible
                equivalent_miles = round(potential_savings * 2.5, 1)  # Approx. 2.5 miles per kg CO2
                equivalent_trees = round(potential_savings / 21 * 365, 1)  # A tree absorbs ~21kg CO2 per year
                
                st.markdown("#### Environmental Impact Equivalents")
                st.markdown(f"💨 Saving **{potential_savings}kg** of CO₂ is equivalent to:")
                st.markdown(f"🚗 Avoiding **{equivalent_miles}** miles of driving")
                st.markdown(f"🌳 The daily CO₂ absorption of **{equivalent_trees/365:.1f}** trees")
                st.markdown(f"💡 Turning off a 60W light bulb for **{round(potential_savings * 11.5, 1)}** hours")
                
                # Environmental impact badge
                if savings_percentage > 40:
                    impact_level = "High Positive Impact"
                    badge_color = "#27ae60"
                elif savings_percentage > 20:
                    impact_level = "Medium Positive Impact"
                    badge_color = "#2980b9"
                else:
                    impact_level = "Positive Impact"
                    badge_color = "#3498db"
                
                st.markdown(f"""
                <div style="background-color: {badge_color}; color: white; padding: 10px; border-radius: 5px; text-align: center; margin-top: 20px;">
                    <h3 style="margin: 0;">🌿 {impact_level}</h3>
                </div>
                """, unsafe_allow_html=True)
        
        # If schedule button is clicked, show task details and confirmation
        if schedule_button:
            st.success(f"✅ Task '{task_name}' scheduled successfully!")
            
            # Calculate optimal start time based on the optimization goal
            if "Emissions" in optimization_goal:
                delay_hours = 3  # Example: delayed by 3 hours for lower carbon intensity
                optimal_start = (datetime.now() + timedelta(hours=delay_hours)).strftime("%Y-%m-%d %H:%M")
                reason = "lowest carbon intensity period within your delay window"
            elif "Balance" in optimization_goal:
                delay_hours = 1  # Example: shorter delay for balance
                optimal_start = (datetime.now() + timedelta(hours=delay_hours)).strftime("%Y-%m-%d %H:%M")
                reason = "good balance between carbon intensity and timing"
            else:
                delay_hours = 0  # No delay for performance-focused
                optimal_start = datetime.now().strftime("%Y-%m-%d %H:%M")
                reason = "immediate execution for maximum performance"
            
            # Select appropriate GPU
            if len(preferred_gpus) > 0 and "Any Available" not in preferred_gpus:
                optimal_gpu = preferred_gpus[0]
            else:
                optimal_gpu = "NVIDIA A100"  # Example
            
            # Show scheduling details
            st.markdown("### Scheduled Task Details")
            
            details_cols = st.columns(2)
            
            with details_cols[0]:
                st.markdown(f"**Task ID:** TASK-{hash(task_name + str(datetime.now()))%1000:03d}")
                st.markdown(f"**Task Name:** {task_name}")
                st.markdown(f"**Task Type:** {task_type}")
                st.markdown(f"**Optimization Goal:** {optimization_goal}")
                st.markdown(f"**Estimated Duration:** {estimated_duration} hours")
                st.markdown(f"**Memory Required:** {memory_required} GB")
            
            with details_cols[1]:
                st.markdown(f"**Scheduled Start:** {optimal_start}")
                st.markdown(f"**Assigned GPU:** {optimal_gpu}")
                st.markdown(f"**Priority Level:** {priority}")
                st.markdown(f"**Estimated CO₂:** {optimal_emissions} kg")
                st.markdown(f"**Estimated Energy:** {total_energy:.1f} kWh")
                st.markdown(f"**CO₂ Reduction:** {savings_percentage}% vs. immediate execution")
            
            # Explanation of scheduling decision
            st.info(f"This task was scheduled to start at {optimal_start} because this is the {reason}.")
            
            # Display a timeline visualization
            time_points = []
            now = datetime.now()
            
            # Add current time point
            time_points.append({
                "time": now,
                "event": "Current Time",
                "description": "Now"
            })
            
            # Add scheduled start
            scheduled_time = now + timedelta(hours=delay_hours)
            time_points.append({
                "time": scheduled_time,
                "event": "Scheduled Start",
                "description": f"Task starts: {task_name}"
            })
            
            # Add estimated completion
            completion_time = scheduled_time + timedelta(hours=estimated_duration)
            time_points.append({
                "time": completion_time,
                "event": "Estimated Completion",
                "description": f"Task completes: {task_name}"
            })
            
            # Convert to DataFrame for plotting
            timeline_df = pd.DataFrame(time_points)
            timeline_df["time_str"] = timeline_df["time"].dt.strftime("%Y-%m-%d %H:%M")
            
            # Create timeline visualization
            fig = px.timeline(
                timeline_df,
                x_start="time",
                x_end="time",
                y="event",
                color="event",
                text="description",
                title="Task Schedule Timeline",
                color_discrete_map={
                    "Current Time": "#3498db",
                    "Scheduled Start": "#2ecc71",
                    "Estimated Completion": "#e74c3c"
                }
            )
            
            fig.update_yaxes(autorange="reversed")
            fig.update_layout(height=200, showlegend=False)
            fig.update_traces(marker_line_width=0)
            
            st.plotly_chart(fig, use_container_width=True)
            
    with scheduler_tabs[1]:
        # Enhanced view of currently scheduled tasks
        st.markdown("### Currently Scheduled Tasks")
        
        # Filter options
        filter_cols = st.columns(4)
        with filter_cols[0]:
            status_filter = st.multiselect(
                "Filter by Status",
                options=["All", "Running", "Scheduled", "Waiting", "Completed", "Failed"],
                default=["Running", "Scheduled", "Waiting"]
            )
        
        with filter_cols[1]:
            type_filter = st.multiselect(
                "Filter by Type",
                options=["All", "Training", "Inference", "Fine-tuning", "Data Processing", "Benchmarking"],
                default=["All"]
            )
        
        with filter_cols[2]:
            time_filter = st.selectbox(
                "Time Range",
                options=["All Time", "Today", "Next 24 Hours", "Next 7 Days"]
            )
        
        with filter_cols[3]:
            sort_by = st.selectbox(
                "Sort By",
                options=["Start Time", "Priority", "Duration", "CO₂ Impact"]
            )
        
        # Sample scheduled tasks with more details
        scheduled_tasks = pd.DataFrame({
            "task_id": [f"TASK-{i:03d}" for i in range(1, 8)],
            "task_name": [
                "BERT Fine-tuning", 
                "ResNet152 Training", 
                "GPT-2 Inference Batch", 
                "Data Preprocessing", 
                "Performance Benchmark",
                "Hyperparameter Tuning",
                "Video Processing"
            ],
            "type": ["Fine-tuning", "Training", "Inference", "Data Processing", "Benchmarking", "Training", "Inference"],
            "status": ["Running", "Scheduled", "Scheduled", "Waiting", "Scheduled", "Completed", "Failed"],
            "priority": ["High", "Medium", "Low", "Medium", "Low", "Critical", "Medium"],
            "start_time": [
                (datetime.now() - timedelta(hours=2)).strftime("%Y-%m-%d %H:%M"),
                (datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M"),
                (datetime.now() + timedelta(hours=5)).strftime("%Y-%m-%d %H:%M"),
                "Waiting for low-carbon period",
                (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d %H:%M"),
                (datetime.now() - timedelta(hours=5)).strftime("%Y-%m-%d %H:%M")
            ],
            "duration": ["8 hours", "12 hours", "2 hours", "4 hours", "6 hours", "24 hours", "3 hours"],
            "assigned_gpu": ["NVIDIA A100", "NVIDIA V100", "NVIDIA T4", "Any", "NVIDIA A100", "NVIDIA A100", "AMD MI250"],
            "progress": [65, 0, 0, 0, 0, 100, 32],
            "co2_impact": ["Medium", "Low", "Low", "Very Low", "Medium", "High", "Medium"]
        })
        
        # Apply filters
        filtered_tasks = scheduled_tasks.copy()
        
        if "All" not in status_filter:
            filtered_tasks = filtered_tasks[filtered_tasks["status"].isin(status_filter)]
        
        if "All" not in type_filter:
            filtered_tasks = filtered_tasks[filtered_tasks["type"].isin(type_filter)]
        
        # Style the dataframe for better visualization
        def color_status(val):
            if val == "Running":
                return "background-color: #d4edda; color: #155724"
            elif val == "Scheduled":
                return "background-color: #d1ecf1; color: #0c5460"
            elif val == "Waiting":
                return "background-color: #fff3cd; color: #856404"
            elif val == "Completed":
                return "background-color: #e2e3e5; color: #383d41"
            elif val == "Failed":
                return "background-color: #f8d7da; color: #721c24"
            return ""
        
        def color_impact(val):
            if val == "Very Low":
                return "color: #27ae60"
            elif val == "Low":
                return "color: #2ecc71"
            elif val == "Medium":
                return "color: #f39c12"
            elif val == "High":
                return "color: #e74c3c"
            return ""
        
        # Create progress bar formatter for the progress column
        def progress_bar(val):
            if val == 0:
                return ""
            
            color = "#2ecc71" if val >= 75 else "#f39c12" if val >= 25 else "#e74c3c"
            return f"""
            <div style="width:100%; background-color: #eee; border-radius: 3px;">
                <div style="width:{val}%; height:10px; background-color:{color}; border-radius: 3px;"></div>
            </div>
            """
        
        # Apply styling and display with progress bars
        styled_tasks = filtered_tasks.style.applymap(color_status, subset=["status"]).applymap(color_impact, subset=["co2_impact"])
        
        # Convert progress column to HTML progress bars
        progress_html = filtered_tasks["progress"].apply(progress_bar)
        
        # Display the styled dataframe
        st.dataframe(
            styled_tasks,
            column_config={
                "progress": st.column_config.ProgressColumn(
                    "Progress",
                    help="Task progress percentage",
                    width="medium",
                    format="%d%%",
                    min_value=0,
                    max_value=100
                ),
                "task_id": st.column_config.Column(
                    "Task ID",
                    width="small"
                ),
                "task_name": st.column_config.Column(
                    "Task Name",
                    width="medium"
                )
            },
            height=400,
            use_container_width=True
        )
        
        # Task actions
        action_cols = st.columns(4)
        with action_cols[0]:
            selected_task = st.selectbox("Select Task for Action", options=filtered_tasks["task_id"].tolist())
        
        with action_cols[1]:
            st.button("View Details", use_container_width=True)
        
        with action_cols[2]:
            st.button("Pause/Resume", use_container_width=True)
        
        with action_cols[3]:
            st.button("Cancel Task", use_container_width=True, type="secondary")
    
    with scheduler_tabs[2]:
        # Task history and analytics
        st.markdown("### Task History Analytics")
        
        # Sample historical data
        history_data = {
            "date": pd.date_range(start=datetime.now() - timedelta(days=30), periods=30, freq="D"),
            "training_tasks": np.random.randint(2, 10, 30),
            "inference_tasks": np.random.randint(5, 20, 30),
            "other_tasks": np.random.randint(1, 8, 30),
            "avg_co2": np.random.uniform(0.2, 0.6, 30).round(2),
            "total_runtime": np.random.uniform(20, 100, 30).round(1)
        }
        
        history_df = pd.DataFrame(history_data)
        history_df["total_tasks"] = history_df["training_tasks"] + history_df["inference_tasks"] + history_df["other_tasks"]
        
        # Task count visualization
        task_type_df = pd.DataFrame({
            "task_type": ["Training", "Inference", "Other"],
            "count": [
                history_df["training_tasks"].sum(),
                history_df["inference_tasks"].sum(),
                history_df["other_tasks"].sum()
            ]
        })
        
        history_cols = st.columns(2)
        
        with history_cols[0]:
            # Task distribution pie chart
            fig = px.pie(
                task_type_df,
                values="count",
                names="task_type",
                title="Task Type Distribution (Last 30 Days)",
                color="task_type",
                color_discrete_map={
                    "Training": "#3498db",
                    "Inference": "#2ecc71",
                    "Other": "#f39c12"
                },
                hole=0.4
            )
            
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with history_cols[1]:
            # CO2 impact over time
            fig = px.line(
                history_df,
                x="date",
                y="avg_co2",
                title="Average CO₂ Impact per Task (kg)",
                markers=True
            )
            
            fig.update_layout(height=350)
            fig.update_yaxes(rangemode="tozero")
            st.plotly_chart(fig, use_container_width=True)
        
        # Task volume over time
        task_volume_df = pd.melt(
            history_df,
            id_vars=["date"],
            value_vars=["training_tasks", "inference_tasks", "other_tasks"],
            var_name="task_type",
            value_name="count"
        )
        
        # Clean up task type names
        task_volume_df["task_type"] = task_volume_df["task_type"].str.replace("_tasks", "").str.capitalize()
        
        fig = px.bar(
            task_volume_df,
            x="date",
            y="count",
            color="task_type",
            title="Daily Task Volume by Type",
            color_discrete_map={
                "Training": "#3498db",
                "Inference": "#2ecc71",
                "Other": "#f39c12"
            }
        )
        
        fig.update_layout(height=350)
        st.plotly_chart(fig, use_container_width=True)
        
        # Summary metrics
        metric_cols = st.columns(4)
        
        with metric_cols[0]:
            st.metric(
                "Total Tasks",
                f"{history_df['total_tasks'].sum()}",
                delta=f"{history_df.iloc[-7:]['total_tasks'].sum() - history_df.iloc[-14:-7]['total_tasks'].sum()}"
            )
        
        with metric_cols[1]:
            st.metric(
                "Avg. Task Duration",
                f"{history_df['total_runtime'].mean():.1f} hrs",
                delta=f"{(history_df.iloc[-7:]['total_runtime'].mean() - history_df.iloc[-14:-7]['total_runtime'].mean()):.1f} hrs"
            )
        
        with metric_cols[2]:
            total_co2 = (history_df["avg_co2"] * history_df["total_tasks"]).sum()
            st.metric(
                "Total CO₂ Impact",
                f"{total_co2:.1f} kg",
                delta=None
            )
        
        with metric_cols[3]:
            avg_co2_per_task = history_df["avg_co2"].mean()
            st.metric(
                "Avg. CO₂ per Task",
                f"{avg_co2_per_task:.2f} kg",
                delta=f"{(history_df.iloc[-7:]['avg_co2'].mean() - history_df.iloc[-14:-7]['avg_co2'].mean()):.2f} kg",
                delta_color="inverse"
            )

with tab3:
    st.header("Carbon Impact Analysis")
    
    # Create tabs for the carbon analysis section
    carbon_tabs = st.tabs(["CO₂ Intensity Forecast", "Task Planning", "Impact Analytics"])
    
    with carbon_tabs[0]:
        st.markdown("### Carbon Intensity Forecast with Optimal Windows")
        
        # Add forecast timeframe selector
        forecast_period = st.select_slider(
            "Forecast Timeframe",
            options=["Next 24 Hours", "Next 48 Hours", "Next 72 Hours", "Next Week"],
            value="Next 72 Hours"
        )
        
        # Map selection to number of hours
        if forecast_period == "Next 24 Hours":
            hours = 24
        elif forecast_period == "Next 48 Hours":
            hours = 48
        elif forecast_period == "Next 72 Hours":
            hours = 72
        else:  # Next Week
            hours = 24 * 7
        
        # Add data source information
        st.markdown("""
        <div style="background-color: #f8f9fa; padding: 10px; border-radius: 5px; margin-bottom: 15px; font-size: 0.9em;">
            <p style="margin: 0;">
                <strong>Data Source:</strong> CO₂ intensity forecasts based on historical grid data and renewable energy production models.
                Last updated: Today at 08:00 UTC. Updates hourly.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Generate forecast data with more realistic patterns
        now = datetime.now().replace(minute=0, second=0, microsecond=0)
        timestamps = [now + timedelta(hours=i) for i in range(hours)]
        
        # Create more realistic patterns with:
        # - Daily cycles (lower at night, higher during day)
        # - Weekly patterns (lower on weekends)
        # - Some random variation
        base_co2 = 180
        day_amplitude = 60  # Daily variation amplitude
        weekend_reduction = 30  # Weekend reduction amount
        
        co2_values = []
        for ts in timestamps:
            hour = ts.hour
            # Daily pattern - lowest at night (2-5 AM), highest during peak hours (6-9 PM)
            hour_factor = np.sin(np.pi * (hour - 2) / 24)
            daily_variation = day_amplitude * hour_factor
            
            # Weekend pattern - lower on weekends
            weekend_factor = 1.0
            if ts.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
                weekend_factor = 0.7  # 30% reduction on weekends
            
            # Renewable energy impact (e.g., solar generation during daylight)
            solar_factor = 0
            if 8 <= hour <= 16:  # Daylight hours
                solar_time = (hour - 8) / 8  # 0 to 1 during daylight
                solar_factor = -30 * np.sin(np.pi * solar_time)  # Max -30 at noon
            
            # Random variation (e.g., weather impacts)
            random_variation = np.random.normal(0, 10)
            
            # Calculate final value
            value = max(50, base_co2 * weekend_factor + daily_variation + solar_factor + random_variation)
            co2_values.append(value)
        
        # Create a forecast DataFrame
        forecast_df = pd.DataFrame({
            "timestamp": timestamps,
            "co2_intensity": co2_values
        })
        
        # Calculate optimal scheduling windows for different durations
        low_carbon_threshold = base_co2 - 40
        high_carbon_threshold = base_co2 + 20
        critical_threshold = base_co2 + 50
        
        # Add a predicted grid mix for enriched information
        energy_sources = ["Solar", "Wind", "Hydro", "Nuclear", "Natural Gas", "Coal"]
        grid_mix = []
        
        for co2 in co2_values:
            # Calculate energy mix based on the CO2 intensity
            if co2 < 100:
                # Very low carbon - high renewables
                mix = [30, 35, 15, 15, 5, 0]
            elif co2 < 150:
                # Low carbon - good renewable conditions
                mix = [25, 25, 10, 15, 20, 5]
            elif co2 < 200:
                # Medium carbon
                mix = [15, 15, 10, 20, 30, 10]
            else:
                # High carbon
                mix = [5, 10, 5, 15, 40, 25]
                
            # Add some random variation
            mix = [max(0, min(100, x + np.random.normal(0, 2))) for x in mix]
            # Normalize to 100%
            mix = [x / sum(mix) * 100 for x in mix]
            
            grid_mix.append(dict(zip(energy_sources, mix)))
        
        # Add grid mix data to DataFrame
        for source in energy_sources:
            forecast_df[source] = [mix[source] for mix in grid_mix]
        
        # Add a renewable percentage column
        forecast_df["renewable_pct"] = forecast_df[["Solar", "Wind", "Hydro"]].sum(axis=1)
        
        # Create an enhanced CO2 intensity forecast plot
        fig = go.Figure()
        
        # Add main CO2 intensity line
        fig.add_trace(go.Scatter(
            x=forecast_df["timestamp"],
            y=forecast_df["co2_intensity"],
            name="CO₂ Intensity",
            line=dict(color="#2C3E50", width=3),
            hovertemplate=
            "<b>%{x|%d %b, %H:%M}</b><br>" +
            "CO₂: %{y:.1f} g/kWh<br>" +
            "<extra></extra>"
        ))
        
        # Add renewable percentage as an area plot
        fig.add_trace(go.Scatter(
            x=forecast_df["timestamp"],
            y=forecast_df["renewable_pct"],
            name="Renewables %",
            fill='tozeroy',
            mode='none',
            fillcolor='rgba(46, 204, 113, 0.2)',
            hoverinfo='skip'
        ))
        
        # Add horizontal lines for thresholds with better styling
        fig.add_shape(
            type="line",
            x0=forecast_df["timestamp"].min(),
            x1=forecast_df["timestamp"].max(),
            y0=low_carbon_threshold,
            y1=low_carbon_threshold,
            line=dict(color="#27AE60", width=2, dash="dash"),
            name="Low Carbon Threshold"
        )
        
        fig.add_shape(
            type="line",
            x0=forecast_df["timestamp"].min(),
            x1=forecast_df["timestamp"].max(),
            y0=high_carbon_threshold,
            y1=high_carbon_threshold,
            line=dict(color="#F39C12", width=2, dash="dash"),
            name="High Carbon Threshold"
        )
        
        fig.add_shape(
            type="line",
            x0=forecast_df["timestamp"].min(),
            x1=forecast_df["timestamp"].max(),
            y0=critical_threshold,
            y1=critical_threshold,
            line=dict(color="#C0392B", width=2, dash="dash"),
            name="Critical Carbon Threshold"
        )
        
        # Add threshold labels
        fig.add_annotation(
            x=forecast_df["timestamp"].min() + timedelta(hours=1),
            y=low_carbon_threshold,
            text="Low Carbon",
            showarrow=False,
            yshift=10,
            font=dict(color="#27AE60")
        )
        
        fig.add_annotation(
            x=forecast_df["timestamp"].min() + timedelta(hours=1),
            y=high_carbon_threshold,
            text="High Carbon",
            showarrow=False,
            yshift=10,
            font=dict(color="#F39C12")
        )
        
        fig.add_annotation(
            x=forecast_df["timestamp"].min() + timedelta(hours=1),
            y=critical_threshold,
            text="Critical",
            showarrow=False,
            yshift=10,
            font=dict(color="#C0392B")
        )
        
        # Find optimal scheduling windows (6-hour duration)
        window_duration = 6
        optimal_windows = []
        
        for i in range(len(forecast_df) - window_duration):
            window = forecast_df.iloc[i:i+window_duration]
            avg_co2 = window["co2_intensity"].mean()
            start_time = window.iloc[0]["timestamp"]
            end_time = window.iloc[-1]["timestamp"]
            
            optimal_windows.append({
                "start": start_time,
                "end": end_time,
                "avg_co2": avg_co2
            })
        
        # Sort by CO2 intensity and get top windows
        optimal_windows.sort(key=lambda x: x["avg_co2"])
        num_highlights = min(5, len(optimal_windows))
        
        # Highlight the optimal scheduling windows on the chart
        for i in range(num_highlights):
            window = optimal_windows[i]
            opacity = 0.3 if i == 0 else max(0.05, 0.2 - (i * 0.04))  # More transparent for less optimal windows
            
            # Add green rectangle to highlight optimal window
            fig.add_shape(
                type="rect",
                x0=window["start"],
                x1=window["end"],
                y0=0,
                y1=forecast_df["co2_intensity"].max() * 1.1,
                fillcolor="#27AE60",
                opacity=opacity,
                layer="below",
                line_width=0,
            )
            
            # Add annotation for the best window
            if i == 0:
                midpoint = window["start"] + (window["end"] - window["start"]) / 2
                fig.add_annotation(
                    x=midpoint,
                    y=forecast_df["co2_intensity"].max() * 0.95,
                    text="Optimal Window",
                    showarrow=True,
                    arrowhead=1,
                    arrowsize=1,
                    arrowcolor="#27AE60",
                    font=dict(color="#27AE60", size=12),
                    arrowwidth=2
                )
        
        # Add vertical line for current time
        fig.add_shape(
            type="line", 
            x0=now, 
            y0=0,
            x1=now, 
            y1=forecast_df["co2_intensity"].max() * 1.1,
            line=dict(color="#3498DB", width=2, dash="solid")
        )
        
        # Add annotation for current time
        fig.add_annotation(
            x=now,
            y=forecast_df["co2_intensity"].max() * 0.9,
            text="Now",
            showarrow=False,
            font=dict(color="#3498DB", size=12)
        )
        
        # Update layout with improved styling
        fig.update_layout(
            title=dict(
                text="CO₂ Intensity Forecast with Optimal Task Windows",
                font=dict(size=20),
                x=0.5,
                xanchor="center"
            ),
            xaxis=dict(
                title="Date & Time",
                gridcolor="rgba(0, 0, 0, 0.1)",
                tickformat="%d %b, %H:%M",
            ),
            yaxis=dict(
                title="CO₂ Intensity (g/kWh)",
                gridcolor="rgba(0, 0, 0, 0.1)",
                zerolinecolor="rgba(0, 0, 0, 0.1)",
                range=[0, forecast_df["co2_intensity"].max() * 1.1]
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            margin=dict(l=0, r=0, t=50, b=0),
            height=450,
            plot_bgcolor="rgba(240, 247, 255, 0.5)",
            hovermode="x unified"
        )
        
        # Add interactive elements
        fig.update_layout(
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(
                            label="Reset View",
                            method="relayout",
                            args=[{"xaxis.range": [forecast_df["timestamp"].min(), forecast_df["timestamp"].max()]}]
                        )
                    ],
                    x=0.05,
                    y=1.1,
                    xanchor="left",
                    yanchor="top"
                )
            ]
        )
        
        # Show the enhanced chart
        st.plotly_chart(fig, use_container_width=True)
        
        # Add explanatory text about the chart
        st.markdown("""
        <div style="background-color: #f0f7ff; padding: 10px; border-radius: 5px; margin-top: 10px;">
            <p style="font-size: 0.9em; margin: 0;">
                <strong>📊 How to Use This Chart:</strong> The line shows predicted carbon intensity of electricity over time. 
                Green highlighted areas indicate optimal windows for scheduling energy-intensive tasks to minimize environmental impact.
                Schedule your GPU tasks during these windows to reduce carbon footprint.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Display grid mix evolution
        st.markdown("### Predicted Grid Energy Mix")
        
        # Sample grid mix at regular intervals
        sample_interval = max(1, len(forecast_df) // 8)  # Show at most 8 time points
        grid_samples = forecast_df.iloc[::sample_interval, :].copy()
        
        # Prepare data for stacked area chart
        grid_mix_data = []
        
        for _, row in grid_samples.iterrows():
            for source in energy_sources:
                grid_mix_data.append({
                    "timestamp": row["timestamp"],
                    "source": source,
                    "percentage": row[source]
                })
        
        grid_mix_df = pd.DataFrame(grid_mix_data)
        
        # Create stacked area chart for energy mix
        fig_mix = px.area(
            grid_mix_df,
            x="timestamp",
            y="percentage",
            color="source",
            title="Predicted Grid Energy Mix Evolution",
            color_discrete_map={
                "Solar": "#F1C40F",
                "Wind": "#3498DB",
                "Hydro": "#2980B9",
                "Nuclear": "#9B59B6",
                "Natural Gas": "#E67E22",
                "Coal": "#7F8C8D"
            }
        )
        
        fig_mix.update_layout(
            xaxis_title="Date & Time",
            yaxis_title="Energy Mix (%)",
            yaxis=dict(range=[0, 100]),
            legend_title="Energy Source",
            height=350,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_mix, use_container_width=True)
    
    with carbon_tabs[1]:
        st.markdown("### CO₂ Savings Calculator for Task Planning")
        
        # Create task configuration form
        st.markdown("""
        <div style="border-left: 4px solid #2ECC71; padding: 10px; background-color: #f0fff0; margin-bottom: 20px;">
            <h4 style="margin-top: 0; color: #2ECC71;">Task Configuration</h4>
            <p style="margin-bottom: 0;">Configure your GPU task to calculate potential carbon savings.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Create columns for inputs
        task_config_cols = st.columns([1.5, 1.5, 1])
        
        with task_config_cols[0]:
            # Basic task parameters
            st.markdown("#### Basic Parameters")
            calc_task_type = st.selectbox(
                "Task Type",
                options=["ML Training", "Inference", "Fine-tuning", "Data Processing", "Rendering"],
                index=0,
                key="calc_task_type"
            )
            
            calc_task_duration = st.slider(
                "Task Duration (hours)",
                min_value=1,
                max_value=48,
                value=8,
                key="calc_task_duration"
            )
            
            calc_gpu_count = st.slider(
                "Number of GPUs",
                min_value=1,
                max_value=8,
                value=2,
                key="calc_gpu_count"
            )
        
        with task_config_cols[1]:
            # GPU and power settings
            st.markdown("#### Hardware Configuration")
            calc_gpu_type = st.selectbox(
                "GPU Type",
                options=["NVIDIA A100", "NVIDIA V100", "NVIDIA T4", "NVIDIA RTX A6000", "AMD MI250"],
                index=0,
                key="calc_gpu_type"
            )
            
            # Power values based on GPU type
            gpu_power_values = {
                "NVIDIA A100": 400,
                "NVIDIA V100": 300,
                "NVIDIA T4": 70,
                "NVIDIA RTX A6000": 300,
                "AMD MI250": 500
            }
            
            # Set default power based on GPU selection
            default_power = gpu_power_values[calc_gpu_type]
            
            calc_gpu_power = st.slider(
                "GPU Power Draw (Watts)",
                min_value=50,
                max_value=600,
                value=default_power,
                key="calc_gpu_power"
            )
            
            calc_utilization = st.slider(
                "Average GPU Utilization (%)",
                min_value=10,
                max_value=100,
                value=85,
                key="calc_gpu_util"
            )
        
        with task_config_cols[2]:
            # Carbon intensity scenarios
            st.markdown("#### Carbon Scenarios")
            
            peak_carbon = forecast_df["co2_intensity"].max().round(1)
            avg_carbon = forecast_df["co2_intensity"].mean().round(1)
            optimal_carbon = optimal_windows[0]["avg_co2"]
            
            calc_peak_carbon = st.number_input(
                "Peak Carbon Intensity (g/kWh)",
                min_value=50.0,
                max_value=500.0,
                value=float(peak_carbon),
                step=10.0,
                key="calc_peak_carbon"
            )
            
            calc_avg_carbon = st.number_input(
                "Average Carbon Intensity (g/kWh)",
                min_value=50.0,
                max_value=500.0,
                value=float(avg_carbon),
                step=10.0,
                key="calc_avg_carbon"
            )
            
            calc_optimal_carbon = st.number_input(
                "Optimal Carbon Intensity (g/kWh)",
                min_value=50.0,
                max_value=500.0,
                value=float(optimal_carbon),
                step=10.0,
                key="calc_optimal_carbon"
            )
        
        # Calculate emissions based on inputs
        task_energy_kwh = (calc_gpu_power * calc_gpu_count * calc_utilization / 100 * calc_task_duration) / 1000
        
        peak_emissions = (calc_peak_carbon * task_energy_kwh) / 1000  # kg CO2
        avg_emissions = (calc_avg_carbon * task_energy_kwh) / 1000  # kg CO2
        optimal_emissions = (calc_optimal_carbon * task_energy_kwh) / 1000  # kg CO2
        
        # Calculate savings
        peak_savings = peak_emissions - optimal_emissions
        peak_savings_pct = (peak_savings / peak_emissions * 100) if peak_emissions > 0 else 0
        
        avg_savings = avg_emissions - optimal_emissions
        avg_savings_pct = (avg_savings / avg_emissions * 100) if avg_emissions > 0 else 0
        
        # Display the results in a visually appealing way
        st.markdown("### Carbon Savings Analysis")
        
        # Emissions comparison chart
        emissions_data = pd.DataFrame({
            "Scenario": ["Peak Hours", "Average Hours", "Optimal Window"],
            "CO₂ Emissions (kg)": [peak_emissions, avg_emissions, optimal_emissions]
        })
        
        fig_emissions = px.bar(
            emissions_data,
            x="Scenario",
            y="CO₂ Emissions (kg)",
            color="Scenario",
            color_discrete_map={
                "Peak Hours": "#E74C3C",
                "Average Hours": "#F39C12",
                "Optimal Window": "#27AE60"
            },
            text_auto='.2f'
        )
        
        fig_emissions.update_layout(
            title="Carbon Emissions Comparison",
            xaxis_title=None,
            showlegend=False,
            height=350
        )
        
        # Add annotations for savings percentages
        fig_emissions.add_annotation(
            x=2,
            y=optimal_emissions * 1.1,
            text=f"{peak_savings_pct:.1f}% reduction<br>vs peak hours",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#27AE60",
            arrowwidth=2,
            arrowsize=1,
            ax=-40,
            ay=-40,
            font=dict(color="#27AE60", size=12)
        )
        
        fig_emissions.add_annotation(
            x=1,
            y=optimal_emissions * 1.1,
            text=f"{avg_savings_pct:.1f}% reduction<br>vs average",
            showarrow=True,
            arrowhead=2,
            arrowcolor="#27AE60",
            arrowwidth=2,
            arrowsize=1,
            ax=-40,
            ay=-40,
            font=dict(color="#27AE60", size=12)
        )
        
        st.plotly_chart(fig_emissions, use_container_width=True)
        
        # Detailed results
        detail_cols = st.columns(2)
        
        with detail_cols[0]:
            st.markdown("#### Task Resource Details")
            st.markdown(f"**Total Energy Consumption:** {task_energy_kwh:.2f} kWh")
            st.markdown(f"**Task Type:** {calc_task_type}")
            st.markdown(f"**Duration:** {calc_task_duration} hours")
            st.markdown(f"**Hardware:** {calc_gpu_count}x {calc_gpu_type}")
            st.markdown(f"**Power Draw:** {calc_gpu_power * calc_gpu_count * calc_utilization / 100:.0f} W (with {calc_utilization}% utilization)")
        
        with detail_cols[1]:
            st.markdown("#### Environmental Impact")
            st.markdown(f"**CO₂ Savings vs Peak:** {peak_savings:.2f} kg ({peak_savings_pct:.1f}%)")
            st.markdown(f"**CO₂ Savings vs Average:** {avg_savings:.2f} kg ({avg_savings_pct:.1f}%)")
            
            # Environmental equivalents
            miles_saved = peak_savings * 2.5  # ~2.5 miles per kg CO2
            trees_day = peak_savings / 21 * 365  # A tree absorbs ~21kg CO2 per year
            lightbulb_hours = peak_savings * 11.5  # 60W bulb for 11.5 hours = 1kg CO2
            
            st.markdown("#### Environmental Equivalents")
            st.markdown(f"Saving {peak_savings:.2f} kg CO₂ compared to peak hours is equivalent to:")
            
            equiv_cols = st.columns(3)
            with equiv_cols[0]:
                st.markdown(f"🚗 **{miles_saved:.1f}** miles<br>not driven", unsafe_allow_html=True)
            with equiv_cols[1]:
                st.markdown(f"🌳 **{trees_day/365:.2f}** trees absorbing<br>CO₂ for a day", unsafe_allow_html=True)
            with equiv_cols[2]:
                st.markdown(f"💡 **{lightbulb_hours:.1f}** hours<br>of 60W bulb off", unsafe_allow_html=True)
        
        # Schedule recommendation
        st.markdown("### Scheduling Recommendation")
        
        best_window = optimal_windows[0]
        start_time = best_window["start"]
        end_time = best_window["end"]
        
        # Check if the task duration fits within the optimal window
        window_duration = (end_time - start_time).total_seconds() / 3600  # in hours
        
        if calc_task_duration <= window_duration:
            recommendation = f"Schedule your task to start at {start_time.strftime('%Y-%m-%d %H:%M')} to minimize carbon impact."
            recommendation_color = "#27AE60"
        else:
            recommendation = f"Your task duration ({calc_task_duration}h) exceeds the optimal window length ({window_duration:.1f}h). Consider splitting the task or accepting sub-optimal scheduling."
            recommendation_color = "#F39C12"
        
        st.markdown(f"""
        <div style="background-color: {recommendation_color}25; border-left: 4px solid {recommendation_color}; padding: 15px; margin-top: 20px;">
            <h4 style="color: {recommendation_color}; margin-top: 0;">Optimal Scheduling Recommendation</h4>
            <p style="margin-bottom: 0;">{recommendation}</p>
        </div>
        """, unsafe_allow_html=True)
        
    with carbon_tabs[2]:
        st.markdown("### Carbon Impact Analytics")
        
        # Create sample historical data
        date_range = pd.date_range(end=datetime.now(), periods=90, freq='D')
        
        # Create historical carbon data
        historical_data = pd.DataFrame({
            "date": date_range,
            "avg_carbon_intensity": np.random.normal(180, 20, 90) + np.sin(np.arange(90) * 0.2) * 10,
            "total_tasks": np.random.randint(5, 20, 90),
            "total_energy": np.random.uniform(40, 200, 90),
            "carbon_saved": np.random.uniform(5, 30, 90)
        })
        
        # Add month and weekday for analysis
        historical_data["month"] = historical_data["date"].dt.month_name()
        historical_data["weekday"] = historical_data["date"].dt.day_name()
        historical_data["week"] = historical_data["date"].dt.isocalendar().week
        
        # Calculate total carbon emissions
        historical_data["carbon_emissions"] = historical_data["avg_carbon_intensity"] * historical_data["total_energy"] / 1000
        
        # Summary metrics
        total_energy = historical_data["total_energy"].sum()
        total_emissions = historical_data["carbon_emissions"].sum()
        total_savings = historical_data["carbon_saved"].sum()
        avg_intensity = historical_data["avg_carbon_intensity"].mean()
        
        # Display summary metrics
        summary_cols = st.columns(4)
        
        with summary_cols[0]:
            st.metric(
                "Total Energy Used",
                f"{total_energy:.1f} kWh",
                delta=None
            )
        
        with summary_cols[1]:
            st.metric(
                "Total CO₂ Emissions",
                f"{total_emissions:.1f} kg",
                delta=None
            )
        
        with summary_cols[2]:
            st.metric(
                "CO₂ Saved by Scheduling",
                f"{total_savings:.1f} kg",
                delta=f"-{(total_savings/(total_emissions+total_savings)*100):.1f}%",
                delta_color="inverse"
            )
        
        with summary_cols[3]:
            st.metric(
                "Avg. Carbon Intensity",
                f"{avg_intensity:.1f} g/kWh",
                delta=None
            )
        
        # Time-based visualizations
        time_cols = st.columns(2)
        
        with time_cols[0]:
            # Monthly carbon intensity
            monthly_data = historical_data.groupby("month")["avg_carbon_intensity"].mean().reset_index()
            month_order = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            monthly_data["month"] = pd.Categorical(monthly_data["month"], categories=month_order, ordered=True)
            monthly_data = monthly_data.sort_values("month")
            
            fig_monthly = px.bar(
                monthly_data,
                x="month",
                y="avg_carbon_intensity",
                title="Average Carbon Intensity by Month",
                color="avg_carbon_intensity",
                color_continuous_scale="RdYlGn_r",
                text_auto='.1f'
            )
            
            fig_monthly.update_layout(
                xaxis_title=None,
                yaxis_title="Carbon Intensity (g/kWh)",
                coloraxis_showscale=False,
                height=300
            )
            
            st.plotly_chart(fig_monthly, use_container_width=True)
        
        with time_cols[1]:
            # Weekday carbon intensity
            weekday_data = historical_data.groupby("weekday")["avg_carbon_intensity"].mean().reset_index()
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekday_data["weekday"] = pd.Categorical(weekday_data["weekday"], categories=weekday_order, ordered=True)
            weekday_data = weekday_data.sort_values("weekday")
            
            fig_weekday = px.bar(
                weekday_data,
                x="weekday",
                y="avg_carbon_intensity",
                title="Average Carbon Intensity by Day of Week",
                color="avg_carbon_intensity",
                color_continuous_scale="RdYlGn_r",
                text_auto='.1f'
            )
            
            fig_weekday.update_layout(
                xaxis_title=None,
                yaxis_title="Carbon Intensity (g/kWh)",
                coloraxis_showscale=False,
                height=300
            )
            
            st.plotly_chart(fig_weekday, use_container_width=True)
        
        # Carbon emissions over time
        emissions_trend = historical_data.resample('W', on='date').agg({
            'carbon_emissions': 'sum',
            'carbon_saved': 'sum'
        }).reset_index()
        
        emissions_trend['potential_emissions'] = emissions_trend['carbon_emissions'] + emissions_trend['carbon_saved']
        
        fig_trend = go.Figure()
        
        # Add potential emissions (if no optimization)
        fig_trend.add_trace(go.Scatter(
            x=emissions_trend['date'],
            y=emissions_trend['potential_emissions'],
            mode='lines',
            line=dict(color='rgba(231, 76, 60, 0.3)', width=0),
            fill='tozeroy',
            fillcolor='rgba(231, 76, 60, 0.3)',
            name='Potential Emissions (No Optimization)',
            hovertemplate="Week of %{x|%Y-%m-%d}<br>Potential Emissions: %{y:.1f} kg CO₂<br><extra></extra>"
        ))
        
        # Add actual emissions
        fig_trend.add_trace(go.Scatter(
            x=emissions_trend['date'],
            y=emissions_trend['carbon_emissions'],
            mode='lines+markers',
            line=dict(color='#2980B9', width=3),
            name='Actual Emissions',
            hovertemplate="Week of %{x|%Y-%m-%d}<br>Actual Emissions: %{y:.1f} kg CO₂<br><extra></extra>"
        ))
        
        # Add savings as a highlighted area
        for i in range(len(emissions_trend)):
            fig_trend.add_shape(
                type="rect",
                x0=emissions_trend['date'].iloc[i] - pd.Timedelta(days=2),
                x1=emissions_trend['date'].iloc[i] + pd.Timedelta(days=2),
                y0=emissions_trend['carbon_emissions'].iloc[i],
                y1=emissions_trend['potential_emissions'].iloc[i],
                fillcolor="rgba(46, 204, 113, 0.5)",
                line=dict(width=0),
                layer="below"
            )
        
        fig_trend.update_layout(
            title="Weekly Carbon Emissions and Savings",
            xaxis_title=None,
            yaxis_title="CO₂ Emissions (kg)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            ),
            height=400,
            hovermode="x unified"
        )
        
        st.plotly_chart(fig_trend, use_container_width=True)
        
        # Add explanatory text about the savings
        total_potential = emissions_trend['potential_emissions'].sum()
        total_actual = emissions_trend['carbon_emissions'].sum()
        total_saved = total_potential - total_actual
        savings_pct = (total_saved / total_potential) * 100
        
        st.markdown(f"""
        <div style="background-color: #27AE6025; border-radius: 5px; padding: 15px; margin-top: 10px;">
            <h4 style="margin-top: 0; color: #27AE60;">Impact Summary</h4>
            <p>Over the last 3 months, green scheduling has saved <strong>{total_saved:.1f} kg CO₂</strong>, 
            a <strong>{savings_pct:.1f}%</strong> reduction compared to standard scheduling.</p>
            <p style="margin-bottom: 0;">This is equivalent to planting <strong>{(total_saved/21):.1f}</strong> trees 
            or avoiding <strong>{(total_saved*2.5):.1f}</strong> miles of driving.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Efficiency metrics
        st.markdown("### Task CO₂ Efficiency")
        
        # Create CO2 efficiency by task type
        task_types = ['ML Training', 'Inference', 'Fine-tuning', 'Data Processing', 'Rendering']
        efficiency_data = pd.DataFrame({
            'task_type': task_types,
            'emissions_per_hour': [0.65, 0.35, 0.55, 0.25, 0.75],
            'optimization_potential': [45, 20, 35, 15, 50]
        })
        
        fig_efficiency = px.bar(
            efficiency_data,
            x='task_type',
            y='emissions_per_hour',
            color='optimization_potential',
            color_continuous_scale='RdYlGn_r',
            title='Carbon Emissions by Task Type',
            labels={
                'task_type': 'Task Type',
                'emissions_per_hour': 'CO₂ Emissions (kg/hr)',
                'optimization_potential': 'Optimization Potential (%)'
            },
            text_auto='.2f'
        )
        
        fig_efficiency.update_layout(
            xaxis_title=None,
            height=350,
            coloraxis_colorbar=dict(
                title="Optimization<br>Potential (%)"
            )
        )
        
        st.plotly_chart(fig_efficiency, use_container_width=True)
        
        # Best practices
        st.markdown("### Best Practices for Carbon Reduction")
        
        best_practices = [
            {
                "title": "Schedule Tasks During Low-Carbon Periods",
                "description": "Use the Carbon Intensity Forecast to schedule non-urgent tasks during periods of lower carbon intensity, typically nights and weekends.",
                "impact": "High"
            },
            {
                "title": "Optimize Model Size",
                "description": "Use smaller, more efficient models when possible to reduce computational requirements.",
                "impact": "High"
            },
            {
                "title": "Increase GPU Utilization",
                "description": "Aim for higher GPU utilization to maximize energy efficiency per computation.",
                "impact": "Medium"
            },
            {
                "title": "Monitor and Track Emissions",
                "description": "Regularly review carbon emissions data to identify optimization opportunities.",
                "impact": "Medium"
            },
            {
                "title": "Use More Efficient GPUs",
                "description": "When possible, select GPUs with better performance per watt metrics.",
                "impact": "High"
            }
        ]
        
        for practice in best_practices:
            impact_color = "#27AE60" if practice["impact"] == "High" else "#F39C12"
            st.markdown(f"""
            <div style="margin-bottom: 10px;">
                <span style="display: inline-block; width: 10px; height: 10px; border-radius: 50%; background-color: {impact_color}; margin-right: 5px;"></span>
                <strong>{practice["title"]}</strong> - {practice["description"]} <span style="color: {impact_color}">({practice["impact"]} Impact)</span>
            </div>
            """, unsafe_allow_html=True)