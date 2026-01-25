import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime, timedelta


def create_gauge_chart(value, title, min_val=0, max_val=100, threshold=None):
    """
    Create a gauge chart for displaying metrics
    
    Args:
        value (float): The value to display
        title (str): The title of the gauge
        min_val (float): Minimum value on gauge
        max_val (float): Maximum value on gauge
        threshold (float, optional): Threshold value to mark on gauge
    
    Returns:
        plotly.graph_objects.Figure: The gauge chart figure
    """
    # Determine color based on value
    if value < max_val * 0.4:
        color = "red"
    elif value < max_val * 0.7:
        color = "orange"
    else:
        color = "green"

    # Create figure
    fig = go.Figure(
        go.Indicator(mode="gauge+number",
                     value=value,
                     domain={
                         'x': [0, 1],
                         'y': [0, 1]
                     },
                     title={'text': title},
                     gauge={
                         'axis': {
                             'range': [min_val, max_val]
                         },
                         'bar': {
                             'color': color
                         },
                         'steps': [{
                             'range': [min_val, max_val * 0.4],
                             'color': "red"
                         }, {
                             'range': [max_val * 0.4, max_val * 0.7],
                             'color': "orange"
                         }, {
                             'range': [max_val * 0.7, max_val],
                             'color': "green"
                         }]
                     }))

    # Add threshold if specified
    if threshold is not None:
        fig.update_layout(shapes=[
            dict(type='line',
                 x0=0,
                 x1=1,
                 y0=threshold,
                 y1=threshold,
                 line=dict(color='red', width=3, dash='dash'))
        ])

    # Update layout
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))

    return fig


def create_time_series(df,
                       x_col,
                       y_col,
                       title,
                       color=None,
                       mode='lines+markers'):
    """
    Create a time series plot
    
    Args:
        df (pandas.DataFrame): The dataframe containing the data
        x_col (str): The column name for x-axis (usually timestamp)
        y_col (str): The column name for y-axis
        title (str): The title of the plot
        color (str, optional): Column name to use for color
        mode (str): Plot mode ('lines', 'markers', 'lines+markers')
    
    Returns:
        plotly.graph_objects.Figure: The time series figure
    """
    if color:
        fig = px.line(df,
                      x=x_col,
                      y=y_col,
                      color=color,
                      title=title,
                      labels={
                          x_col: x_col,
                          y_col: y_col
                      })
    else:
        fig = px.line(df,
                      x=x_col,
                      y=y_col,
                      title=title,
                      labels={
                          x_col: x_col,
                          y_col: y_col
                      })

    # Update layout
    fig.update_layout(xaxis_title=x_col,
                      yaxis_title=y_col,
                      legend_title_text='Legend',
                      height=400,
                      margin=dict(l=20, r=20, t=50, b=20))

    return fig


def create_heatmap(data, x_labels, y_labels, title):
    """
    Create a heatmap visualization
    
    Args:
        data (numpy.ndarray): 2D array of values
        x_labels (list): Labels for x-axis
        y_labels (list): Labels for y-axis
        title (str): The title of the heatmap
    
    Returns:
        plotly.graph_objects.Figure: The heatmap figure
    """
    fig = go.Figure(data=go.Heatmap(
        z=data, x=x_labels, y=y_labels, colorscale='Viridis', showscale=True))

    fig.update_layout(title=title,
                      height=400,
                      margin=dict(l=20, r=20, t=50, b=20))

    return fig


def create_bar_chart(df, x_col, y_col, title, color=None):
    """
    Create a bar chart
    
    Args:
        df (pandas.DataFrame): The dataframe containing the data
        x_col (str): The column name for x-axis
        y_col (str): The column name for y-axis
        title (str): The title of the plot
        color (str, optional): Column name to use for color
    
    Returns:
        plotly.graph_objects.Figure: The bar chart figure
    """
    if color:
        fig = px.bar(df,
                     x=x_col,
                     y=y_col,
                     color=color,
                     title=title,
                     labels={
                         x_col: x_col,
                         y_col: y_col
                     })
    else:
        fig = px.bar(df,
                     x=x_col,
                     y=y_col,
                     title=title,
                     labels={
                         x_col: x_col,
                         y_col: y_col
                     })

    # Update layout
    fig.update_layout(xaxis_title=x_col,
                      yaxis_title=y_col,
                      height=400,
                      margin=dict(l=20, r=20, t=50, b=20))

    return fig


def create_pie_chart(df, values, names, title):
    """
    Create a pie chart
    
    Args:
        df (pandas.DataFrame): The dataframe containing the data
        values (str): The column name for values
        names (str): The column name for segment names
        title (str): The title of the plot
    
    Returns:
        plotly.graph_objects.Figure: The pie chart figure
    """
    fig = px.pie(df, values=values, names=names, title=title)

    # Update layout
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=50, b=20))

    return fig
