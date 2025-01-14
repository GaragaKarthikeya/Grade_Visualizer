# plotting.py
import plotly.graph_objects as go
import numpy as np

def create_histogram(final_values):
    fig = go.Figure(go.Histogram(x=final_values, nbinsx=10, marker_color='lightskyblue'))
    fig.update_layout(title="Histogram of Final CGPAs", xaxis_title="Final CGPA", yaxis_title="Count")
    return fig

def create_box_plot(final_values):
    fig = go.Figure(go.Box(y=final_values, name="Final CGPAs", boxpoints="all", jitter=0.5, marker_color="indianred"))
    fig.update_layout(title="Box Plot of Final CGPAs")
    return fig

def create_pie_chart(final_values):
    arr = np.array(final_values)
    success_count = np.sum(arr >= 3.0)
    struggle_count = len(arr) - success_count
    fig = go.Figure(go.Pie(labels=["CGPA≥3.0", "CGPA<3.0"], values=[success_count, struggle_count], hole=0.4))
    fig.update_layout(title="CGPA≥3.0 vs. CGPA<3.0")
    return fig
