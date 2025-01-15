import plotly.graph_objects as go

# Data for plotting
semesters = ["Semester 1", "Semester 2", "Semester 3", "Semester 4", "Semester 5"]
student_a_cgpa = [9.0, 8.75, 8.733333, 8.775, 8.82]
student_b_cgpa = [8.733333, 8.775, 8.82, 9.0, 8.75]

# Create the plot
fig = go.Figure()

# Add traces for each student
fig.add_trace(go.Scatter(
    x=semesters,
    y=student_a_cgpa,
    mode='lines+markers',
    name='Student A (Original Order)',
    line=dict(width=2)
))

fig.add_trace(go.Scatter(
    x=semesters,
    y=student_b_cgpa,
    mode='lines+markers',
    name='Student B (Shuffled Order)',
    line=dict(width=2, dash='dash')
))

# Customize the layout
fig.update_layout(
    title="CGPA Progression: Original vs Shuffled Order",
    xaxis_title="Semesters",
    yaxis_title="CGPA",
    legend_title="Students",
    template="plotly_white",
    font=dict(size=14)
)

# Show the plot
fig.show()
