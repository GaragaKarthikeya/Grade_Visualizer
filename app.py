import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import io
from reportlab.pdfgen import canvas

from rich.console import Console

from paths import (
    generate_balanced_growth, generate_high_achiever, generate_downfall_recovery,
    generate_up_down, generate_perfectionist, generate_consistent_improvement,
    generate_chaotic, generate_late_bloomer, generate_spike_plateau, generate_senioritis,
    generate_no_study, generate_burnout, generate_triumph_over_adversity
)
from analysis import summarize_statistics, create_plotly_table
from plotting import create_histogram, create_box_plot, create_pie_chart

@st.cache_data
def compute_trajectory(_func, start_cgpa, steps, seed=None):
    return _func(start_cgpa, steps=steps, seed=seed)

sns.set_theme(style="darkgrid")
console = Console()

def estimate_job_probability(final_cgpa):
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

def main():
    st.title("The Ultimate CGPA Multiverse: Extended Stats Edition")
    st.markdown("""
    Explore how your CGPA evolves under different scenarios, now with richer statistical insights!
    """)

    # Sidebar Inputs
    st.sidebar.header("User Inputs")
    variations = st.sidebar.slider("How many trajectories per path?", 1, 10, 5)
    all_paths = [
        "Balanced Growth", "High Achiever", "Downfall & Recovery", "Up & Down",
        "Perfectionist", "Consistent Improve", "Chaotic", "Late Bloomer",
        "Spike Plateau", "Senioritis", "No Study", "Burnout", "Triumph Over Adversity"
    ]
    selected_paths = st.sidebar.multiselect(
        "Select paths to simulate:",
        options=all_paths,
        default=["Balanced Growth", "High Achiever"]
    )
    current_semester = st.sidebar.slider("Current Semester (1 to 10)", 1, 10, 1)
    current_cgpa = st.sidebar.slider("Current CGPA (0.0 to 4.0)", 0.0, 4.0, 2.91, 0.01)

    with st.sidebar.expander("What-If Future CGPA Adjustments"):
        st.markdown("Hypothesize future performance to see potential impacts on your final CGPA.")
        what_if_adjust = st.slider("Adjust future CGPAs by ±", -1.0, 1.0, 0.0, 0.05)
        st.write(f"Applying an adjustment of {what_if_adjust:.2f} to future steps.")

    st.sidebar.markdown("### Additional Options")
    with st.sidebar.expander("Advanced Options"):
        st.write("Future: Tweak growth rates, add event triggers, etc.")

    steps = 1 if current_semester >= 10 else 10 - current_semester + 1
    future_semesters = np.arange(current_semester, current_semester + steps)

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

    st.sidebar.markdown("---")
    st.sidebar.write("All inputs set. Running simulation...")

    fig = go.Figure()
    final_cgpas = []

    for path_name in selected_paths:
        func = path_map[path_name]
        for variation_index in range(variations):
            seed = (42 + hash(path_name) + variation_index) % (2**32)
            traj = compute_trajectory(func, current_cgpa, steps, seed)

            for i in range(1, len(traj)):
                traj[i] = min(max(2.0, traj[i] + what_if_adjust), 4.0)

            final_cgpas.append((path_name, variation_index + 1, traj[-1]))

            customdata = []
            for idx in range(len(future_semesters)):
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
        title="CGPA Evolution with Extended Analysis",
        xaxis_title="Semester",
        yaxis_title="Cumulative CGPA",
        hovermode="closest",
        transition_duration=500
    )
    fig.add_hline(y=3.6, line_dash="dash", line_color="gray",
                  annotation_text="Dean's List (3.6)", annotation_position="bottom right")

    tabs = st.tabs(["Interactive Graph", "Post-Simulation Analysis", "Distributions & Exports"])

    with tabs[0]:
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        table_data = []
        final_values_only = []
        for p_name, var_idx, final_val in final_cgpas:
            job_prob = estimate_job_probability(final_val)
            if final_val < 3.0:
                advice = "Below 3.0: Face filters. Boost fundamentals."
            elif final_val < 3.5:
                advice = "3.0-3.5: Safe zone. Strengthen projects."
            elif final_val < 3.6:
                advice = "3.5-3.6: Stand out. Aim higher."
            elif final_val < 3.8:
                advice = "3.6-3.8: Dean's List potential. Seek leadership."
            else:
                advice = "3.8-4.0: Near perfection. Expand to R&D."
            table_data.append([p_name, var_idx, f"{final_val:.2f}", f"{job_prob*100:.1f}%", advice])
            final_values_only.append(final_val)

        st.subheader("Post-Simulation Analysis")
        plotly_table = create_plotly_table(table_data)
        st.plotly_chart(plotly_table, use_container_width=True)

        st.markdown("### Statistical Summary of Final CGPAs")
        if final_values_only:
            stats = summarize_statistics(final_values_only)
            for key, value in stats.items():
                st.write(f"**{key.capitalize()}**: {value:.2f}")
        else:
            st.write("No data available.")

        st.markdown("""
        **Quick Recruiter Insights:**
        - **Below 3.0**: Some companies may have a cutoff.
        - **3.0-3.5**: Comfortable baseline.
        - **3.5-3.6**: You stand out.
        - **3.6-3.8+**: Dean's List potential.
        - **3.8+**: Near-perfect—balance with projects!
        """)

    with tabs[2]:
        st.markdown("### Final CGPA Distributions")
        if final_values_only:
            hist_fig = create_histogram(final_values_only)
            st.plotly_chart(hist_fig, use_container_width=True)

            box_fig = create_box_plot(final_values_only)
            st.plotly_chart(box_fig, use_container_width=True)

            pie_fig = create_pie_chart(final_values_only)
            st.plotly_chart(pie_fig, use_container_width=True)

        st.markdown("### Export Simulation Results")
        df_results = pd.DataFrame(table_data, columns=["Path", "Variation", "Final CGPA", "Job Prob(%)", "Insights"])
        csv_data = df_results.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv_data, file_name="cgpa_simulation_results.csv", mime="text/csv")

        if st.button("Download as PDF"):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer)
            c.setFont("Helvetica", 12)
            c.drawString(100, 800, "CGPA Simulation Results")
            y_pos = 770
            for row in table_data:
                line = f"{row[0]} Var {row[1]}: CGPA={row[2]}, Prob={row[3]}, {row[4]}"
                c.drawString(50, y_pos, line)
                y_pos -= 20
            c.save()
            st.download_button("Download PDF", data=buffer.getvalue(), file_name="cgpa_results.pdf", mime="application/pdf")

    st.markdown("""
    **Potential Next Steps:**
    1. Integrate machine learning for predictive modeling.
    2. Real-time data integration from LMS.
    3. Multiplayer mode or leaderboards.
    4. Deeper gamification with achievements.
    """)

if __name__ == "__main__":
    main()
