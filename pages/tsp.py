import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import time

_CSS = """
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
"""

# -- helpers ------------------------------------------------------------------

def generate_cities(n, seed):
    rng = np.random.default_rng(seed)
    return rng.uniform(0, 100, (n, 2)).tolist()

def euclidean_matrix(cities):
    n = len(cities)
    return [[np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
             for j in range(n)] for i in range(n)]

def plot_tour(cities, tour, title="Tour", color="#818cf8"):
    if tour is None:
        return go.Figure()
    route = tour + [tour[0]]
    xs = [cities[i][0] for i in route]
    ys = [cities[i][1] for i in route]
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines",
                             line=dict(color=color, width=2), name="Route"))
    fig.add_trace(go.Scatter(
        x=[c[0] for c in cities], y=[c[1] for c in cities],
        mode="markers+text",
        marker=dict(size=10, color="#f8fafc", line=dict(color=color, width=2)),
        text=[str(i) for i in range(len(cities))],
        textposition="top center", name="Cities"
    ))
    fig.update_layout(
        title=title, height=380,
        paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
        font_color="#e2e8f0", margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
    )
    return fig

def plot_convergence(histories, labels, colors, title="Convergence"):
    fig = go.Figure()
    for hist, label, color in zip(histories, labels, colors):
        fig.add_trace(go.Scatter(y=hist, mode="lines", name=label,
                                 line=dict(color=color, width=2)))
    fig.update_layout(
        title=title, xaxis_title="Iteration", yaxis_title="Tour cost",
        height=320, paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
        font_color="#e2e8f0", margin=dict(l=20, r=20, t=40, b=20),
        legend=dict(bgcolor="#1e293b"),
    )
    return fig

# -- page render --------------------------------------------------------------

