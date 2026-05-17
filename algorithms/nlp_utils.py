"""NLP utilities: datasets, pipeline building, evaluation."""
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                              accuracy_score, f1_score)
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

def load_data(dataset_name):
    """Load train/test split for the chosen dataset."""
    cfg = DATASETS[dataset_name]
    if cfg["loader"] == "newsgroups":
        train = fetch_20newsgroups(subset="train", categories=cfg["categories"],
                                   remove=("headers", "footers", "quotes"),
                                   random_state=42)
        test  = fetch_20newsgroups(subset="test",  categories=cfg["categories"],
                                   remove=("headers", "footers", "quotes"),
                                   random_state=42)
        return train.data, test.data, train.target, test.target, train.target_names

def build_pipeline(classifier_name, max_features=10000, ngram_max=1,
                   sublinear_tf=True, use_idf=True):
    """Build sklearn TF-IDF + classifier pipeline."""
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
    """Fit pipeline and return evaluation metrics dict."""
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

def compare_classifiers(X_train, X_test, y_train, y_test,
                        max_features=10000, ngram_max=1):
    """Run all 4 classifiers and return list of result dicts."""
    results = []
    for name in CLASSIFIERS:
        pipe = build_pipeline(name, max_features=max_features, ngram_max=ngram_max)
        metrics = train_and_evaluate(pipe, X_train, X_test, y_train, y_test)
        metrics["classifier"] = name
        results.append(metrics)
    return results
