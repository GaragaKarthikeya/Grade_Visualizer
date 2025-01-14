# analysis.py
import numpy as np
import pandas as pd
import plotly.graph_objects as go

def summarize_statistics(final_values):
    """Return a dictionary of statistical summaries given an array of final CGPA values."""
    if len(final_values) == 0:
        return {}
    arr = np.array(final_values)
    return {
        "count": len(arr),
        "mean": np.mean(arr),
        "median": np.median(arr),
        "std": np.std(arr),
        "min": np.min(arr),
        "max": np.max(arr),
        "variance": np.var(arr),
        "25th_percentile": np.percentile(arr, 25),
        "75th_percentile": np.percentile(arr, 75),
    }

def create_plotly_table(table_data):
    """Return a Plotly Table figure given table data."""
    header_color = 'lightskyblue'
    row_colors = ['white', 'lightgrey']  # alternating row colors
    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=["Path", "Variation", "Final CGPA", "Job Prob(%)", "Insights"],
            fill_color=header_color,
            align='center'
        ),
        cells=dict(
            values=list(zip(*table_data)) if table_data else [[]]*5,
            fill_color=[row_colors * len(table_data)],
            align='left'
        )
    )])
    return fig_table
