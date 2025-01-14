import numpy as np
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns
import streamlit as st

from rich.console import Console
from rich.table import Table
from rich import box

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
    return _func(start_cgpa, steps=steps, seed=seed)

sns.set_theme(style="darkgrid")
console = Console()

# ----------------------------------------------------------------------------------
# 2. Streamlit App
# ----------------------------------------------------------------------------------
def main():
    st.title("The Ultimate CGPA Multiverse (Animated!)")
    st.markdown("""
    Explore how your CGPA evolves under different academic scenarios. 
    **Now with smoother animations** as you adjust your inputs! 
    """)

    # Sidebar Inputs
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

    st.sidebar.markdown("### Advanced Options")
    with st.sidebar.expander("Placeholder for Additional Settings"):
        st.write("Future: Tweak growth rates, add event triggers, etc.")

    # Determine steps & future semesters
    steps = 1 if current_semester >= 10 else 10 - current_semester + 1
    future_semesters = np.arange(current_semester, current_semester + steps)

    # Define path styles
    path_styles = {
        "Balanced Growth":        {"func": generate_balanced_growth,        "color": "blue",      "marker": "circle"},
        "High Achiever":          {"func": generate_high_achiever,          "color": "green",     "marker": "circle"},
        "Downfall & Recovery":    {"func": generate_downfall_recovery,      "color": "red",       "marker": "circle"},
        "Up & Down":              {"func": generate_up_down,                "color": "orange",    "marker": "circle"},
        "Perfectionist":          {"func": generate_perfectionist,          "color": "purple",    "marker": "circle"},
        "Consistent Improve":     {"func": generate_consistent_improvement, "color": "cyan",      "marker": "circle"},
        "Chaotic":                {"func": generate_chaotic,                "color": "magenta",   "marker": "circle"},
        "Late Bloomer":           {"func": generate_late_bloomer,           "color": "darkblue",  "marker": "circle"},
        "Spike Plateau":          {"func": generate_spike_plateau,          "color": "lime",      "marker": "circle"},
        "Senioritis":             {"func": generate_senioritis,             "color": "brown",     "marker": "circle"},
        "No Study":               {"func": generate_no_study,               "color": "black",     "marker": "circle"},
        "Burnout":                {"func": generate_burnout,                "color": "goldenrod", "marker": "circle"},
        "Triumph Over Adversity": {"func": generate_triumph_over_adversity, "color": "teal",      "marker": "circle"}
    }

    selected_path_data = {p: path_styles[p] for p in selected_paths}

    st.sidebar.markdown("---")
    st.sidebar.write("All inputs set. The simulation will run based on these parameters.")

    console.log(f"Selected Paths: {selected_paths}")

    fig = go.Figure()
    final_cgpas = []

    for path_name, style_info in selected_path_data.items():
        func = style_info["func"]
        color = style_info["color"]
        marker = style_info["marker"]

        for variation_index in range(variations):
            seed_for_variation = (42 + hash(path_name) + variation_index) % (2**32)
            trajectory = compute_trajectory(func, current_cgpa, steps, seed_for_variation)
            final_cgpas.append((path_name, variation_index + 1, trajectory[-1]))

            customdata = []
            for idx, sem in enumerate(future_semesters):
                if idx < len(trajectory)-1:
                    customdata.append(f"{trajectory[idx+1]:.2f}")
                else:
                    customdata.append("N/A")

            fig.add_trace(go.Scatter(
                x=future_semesters,
                y=trajectory,
                customdata=customdata,
                mode='lines+markers',
                name=f"{path_name} Var {variation_index+1}" if variation_index == 0 else None,
                line=dict(color=color),
                marker=dict(symbol=marker),
                opacity=0.6,
                hovertemplate=(
                    "Semester: %{x}<br>"
                    "CGPA: %{y:.2f}<br>"
                    "Expected Next CGPA: %{customdata}<extra>%{fullData.name}</extra>"
                )
            ))

    fig.update_layout(
        title="The Ultimate CGPA Multiverse",
        xaxis_title="Semester",
        yaxis_title="Cumulative CGPA",
        hovermode="closest",
        transition_duration=500
    )
    fig.add_hline(y=3.6, line_dash="dash", line_color="gray",
                  annotation_text="Dean's List (3.6)", annotation_position="bottom right")

    st.plotly_chart(fig, use_container_width=True)

    table_data = []
    for path_name, variation_num, final_cg in final_cgpas:
        if final_cg < 3.0:
            category_msg = ("Below 3.0: Could face interview filters.\n"
                            "Tip: Boost fundamentals + real-world projects.")
        elif final_cg < 3.5:
            category_msg = ("3.0-3.5: Safe for many roles.\n"
                            "Tip: Strong projects/internships can stand out.")
        elif final_cg < 3.6:
            category_msg = ("3.5-3.6: You stand out.\n"
                            "Tip: Aim for advanced courses or certifications.")
        elif final_cg < 3.8:
            category_msg = ("3.6-3.8: Dean's List territory.\n"
                            "Tip: Leadership roles, hackathons, or research.")
        else:
            category_msg = ("3.8-4.0: Near perfection!\n"
                            "Tip: Expand to open-source or specialized R&D.")
        table_data.append((path_name, variation_num, f"{final_cg:.2f}", category_msg))

    st.subheader("Post-Simulation Analysis")
    st.table(pd.DataFrame(table_data, columns=["Path", "Variation", "Final CGPA", "Insights"]))

    st.markdown("""
    **Quick Recruiter Insights:**
    - **Below 3.0**: Some companies or roles may have a cutoff.
    - **3.0 to 3.5**: Comfortable baseline for many mainstream applications.
    - **3.5 to 3.6**: Strong contender; you’ll attract solid interest.
    - **3.6 to 3.8+**: Dean's List territory, appealing to highly selective employers.
    - **3.8+**: Near-perfect academically—balance with real-world projects too!

    **Remember:** CGPA isn’t everything! Practical skills, projects, internships,
    and your personal spark can tip the scales in your favor.
    """)

    with st.expander("Skill-based Quizzes"):
        st.markdown("*Placeholder*: Interactive quizzes to refine your study habits, track daily schedule, etc.")

    with st.expander("Project Recommendations"):
        st.markdown("*Placeholder*: Provide curated project ideas, research topics, open-source opportunities, etc.")

    df_results = pd.DataFrame(table_data, columns=["Path", "Variation", "Final CGPA", "Insights"])
    csv_data = df_results.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Results as CSV",
        data=csv_data,
        file_name="cgpa_simulation_results.csv",
        mime="text/csv"
    )

    st.markdown("""
    **Potential Next Steps:**
    1. Real skill-based quizzes that affect CGPA trajectory.
    2. Enhanced project recommendations or mentorship matching.
    3. Machine learning integration for personalized CGPA predictions.
    4. Real-time data integration from LMS or grade logs.
    """)

if __name__ == "__main__":
    main()
