import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def get_sample_trustlog_data():
    """
    Generate sample AI output logging data for TrustLog
    """
    # Create timestamps for the past 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Sample data
    models = ["GPT-4", "Llama-2", "Claude-2", "Falcon-180B"]
    users = ["user_1", "user_2", "user_3", "user_4", "user_5"]
    content_types = ["Text", "Code", "Image Description", "QA", "Summary"]
    
    # Generate random data
    n_samples = len(timestamps)
    
    data = {
        "timestamp": timestamps,
        "model": np.random.choice(models, n_samples),
        "user": np.random.choice(users, n_samples),
        "content_type": np.random.choice(content_types, n_samples),
        "output_length": np.random.randint(10, 5000, n_samples),
        "verification_status": np.random.choice(["Verified", "Unverified", "Failed"], n_samples, p=[0.8, 0.15, 0.05]),
        "risk_score": np.random.randint(0, 100, n_samples)
    }
    
    return pd.DataFrame(data)

def get_sample_risk_data():
    """
    Generate sample risk score data for AgentGuard
    """
    # Create timestamps for the past 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='3H')
    
    # Models
    models = ["GPT-4", "Llama-2", "Claude-2"]
    
    # Generate data for each model
    data = []
    
    for model in models:
        # Base risk level for the model
        base_risk = 50 if model == "GPT-4" else (60 if model == "Llama-2" else 40)
        
        # Daily variation - risk generally lower at night, higher during day
        for ts in timestamps:
            hour = ts.hour
            
            # Hour factor - higher during business hours
            hour_factor = -10 if 1 <= hour <= 5 else (15 if 9 <= hour <= 17 else 0)
            
            # Random variation
            random_var = np.random.normal(0, 8)
            
            # Calculate risk score with constraints
            risk_score = max(5, min(95, base_risk + hour_factor + random_var))
            
            data.append({
                "timestamp": ts,
                "model": model,
                "risk_score": risk_score
            })
    
    return pd.DataFrame(data)

def get_risk_threshold_data():
    """
    Generate sample risk threshold data for AgentGuard settings
    """
    models = ["GPT-4", "Llama-2", "Claude-2", "Falcon-180B"]
    
    data = []
    
    for model in models:
        data.append({
            "model": model,
            "risk_level": "Low",
            "min_threshold": 0,
            "max_threshold": 40,
            "action": "Allow All Output"
        })
        
        data.append({
            "model": model,
            "risk_level": "Medium",
            "min_threshold": 40,
            "max_threshold": 70,
            "action": "Allow with Warning"
        })
        
        data.append({
            "model": model,
            "risk_level": "High",
            "min_threshold": 70,
            "max_threshold": 90,
            "action": "Require Human Review"
        })
        
        data.append({
            "model": model,
            "risk_level": "Critical",
            "min_threshold": 90,
            "max_threshold": 100,
            "action": "Block Output"
        })
    
    return pd.DataFrame(data)

def get_gpu_emission_data():
    """
    Generate sample CO2 emission data for GreenGPU
    """
    # Create timestamps for the past 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate CO2 intensity data
    # CO2 intensity tends to be lower at night when renewable energy is a larger portion of the grid
    data = []
    
    for ts in timestamps:
        hour = ts.hour
        
        # Base CO2 value (average grid intensity)
        base_co2 = 180
        
        # Daily cycle: lower at night (2-5 AM), higher during peak hours (6-9 PM)
        hour_factor = 30 * np.sin(np.pi * (hour - 2) / 24)
        
        # Add some random variation
        random_var = np.random.normal(0, 15)
        
        # Ensure we don't go below realistic minimums
        co2_intensity = max(50, base_co2 + hour_factor + random_var)
        
        data.append({
            "timestamp": ts,
            "co2_intensity": co2_intensity
        })
    
    return pd.DataFrame(data)

def get_gpu_temperature_data():
    """
    Generate sample GPU temperature data for GreenGPU
    """
    # Create timestamps for the past 7 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='H')
    
    # Generate temperature data
    # Temperature tends to follow workload patterns and ambient temperature
    data = []
    
    for ts in timestamps:
        hour = ts.hour
        
        # Base temperature
        base_temp = 65
        
        # Higher during working hours
        hour_factor = 8 if 9 <= hour <= 17 else 0
        
        # Add some random variation
        random_var = np.random.normal(0, 3)
        
        # Calculate temperature
        avg_temperature = base_temp + hour_factor + random_var
        
        data.append({
            "timestamp": ts,
            "avg_temperature": avg_temperature
        })
    
    return pd.DataFrame(data)

def get_gpu_health_data(gpu_id="gpu-1"):
    """
    Generate sample GPU health data for the GPU Health page
    
    Args:
        gpu_id (str): GPU identifier
    
    Returns:
        DataFrame: Generated health data
    """
    # Create timestamps for the past 90 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    timestamps = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Generate health scores
    # Generally declining over time with fluctuations
    
    # Base starting score (newer GPUs start higher)
    gpu_number = int(gpu_id.split('-')[1])
    base_score = 95 - (gpu_number * 3) % 15
    
    # Decline rate (some GPUs decline faster)
    decline_rate = 0.1 + (gpu_number * 0.02) % 0.1
    
    # Generate health scores
    health_scores = []
    memory_health = []
    temp_stability = []
    power_efficiency = []
    perf_consistency = []
    
    for i, _ in enumerate(timestamps):
        # Calculate decline
        decline = decline_rate * i
        
        # Add random variation
        random_var = np.random.normal(0, 5)
        
        # Random events (occasional drops or improvements)
        event_factor = 0
        if np.random.random() < 0.05:  # 5% chance of an event
            event_factor = np.random.choice([-10, -5, 5]) 
        
        # Calculate health score with constraints
        score = max(10, min(100, base_score - decline + random_var + event_factor))
        health_scores.append(score)
        
        # Component scores
        mem_health = max(10, min(100, score + np.random.normal(0, 8)))
        memory_health.append(mem_health)
        
        temp_stab = max(10, min(100, score + np.random.normal(0, 10)))
        temp_stability.append(temp_stab)
        
        power_eff = max(10, min(100, score + np.random.normal(0, 7)))
        power_efficiency.append(power_eff)
        
        perf_cons = max(10, min(100, score + np.random.normal(0, 12)))
        perf_consistency.append(perf_cons)
    
    # Create DataFrame
    data = {
        "timestamp": timestamps,
        "health_score": health_scores,
        "memory_health": memory_health,
        "temp_stability": temp_stability,
        "power_efficiency": power_efficiency,
        "perf_consistency": perf_consistency
    }
    
    return pd.DataFrame(data)
