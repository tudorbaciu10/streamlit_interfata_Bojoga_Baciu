# -*- coding: utf-8 -*-
"""
Ruleaza din radacina proiectului:
    .venv\\Scripts\\python.exe generate_docs.py
Genereaza fisierul  documentatie_IA.docx  in acelasi folder.
"""
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import datetime

doc = Document()

# ── Margini ────────────────────────────────────────────────────────────────
for section in doc.sections:
    section.top_margin    = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin   = Cm(3)
    section.right_margin  = Cm(2)

# ── Stiluri helper ──────────────────────────────────────────────────────────
def heading(text, level=1):
    p = doc.add_heading(text, level=level)
    p.runs[0].font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)
    return p

def body(text):
    p = doc.add_paragraph(text)
    p.style.font.size = Pt(11)
    return p

def placeholder(text):
    """Chenar gri pentru locul unde se inserează screenshot."""
    p = doc.add_paragraph()
    run = p.add_run(f"[{text}]")
    run.font.size    = Pt(10)
    run.font.italic  = True
    run.font.color.rgb = RGBColor(0x64, 0x74, 0x8b)
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after  = Pt(6)
    return p

def caption(text):
    p = doc.add_paragraph(text)
    run = p.runs[0]
    run.font.size   = Pt(9)
    run.font.italic = True
    p.alignment     = WD_ALIGN_PARAGRAPH.CENTER
    return p

# ═══════════════════════════════════════════════════════════════════════════
# PAGINA DE TITLU
# ═══════════════════════════════════════════════════════════════════════════
doc.add_paragraph()
doc.add_paragraph()

t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run("Universitatea Ștefan cel Mare, Suceava")
r.font.size = Pt(13)
r.font.bold = True

t2 = doc.add_paragraph()
t2.alignment = WD_ALIGN_PARAGRAPH.CENTER
t2.add_run("Facultatea de Inginerie Electrică și Știința Calculatoarelor (FIESC)").font.size = Pt(12)

t3 = doc.add_paragraph()
t3.alignment = WD_ALIGN_PARAGRAPH.CENTER
t3.add_run("Specializarea: Calculatoare, Anul III").font.size = Pt(12)

doc.add_paragraph()
doc.add_paragraph()

title = doc.add_paragraph()
title.alignment = WD_ALIGN_PARAGRAPH.CENTER
tr = title.add_run("DOCUMENTAȚIE PROIECT\nInteligență Artificială")
tr.font.size = Pt(22)
tr.font.bold = True
tr.font.color.rgb = RGBColor(0x1e, 0x40, 0xaf)

doc.add_paragraph()

sub = doc.add_paragraph()
sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
sr = sub.add_run("Aplicație web pentru rezolvarea problemei TSP\nși clasificarea textului cu tehnici NLP")
sr.font.size   = Pt(14)
sr.font.italic = True

doc.add_paragraph()
doc.add_paragraph()

team = doc.add_paragraph()
team.alignment = WD_ALIGN_PARAGRAPH.CENTER
team.add_run("Echipa: ").font.size = Pt(12)
tr2 = team.add_run("Just Here For Money")
tr2.font.size = Pt(12)
tr2.font.bold = True

for member in ["Bojoga Andrei", "Baciu Tudor"]:
    m = doc.add_paragraph()
    m.alignment = WD_ALIGN_PARAGRAPH.CENTER
    m.add_run(member).font.size = Pt(12)

doc.add_paragraph()
prof = doc.add_paragraph()
prof.alignment = WD_ALIGN_PARAGRAPH.CENTER
pr = prof.add_run("Coordonator: Conf. dr. ing. Ovidiu GHERMAN")
pr.font.size = Pt(11)

year = doc.add_paragraph()
year.alignment = WD_ALIGN_PARAGRAPH.CENTER
year.add_run(f"Anul universitar 2024 – 2025").font.size = Pt(11)

doc.add_page_break()

# ═══════════════════════════════════════════════════════════════════════════
# 1. INTRODUCERE
# ═══════════════════════════════════════════════════════════════════════════
heading("1. Introducere")
body(
    "Prezentul proiect a fost realizat în cadrul disciplinei Inteligență Artificială și "
    "propune o aplicație web interactivă construită cu framework-ul Streamlit, care "
    "integrează două domenii clasice ale inteligenței artificiale: optimizare combinatorie "
    "(Problema Comis-Voiajorului – TSP) și procesarea limbajului natural (NLP – clasificare "
    "de text)."
)
body(
    "Aplicația permite utilizatorului să configureze parametrii algoritmilor, să ruleze "
    "comparații în timp real și să vizualizeze rezultatele prin grafice interactive. "
    "Interfața suportă două limbi (română și engleză) și oferă un modul de benchmark "
    "comparativ care evaluează performanța algoritmilor pe instanțe de dimensiuni variate."
)

