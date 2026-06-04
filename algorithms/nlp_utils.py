"""NLP utilities: datasets, pipeline building, evaluation, keyword dictionaries."""
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score, classification_report
import numpy as np
import time

DATASETS = {
    "20 Newsgroups (4 categories)": {
        "loader": "newsgroups",
        "categories": ["sci.space", "rec.sport.hockey",
                       "talk.politics.guns", "comp.graphics"],
    },
    "20 Newsgroups (Science)": {
        "loader": "newsgroups",
        "categories": ["sci.space", "sci.med", "sci.electronics", "sci.crypt"],
    },
    "20 Newsgroups (Full - 20 classes)": {
        "loader": "newsgroups",
        "categories": None,
    },
}

CLASSIFIERS = {
    "Naive Bayes": lambda: MultinomialNB(),
    "SVM (LinearSVC)": lambda: LinearSVC(max_iter=2000, C=1.0),
    "Logistic Regression": lambda: LogisticRegression(max_iter=1000, C=1.0),
    "Random Forest": lambda: RandomForestClassifier(n_estimators=100, n_jobs=-1),
}

# One keyword dictionary per newsgroup category used for rule-based classification
KEYWORD_DICTS = {
    "sci.space": [
        "nasa", "orbit", "shuttle", "satellite", "moon", "launch", "rocket",
        "astronaut", "space", "earth", "mission", "solar", "planet", "telescope",
        "galaxy", "cosmos", "hubble", "spacecraft", "asteroid", "comet", "mars",
        "venus", "jupiter", "probe", "apollo", "iss",
    ],
    "rec.sport.hockey": [
        "hockey", "nhl", "goal", "puck", "ice", "player", "team", "season",
        "game", "cup", "score", "penalty", "coach", "arena", "rink", "skate",
        "goalie", "assist", "playoffs", "referee", "period", "stick",
    ],
    "talk.politics.guns": [
        "gun", "weapon", "firearm", "amendment", "rifle", "bullet", "shoot",
        "crime", "law", "ban", "control", "nra", "pistol", "handgun", "caliber",
        "carry", "permit", "militia", "constitutional", "trigger", "armed",
    ],
    "comp.graphics": [
        "graphics", "image", "pixel", "render", "display", "screen", "resolution",
        "color", "software", "computer", "algorithm", "format", "jpeg", "png",
        "gif", "bitmap", "texture", "polygon", "opengl", "3d", "animation",
        "shader", "ray", "tracing",
    ],
    "sci.med": [
        "medical", "patient", "disease", "drug", "treatment", "doctor", "hospital",
        "health", "medicine", "symptom", "diagnosis", "therapy", "surgery", "cancer",
        "blood", "virus", "bacteria", "clinical", "trial", "dose", "prescription",
    ],
    "sci.electronics": [
        "circuit", "voltage", "current", "resistor", "transistor", "electronic",
        "component", "signal", "power", "battery", "capacitor", "diode", "amplifier",
        "frequency", "analog", "digital", "microcontroller", "pcb", "soldering",
    ],
    "sci.crypt": [
        "encryption", "decrypt", "cipher", "key", "algorithm", "security", "hash",
        "rsa", "protocol", "cryptography", "password", "pgp", "des", "aes",
        "prime", "certificate", "ssl", "tls", "public", "private",
    ],
    "talk.politics.misc": [
        "government", "president", "congress", "senate", "democrat", "republican",
        "election", "vote", "policy", "political", "party", "tax", "bill",
        "legislation", "state", "federal", "constitution",
    ],
    "talk.politics.mideast": [
        "israel", "arab", "palestine", "jews", "muslim", "war", "peace", "territory",
        "settlement", "conflict", "region", "middle", "east", "military", "iraqi",
        "lebanese", "iranian",
    ],
    "soc.religion.christian": [
        "christian", "god", "jesus", "church", "bible", "faith", "prayer",
        "salvation", "sin", "holy", "spirit", "scripture", "worship", "heaven",
        "lord", "christ", "resurrection",
    ],
    "talk.religion.misc": [
        "religion", "belief", "worship", "spiritual", "moral", "ethics", "faith",
        "divine", "prayer", "soul", "sacred", "theology", "doctrine",
    ],
    "alt.atheism": [
        "atheist", "atheism", "religion", "god", "belief", "evidence", "rational",
        "secular", "agnostic", "proof", "supernatural", "evolution", "skeptic",
    ],
    "rec.autos": [
        "car", "engine", "vehicle", "drive", "motor", "auto", "speed", "road",
        "transmission", "brake", "tire", "fuel", "oil", "repair", "dealer",
        "mph", "sedan", "horsepower",
    ],
    "rec.motorcycles": [
        "motorcycle", "bike", "ride", "rider", "helmet", "road", "gear",
        "engine", "speed", "accident", "license", "kawasaki", "honda", "yamaha",
        "harley", "clutch",
    ],
    "rec.sport.baseball": [
        "baseball", "pitcher", "batter", "inning", "run", "hit", "home",
        "stadium", "team", "league", "season", "game", "coach", "player",
        "mlb", "batting", "outfield",
    ],
    "comp.sys.mac.hardware": [
        "mac", "apple", "macintosh", "hardware", "disk", "memory", "cpu",
        "processor", "screen", "keyboard", "monitor", "powerbook", "imac",
    ],
    "comp.sys.ibm.pc.hardware": [
        "ibm", "pc", "hardware", "disk", "memory", "cpu", "processor",
        "drive", "card", "motherboard", "bios", "dos", "windows", "486", "vga",
    ],
    "comp.os.ms-windows.misc": [
        "windows", "microsoft", "dos", "registry", "driver", "install",
        "software", "error", "crash", "update", "patch", "win32", "reboot",
    ],
    "comp.windows.x": [
        "xwindows", "xterm", "motif", "display", "widget", "toolkit",
        "server", "client", "unix", "linux", "application", "xlib", "xfree",
    ],
    "misc.forsale": [
        "sale", "sell", "buy", "price", "offer", "shipping", "condition",
        "excellent", "asking", "trade", "cash", "payment", "obo", "mint",
    ],
}


