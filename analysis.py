# analysis.py

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from math import sqrt
from typing import List, Dict, Any

def categorize_cgpa(cgpa: float) -> str:
    """
    Assign a label (emoji + text) based on the CGPA range.
    Helps with conditional formatting in tables.
    """
    if cgpa < 2.0:
        return "🔴 Very Low"
    elif cgpa < 3.0:
        return "🟠 Below 3.0"
    elif cgpa < 3.5:
        return "🟡 Safe Zone"
    elif cgpa < 3.6:
        return "🟢 Strong"
    elif cgpa < 3.8:
        return "🔵 Dean's List Range"
    else:
        return "💎 Near Perfection"

def summarize_statistics(final_values: List[float]) -> Dict[str, float]:
    """
    Return a dictionary of extended statistical summaries
    given an array of final CGPA values.
    """
    if len(final_values) == 0:
        return {}

    arr = np.array(final_values)
    mean_val = np.mean(arr)
    n = len(arr)

    # 95% Confidence Interval for the mean (approx. for demonstration)
    # Typically uses t-distribution for small n, but we keep it simple here.
    std_err = np.std(arr, ddof=1) / sqrt(n)
    ci_lower = mean_val - 1.96 * std_err
    ci_upper = mean_val + 1.96 * std_err

    return {
        "count": n,
        "mean": mean_val,
        "median": np.median(arr),
        "std": np.std(arr, ddof=1),
        "min": np.min(arr),
        "max": np.max(arr),
        "variance": np.var(arr, ddof=1),
        "25th_percentile": np.percentile(arr, 25),
        "75th_percentile": np.percentile(arr, 75),
        "95ci_lower": ci_lower,
        "95ci_upper": ci_upper,
    }

def compute_category_counts(final_values: List[float]) -> Dict[str, int]:
    """
    Return the count of each CGPA category in the final results.
    """
    counts = {
        "🔴 Very Low": 0,
        "🟠 Below 3.0": 0,
        "🟡 Safe Zone": 0,
        "🟢 Strong": 0,
        "🔵 Dean's List Range": 0,
        "💎 Near Perfection": 0,
    }
    for val in final_values:
        cat = categorize_cgpa(val)
        if cat in counts:
            counts[cat] += 1
        else:
            # If a category not in dictionary, initialize
            counts[cat] = 1
    return counts

def create_plotly_table(table_data: List[List[Any]]) -> go.Figure:
    """
    Return a Plotly Table figure given table data.
    Each item in table_data: [Path, Variation, Final CGPA, Job Prob, Insights, Category].
    We'll do conditional coloring in the table cells based on category.
    """
    if not table_data:
        # if no data, return an empty figure
        return go.Figure(data=[go.Table(header=dict(values=[]), cells=dict(values=[]))])

    # Transpose the table_data for Plotly
    columns = list(zip(*table_data))  # Path, Variation, CGPA, JobProb, Insights, Category
    # We'll do color mapping: e.g., color cell if category is certain
    # category is the last item in columns
    category_col = columns[-1]

    # Build the fill_color array
    fill_colors = []
    for cat in category_col:
        if "🔴" in cat:
            fill_colors.append("rgb(255, 204, 204)")  # light red
        elif "🟠" in cat:
            fill_colors.append("rgb(255, 229, 204)")  # light orange
        elif "🟡" in cat:
            fill_colors.append("rgb(255, 255, 204)")  # light yellow
        elif "🟢" in cat:
            fill_colors.append("rgb(218, 240, 218)")  # light green
        elif "🔵" in cat:
            fill_colors.append("rgb(210, 233, 255)")  # light blue
        elif "💎" in cat:
            fill_colors.append("rgb(225, 225, 255)")  # slightly different pastel
        else:
            fill_colors.append("white")

    # We'll apply a row-based approach for fill_color
    # But we want the category column specifically colored.
    # Approach: we color only the category column. The rest remain white or alternate row color.
    # For simplicity, we'll fill entire row with the category color, or do stripes if desired.
    # Let's do entire row color for emphasis:

    fill_colors_by_row = []
    for i, cat_color in enumerate(fill_colors):
        fill_colors_by_row.append([cat_color]*len(columns))  # entire row same color

    fig_table = go.Figure(data=[go.Table(
        header=dict(
            values=["Path", "Variation", "Final CGPA", "Job Prob(%)", "Insights", "Category"],
            fill_color="rgb(180, 210, 255)",
            align='center',
            font=dict(color="black", size=12)
        ),
        cells=dict(
            values=columns,
            fill_color=fill_colors_by_row,
            align='left',
            font=dict(color="black", size=11)
        )
    )])
    fig_table.update_layout(width=800, height=600)
    return fig_table

def generate_category_distribution_bar(final_values: List[float]) -> go.Figure:
    """
    Create a bar chart that displays how many CGPAs fall into each category.
    """
    cat_counts = compute_category_counts(final_values)
    categories = list(cat_counts.keys())
    counts = list(cat_counts.values())

    fig_bar = go.Figure(data=[go.Bar(x=categories, y=counts, text=counts, textposition='auto')])
    fig_bar.update_layout(
        title="Count of CGPA Categories",
        xaxis_title="Category",
        yaxis_title="Count",
        template="plotly_white"
    )
    return fig_bar