def render():
    st.markdown("## TSP - Travelling Salesman Problem")
    st.markdown("Configure the problem, pick algorithms, run them, and compare results side-by-side.")

    with st.sidebar:
        st.markdown("### TSP Settings")
        n_cities = st.slider("Number of cities", 5, 20, 10)
        seed = st.number_input("Random seed", 0, 9999, 42, step=1)
        st.markdown("---")
        st.markdown("**Algorithms to run**")
        run_bkt = st.checkbox("BKT - Backtracking", value=True)
        run_nn  = st.checkbox("NN  - Nearest Neighbour", value=True)
        run_hc  = st.checkbox("HC  - Hill Climbing", value=True)
        run_sa  = st.checkbox("SA  - Simulated Annealing", value=True)
        run_ga  = st.checkbox("GA  - Genetic Algorithm", value=True)
        st.markdown("---")

        if run_bkt:
            st.markdown("**BKT params**")
            bkt_mode = st.selectbox("Stop mode", ["first", "all", "time", "y_solutions"])
            bkt_time = st.slider("Time limit (s)", 1, 30, 5) if bkt_mode == "time" else 5
            bkt_y    = st.slider("Y solutions", 1, 50, 10) if bkt_mode == "y_solutions" else 10
        else:
            bkt_mode, bkt_time, bkt_y = "first", 5, 10

        if run_hc:
            st.markdown("**HC params**")
            hc_restarts = st.slider("Restarts", 1, 10, 3)
            hc_iters    = st.slider("Max iterations", 500, 10000, 3000, step=500)
        else:
            hc_restarts, hc_iters = 3, 3000

        if run_sa:
            st.markdown("**SA params**")
            sa_tmax  = st.number_input("T_max", 100.0, 5000.0, 1000.0, step=100.0)
            sa_alpha = st.slider("Cooling rate alpha", 0.90, 0.999, 0.995, step=0.001, format="%.3f")
            sa_iters = st.slider("Max iterations", 1000, 50000, 10000, step=1000)
            sa_init  = st.radio("Initial solution", ["nn", "random"])
        else:
            sa_tmax, sa_alpha, sa_iters, sa_init = 1000.0, 0.995, 10000, "nn"

        if run_ga:
            st.markdown("**GA params**")
            ga_pop   = st.slider("Population size", 20, 200, 80, step=10)
            ga_gens  = st.slider("Generations", 50, 1000, 300, step=50)
            ga_mut   = st.slider("Mutation rate", 0.05, 0.90, 0.30, step=0.05)
            ga_elite = st.slider("Elitism", 0, 5, 2)
            ga_sel   = st.radio("Selection", ["tournament", "roulette"])
        else:
            ga_pop, ga_gens, ga_mut, ga_elite, ga_sel = 80, 300, 0.30, 2, "tournament"

    # City map preview
    cities = generate_cities(n_cities, int(seed))
    dist_matrix = euclidean_matrix(cities)

    fig_cities = go.Figure()
    fig_cities.add_trace(go.Scatter(
        x=[c[0] for c in cities], y=[c[1] for c in cities],
        mode="markers+text",
        marker=dict(size=12, color="#818cf8"),
        text=[str(i) for i in range(n_cities)],
        textposition="top center",
    ))
    fig_cities.update_layout(
        title=f"{n_cities} cities (seed={seed})", height=320,
        paper_bgcolor="#0f172a", plot_bgcolor="#1e293b", font_color="#e2e8f0",
        margin=dict(l=20, r=20, t=40, b=20), showlegend=False,
    )
    st.plotly_chart(fig_cities, use_container_width=True)

    if st.button("Run selected algorithms", type="primary", use_container_width=True):
        steps = sum([run_bkt, run_nn, run_hc, run_sa, run_ga])
        if steps == 0:
            st.warning("Select at least one algorithm.")
        else:
            results = {}
            progress = st.progress(0, text="Running algorithms...")
            done = 0

            if run_bkt:
                from algorithms.backtracking import solve_bkt
                with st.spinner("BKT running..."):
                    r = solve_bkt(dist_matrix, mode=bkt_mode,
                                  time_limit=bkt_time, max_solutions=bkt_y)
                results["BKT"] = r
                done += 1
                progress.progress(done / steps, text=f"BKT done ({r['elapsed']:.2f}s)")

            if run_nn:
                from algorithms.nearest_neighbour import solve_nn_multistart
                t0 = time.perf_counter()
                tour, cost, all_r = solve_nn_multistart(dist_matrix)
                elapsed = time.perf_counter() - t0
                results["NN"] = {"best_tour": tour, "best_cost": cost,
                                 "elapsed": elapsed, "all_starts": all_r}
                done += 1
                progress.progress(done / steps, text="NN done")

            if run_hc:
                from algorithms.hill_climbing import solve_hc
                with st.spinner("HC running..."):
                    r = solve_hc(dist_matrix, max_iterations=hc_iters, restarts=hc_restarts)
                results["HC"] = r
                done += 1
                progress.progress(done / steps, text="HC done")

            if run_sa:
                from algorithms.simulated_annealing import solve_sa
                with st.spinner("SA running..."):
                    r = solve_sa(dist_matrix, T_max=sa_tmax, alpha=sa_alpha,
                                 iterations=sa_iters, init_mode=sa_init)
                results["SA"] = r
                done += 1
                progress.progress(done / steps, text="SA done")

            if run_ga:
                from algorithms.genetic import solve_ga
                with st.spinner("GA running..."):
                    r = solve_ga(dist_matrix, pop_size=ga_pop, n_generations=ga_gens,
                                 mutation_rate=ga_mut, elitism=ga_elite, selection=ga_sel)
                results["GA"] = r
                done += 1
                progress.progress(done / steps, text="GA done")

            progress.empty()
            st.session_state["tsp_results"] = results
            st.session_state["tsp_cities"] = cities

    if "tsp_results" in st.session_state and st.session_state["tsp_results"]:
        results = st.session_state["tsp_results"]
        cities  = st.session_state["tsp_cities"]
        st.markdown("---")
        st.markdown("### Results")

        COLORS = {"BKT": "#818cf8", "NN": "#38bdf8", "HC": "#34d399",
                  "SA": "#f472b6", "GA": "#fb923c"}
        names = list(results.keys())
        costs = [results[n]["best_cost"] for n in names]

        fig_bar = go.Figure(go.Bar(
            x=names, y=costs,
            marker_color=[COLORS.get(n, "#888") for n in names],
            text=[f"{c:.1f}" for c in costs], textposition="outside",
        ))
        fig_bar.update_layout(
            title="Tour cost comparison (lower = better)",
            paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
            font_color="#e2e8f0", height=320,
            yaxis=dict(range=[0, max(costs) * 1.15]),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("#### Tour maps")
        cols = st.columns(min(len(results), 3))
        for idx, (name, res) in enumerate(results.items()):
            with cols[idx % len(cols)]:
                fig = plot_tour(cities, res["best_tour"],
                                title=f"{name}  |  cost {res['best_cost']:.1f}",
                                color=COLORS.get(name, "#888"))
                st.plotly_chart(fig, use_container_width=True)

        conv_hists, conv_labels, conv_colors = [], [], []
        if "SA" in results:
            conv_hists.append(results["SA"]["cost_history"])
            conv_labels.append("SA"); conv_colors.append("#f472b6")
        if "GA" in results:
            conv_hists.append(results["GA"]["convergence"])
            conv_labels.append("GA"); conv_colors.append("#fb923c")
        if "HC" in results:
            conv_hists.append(results["HC"]["cost_history"][0])
            conv_labels.append("HC restart 1"); conv_colors.append("#34d399")
        if conv_hists:
            st.markdown("#### Convergence curves")
            st.plotly_chart(plot_convergence(conv_hists, conv_labels, conv_colors),
                            use_container_width=True)

        st.markdown("#### Summary table")
        import pandas as pd
        rows = []
        for name, res in results.items():
            rows.append({
                "Algorithm": name,
                "Best cost": f"{res['best_cost']:.2f}",
                "Time (s)": f"{res.get('elapsed', 0):.3f}",
                "Solutions found": res.get("solutions_found", "-"),
            })
        st.dataframe(pd.DataFrame(rows).set_index("Algorithm"), use_container_width=True)


# -- Entry point (called by Streamlit when navigating to this page) ----------
st.set_page_config(
    page_title="TSP Algorithms - AI Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(_CSS, unsafe_allow_html=True)
render()
