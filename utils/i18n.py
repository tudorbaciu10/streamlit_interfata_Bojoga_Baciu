"""Internationalization: RO/EN translations + sidebar language switcher."""
import streamlit as st

TRANSLATIONS = {
    "ro": {
        # --- Task Manager ---
        "tm_title":         "Task Manager - Streamlit",
        "tm_form_header":   "Adaugă un task nou",
        "tm_field_label":   "Descriere task",
        "tm_placeholder":   "Scrie descrierea task-ului...",
        "tm_add_btn":       "Adaugă",
        "tm_empty_warning": "Câmpul nu poate fi gol.",
        "tm_no_tasks":      "Niciun task adăugat. Scrieți o descriere în câmpul de mai sus și apăsați «Adaugă».",
        "tm_progress":      "{done}/{total} task-uri finalizate",

        # --- Echipa ---
        "echipa_title":       "Despre echipă",
        "echipa_team_label":  "Echipa",
        "echipa_fac_label":   "Facultatea",
        "echipa_fac_val":     "FIESC — Facultatea de Inginerie Electrică și Știința Calculatoarelor",
        "echipa_univ_label":  "Universitatea",
        "echipa_univ_val":    "Universitatea Ștefan cel Mare, Suceava (USV)",
        "echipa_spec_label":  "Specializarea",
        "echipa_spec_val":    "Calculatoare",
        "echipa_year_label":  "An de studiu",
        "echipa_year_val":    "Anul III",
        "echipa_subj_label":  "Disciplina",
        "echipa_subj_val":    "Inteligență Artificială",
        "echipa_prof_label":  "Profesor coordonator",
        "echipa_prof_val":    "Conf. dr. ing. Ovidiu GHERMAN",
        "echipa_members":     "Membri",
        "echipa_student":     "Student — Calculatoare, Anul III",
        "echipa_fiesc":       "FIESC, USV Suceava",
        "echipa_about":       "Despre proiect",
        "echipa_about_text":  (
            "Proiect realizat pentru disciplina **Inteligență Artificială**, ce include:\n\n"
            "- **TSP Solver** — implementare și comparare a 5 algoritmi pentru problema "
            "comis-voiajorului: Backtracking, Nearest Neighbour, Hill Climbing, "
            "Simulated Annealing, Genetic Algorithm\n"
            "- **NLP Classifier** — clasificare de text cu TF-IDF + clasificatori ML "
            "(Naive Bayes, SVM, Logistic Regression, Random Forest) și clasificator "
            "bazat pe dicționare de cuvinte-cheie\n"
            "- **Task Manager** — aplicație simplă de gestiune a task-urilor"
        ),

        # --- TSP ---
        "tsp_title":          "TSP - Problema Comis-Voiajorului",
        "tsp_subtitle":       "Configurează problema, alege algoritmi, rulează și compară rezultatele.",
        "tsp_sidebar":        "Setări TSP",
        "tsp_n_cities":       "Număr de orașe",
        "tsp_seed":           "Seed aleator",
        "tsp_algos":          "Algoritmi de rulat",
        "tsp_matrix_hdr":     "Oraș / Matrice de distanțe",
        "tsp_upload":         "Încarcă matrice CSV (opțional)",
        "tsp_download":       "Descarcă matricea curentă ca CSV",
        "tsp_custom_ok":      "Matrice personalizată încărcată: {n}×{n}",
        "tsp_custom_info":    "Se folosește matricea {n}×{n} — harta orașelor nu este disponibilă.",
        "tsp_run_btn":        "Rulează algoritmii selectați",
        "tsp_no_algo":        "Selectează cel puțin un algoritm.",
        "tsp_results":        "Rezultate",
        "tsp_cost_title":     "Comparare cost traseu (mai mic = mai bun)",
        "tsp_time_title":     "Timp de execuție (secunde)",
        "tsp_scatter_title":  "Performanță: cost vs timp  (stânga-jos = cel mai bun)",
        "tsp_scatter_x":      "Timp de execuție (s)",
        "tsp_scatter_y":      "Cost traseu",
        "tsp_tour_maps":      "Hărți traseu",
        "tsp_convergence":    "Curbe de convergență",
        "tsp_summary":        "Tabel sumar",
        "tsp_col_cost":       "Cost optim",
        "tsp_col_time":       "Timp (s)",
        "tsp_col_sol":        "Soluții găsite",
        "tsp_bm_hdr":         "Benchmark comparativ",
        "tsp_bm_desc":        (
            "Rulează algoritmii selectați pe mai multe dimensiuni de problemă și seed-uri "
            "multiple pentru a compara performanța agregată."
        ),
        "tsp_bm_sizes":       "Dimensiuni problemă (nr. orașe)",
        "tsp_bm_seeds":       "Rulări per dimensiune (seed-uri)",
        "tsp_bm_algos":       "Algoritmi incluși:",
        "tsp_bm_note":        "BKT este omis automat pentru N > 10.",
        "tsp_bm_btn":         "Rulează Benchmark",
        "tsp_bm_no_size":     "Selectează cel puțin o dimensiune.",
        "tsp_bm_done":        "Benchmark finalizat!",
        "tsp_bm_running":     "Se rulează benchmark-ul...",
        "tsp_bm_cost_title":  "Cost mediu vs dimensiunea problemei (bare eroare = std dev)",
        "tsp_bm_time_title":  "Timp mediu vs dimensiunea problemei (scară log)",
        "tsp_bm_box_title":   "Distribuția costurilor per algoritm (toate dimensiunile)",
        "tsp_bm_table_hdr":   "Tabel sumar (cost mediu ± std | timp mediu)",

        # --- NLP ---
        "nlp_title":          "NLP - Clasificare Text",
        "nlp_subtitle":       "Antrenează și compară clasificatori pe seturi de date reale cu parametri TF-IDF configurabili.",
        "nlp_sidebar":        "Setări NLP",
        "nlp_dataset":        "Set de date",
        "nlp_tfidf_hdr":      "Parametri TF-IDF",
        "nlp_clf_hdr":        "Clasificatori de rulat",
        "nlp_dict_clf":       "Clasificator Dicționar (reguli)",
        "nlp_tab_compare":    "Compară toți",
        "nlp_tab_single":     "Clasificator individual",
        "nlp_tab_live":       "Predictor live",
        "nlp_tab_dicts":      "Dicționare cuvinte-cheie",
        "nlp_compare_hdr":    "Compară toți clasificatorii selectați",
        "nlp_run_btn":        "Antrenează & Compară",
        "nlp_no_clf":         "Selectează cel puțin un clasificator.",
        "nlp_loaded":         "Set de date încărcat: {train} antrenare / {test} testare, {cls} clase.",
        "nlp_acc_f1_title":   "Acuratețe vs F1 macro",
        "nlp_time_title":     "Timp de antrenare (secunde)",
        "nlp_perf_title":     "Performanță: acuratețe vs timp  (stânga-sus = cel mai bun)",
        "nlp_cm_hdr":         "Matrici de confuzie",
        "nlp_single_hdr":     "Clasificator individual — studiu parametri",
        "nlp_study_effect":   "Studiază efectul parametrului",
        "nlp_study_btn":      "Rulează studiul de parametri",
        "nlp_live_hdr":       "Predictor text live",
        "nlp_live_desc":      "Antrenează un model, apoi scrie orice text englezesc pentru a vedea categoria prezisă.",
        "nlp_train_btn":      "Antrenează modelul live",
        "nlp_model_ready":    "Model pregătit! ({clf})",
        "nlp_text_label":     "Introdu text englezesc pentru clasificare:",
        "nlp_text_ph":        "Scrie orice text...",
        "nlp_predict_btn":    "Prezice",
        "nlp_predicted":      "Categorie prezisă:",
        "nlp_proba_title":    "Probabilități / scoruri per clasă",
        "nlp_dicts_hdr":      "Dicționare de cuvinte-cheie per categorie",
        "nlp_dicts_desc":     (
            "Clasificatorul bazat pe reguli folosește câte o listă de cuvinte-cheie per "
            "categorie. Mai jos sunt dicționarele active pentru setul de date selectat."
        ),
        "nlp_dicts_footer":   "{n} dicționare active · {total} cuvinte-cheie totale",
    },

    "en": {
        # --- Task Manager ---
        "tm_title":         "Task Manager - Streamlit",
        "tm_form_header":   "Add a new task",
        "tm_field_label":   "Task description",
        "tm_placeholder":   "Write task description...",
        "tm_add_btn":       "Add",
        "tm_empty_warning": "Field cannot be empty.",
        "tm_no_tasks":      "No tasks added. Write a description in the field above and press «Add».",
        "tm_progress":      "{done}/{total} tasks completed",

        # --- Echipa ---
        "echipa_title":       "About the team",
        "echipa_team_label":  "Team",
        "echipa_fac_label":   "Faculty",
        "echipa_fac_val":     "FIESC — Faculty of Electrical Engineering and Computer Science",
        "echipa_univ_label":  "University",
        "echipa_univ_val":    "Stefan cel Mare University, Suceava (USV)",
        "echipa_spec_label":  "Specialization",
        "echipa_spec_val":    "Computer Science",
        "echipa_year_label":  "Year of study",
        "echipa_year_val":    "Year III",
        "echipa_subj_label":  "Subject",
        "echipa_subj_val":    "Artificial Intelligence",
        "echipa_prof_label":  "Supervising professor",
        "echipa_prof_val":    "Assoc. prof. dr. eng. Ovidiu GHERMAN",
        "echipa_members":     "Members",
        "echipa_student":     "Student — Computer Science, Year III",
        "echipa_fiesc":       "FIESC, USV Suceava",
        "echipa_about":       "About the project",
        "echipa_about_text":  (
            "Project developed for the **Artificial Intelligence** course, including:\n\n"
            "- **TSP Solver** — implementation and comparison of 5 algorithms for the "
            "Travelling Salesman Problem: Backtracking, Nearest Neighbour, Hill Climbing, "
            "Simulated Annealing, Genetic Algorithm\n"
            "- **NLP Classifier** — text classification with TF-IDF + ML classifiers "
            "(Naive Bayes, SVM, Logistic Regression, Random Forest) and a rule-based "
            "keyword dictionary classifier\n"
            "- **Task Manager** — simple task management application"
        ),

        # --- TSP ---
        "tsp_title":          "TSP - Travelling Salesman Problem",
        "tsp_subtitle":       "Configure the problem, pick algorithms, run them, and compare results side-by-side.",
        "tsp_sidebar":        "TSP Settings",
        "tsp_n_cities":       "Number of cities",
        "tsp_seed":           "Random seed",
        "tsp_algos":          "Algorithms to run",
        "tsp_matrix_hdr":     "City / Distance Matrix",
        "tsp_upload":         "Upload adjacency matrix CSV (optional)",
        "tsp_download":       "Download current matrix as CSV",
        "tsp_custom_ok":      "Custom matrix loaded: {n}×{n}",
        "tsp_custom_info":    "Using custom {n}×{n} adjacency matrix — city map not available.",
        "tsp_run_btn":        "Run selected algorithms",
        "tsp_no_algo":        "Select at least one algorithm.",
        "tsp_results":        "Results",
        "tsp_cost_title":     "Tour cost comparison (lower = better)",
        "tsp_time_title":     "Execution time (seconds)",
        "tsp_scatter_title":  "Performance: cost vs execution time  (bottom-left = best)",
        "tsp_scatter_x":      "Execution time (s)",
        "tsp_scatter_y":      "Tour cost",
        "tsp_tour_maps":      "Tour maps",
        "tsp_convergence":    "Convergence curves",
        "tsp_summary":        "Summary table",
        "tsp_col_cost":       "Best cost",
        "tsp_col_time":       "Time (s)",
        "tsp_col_sol":        "Solutions found",
        "tsp_bm_hdr":         "Comparative Benchmark",
        "tsp_bm_desc":        (
            "Run selected algorithms on multiple problem sizes and multiple seeds "
            "to compare aggregate performance."
        ),
        "tsp_bm_sizes":       "Problem sizes (number of cities)",
        "tsp_bm_seeds":       "Runs per size (seeds)",
        "tsp_bm_algos":       "Algorithms included:",
        "tsp_bm_note":        "BKT is automatically skipped for N > 10.",
        "tsp_bm_btn":         "Run Benchmark",
        "tsp_bm_no_size":     "Select at least one problem size.",
        "tsp_bm_done":        "Benchmark complete!",
        "tsp_bm_running":     "Running benchmark...",
        "tsp_bm_cost_title":  "Avg tour cost vs problem size (error bars = std dev)",
        "tsp_bm_time_title":  "Avg execution time vs problem size (log scale)",
        "tsp_bm_box_title":   "Cost distribution per algorithm (all problem sizes)",
        "tsp_bm_table_hdr":   "Summary table (avg cost ± std | avg time)",

        # --- NLP ---
        "nlp_title":          "NLP - Text Classification",
        "nlp_subtitle":       "Train and compare classifiers on real English datasets with configurable TF-IDF parameters.",
        "nlp_sidebar":        "NLP Settings",
        "nlp_dataset":        "Dataset",
        "nlp_tfidf_hdr":      "TF-IDF Parameters",
        "nlp_clf_hdr":        "Classifiers to run",
        "nlp_dict_clf":       "Dictionary Classifier (rules)",
        "nlp_tab_compare":    "Compare all",
        "nlp_tab_single":     "Single classifier",
        "nlp_tab_live":       "Live predictor",
        "nlp_tab_dicts":      "Keyword dictionaries",
        "nlp_compare_hdr":    "Compare all selected classifiers",
        "nlp_run_btn":        "Train & Compare",
        "nlp_no_clf":         "Select at least one classifier.",
        "nlp_loaded":         "Dataset loaded: {train} train / {test} test, {cls} classes.",
        "nlp_acc_f1_title":   "Accuracy vs F1 macro",
        "nlp_time_title":     "Training time (seconds)",
        "nlp_perf_title":     "Performance: accuracy vs training time  (top-left = best)",
        "nlp_cm_hdr":         "Confusion matrices",
        "nlp_single_hdr":     "Single classifier — parameter study",
        "nlp_study_effect":   "Study effect of",
        "nlp_study_btn":      "Run parameter study",
        "nlp_live_hdr":       "Live text predictor",
        "nlp_live_desc":      "Train a model, then type any English text to see the predicted category.",
        "nlp_train_btn":      "Train live model",
        "nlp_model_ready":    "Model ready! ({clf})",
        "nlp_text_label":     "Enter English text to classify:",
        "nlp_text_ph":        "Type any text here...",
        "nlp_predict_btn":    "Predict",
        "nlp_predicted":      "Predicted category:",
        "nlp_proba_title":    "Class probabilities / scores",
        "nlp_dicts_hdr":      "Keyword dictionaries per category",
        "nlp_dicts_desc":     (
            "The rule-based Dictionary Classifier uses one keyword list per newsgroup "
            "category. Shown below are the active dictionaries for the selected dataset."
        ),
        "nlp_dicts_footer":   "{n} active dictionaries · {total} total keywords",
    },
}


def t(key, **kwargs):
    """Return the translated string for the current session language."""
    lang = st.session_state.get("lang", "ro")
    text = TRANSLATIONS.get(lang, TRANSLATIONS["ro"]).get(key, key)
    return text.format(**kwargs) if kwargs else text


def lang_switcher_sidebar(page_key: str = ""):
    """Render a RO / EN toggle at the bottom of the sidebar."""
    if "lang" not in st.session_state:
        st.session_state["lang"] = "ro"
    lang = st.session_state["lang"]
    with st.sidebar:
        st.markdown("---")
        c1, c2 = st.columns(2)
        if c1.button(
            "🇷🇴 RO",
            type="primary" if lang == "ro" else "secondary",
            use_container_width=True,
            key=f"lang_ro_{page_key}",
        ):
            st.session_state["lang"] = "ro"
            st.rerun()
        if c2.button(
            "🇬🇧 EN",
            type="primary" if lang == "en" else "secondary",
            use_container_width=True,
            key=f"lang_en_{page_key}",
        ):
            st.session_state["lang"] = "en"
            st.rerun()
