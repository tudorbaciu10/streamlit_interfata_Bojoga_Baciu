import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd
import time
import io
import csv
from utils.i18n import t, lang_switcher_sidebar

_CSS = """
<style>
[data-testid="stSidebar"] { background: #0f172a; }
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
</style>
"""

COLORS = {"BKT": "#818cf8", "NN": "#38bdf8", "HC": "#34d399",
          "SA": "#f472b6", "GA": "#fb923c"}


def generate_cities(n, seed):
    rng = np.random.default_rng(seed)
    return rng.uniform(0, 100, (n, 2)).tolist()


def euclidean_matrix(cities):
    n = len(cities)
    return [[np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
             for j in range(n)] for i in range(n)]


def matrix_to_csv_bytes(matrix):
    buf = io.StringIO()
    writer = csv.writer(buf)
    for row in matrix:
        writer.writerow([f"{v:.4f}" for v in row])
    return buf.getvalue().encode()


def csv_bytes_to_matrix(uploaded_file):
    content = uploaded_file.read().decode()
    reader = csv.reader(io.StringIO(content))
    matrix = []
    for row in reader:
        stripped = [c.strip() for c in row if c.strip()]
        if stripped:
            matrix.append([float(v) for v in stripped])
    n = len(matrix)
    if any(len(r) != n for r in matrix):
        raise ValueError(f"Matrix is not square (expected {n}×{n})")
    return matrix


def plot_tour(cities, tour, title="Tour", color="#818cf8"):
    if tour is None or cities is None:
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
        textposition="top center", name="Cities",
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


def run_single(name, dist_matrix, params):
    from algorithms.backtracking import solve_bkt
    from algorithms.nearest_neighbour import solve_nn_multistart
    from algorithms.hill_climbing import solve_hc
    from algorithms.simulated_annealing import solve_sa
    from algorithms.genetic import solve_ga

    t0 = time.perf_counter()
    if name == "BKT":
        r = solve_bkt(dist_matrix, mode="first")
        cost = r["best_cost"]
    elif name == "NN":
        _, cost, _ = solve_nn_multistart(dist_matrix)
    elif name == "HC":
        r = solve_hc(dist_matrix,
                     max_iterations=params["hc_iters"],
                     restarts=params["hc_restarts"])
        cost = r["best_cost"]
    elif name == "SA":
        r = solve_sa(dist_matrix,
                     T_max=params["sa_tmax"],
                     alpha=params["sa_alpha"],
                     iterations=params["sa_iters"],
                     init_mode=params["sa_init"])
        cost = r["best_cost"]
    elif name == "GA":
        r = solve_ga(dist_matrix,
                     pop_size=params["ga_pop"],
                     n_generations=params["ga_gens"],
                     mutation_rate=params["ga_mut"],
                     elitism=params["ga_elite"],
                     selection=params["ga_sel"])
        cost = r["best_cost"]
    else:
        cost = float("inf")
    return cost, time.perf_counter() - t0


