import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st
import io
from reportlab.pdfgen import canvas
from rich.console import Console
import random

# --------------------------------------------------------------------------
# Import path functions which expect a 'start' CGPA, steps, and seed,
# and return a list of single-semester GPAs (0-4).
# --------------------------------------------------------------------------
from paths import (
    generate_balanced_growth,
    generate_high_achiever,
    generate_downfall_recovery,
    generate_up_down,
    generate_perfectionist,
    generate_consistent_improvement,
    generate_chaotic,
    generate_late_bloomer,
    generate_spike_plateau,
    generate_senioritis,
    generate_no_study,
    generate_burnout,
    generate_triumph_over_adversity
)

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

sns.set_theme(style="darkgrid")
console = Console()

# Helper function updated to include 'start' parameter
def generate_semester_gpas(_func, start, steps, seed=None):
    """
    Generate single-semester GPAs for 'steps' future semesters using the
    provided path function, starting from a given CGPA.
    """
    return _func(start, steps=steps, seed=seed)

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

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))

def main():
    st.title("The Ultimate CGPA Multiverse: No-Limit Advanced Stats Edition")
    st.markdown("""
    Welcome! Explore detailed information about various academic paths and 
    how to interpret the ensuing plots.
    """)

    st.sidebar.header("Simulation Configuration")
    mass_mode = st.sidebar.checkbox(
        "Enable Mass Simulation Mode (Range Band)",
        value=False
    )
    variations = st.sidebar.slider(
        "How many trajectories per path?",
        1, 5000, 500 if mass_mode else 5
    )
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
    # Update slider to allow up to semester 11
    current_semester = st.sidebar.slider("Current Semester (1-11)", 1, 11, 1)
    current_cgpa = st.sidebar.slider("Current CGPA (0.0 - 4.0)", 0.0, 4.0, 2.91, 0.01)

    with st.sidebar.expander("What-If Future GPA Adjustments"):
        st.markdown("Add a constant shift to each single-semester GPA.")
        what_if_adjust = st.slider("Adjust future single-semester GPA by ±", -1.0, 1.0, 0.0, 0.05)
        st.write(f"Applying ±{what_if_adjust:.2f} shift to each semester's GPA.")

    # Set total semesters to 10
    total_semesters = 10
    # Calculate number of future semesters based on current semester
    steps = total_semesters - current_semester
    # Generate an array for future semester labels
    future_semesters = np.arange(current_semester + 1, total_semesters + 1)

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
    style_map = {
        "Balanced Growth": {"color": "#0000FF", "dash": "solid"},
        "High Achiever": {"color": "#008000", "dash": "dash"},
        "Downfall & Recovery": {"color": "#FF0000", "dash": "dot"},
        "Up & Down": {"color": "#FFA500", "dash": "dashdot"},
        "Perfectionist": {"color": "#800080", "dash": "solid"},
        "Consistent Improve": {"color": "#A52A2A", "dash": "dash"},
        "Chaotic": {"color": "#FF00FF", "dash": "dot"},
        "Late Bloomer": {"color": "#008080", "dash": "dashdot"},
        "Spike Plateau": {"color": "#808080", "dash": "solid"},
        "Senioritis": {"color": "#00FFFF", "dash": "dash"},
        "No Study": {"color": "#FFD700", "dash": "dot"},
        "Burnout": {"color": "#000080", "dash": "dashdot"},
        "Triumph Over Adversity": {"color": "#DC143C", "dash": "solid"}
    }

    final_cgpas = []
    fig = go.Figure()

    for path_name in selected_paths:
        all_trajectories = []
        for variation_index in range(variations):
            seed_val = (42 + hash(path_name) + variation_index) % (2 ** 32)
            random.seed(seed_val)

            # Generate single-semester GPAs using the current CGPA as start
            future_sem_gpas = generate_semester_gpas(
                path_map[path_name],
                start=current_cgpa,
                steps=steps,
                seed=seed_val
            )

            # Apply adjustments to future semester GPAs
            for i in range(len(future_sem_gpas)):
                future_sem_gpas[i] = min(max(future_sem_gpas[i] + what_if_adjust, 0.0), 4.0)

            cgpa_history = []
            sem_history = []
            current_gpa = current_cgpa
            completed_semesters = current_semester

            for single_sem_gpa in future_sem_gpas:
                new_cgpa = ((current_gpa * completed_semesters) + single_sem_gpa) / (completed_semesters + 1)
                cgpa_history.append(new_cgpa)
                sem_history.append(single_sem_gpa)
                current_gpa = new_cgpa
                completed_semesters += 1

            final_val = cgpa_history[-1] if cgpa_history else current_cgpa
            cat = categorize_cgpa(final_val)
            job_prob = estimate_job_probability(final_val)
            advice = (
                "Focus on fundamentals." if final_val < 3.0 else
                "Strengthen projects/internships." if final_val < 3.5 else
                "Aim for advanced courses." if final_val < 3.6 else
                "Seek leadership roles." if final_val < 3.8 else
                "Expand into R&D."
            )
            final_cgpas.append((path_name, variation_index + 1, final_val, cat, job_prob, advice))
            all_trajectories.append(cgpa_history)

            if not mass_mode:
                custom_data = [f"{gpa:.2f}" for gpa in sem_history]
                line_name = f"{path_name} Var {variation_index + 1}" if variation_index == 0 else None
                fig.add_trace(go.Scatter(
                    x=future_semesters,
                    y=cgpa_history,
                    mode='lines+markers',
                    name=line_name,
                    customdata=custom_data,
                    hovertemplate=(
                        "Semester: %{x}<br>"
                        "Cumulative CGPA: %{y:.2f}<br>"
                        "Single-Sem GPA: %{customdata}<br>"
                        "<extra>%{fullData.name}</extra>"
                    ),
                    line=dict(
                        color=style_map[path_name]["color"],
                        dash=style_map[path_name]["dash"],
                        width=2
                    )
                ))

        if mass_mode and variations > 1:
            all_trajectories = np.array(all_trajectories)
            min_curve = np.min(all_trajectories, axis=0)
            max_curve = np.max(all_trajectories, axis=0)
            x_band = np.concatenate([future_semesters, future_semesters[::-1]])
            y_band = np.concatenate([max_curve, min_curve[::-1]])
            path_style = style_map[path_name]
            rgb = hex_to_rgb(path_style["color"])
            fig.add_trace(go.Scatter(
                x=x_band,
                y=y_band,
                fill='toself',
                name=f"{path_name} Range",
                mode='lines',
                line=dict(width=2, color=path_style["color"]),
                fillcolor=f'rgba({rgb[0]},{rgb[1]},{rgb[2]},0.2)',
                hoverinfo='skip',
                showlegend=True
            ))

    fig.update_layout(
        title="CGPA Evolution (Refactored for Logical Single-Semester GPAs)",
        xaxis_title="Semester",
        yaxis_title="Cumulative CGPA",
        hovermode="closest",
        transition_duration=500,
        template="plotly_white"
    )
    fig.add_hline(
        y=3.6,
        line_dash="dash",
        line_color="gray",
        annotation_text="Dean's List (3.6)",
        annotation_position="bottom right"
    )

    tabs = st.tabs([
        "Path Information",
        "Interactive Graph",
        "Post-Simulation Analysis",
        "Distributions & Exports"
    ])

    with tabs[0]:
        st.header("Detailed Path Information & Interpretation")
        st.markdown("""
        ### Simulation Paths Explained
        Each path function returns single-semester GPAs (0-4).
        The app computes the cumulative GPA step-by-step.
        """)

    with tabs[1]:
        if mass_mode and variations > 100:
            st.info("Showing range band for many lines. This might be computationally heavy!")
        st.plotly_chart(fig, use_container_width=True)

    with tabs[2]:
        table_data = []
        final_values_only = []
        for (p_name, var_idx, final_val, cat, job_prob, advice) in final_cgpas:
            table_data.append([
                p_name, var_idx, f"{final_val:.2f}",
                f"{job_prob * 100:.1f}%", advice, cat
            ])
            final_values_only.append(final_val)

        st.subheader("Post-Simulation Analysis")
        fig_table = create_plotly_table(table_data)
        st.plotly_chart(fig_table, use_container_width=True)

        if final_values_only:
            st.markdown("#### Violin Plot of Final CGPAs")
            fig_violin = go.Figure()
            fig_violin.add_trace(go.Violin(
                y=final_values_only,
                box_visible=True,
                meanline_visible=True,
                fillcolor='lightseagreen',
                opacity=0.6,
                line_color='darkblue',
                name='Final CGPAs'
            ))
            fig_violin.update_layout(
                xaxis_title="All Trajectories",
                yaxis_title="Final CGPA",
                template="plotly_white"
            )
            st.plotly_chart(fig_violin, use_container_width=True)

            st.markdown("#### Scatter Plot of Final CGPAs")
            var_indices = [var_idx for (_, var_idx, _, _, _, _) in final_cgpas]
            fig_scatter = go.Figure(data=go.Scatter(
                x=var_indices,
                y=final_values_only,
                mode='markers',
                marker=dict(
                    size=8,
                    color=final_values_only,
                    colorscale='Viridis',
                    showscale=True
                )
            ))
            fig_scatter.update_layout(
                xaxis_title="Variation Index",
                yaxis_title="Final CGPA",
                template="plotly_white"
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

            st.markdown("#### Bar Chart of CGPA Categories")
            categories = [categorize_cgpa(val) for val in final_values_only]
            category_series = pd.Series(categories)
            category_counts = category_series.value_counts().sort_index()
            fig_bar = go.Figure(
                data=go.Bar(
                    x=category_counts.index,
                    y=category_counts.values,
                    marker_color='teal'
                )
            )
            fig_bar.update_layout(
                xaxis_title="CGPA Category",
                yaxis_title="Count",
                template="plotly_white"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

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
                st.write(f"**P(CGPA > 3.5)**: {np.mean(arr > 3.5) * 100:.2f}%")
                st.write(f"**P(CGPA > 3.6)**: {np.mean(arr > 3.6) * 100:.2f}%")
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

    with tabs[3]:
        st.markdown("### Final CGPA Distributions")
        if final_values_only:
            st.plotly_chart(create_histogram(final_values_only), use_container_width=True)
            st.plotly_chart(create_box_plot(final_values_only), use_container_width=True)
            st.plotly_chart(create_pie_chart(final_values_only), use_container_width=True)
            st.plotly_chart(generate_category_distribution_bar(final_values_only), use_container_width=True)

        st.markdown("### Export Simulation Results")
        df_results = pd.DataFrame(table_data, columns=[
            "Path", "Variation", "Final CGPA", "Job Prob(%)", "Advice", "Category"
        ])
        csv_data = df_results.to_csv(index=False).encode('utf-8')
        st.download_button(
            "Download CSV",
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
                line = f"{row[0]} Var {row[1]}: CGPA={row[2]}, Prob={row[3]}, {row[4]}, Category={row[5]}"
                c.drawString(50, y_pos, line)
                y_pos -= 20
            c.save()
            st.download_button(
                "Download PDF",
                data=buffer.getvalue(),
                file_name="cgpa_simulation_results.pdf",
                mime="application/pdf"
            )

if __name__ == "__main__":
    main()
