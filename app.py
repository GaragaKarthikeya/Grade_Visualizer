import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import io  # for PDF export
from reportlab.pdfgen import canvas  # minimal PDF generation

from rich.console import Console

# Import path functions from your paths.py
from paths import (
    generate_balanced_growth, generate_high_achiever, generate_downfall_recovery,
    generate_up_down, generate_perfectionist, generate_consistent_improvement,
    generate_chaotic, generate_late_bloomer, generate_spike_plateau, generate_senioritis,
    generate_no_study, generate_burnout, generate_triumph_over_adversity
)

# ----------------------------------------------------------------------------------
# 1. Caching & Setup
# ----------------------------------------------------------------------------------
@st.cache_data
def compute_trajectory(_func, start_cgpa, steps, seed=None):
    """Uses the path-generation function to compute a trajectory, cached by Streamlit."""
    return _func(start_cgpa, steps=steps, seed=seed)

# Minimal placeholder function: job placement probability
def estimate_job_probability(final_cgpa):
    """Mock logic for demonstration purposes."""
    if final_cgpa < 2.5:
        return 0.4
    elif final_cgpa < 3.0:
        return 0.5
    elif final_cgpa < 3.5:
        return 0.7
    elif final_cgpa < 3.8:
        return 0.85
    else:
        return 0.95

# Initialize styling
sns.set_theme(style="darkgrid")
console = Console()

