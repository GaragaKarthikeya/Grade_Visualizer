import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import io
import random
from reportlab.pdfgen import canvas

from rich.console import Console

# Import path functions from your paths.py
from paths import (
    generate_balanced_growth, generate_high_achiever, generate_downfall_recovery,
    generate_up_down, generate_perfectionist, generate_consistent_improvement,
    generate_chaotic, generate_late_bloomer, generate_spike_plateau, generate_senioritis,
    generate_no_study, generate_burnout, generate_triumph_over_adversity
)
# Import advanced analysis & plotting utilities
from analysis import (
    summarize_statistics,
    create_plotly_table,
    categorize_cgpa,
    generate_category_distribution_bar
)
from plotting import (
    create_histogram,
    create_box_plot,
    create_pie_chart
)

@st.cache_data
def compute_trajectory(_func, start_cgpa, steps, seed=None):
    """Compute a single CGPA trajectory for a given function/path."""
    return _func(start_cgpa, steps=steps, seed=seed)

sns.set_theme(style="darkgrid")
console = Console()

def estimate_job_probability(final_cgpa):
    """A simple placeholder function to estimate job probabilities by CGPA."""
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
    st.title("The Ultimate CGPA Multiverse: No-Limit Advanced Stats Edition")
    st.markdown("""
    Explore large-scale CGPA simulations with **no forced line-limit**, detailed statistical summaries, 
    mass-mode range bands, and user-selectable Plotly themes for a visually appealing experience.
    """)

    # -------------------------------------------
    # 1. SIDEBAR: Simulation & UI Config
    # -------------------------------------------
    st.sidebar.header("Simulation Configuration")

    # Theme selection
    user_theme = st.sidebar.selectbox(
        "Select Plotly Theme",
        options=["plotly_white", "plotly_dark", "plotly", "ggplot2", "seaborn"],
        index=0
    )

    # Mass Simulation toggle
    mass_mode = st.sidebar.checkbox(
        "Enable Mass Simulation Mode (Range Band)",
        value=False,
        help="When enabled, lines won't be limited. We also plot a 'range band' if many lines are generated."
    )

    # Slider for the number of trajectories
    # We'll allow up to 5000 to fully remove forced limits, but user can go higher if they want
    variations = st.sidebar.slider("How many trajectories per path?", 1, 5000, 500 if mass_mode else 5)

    # Path selection
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

    # Current semester & CGPA
    current_semester = st.sidebar.slider("Current Semester (1-10)", 1, 10, 1)
    current_cgpa = st.sidebar.slider("Current CGPA (0.0 - 4.0)", 0.0, 4.0, 2.91, 0.01)

    # What-If CGPA Adjust
    with st.sidebar.expander("What-If Future CGPA Adjustments"):
        st.markdown("Simulate a consistent positive or negative shift each semester.")
        what_if_adjust = st.slider("Adjust future CGPAs by ±", -1.0, 1.0, 0.0, 0.05)
        st.write(f"Applying ±{what_if_adjust:.2f} shift to future steps.")

    with st.sidebar.expander("Advanced Options"):
        st.write("E.g., tweak growth rates, incorporate real data, or add custom events here...")

    st.sidebar.markdown("---")
    st.sidebar.info("All set! Let's run the simulation...")

    # Setup steps & semester array
    steps = 1 if current_semester >= 10 else (10 - current_semester + 1)
    future_semesters = np.arange(current_semester, current_semester + steps)

    # Mapping path names to generator funcs
    path_map = {
        "Balanced Growth":        generate_balanced_growth,
        "High Achiever":          generate_high_achiever,
        "Downfall & Recovery":    generate_downfall_recovery,
        "Up & Down":              generate_up_down,
        "Perfectionist":          generate_perfectionist,
        "Consistent Improve":     generate_consistent_improvement,
        "Chaotic":                generate_chaotic,
        "Late Bloomer":           generate_late_bloomer,
        "Spike Plateau":          generate_spike_plateau,
        "Senioritis":             generate_senioritis,
        "No Study":               generate_no_study,
        "Burnout":                generate_burnout,
        "Triumph Over Adversity": generate_triumph_over_adversity
    }

    # -------------------------------------------
    # 2. MAIN CHART: Lines or Range Band
    # -------------------------------------------
    final_cgpas = []
    fig = go.Figure()

    # For each selected path, we'll either show all lines or a range band if mass_mode
    for path_name in selected_paths:
        all_trajectories = []  # store arrays of shape [variations, steps] for range band
        for variation_index in range(variations):
            # seed for reproducibility
            seed_val = (42 + hash(path_name) + variation_index) % (2**32)
            traj = compute_trajectory(path_map[path_name], current_cgpa, steps, seed_val)

            # apply CGPA shift
            for i in range(1, len(traj)):
                traj[i] = min(max(2.0, traj[i] + what_if_adjust), 4.0)

            final_val = traj[-1]
            cat = categorize_cgpa(final_val)
            job_prob = estimate_job_probability(final_val)

            # basic advice
            if final_val < 3.0:
                advice = "Focus on fundamentals."
            elif final_val < 3.5:
                advice = "Strengthen projects/internships."
            elif final_val < 3.6:
                advice = "Aim for advanced courses."
            elif final_val < 3.8:
                advice = "Seek leadership roles."
            else:
                advice = "Expand into R&D."

            final_cgpas.append((path_name, variation_index+1, final_val, cat, job_prob, advice))
            all_trajectories.append(traj)

        all_trajectories = np.array(all_trajectories)  # shape: (variations, steps)

        if mass_mode and variations > 1:
            # Create a range band by computing min & max at each step
            min_curve = np.min(all_trajectories, axis=0)
            max_curve = np.max(all_trajectories, axis=0)
            x_band = np.concatenate([future_semesters, future_semesters[::-1]])
            y_band = np.concatenate([max_curve, min_curve[::-1]])

            # Add a filled shape for the entire range
            fig.add_trace(go.Scatter(
                x=x_band,
                y=y_band,
                fill='toself',
                name=f"{path_name} Range",
                mode='lines',
                line=dict(width=0),
                hoverinfo='skip',
                showlegend=True  # Show path name once
            ))
        else:
            # If not mass mode or variations <= 1, just add lines individually
            # (Might be a lot of lines for large variations; user has no line-limit)
            for i in range(variations):
                traj = all_trajectories[i]
                # build custom data for next CG
                customdata = []
                for idx in range(steps):
                    if idx < steps - 1:
                        customdata.append(f"{traj[idx+1]:.2f}")
                    else:
                        customdata.append("N/A")
                # label the first line from each path in legend
                line_name = f"{path_name} Var {i+1}" if i == 0 else None

                fig.add_trace(go.Scatter(
                    x=future_semesters,
                    y=traj,
                    mode='lines+markers',
                    name=line_name,
                    customdata=customdata,
                    hovertemplate=(
                        "Semester: %{x}<br>"
                        "CGPA: %{y:.2f}<br>"
                        "Next CGPA: %{customdata}<extra>%{fullData.name}</extra>"
                    )
                ))

    # Theme logic
    fig.update_layout(
        title="CGPA Evolution (No-Limit Edition)",
        xaxis_title="Semester",
        yaxis_title="Cumulative CGPA",
        hovermode="closest",
        transition_duration=500,
        template=st.sidebar.selectbox(
            "Choose a Plotly Theme:",
            ["plotly_white", "plotly_dark", "plotly", "ggplot2", "seaborn"],
            index=0
        )
    )
    fig.add_hline(
        y=3.6,
        line_dash="dash",
        line_color="gray",
        annotation_text="Dean's List (3.6)",
        annotation_position="bottom right"
    )

    # TAB structure
    tabs = st.tabs(["Interactive Graph", "Post-Simulation Analysis", "Distributions & Exports"])

    # TAB 1: Graph
    with tabs[0]:
        # If user is in mass_mode with large variations, we note the approach
        if mass_mode and variations > 100:
            st.info("Showing range band or many lines. This might be computationally heavy!")
        st.plotly_chart(fig, use_container_width=True)

    # TAB 2: Analysis
    with tabs[1]:
        table_data = []
        final_values_only = []
        for (p_name, var_idx, final_val, cat, job_prob, advice) in final_cgpas:
            table_data.append([
                p_name,
                var_idx,
                f"{final_val:.2f}",
                f"{job_prob*100:.1f}%",
                advice,
                cat
            ])
            final_values_only.append(final_val)

        st.subheader("Post-Simulation Analysis")
        # Create color-coded table
        fig_table = create_plotly_table(table_data)
        st.plotly_chart(fig_table, use_container_width=True)

        st.markdown("### Extended Statistical Summary of Final CGPAs")
        if final_values_only:
            stats = summarize_statistics(final_values_only)
            if stats:
                st.write(f"**Count**: {stats['count']}")
                st.write(f"**Mean**: {stats['mean']:.2f}")
                st.write(f"**Median**: {stats['median']:.2f}")
                st.write(f"**Std**: {stats['std']:.2f}")
                st.write(f"**Variance**: {stats['variance']:.2f}")
                st.write(f"**Min**: {stats['min']:.2f}")
                st.write(f"**Max**: {stats['max']:.2f}")
                st.write(f"**25th Percentile**: {stats['25th_percentile']:.2f}")
                st.write(f"**75th Percentile**: {stats['75th_percentile']:.2f}")
                if "95ci_lower" in stats and "95ci_upper" in stats:
                    st.write(f"**95% CI**: ({stats['95ci_lower']:.2f}, {stats['95ci_upper']:.2f})")
                arr = np.array(final_values_only)
                # Probability of crossing thresholds
                st.write(f"**P(CGPA > 3.5)**: {np.mean(arr>3.5)*100:.2f}%")
                st.write(f"**P(CGPA > 3.6)**: {np.mean(arr>3.6)*100:.2f}%")
            else:
                st.write("No statistics available.")
        else:
            st.write("No CGPAs to analyze.")

        st.markdown("""
        **Quick Recruiter Insights:**
        - **Below 3.0**: Potential cutoffs for many companies.
        - **3.0-3.5**: Decent zone—employers look at strong projects/internships.
        - **3.5-3.6**: Competitive; advanced courses stand out.
        - **3.6-3.8**: Dean's List territory—seek leadership/unique experiences.
        - **3.8+**: Near-perfect—focus on real-world, R&D, or specialized achievements!
        """)

    # TAB 3: Distributions & Exports
    with tabs[2]:
        st.markdown("### Final CGPA Distributions")
        if final_values_only:
            hist_fig = create_histogram(final_values_only)
            st.plotly_chart(hist_fig, use_container_width=True)

            box_fig = create_box_plot(final_values_only)
            st.plotly_chart(box_fig, use_container_width=True)

            pie_fig = create_pie_chart(final_values_only)
            st.plotly_chart(pie_fig, use_container_width=True)

            bar_fig = generate_category_distribution_bar(final_values_only)
            st.plotly_chart(bar_fig, use_container_width=True)

        st.markdown("### Export Simulation Results")
        df_results = pd.DataFrame(table_data, columns=[
            "Path", "Variation", "Final CGPA", "Job Prob(%)", "Advice", "Category"
        ])
        csv_data = df_results.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv_data, file_name="cgpa_simulation_results.csv", mime="text/csv")

        if st.button("Download as PDF"):
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer)
            c.setFont("Helvetica", 12)
            c.drawString(100, 800, "CGPA Simulation Results")
            y_pos = 770
            for row in table_data:
                line = f"{row[0]} Var {row[1]}: CGPA={row[2]}, Prob={row[3]}, {row[4]}, Category={row[5]}"
                c.drawString(50, y_pos, line)
                y_pos -= 20
            c.save()
            st.download_button("Download PDF",
                data=buffer.getvalue(),
                file_name="cgpa_simulation_results.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