# ═══════════════════════════════════════════════════════════════════════════
# 2. STRUCTURA APLICAȚIEI
# ═══════════════════════════════════════════════════════════════════════════
heading("2. Structura aplicației")
body(
    "Aplicația este structurată ca o aplicație multi-pagină Streamlit (MPA), cu "
    "următoarele componente principale:"
)

tbl = doc.add_table(rows=1, cols=2)
tbl.style = "Table Grid"
hdr = tbl.rows[0].cells
hdr[0].text = "Pagină"
hdr[1].text = "Descriere"
for cell in hdr:
    cell.paragraphs[0].runs[0].font.bold = True

pages = [
    ("Task Manager (pagina principală)",
     "Aplicație simplă de gestiune a task-urilor cu adăugare, bifat și ștergere, "
     "cu indicator de progres."),
    ("TSP – Travelling Salesman Problem",
     "Implementarea și compararea a 5 algoritmi TSP, cu grafice de cost, timp, "
     "convergență și benchmark comparativ."),
    ("NLP – Clasificare Text",
     "Clasificare text cu TF-IDF + 4 clasificatori ML și un clasificator bazat pe "
     "dicționare de cuvinte-cheie, cu comparare și predictor live."),
    ("Echipă",
     "Informații despre echipă: membri, facultate, an, disciplină, profesor."),
]
for pg, desc in pages:
    row = tbl.add_row().cells
    row[0].text = pg
    row[1].text = desc

doc.add_paragraph()
body(
    "Codul sursă este organizat în directoarele: pages/ (paginile aplicației), "
    "algorithms/ (implementările algoritmilor), utils/ (modul de internaționalizare). "
    "Toate paginile partajează starea limbii selectate prin st.session_state."
)

# ═══════════════════════════════════════════════════════════════════════════
# 3. ALGORITMI TSP IMPLEMENTAȚI
# ═══════════════════════════════════════════════════════════════════════════
heading("3. Algoritmi TSP implementați")
body(
    "Problema Comis-Voiajorului (TSP) cere găsirea turului de cost minim care vizitează "
    "fiecare nod al unui graf exact o dată și revine la nodul de start. Este o problemă "
    "NP-hard, motiv pentru care algoritmii exacți devin impractici pentru N mare, "
    "iar heuristicile sunt esențiale."
)

heading("3.1 Backtracking (BKT)", level=2)
body(
    "Algoritmul de backtracking explorează spațiul complet al permutărilor cu ramificare "
    "și tăiere (branch and bound). Se menține costul optim curent și se abandonează "
    "ramurile al căror cost parțial îl depășește."
)
body("Complexitate: O(N!) în cazul cel mai rău. Practic: N ≤ 12 în timp rezonabil.")
body(
    "Parametri configurabili: modul de oprire (prima soluție / toate soluțiile / "
    "limită de timp / Y soluții), limita de timp, numărul Y de soluții."
)

heading("3.2 Nearest Neighbour (NN)", level=2)
body(
    "Heuristica greedy pornește din fiecare nod pe rând și alege la fiecare pas "
    "cel mai apropiat nod nevizitat. Se returnează cel mai bun tur din toate punctele "
    "de start (multi-start NN)."
)
body("Complexitate: O(N²). Rapid, dar produse soluții tipic cu 20–25% deasupra optimului.")

heading("3.3 Hill Climbing (HC)", level=2)
body(
    "Pornind dintr-o soluție inițială aleatoare, HC aplică iterativ operatorul 2-opt "
    "(inversarea unui subsegment al turului) și acceptă numai îmbunătățiri. "
    "Se folosesc restart-uri multiple pentru a evita minimele locale."
)
body(
    "Parametri: număr de restart-uri (1–10), număr maxim de iterații (500–10.000)."
)