# ----------------------------------------------------------------------------------
# 2. Streamlit App
# ----------------------------------------------------------------------------------
def main():
    st.title("The Ultimate CGPA Multiverse: Extended Stats Edition")
    st.markdown("""
    Explore how your CGPA evolves under different academic scenarios, 
    now with **additional statistical analyses** for more in-depth insights.
    """)

    # 2.1 Sidebar Inputs
    st.sidebar.header("User Inputs")
    variations = st.sidebar.slider("How many trajectories per path?", 1, 10, 5)
    all_paths = [
        "Balanced Growth", "High Achiever", "Downfall & Recovery", "Up & Down",
        "Perfectionist", "Consistent Improve", "Chaotic", "Late Bloomer",
        "Spike Plateau", "Senioritis", "No Study",
        "Burnout", "Triumph Over Adversity"
    ]
    selected_paths = st.sidebar.multiselect(
        "Select which paths to simulate:",
        options=all_paths,
        default=["Balanced Growth", "High Achiever"]
    )
    current_semester = st.sidebar.slider("Current Semester (1 to 10)", 1, 10, 1)
    current_cgpa = st.sidebar.slider("Current CGPA (0.0 to 4.0)", 0.0, 4.0, 2.91, 0.01)

    with st.sidebar.expander("What-If Future CGPA Adjustments"):
        st.markdown("Hypothesize future performance to see potential impacts on your final CGPA.")
        what_if_adjust = st.slider("Adjust future CGPAs by ± ...", -1.0, 1.0, 0.0, 0.05)
        st.write(f"Applying {what_if_adjust:.2f} to each future step as a 'What-If' scenario.")

    # Determine steps & future semesters
    steps = 1 if current_semester >= 10 else 10 - current_semester + 1
    future_semesters = np.arange(current_semester, current_semester + steps)

    # Path function map
    path_map = {
        "Balanced Growth": generate_balanced_growth,
        "High Achiever": generate_high_achiever,
        "Downfall & Recovery": generate_downfall_recovery,
        "Up & Down": generate_up_down,
        "Perfectionist": generate_perfectionist,
        "Consistent Improve": generate_consistent_improvement,
        "Chaotic": generate_chaotic,
        "Late Bloomer": generate_late_bloomer,
        "Spike Plateau": generate_spike_plateau,
        "Senioritis": generate_senioritis,
        "No Study": generate_no_study,
        "Burnout": generate_burnout,
        "Triumph Over Adversity": generate_triumph_over_adversity
    }

    fig = go.Figure()
    final_cgpas = []

    for path_name in selected_paths:
        for variation_index in range(variations):
            seed_for_variation = (42 + hash(path_name) + variation_index) % (2**32)
            traj = compute_trajectory(path_map[path_name], current_cgpa, steps, seed_for_variation)

            # Apply the "What-If" scenario adjust
            for i in range(1, len(traj)):
                new_val = traj[i] + what_if_adjust
                traj[i] = min(max(2.0, new_val), 4.0)

            # Record final CG
            final_cgpas.append((path_name, variation_index + 1, traj[-1]))

            # Hover data for next CG
            customdata = []
            for idx in range(len(traj)):
                if idx < len(traj)-1:
                    customdata.append(f"{traj[idx+1]:.2f}")
                else:
                    customdata.append("N/A")

            fig.add_trace(go.Scatter(
                x=future_semesters,
                y=traj,
                customdata=customdata,
                mode='lines+markers',
                name=f"{path_name} Var {variation_index+1}" if variation_index == 0 else None,
                hovertemplate=(
                    "Semester: %{x}<br>"
                    "CGPA: %{y:.2f}<br>"
                    "Next CGPA: %{customdata}<extra>%{fullData.name}</extra>"
                )
            ))

    fig.update_layout(
        title="CGPA Evolution with Additional Stats",
        xaxis_title="Semester",
        yaxis_title="Cumulative CGPA",
        hovermode="closest",
        transition_duration=500
    )
    fig.add_hline(
        y=3.6,
        line_dash="dash",
        line_color="gray",
        annotation_text="Dean's List (3.6)",
        annotation_position="bottom right"
    )

    st.plotly_chart(fig, use_container_width=True)

    # 2.2 More Analysis
    st.subheader("Post-Simulation Analysis & Statistics")
    table_data = []
    final_values_only = []
    for p_name, var_idx, final_val in final_cgpas:
        job_prob = estimate_job_probability(final_val)
        # Basic category message
        if final_val < 3.0:
            category_msg = ("Below 3.0: Could face interview filters.\n"
                            "Tip: Boost fundamentals + real-world projects.")
        elif final_val < 3.5:
            category_msg = ("3.0-3.5: Safe for many roles.\n"
                            "Tip: Strong projects/internships can stand out.")
        elif final_val < 3.6:
            category_msg = ("3.5-3.6: You stand out.\n"
                            "Tip: Aim for advanced courses or certifications.")
        elif final_val < 3.8:
            category_msg = ("3.6-3.8: Dean's List territory.\n"
                            "Tip: Leadership roles, hackathons, or research.")
        else:
            category_msg = ("3.8-4.0: Near perfection!\n"
                            "Tip: Expand to open-source or specialized R&D.")
        table_data.append([p_name, var_idx, f"{final_val:.2f}", f"{job_prob*100:.1f}%", category_msg])
        final_values_only.append(final_val)

    # Summaries
    df_table = pd.DataFrame(table_data, columns=["Path", "Variation", "Final CGPA", "Job Prob(%)", "Insights"])
    st.table(df_table)

    st.markdown("### Statistical Summary of Final CGPAs")
    final_arr = np.array(final_values_only)
    if len(final_arr) > 0:
        mean_val = np.mean(final_arr)
        median_val = np.median(final_arr)
        std_val = np.std(final_arr)
        min_val = np.min(final_arr)
        max_val = np.max(final_arr)

        st.write(f"**Count**: {len(final_arr)}")
        st.write(f"**Mean**: {mean_val:.2f}")
        st.write(f"**Median**: {median_val:.2f}")
        st.write(f"**Std Dev**: {std_val:.2f}")
        st.write(f"**Min**: {min_val:.2f}")
        st.write(f"**Max**: {max_val:.2f}")
    else:
        st.write("No final CGPAs computed (maybe no paths selected).")

    # Additional charts
    st.markdown("#### Final CGPA Distributions")
    col1, col2 = st.columns(2)

    with col1:
        # Histogram
        if len(final_arr) > 0:
            hist_fig = go.Figure()
            hist_fig.add_trace(go.Histogram(x=final_arr, nbinsx=10, marker_color='lightskyblue'))
            hist_fig.update_layout(
                title="Histogram of Final CGPAs",
                xaxis_title="Final CGPA",
                yaxis_title="Count"
            )
            st.plotly_chart(hist_fig, use_container_width=True)

    with col2:
        if len(final_arr) > 0:
            # Box Plot
            box_fig = go.Figure()
            box_fig.add_trace(go.Box(y=final_arr, name="Final CGPAs", boxpoints="all", jitter=0.5, marker_color="indianred"))
            box_fig.update_layout(title="Box Plot of Final CGPAs")
            st.plotly_chart(box_fig, use_container_width=True)

    st.markdown("#### Ratio: CGPA>=3.0 vs. CGPA<3.0")
    if len(final_arr) > 0:
        success_count = np.sum(final_arr >= 3.0)
        struggle_count = len(final_arr) - success_count
        pie_fig = go.Figure(data=[go.Pie(
            labels=["CGPA≥3.0", "CGPA<3.0"],
            values=[success_count, struggle_count],
            hole=0.4
        )])
        pie_fig.update_layout(title="CGPA≥3.0 vs. CGPA<3.0")
        st.plotly_chart(pie_fig, use_container_width=True)

    st.markdown("""
    **Note**: CGPA is not the sole factor. The *Job Probability* column is a 
    placeholder estimate. Real outcomes depend on internships, projects, networking, etc.
    """)

    # (11) Export Options: CSV and minimal PDF
    st.markdown("### Export Simulation Results")
    csv_data = df_table.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv_data,
        file_name="cgpa_simulation_results.csv",
        mime="text/csv"
    )

    if st.button("Download as PDF"):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer)
        c.setFont("Helvetica", 12)
        c.drawString(100, 800, "CGPA Simulation Results")
        y_pos = 770
        for row in table_data:
            line = f"{row[0]} (Var {row[1]}): CGPA={row[2]}, Prob={row[3]}, {row[4]}"
            c.drawString(50, y_pos, line)
            y_pos -= 20
        c.save()
        st.download_button(
            label="Download PDF",
            data=buffer.getvalue(),
            file_name="cgpa_results.pdf",
            mime="application/pdf"
        )

    with st.expander("Skill-based Quizzes"):
        st.markdown("*Placeholder*: Possibly add timed quizzes, daily challenge, etc.")

    with st.expander("Project Recommendations"):
        st.markdown("*Placeholder*: Provide curated project ideas based on CGPA and user interests.")

    st.markdown("""
    **Potential Next Steps**:
    1. Machine learning integration for real predictive modeling.
    2. Real-time data from an LMS or grade logs.
    3. Multiplayer mode or leaderboards.
    4. Deeper gamification with achievements or badges.
    """)


if __name__ == "__main__":
    main()
