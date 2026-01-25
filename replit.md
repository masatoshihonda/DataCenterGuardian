# Overview

Prefrontal™ is an AI Infrastructure Governance and Cross-border Energy Optimization platform built using Streamlit. The system provides comprehensive monitoring and control capabilities for AI workloads across multiple domains including environmental optimization, hardware health monitoring, risk management, output verification, and system synchronization. The platform focuses on sustainable AI operations by integrating environmental factors, predictive maintenance, and security controls into a unified dashboard interface.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit-based web application with multi-page architecture
- **Page Structure**: Modular design with separate pages for each major feature (GreenGPU, GPU Health, AgentGuard, TrustLog, EdgeSync)
- **UI Components**: Custom CSS styling for professional appearance, integrated Plotly visualizations for interactive charts and dashboards
- **Navigation**: Tab-based interfaces within pages for organizing related functionality

## Core Modules
- **GreenGPU**: Environmental optimization module that schedules GPU tasks based on CO2 emissions and temperature data
- **GPU Health**: Hardware monitoring system with predictive maintenance capabilities and memory fragmentation analysis
- **AgentGuard**: Risk-based output control system that dynamically adjusts AI output modes based on calculated risk scores
- **TrustLog**: Cryptographic verification system for AI outputs with integrity checking and audit trails
- **EdgeSync**: System-wide monitoring dashboard for AI infrastructure coordination

## Data Layer
- **Data Generation**: Synthetic data generation utilities for simulation and testing purposes
- **Time Series Data**: Historical metrics tracking with configurable time ranges and frequencies
- **Risk Assessment**: Dynamic risk scoring algorithms with configurable thresholds
- **Verification Systems**: Hash-based output verification and signature validation

## Visualization Layer
- **Charting Library**: Plotly Express and Plotly Graph Objects for interactive visualizations
- **Dashboard Components**: Gauge charts, time series plots, status indicators, and metric cards
- **Real-time Updates**: Dynamic data refresh capabilities for live monitoring
- **Custom Styling**: CSS-based theming for consistent visual identity

## Security and Governance
- **Output Verification**: Cryptographic hash generation and verification for AI outputs
- **Risk Management**: Multi-tier risk assessment with automated threshold-based controls
- **Audit Logging**: Comprehensive logging system for all AI operations and decisions
- **Access Control**: User-based filtering and permission systems

# External Dependencies

## Core Framework
- **Streamlit**: Web application framework for the entire user interface
- **Pandas**: Data manipulation and analysis for all data processing operations
- **NumPy**: Numerical computations for data generation and calculations

## Visualization
- **Plotly Express**: High-level statistical visualization library
- **Plotly Graph Objects**: Low-level plotting library for custom chart components

## Machine Learning
- **Scikit-learn**: Machine learning utilities including LinearRegression and StandardScaler for predictive maintenance features

## Data Processing
- **Datetime**: Built-in Python library for timestamp and time range management
- **Hashlib**: Cryptographic hashing for output verification
- **Base64**: Encoding utilities for data serialization
- **Time**: System time utilities for real-time operations

## Potential Integrations
- **GPU Monitoring APIs**: Hardware monitoring interfaces for real-world GPU metrics
- **Environmental Data Sources**: External APIs for CO2 emissions and environmental data
- **Authentication Services**: User management and access control systems
- **Database Systems**: Persistent storage for historical data and configurations