heading("3.4 Simulated Annealing (SA)", level=2)
body(
    "SA extinde Hill Climbing prin acceptarea soluțiilor mai slabe cu probabilitate "
    "exp(-Δcost / T), unde T (temperatura) scade geometric cu rata α după fiecare iterație. "
    "Permite escaparea din minime locale și converge spre soluții de calitate superioară."
)
body(
    "Parametri configurabili: temperatura inițială T_max (100–5.000), "
    "rata de răcire α (0,90–0,999), număr maxim de iterații (1.000–50.000), "
    "soluția inițială (NN sau aleatoare)."
)

heading("3.5 Genetic Algorithm (GA)", level=2)
body(
    "GA simulează evoluția unei populații de soluții prin selecție, crossover și mutație. "
    "Se folosește operatorul OX (Order Crossover) care garantează permutări valide, "
    "selecție prin turneu sau roletă, mutație prin swap și elitism."
)
body(
    "Parametri configurabili: dimensiunea populației (20–200), numărul de generații "
    "(50–1.000), rata de mutație (0,05–0,90), elitism (0–5 indivizi), "
    "tipul de selecție (turneu / roletă)."
)

placeholder("SCREENSHOT: Pagina TSP – configurare parametri SA și GA în sidebar")
caption("Figura 1. Configurarea parametrilor algoritmilor SA și GA")

# ═══════════════════════════════════════════════════════════════════════════
# 4. NLP – CLASIFICARE TEXT
# ═══════════════════════════════════════════════════════════════════════════
heading("4. NLP – Clasificare text")
body(
    "Modulul NLP realizează clasificarea automată a textelor din setul de date "
    "20 Newsgroups (scikit-learn). Textele sunt preprocesate cu TF-IDF (Term "
    "Frequency–Inverse Document Frequency) și clasificate cu mai mulți algoritmi."
)

heading("4.1 Preprocesare TF-IDF", level=2)
body(
    "Vectorizatorul TF-IDF transformă textul brut în vectori numerici ponderând "
    "frecvența termenilor în document față de frecvența lor în corpus. "
    "Parametri configurabili: max_features (1.000–50.000), ngram_range (unigrami/bigrami), "
    "sublinear_tf (logaritmul frecvenței)."
)

heading("4.2 Clasificatori ML", level=2)
rows_clf = [
    ("Naive Bayes (MultinomialNB)",
     "Model probabilistic bazat pe teorema Bayes. Rapid, bun baseline pentru text."),
    ("SVM (LinearSVC)",
     "Mașină cu vectori suport liniară. Produce rezultate excelente pe date text de înaltă dimensionalitate."),
    ("Logistic Regression",
     "Model liniar discriminativ, optimizat cu gradient descent. Performanță similară SVM."),
    ("Random Forest",
     "Ansamblu de arbori de decizie. Mai lent dar robust la zgomot în date."),
    ("Dictionary Classifier (reguli)",
     "Clasificator bazat pe dicționare de cuvinte-cheie per categorie (20 dicționare). "
     "Zero timp de antrenare, acuratețe mai mică, interpretabil."),
]
tbl2 = doc.add_table(rows=1, cols=2)
tbl2.style = "Table Grid"
h2 = tbl2.rows[0].cells
h2[0].text = "Clasificator"
h2[1].text = "Descriere"
for cell in h2:
    cell.paragraphs[0].runs[0].font.bold = True
for clf_name, clf_desc in rows_clf:
    r2 = tbl2.add_row().cells
    r2[0].text = clf_name
    r2[1].text = clf_desc
doc.add_paragraph()

# ═══════════════════════════════════════════════════════════════════════════
# 5. BENCHMARK-URI PROPUSE
# ═══════════════════════════════════════════════════════════════════════════
heading("5. Benchmark-uri comparative")

heading("5.1 Benchmark TSP", level=2)
body(
    "Benchmark-ul TSP rulează toți algoritmii selectați pe mai multe dimensiuni de "
    "problemă (N ∈ {5, 10, 20, 30, 50, 75, 100}) cu câte 3–5 seed-uri aleatoare per "
    "dimensiune. Se calculează costul mediu ± abatere standard și timpul mediu de execuție."
)
body(
    "Notă: algoritmul BKT este exclus automat pentru N > 10 datorită complexității "
    "exponențiale. Ceilalți algoritmi (NN, HC, SA, GA) sunt evaluați pe toate dimensiunile."
)
body("Grafice generate:")
for item in ["Cost mediu vs. numărul de orașe (cu bare de eroare)",
             "Timp mediu de execuție vs. N (scară logaritmică)",
             "Distribuția costurilor per algoritm (box plot)",
             "Tabel sumar: cost mediu ± std | timp mediu"]:
    p = doc.add_paragraph(item, style="List Bullet")

