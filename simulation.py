# simulation.py
import seaborn as sns
import plotly.graph_objects as go
from rich.console import Console
from rich.table import Table
from rich import box
import numpy as np

from paths import (
    generate_balanced_growth, generate_high_achiever, generate_downfall_recovery,
    generate_up_down, generate_perfectionist, generate_consistent_improvement,
    generate_chaotic, generate_late_bloomer, generate_spike_plateau, generate_senioritis,
    generate_no_study, generate_burnout, generate_triumph_over_adversity
)

console = Console()

def main():
    sns.set_theme(style="darkgrid")
    ascii_art = r"""
     __  __ ___ ___ _  _   ___  _   _ ___  ___ 
    |  \/  |_ _/ __| || | / _ \| | | | _ \/ __|
    | |\/| || |\__ \ __ |( (_) ) |_| |  _/\__ \
    |_|  |_|___|___/_||_| \___/ \___/|_|  |___/
    """
    Boss = "Boss"
    console.print(ascii_art, style="bold cyan")
    console.print(f"Greetings, {Boss}! Let's shape your CGPA multiverse with ultimate realism.\n",
                  style="bold magenta")

    # 2.1 Gather User Input
    while True:
        variations_input = console.input("[bold green]How many CGPA trajectories per path would you like to generate?[/] ")
        try:
            variations_per_path = int(variations_input)
            if variations_per_path < 1:
                raise ValueError
            break
        except ValueError:
            console.print(f"[red]{Boss}, that input isn't valid. Please enter a positive integer.[/]\n")

    all_paths = [
        "Balanced Growth", "High Achiever", "Downfall & Recovery", "Up & Down",
        "Perfectionist", "Consistent Improve", "Chaotic", "Late Bloomer",
        "Spike Plateau", "Senioritis", "No Study",
        "Burnout", "Triumph Over Adversity"
    ]

    console.print("\nWhich CGPA evolution paths would you like to explore?\n", style="bold yellow")
    for i, p in enumerate(all_paths, start=1):
        console.print(f"  {i}. {p}", style="bold white")

    console.print("\nType the numbers of the paths you'd like, separated by spaces (e.g. '1 3 5').\n"
                  "Or type 'all' to explore every path under the sun.\n", style="bold yellow")
    selection_input = console.input("[bold green]Your selection:[/] ")

    if selection_input.strip().lower() == "all":
        selected_paths = all_paths
        console.print(f"\nAlright, {Boss}, we’ll include ALL paths. Buckle up!\n", style="bold magenta")
    else:
        try:
            indices = [int(num) for num in selection_input.split()]
            selected_paths = [all_paths[i - 1] for i in indices if 1 <= i <= len(all_paths)]
            if not selected_paths:
                console.print(f"\nNo valid selections, {Boss}. We'll default to all paths.\n", style="red")
                selected_paths = all_paths
        except Exception:
            console.print(f"\nWe couldn't process your selection, {Boss}. Defaulting to all paths.\n", style="red")
            selected_paths = all_paths

    while True:
        semester_input = console.input("[bold green]Which semester are you in right now (1-10)?[/] ")
        try:
            current_semester = int(semester_input)
            if not (1 <= current_semester <= 10):
                raise ValueError
            break
        except ValueError:
            console.print(f"[red]{Boss}, that doesn't look like a valid semester number. Please try again.[/]\n")

    if current_semester == 1:
        console.print(f"\n{Boss}, you're at the very start of your academic journey! The possibilities are endless.\n",
                      style="bold cyan")
    elif current_semester <= 7:
        console.print(f"\n{Boss}, you've made some progress—Semester {current_semester}! "
                      f"Let's see how the future might shape up.\n", style="bold cyan")
    else:
        console.print(f"\nWow, {Boss}, you're near the finish line in Semester {current_semester}! "
                      f"Let's wrap things up in style.\n", style="bold cyan")

    while True:
        cgpa_input = console.input("[bold green]What's your current CGPA? (0.0 - 4.0)[/] ")
        try:
            current_cgpa = float(cgpa_input)
            if not (0.0 <= current_cgpa <= 4.0):
                raise ValueError
            break
        except ValueError:
            console.print(f"[red]{Boss}, CGPA must be between 0.0 and 4.0. Try again.[/]\n")

    if current_cgpa < 2.0:
        console.print(f"\n** Warning, {Boss} **: A CGPA below 2.0 can lead to academic probation. Time to hustle!\n",
                      style="bold red")
    elif current_cgpa >= 3.9:
        console.print(f"\n** Impressively High, {Boss}! ** You're flirting with a perfect 4.0—show us how it's done!\n",
                      style="bold cyan")
    else:
        console.print(f"\nSolid CGPA, {Boss}. Let’s see if you can climb higher (or maintain the momentum)!\n",
                      style="bold white")

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

    if current_semester >= 10:
        steps = 1
    else:
        steps = 10 - current_semester + 1

    future_semesters = np.arange(current_semester, current_semester + steps)

    console.print(f"Alright, plotting from semester {current_semester} through semester {current_semester + steps - 1}...\n",
                  style="bold yellow")

    fig = go.Figure()
    final_cgpas = []

    for path_name, style_info in selected_path_data.items():
        func = style_info["func"]
        color = style_info["color"]
        marker = style_info["marker"]

        for variation_index in range(variations_per_path):
            seed_for_variation = (42 + hash(path_name) + variation_index) % (2**32)
            trajectory = func(current_cgpa, steps=steps, seed=seed_for_variation)
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
        hovermode="closest"
    )
    fig.add_hline(y=3.6, line_dash="dash", line_color="gray",
                  annotation_text="Dean's List (3.6)", annotation_position="bottom right")
    fig.show()

    console.print("\n===== [bold magenta]POST-SIMULATION ANALYSIS[/] =====\n")
    table = Table(title="Final CGPA Outcomes & Advice", box=box.ROUNDED, style="bold white")
    table.add_column("Path", justify="center", style="bold cyan")
    table.add_column("Variation", justify="center", style="bold green")
    table.add_column("Final CGPA", justify="center", style="bold yellow")
    table.add_column("Category & Advice", justify="left", style="bold magenta")

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

        table.add_row(
            path_name,
            str(variation_num),
            f"{final_cg:.2f}",
            category_msg
        )

    console.print(table)

    console.print("""
[bold cyan]Quick Recruiter Insights:[/]
- [yellow]Below 3.0[/]: Some companies or roles may have a cutoff.
- [yellow]3.0 to 3.5[/]: Comfortable baseline for many mainstream applications.
- [yellow]3.5 to 3.6[/]: Strong contender; you’ll attract solid interest.
- [yellow]3.6 to 3.8+[/]: Dean's List territory, appealing to highly selective employers.
- [yellow]3.8+[/]: Near-perfect academically—balance with real-world projects too!

[bold magenta]Remember:[/bold magenta] CGPA isn’t everything! Practical skills, projects, internships,
and your personal spark can tip the scales in your favor.

[bold green]Potential Next Steps:[/]
1. [underline]Skill-based Quizzes[/] to refine trajectory: e.g., choose between Netflix or finishing assignments.
2. [underline]Project Recommendations[/] to boost profile if CGPA dips or to complement a 3.8+.
3. [underline]Export Results[/] for academic counseling or further analysis.
4. [underline]Machine Learning Integration[/] for data-driven predictions using real grade logs.
""", style="bold white")

    ascii_farewell = r"""
    ______________________________________________
   |                                              |
   |   Simulation complete! May your CGPA dreams  |
   |   come true across these parallel universes, |
   |   Boss. Go forth and conquer those grades!   |
   |______________________________________________|
    """
    console.print(ascii_farewell, style="bold cyan")


if __name__ == "__main__":
    main()