class DictionaryClassifier:
    """Rule-based classifier that scores raw texts against per-category keyword dictionaries."""

    def fit(self, X, y, target_names=None):
        self.classes_ = np.unique(y)
        self.target_names_ = (list(target_names) if target_names is not None
                              else [str(c) for c in self.classes_])
        self._build_keyword_map()
        return self

    def _build_keyword_map(self):
        self.keyword_map_ = {}
        for cls_idx, name in zip(self.classes_, self.target_names_):
            matched_words = []
            name_lower = name.lower()
            for dict_key, words in KEYWORD_DICTS.items():
                # Match if any dot-separated part of the dict key appears in the category name
                if any(part in name_lower for part in dict_key.lower().split(".")):
                    matched_words.extend(words)
            self.keyword_map_[int(cls_idx)] = list(set(matched_words))

    def predict(self, X):
        preds = []
        for text in X:
            text_lower = text.lower()
            scores = {cls: sum(1 for w in words if w in text_lower)
                      for cls, words in self.keyword_map_.items()}
            preds.append(max(scores, key=scores.get))
        return np.array(preds)

    def predict_proba(self, X):
        n_classes = len(self.classes_)
        proba = np.zeros((len(X), n_classes))
        for i, text in enumerate(X):
            text_lower = text.lower()
            scores = np.array([
                float(sum(1 for w in self.keyword_map_.get(int(cls), []) if w in text_lower))
                for cls in self.classes_
            ])
            total = scores.sum()
            proba[i] = scores / total if total > 0 else np.ones(n_classes) / n_classes
        return proba


def load_data(dataset_name):
    cfg = DATASETS[dataset_name]
    if cfg["loader"] == "newsgroups":
        train = fetch_20newsgroups(subset="train", categories=cfg["categories"],
                                   remove=("headers", "footers", "quotes"),
                                   random_state=42)
        test = fetch_20newsgroups(subset="test", categories=cfg["categories"],
                                  remove=("headers", "footers", "quotes"),
                                  random_state=42)
        return train.data, test.data, train.target, test.target, train.target_names


def build_pipeline(classifier_name, max_features=10000, ngram_max=1,
                   sublinear_tf=True, use_idf=True):
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, ngram_max),
        sublinear_tf=sublinear_tf,
        use_idf=use_idf,
        stop_words="english",
    )
    clf = CLASSIFIERS[classifier_name]()
    return Pipeline([("tfidf", vectorizer), ("clf", clf)])


def train_and_evaluate(pipeline, X_train, X_test, y_train, y_test):
    t0 = time.perf_counter()
    pipeline.fit(X_train, y_train)
    train_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    y_pred = pipeline.predict(X_test)
    predict_time = time.perf_counter() - t1

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_macro": f1_score(y_test, y_pred, average="macro"),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "report": classification_report(y_test, y_pred, output_dict=True),
        "train_time": train_time,
        "predict_time": predict_time,
        "y_pred": y_pred,
    }


def dict_train_and_evaluate(X_train, X_test, y_train, y_test, target_names):
    """Train and evaluate the rule-based DictionaryClassifier."""
    clf = DictionaryClassifier()
    t0 = time.perf_counter()
    clf.fit(X_train, y_train, target_names=target_names)
    train_time = time.perf_counter() - t0

    t1 = time.perf_counter()
    y_pred = clf.predict(X_test)
    predict_time = time.perf_counter() - t1

    return {
        "accuracy": accuracy_score(y_test, y_pred),
        "f1_macro": f1_score(y_test, y_pred, average="macro", zero_division=0),
        "confusion_matrix": confusion_matrix(y_test, y_pred),
        "report": classification_report(y_test, y_pred, output_dict=True, zero_division=0),
        "train_time": train_time,
        "predict_time": predict_time,
        "y_pred": y_pred,
        "clf": clf,
    }


def compare_classifiers(X_train, X_test, y_train, y_test,
                        max_features=10000, ngram_max=1):
    results = []
    for name in CLASSIFIERS:
        pipe = build_pipeline(name, max_features=max_features, ngram_max=ngram_max)
        metrics = train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
        metrics["classifier"] = name
        results.append(metrics)
    return results