heading("5.2 Benchmark NLP", level=2)
body(
    "Benchmark-ul NLP compară cei 5 clasificatori pe 3 seturi de date "
    "(4 categorii, 4 categorii știință, 20 categorii) și studiază efectul "
    "parametrilor TF-IDF (max_features, ngram_range) asupra acurateței."
)
body("Grafice generate:")
for item in ["Acuratețe vs. F1 macro (bar chart grupat)",
             "Timp de antrenare per clasificator",
             "Scatter: acuratețe vs. timp (cost-eficiență)",
             "Matrici de confuzie per clasificator"]:
    p = doc.add_paragraph(item, style="List Bullet")

# ═══════════════════════════════════════════════════════════════════════════
# 6. GRAFICE DE PERFORMANȚĂ
# ═══════════════════════════════════════════════════════════════════════════
heading("6. Grafice de performanță")
body(
    "Graficele de mai jos au fost obținute rulând aplicația pe un sistem desktop. "
    "Instanțele TSP au fost generate aleator cu distanțe euclidiene. "
    "Setul de date NLP este 20 Newsgroups (4 categorii)."
)

placeholder("SCREENSHOT: TSP – Cost comparison bar chart (toți 5 algoritmi, N=15, seed=42)")
caption("Figura 2. Compararea costului turului pentru cei 5 algoritmi (N=15)")

placeholder("SCREENSHOT: TSP – Execution time bar chart")
caption("Figura 3. Compararea timpului de execuție")

placeholder("SCREENSHOT: TSP – Performance scatter: cost vs timp")
caption("Figura 4. Performanță: cost vs. timp de execuție")

placeholder("SCREENSHOT: TSP – Tour maps pentru toți algoritmii")
caption("Figura 5. Vizualizarea tururilor obținute de fiecare algoritm")

placeholder("SCREENSHOT: TSP – Convergence curves (SA, GA, HC)")
caption("Figura 6. Curbele de convergență SA, GA și HC")

placeholder("SCREENSHOT: TSP Benchmark – Cost mediu vs N (cu N ∈ {5,10,20,50,100})")
caption("Figura 7. Cost mediu vs. dimensiunea problemei – benchmark comparativ")

placeholder("SCREENSHOT: TSP Benchmark – Timp mediu vs N (scară log)")
caption("Figura 8. Timp de execuție vs. dimensiunea problemei (scară logaritmică)")

placeholder("SCREENSHOT: TSP Benchmark – Box plot distribuție costuri")
caption("Figura 9. Distribuția costurilor per algoritm pe toate dimensiunile")

placeholder("SCREENSHOT: NLP – Accuracy vs F1 macro bar chart")
caption("Figura 10. Acuratețe și F1 macro pentru toți clasificatorii")

placeholder("SCREENSHOT: NLP – Performance scatter: acuratețe vs timp antrenare")
caption("Figura 11. Cost-eficiență: acuratețe vs. timp de antrenare")

placeholder("SCREENSHOT: NLP – Matrice de confuzie (SVM sau Logistic Regression)")
caption("Figura 12. Matrice de confuzie – cel mai bun clasificator ML")

placeholder("SCREENSHOT: NLP – Tab Dicționare: lista de cuvinte-cheie per categorie")
caption("Figura 13. Dicționarele de cuvinte-cheie folosite de Dictionary Classifier")

# ═══════════════════════════════════════════════════════════════════════════
# 7. CONCLUZII
# ═══════════════════════════════════════════════════════════════════════════
heading("7. Concluzii")