def render():
    st.markdown(f"## {t('tsp_title')}")
    st.markdown(t("tsp_subtitle"))

    # ---- Sidebar ------------------------------------------------------------
    with st.sidebar:
        st.markdown(f"### {t('tsp_sidebar')}")
        n_cities = st.slider(t("tsp_n_cities"), 5, 20, 10)
        seed = st.number_input(t("tsp_seed"), 0, 9999, 42, step=1)
        st.markdown("---")
        st.markdown(f"**{t('tsp_algos')}**")
        run_bkt = st.checkbox("BKT - Backtracking",    value=True)
        run_nn  = st.checkbox("NN  - Nearest Neighbour", value=True)
        run_hc  = st.checkbox("HC  - Hill Climbing",   value=True)
        run_sa  = st.checkbox("SA  - Simulated Annealing", value=True)
        run_ga  = st.checkbox("GA  - Genetic Algorithm",   value=True)
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
            sa_alpha = st.slider("Cooling rate alpha", 0.90, 0.999, 0.995,
                                 step=0.001, format="%.3f")
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

    lang_switcher_sidebar("tsp")

    params = dict(
        hc_iters=hc_iters, hc_restarts=hc_restarts,
        sa_tmax=sa_tmax, sa_alpha=sa_alpha, sa_iters=sa_iters, sa_init=sa_init,
        ga_pop=ga_pop, ga_gens=ga_gens, ga_mut=ga_mut, ga_elite=ga_elite, ga_sel=ga_sel,
    )

    # ---- Matrix source ------------------------------------------------------
    st.markdown(f"### {t('tsp_matrix_hdr')}")
    up_col, dl_col = st.columns(2)

    with up_col:
        uploaded = st.file_uploader(t("tsp_upload"), type="csv")

    custom_matrix = None
    if uploaded is not None:
        try:
            custom_matrix = csv_bytes_to_matrix(uploaded)
            st.success(t("tsp_custom_ok", n=len(custom_matrix)))
        except Exception as exc:
            st.error(f"Could not parse CSV: {exc}")

    cities = generate_cities(n_cities, int(seed))
    dist_matrix  = custom_matrix if custom_matrix is not None else euclidean_matrix(cities)
    active_cities = None if custom_matrix is not None else cities
    active_n = len(dist_matrix)

    with dl_col:
        st.download_button(
            label=t("tsp_download"),
            data=matrix_to_csv_bytes(dist_matrix),
            file_name=f"tsp_matrix_{active_n}cities.csv",
            mime="text/csv",
        )

    if custom_matrix is None:
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
    else:
        st.info(t("tsp_custom_info", n=active_n))

    # ---- Run algorithms -----------------------------------------------------
    if st.button(t("tsp_run_btn"), type="primary", use_container_width=True):
        steps = sum([run_bkt, run_nn, run_hc, run_sa, run_ga])
        if steps == 0:
            st.warning(t("tsp_no_algo"))
        else:
            results  = {}
            progress = st.progress(0, text="Running algorithms...")
            done     = 0

            if run_bkt:
                from algorithms.backtracking import solve_bkt
                with st.spinner("BKT running..."):
                    t0 = time.perf_counter()
                    r = solve_bkt(dist_matrix, mode=bkt_mode,
                                  time_limit=bkt_time, max_solutions=bkt_y)
                    r["elapsed"] = time.perf_counter() - t0
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
                    t0 = time.perf_counter()
                    r = solve_hc(dist_matrix, max_iterations=hc_iters, restarts=hc_restarts)
                    r["elapsed"] = time.perf_counter() - t0
                results["HC"] = r
                done += 1
                progress.progress(done / steps, text="HC done")

            if run_sa:
                from algorithms.simulated_annealing import solve_sa
                with st.spinner("SA running..."):
                    t0 = time.perf_counter()
                    r = solve_sa(dist_matrix, T_max=sa_tmax, alpha=sa_alpha,
                                 iterations=sa_iters, init_mode=sa_init)
                    r["elapsed"] = time.perf_counter() - t0
                results["SA"] = r
                done += 1
                progress.progress(done / steps, text="SA done")

            if run_ga:
                from algorithms.genetic import solve_ga
                with st.spinner("GA running..."):
                    t0 = time.perf_counter()
                    r = solve_ga(dist_matrix, pop_size=ga_pop, n_generations=ga_gens,
                                 mutation_rate=ga_mut, elitism=ga_elite, selection=ga_sel)
                    r["elapsed"] = time.perf_counter() - t0
                results["GA"] = r
                done += 1
                progress.progress(done / steps, text="GA done")

            progress.empty()
            st.session_state["tsp_results"] = results
            st.session_state["tsp_cities"]  = active_cities

    # ---- Results ------------------------------------------------------------
    if "tsp_results" in st.session_state and st.session_state["tsp_results"]:
        results    = st.session_state["tsp_results"]
        res_cities = st.session_state["tsp_cities"]
        st.markdown("---")
        st.markdown(f"### {t('tsp_results')}")

        names  = list(results.keys())
        costs  = [results[n]["best_cost"] for n in names]
        times  = [results[n].get("elapsed", 0.0) for n in names]
        colors = [COLORS.get(n, "#888") for n in names]

        fig_bar = go.Figure(go.Bar(
            x=names, y=costs, marker_color=colors,
            text=[f"{c:.1f}" for c in costs], textposition="outside",
        ))
        fig_bar.update_layout(
            title=t("tsp_cost_title"),
            paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
            font_color="#e2e8f0", height=320,
            yaxis=dict(range=[0, max(costs) * 1.15]),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        fig_time_bar = go.Figure(go.Bar(
            x=names, y=times, marker_color=colors,
            text=[f"{tv:.3f}s" for tv in times], textposition="outside",
        ))
        fig_time_bar.update_layout(
            title=t("tsp_time_title"),
            paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
            font_color="#e2e8f0", height=280,
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_time_bar, use_container_width=True)

        fig_scatter = go.Figure()
        for name, cost, tv in zip(names, costs, times):
            fig_scatter.add_trace(go.Scatter(
                x=[tv], y=[cost],
                mode="markers+text",
                marker=dict(size=20, color=COLORS.get(name, "#888"),
                            line=dict(color="#e2e8f0", width=1)),
                text=[name], textposition="top center",
                name=name,
            ))
        fig_scatter.update_layout(
            title=t("tsp_scatter_title"),
            xaxis_title=t("tsp_scatter_x"), yaxis_title=t("tsp_scatter_y"),
            paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
            font_color="#e2e8f0", height=360,
            legend=dict(bgcolor="#1e293b"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

        if res_cities is not None:
            st.markdown(f"#### {t('tsp_tour_maps')}")
            cols = st.columns(min(len(results), 3))
            for idx, (name, res) in enumerate(results.items()):
                with cols[idx % len(cols)]:
                    fig = plot_tour(res_cities, res["best_tour"],
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
            st.markdown(f"#### {t('tsp_convergence')}")
            st.plotly_chart(plot_convergence(conv_hists, conv_labels, conv_colors),
                            use_container_width=True)

        st.markdown(f"#### {t('tsp_summary')}")
        rows = []
        for name, res in results.items():
            rows.append({
                "Algorithm":          name,
                t("tsp_col_cost"):    f"{res['best_cost']:.2f}",
                t("tsp_col_time"):    f"{res.get('elapsed', 0):.3f}",
                t("tsp_col_sol"):     res.get("solutions_found", "-"),
            })
        st.dataframe(pd.DataFrame(rows).set_index("Algorithm"), use_container_width=True)

    # ---- Benchmark ----------------------------------------------------------
    st.markdown("---")
    with st.expander(t("tsp_bm_hdr"), expanded=False):
        st.markdown(t("tsp_bm_desc"))

        bm_c1, bm_c2 = st.columns(2)
        with bm_c1:
            bm_sizes = st.multiselect(t("tsp_bm_sizes"), [5, 8, 10, 12, 15],
                                      default=[5, 8, 10, 12], key="bm_sizes")
            bm_seeds = st.slider(t("tsp_bm_seeds"), 1, 5, 3, key="bm_seeds")
        with bm_c2:
            st.markdown(f"**{t('tsp_bm_algos')}**")
            bm_bkt = st.checkbox("BKT", value=True, key="bm_bkt")
            bm_nn  = st.checkbox("NN",  value=True, key="bm_nn")
            bm_hc  = st.checkbox("HC",  value=True, key="bm_hc")
            bm_sa  = st.checkbox("SA",  value=True, key="bm_sa")
            bm_ga  = st.checkbox("GA",  value=True, key="bm_ga")
            st.caption(t("tsp_bm_note"))

        if st.button(t("tsp_bm_btn"), type="primary", key="run_benchmark"):
            if not bm_sizes:
                st.warning(t("tsp_bm_no_size"))
            else:
                run_flags  = {"BKT": bm_bkt, "NN": bm_nn, "HC": bm_hc,
                              "SA": bm_sa, "GA": bm_ga}
                active_algos = [n for n, f in run_flags.items() if f]
                bm_data = {n: {sz: {"costs": [], "times": []} for sz in bm_sizes}
                           for n in active_algos}

                total_steps = len(bm_sizes) * bm_seeds * len(active_algos)
                prog = st.progress(0, text=t("tsp_bm_running"))
                step = 0

                for sz in sorted(bm_sizes):
                    for s in range(bm_seeds):
                        bm_cities = generate_cities(sz, s * 137 + sz)
                        bm_matrix = euclidean_matrix(bm_cities)
                        for algo in active_algos:
                            if algo == "BKT" and sz > 10:
                                step += 1
                                prog.progress(min(step / total_steps, 1.0))
                                continue
                            cost, elapsed = run_single(algo, bm_matrix, params)
                            bm_data[algo][sz]["costs"].append(cost)
                            bm_data[algo][sz]["times"].append(elapsed)
                            step += 1
                            prog.progress(min(step / total_steps, 1.0))

                prog.empty()
                st.session_state["bm_data"]         = bm_data
                st.session_state["bm_sizes_stored"] = sorted(bm_sizes)
                st.success(t("tsp_bm_done"))

        if "bm_data" in st.session_state:
            bm_data    = st.session_state["bm_data"]
            bm_stored  = st.session_state["bm_sizes_stored"]
            algo_names = list(bm_data.keys())

            fig_cost = go.Figure()
            for algo in algo_names:
                xs, avgs, errs = [], [], []
                for sz in bm_stored:
                    c_list = bm_data[algo][sz]["costs"]
                    if c_list:
                        xs.append(sz)
                        avgs.append(float(np.mean(c_list)))
                        errs.append(float(np.std(c_list)))
                if xs:
                    fig_cost.add_trace(go.Scatter(
                        x=xs, y=avgs, mode="lines+markers", name=algo,
                        line=dict(color=COLORS.get(algo, "#888"), width=2),
                        error_y=dict(type="data", array=errs, visible=True,
                                     color=COLORS.get(algo, "#888")),
                    ))
            fig_cost.update_layout(
                title=t("tsp_bm_cost_title"),
                xaxis_title="N cities", yaxis_title="Avg cost",
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=360, legend=dict(bgcolor="#1e293b"),
            )
            st.plotly_chart(fig_cost, use_container_width=True)

            fig_time = go.Figure()
            for algo in algo_names:
                xs, avgs = [], []
                for sz in bm_stored:
                    t_list = bm_data[algo][sz]["times"]
                    if t_list:
                        xs.append(sz)
                        avgs.append(float(np.mean(t_list)))
                if xs:
                    fig_time.add_trace(go.Scatter(
                        x=xs, y=avgs, mode="lines+markers", name=algo,
                        line=dict(color=COLORS.get(algo, "#888"), width=2),
                    ))
            fig_time.update_layout(
                title=t("tsp_bm_time_title"),
                xaxis_title="N cities", yaxis_title="Avg time (s)",
                yaxis_type="log",
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=320, legend=dict(bgcolor="#1e293b"),
            )
            st.plotly_chart(fig_time, use_container_width=True)

            fig_box = go.Figure()
            for algo in algo_names:
                all_costs = []
                for sz in bm_stored:
                    all_costs.extend(bm_data[algo][sz]["costs"])
                if all_costs:
                    fig_box.add_trace(go.Box(
                        y=all_costs, name=algo,
                        marker_color=COLORS.get(algo, "#888"),
                        line_color=COLORS.get(algo, "#888"),
                    ))
            fig_box.update_layout(
                title=t("tsp_bm_box_title"), yaxis_title="Tour cost",
                paper_bgcolor="#0f172a", plot_bgcolor="#1e293b",
                font_color="#e2e8f0", height=320,
            )
            st.plotly_chart(fig_box, use_container_width=True)

            st.markdown(f"#### {t('tsp_bm_table_hdr')}")
            rows = []
            for sz in bm_stored:
                row = {"N cities": sz}
                for algo in algo_names:
                    c_list = bm_data[algo][sz]["costs"]
                    t_list = bm_data[algo][sz]["times"]
                    if c_list:
                        row[f"{algo} cost"] = f"{np.mean(c_list):.1f}±{np.std(c_list):.1f}"
                        row[f"{algo} time"] = f"{np.mean(t_list):.3f}s"
                    else:
                        row[f"{algo} cost"] = "N/A"
                        row[f"{algo} time"] = "N/A"
                rows.append(row)
            st.dataframe(pd.DataFrame(rows).set_index("N cities"), use_container_width=True)


# -- Entry point --------------------------------------------------------------
st.set_page_config(
    page_title="TSP Algorithms - AI Explorer",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(_CSS, unsafe_allow_html=True)
render()
