from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


@dataclass
class EvalReport:
    accuracy: float
    macro_f1: float
    detail: str


def build_model(kind: str = "logreg", **params: Any) -> Pipeline:
    """Construct a scikit-learn pipeline for the requested model kind."""
    if kind == "logreg":
        clf = LogisticRegression(max_iter=params.pop("max_iter", 1000), **params)
        return Pipeline([("scaler", StandardScaler()), ("clf", clf)])
    if kind == "rf":
        clf = RandomForestClassifier(
            n_estimators=params.pop("n_estimators", 200),
            random_state=params.pop("random_state", 42),
            **params,
        )
        return Pipeline([("clf", clf)])
    if kind == "svm":
        clf = SVC(
            C=params.pop("C", 1.0),
            kernel=params.pop("kernel", "rbf"),
            random_state=params.pop("random_state", 42),
            **params,
        )
        return Pipeline([("scaler", StandardScaler()), ("clf", clf)])
    raise ValueError(f"Unknown model kind: {kind!r}")


def train_and_evaluate(
    model: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
) -> EvalReport:
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    return EvalReport(
        accuracy=accuracy_score(y_test, preds),
        macro_f1=f1_score(y_test, preds, average="macro"),
        detail=classification_report(y_test, preds),
    )