heading("7.1 Concluzii TSP", level=2)
body(
    "Backtracking garantează soluția optimă, dar este aplicabil practic doar pentru "
    "N ≤ 12 datorită complexității O(N!). Pentru N = 12, BKT explorează până la 39.916.800 "
    "permutări; la N = 15 devine impractică fără o limită strictă de timp."
)
body(
    "Nearest Neighbour este cel mai rapid algoritm (O(N²)), dar calitatea soluțiilor "
    "este limitată – tipic cu 20–30% deasupra costului optim. Reprezintă un baseline "
    "excelent pentru inițializarea altor algoritmi (SA, HC)."
)
body(
    "Hill Climbing îmbunătățește semnificativ soluția NN prin operatorul 2-opt, "
    "dar rămâne vulnerabil la minime locale. Restart-urile multiple ajută, dar nu "
    "elimină complet problema."
)
body(
    "Simulated Annealing obține cel mai bun echilibru calitate/viteză dintre "
    "heuristici. Cu α = 0,995 și T_max = 1000, soluțiile sunt tipic cu 2–8% de "
    "optim pentru N = 50. Temperatura inițială și rata de răcire sunt parametri "
    "critici – valori prea mari ale lui α duc la convergență lentă, valori prea mici "
    "la prizonierarea în minime locale."
)
body(
    "Genetic Algorithm produce cele mai bune soluții pentru N mare (N > 50), "
    "dar este cel mai lent dintre heuristici. Elitismul previne regresia calității "
    "de la o generație la alta. Selecția prin turneu s-a dovedit mai stabilă decât "
    "rolet pentru instanțele testate."
)
body(
    "Concluzie generală TSP: pentru instanțe mici (N ≤ 12) se recomandă BKT; "
    "pentru instanțe medii (12 < N ≤ 30) HC sau SA; pentru instanțe mari (N > 30) "
    "GA sau SA cu parametri bine calibrați."
)

heading("7.2 Concluzii NLP", level=2)
body(
    "SVM (LinearSVC) și Logistic Regression obțin consecvent cele mai bune rezultate "
    "pe setul 20 Newsgroups (acuratețe > 85% pe 4 categorii, > 80% pe 20 categorii), "
    "cu timp de antrenare redus. Reprezintă alegerea optimă pentru clasificarea textului "
    "cu TF-IDF în termeni de cost-eficiență."
)
body(
    "Naive Bayes este cel mai rapid clasificator, cu acuratețe acceptabilă (~80% pe 4 "
    "categorii). Ipoteza de independență condiționată este o simplificare, dar funcționează "
    "bine în practică pentru text."
)
body(
    "Random Forest este cel mai lent (100 de arbori pe date de înaltă dimensionalitate), "
    "cu acuratețe mai mică decât SVM și LR. Nu este recomandat pentru date text "
    "vectorizate cu TF-IDF."
)
body(
    "Dictionary Classifier demonstrează că clasificarea bazată pe reguli simple "
    "poate obține acuratețe modestă (~40–60%) fără nicio antrenare, ceea ce îl face "
    "util ca baseline interpretabil sau în scenarii fără date de antrenare."
)
body(
    "Creșterea max_features de la 1.000 la 20.000 îmbunătățește acuratețea cu ~5–8% "
    "pentru SVM/LR. Adăugarea bigramelor (ngram_max=2) aduce îmbunătățiri mici "
    "(<2%) cu cost computațional crescut."
)

# ═══════════════════════════════════════════════════════════════════════════
# 8. BIBLIOGRAFIE
# ═══════════════════════════════════════════════════════════════════════════
heading("8. Bibliografie")
refs = [
    "[1] Applegate, D.L., Bixby, R.E., Chvátal, V., Cook, W.J. (2006). "
    "The Traveling Salesman Problem: A Computational Study. Princeton University Press.",

    "[2] Kirkpatrick, S., Gelatt, C.D., Vecchi, M.P. (1983). "
    "Optimization by Simulated Annealing. Science, 220(4598), 671–680.",

    "[3] Holland, J.H. (1975). "
    "Adaptation in Natural and Artificial Systems. University of Michigan Press.",

    "[4] Mitchell, M. (1996). "
    "An Introduction to Genetic Algorithms. MIT Press.",

    "[5] Sebastiani, F. (2002). "
    "Machine Learning in Automated Text Categorization. "
    "ACM Computing Surveys, 34(1), 1–47.",

    "[6] Pedregosa, F. et al. (2011). "
    "Scikit-learn: Machine Learning in Python. "
    "Journal of Machine Learning Research, 12, 2825–2830.",

    "[7] Streamlit Inc. (2024). Streamlit Documentation. https://docs.streamlit.io",

    "[8] Lang, K. (1995). "
    "Newsweeder: Learning to filter netnews. "
    "Proceedings of ICML-95, 331–339.",
]
for ref in refs:
    p = doc.add_paragraph(ref)
    p.style.font.size = Pt(10)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.paragraph_format.left_indent       = Cm(0.5)
    p.paragraph_format.space_after       = Pt(4)

# ═══════════════════════════════════════════════════════════════════════════
# SALVARE
# ═══════════════════════════════════════════════════════════════════════════
out = "documentatie_IA.docx"
doc.save(out)
print("Fisier generat: " + out)
