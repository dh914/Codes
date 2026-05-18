from __future__ import annotations

from pathlib import Path

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split


def load_dataset(name: str = "iris", path: str | Path | None = None) -> pd.DataFrame:
    """Load a dataset by name or from a CSV path.

    Built-in names: "iris". Otherwise, `path` must point to a CSV file.
    """
    if path is not None:
        return pd.read_csv(path)

    if name == "iris":
        bunch = load_iris(as_frame=True)
        df = bunch.frame.rename(columns={"target": "label"})
        return df

    raise ValueError(f"Unknown dataset: {name!r}")


def train_test_split_df(
    df: pd.DataFrame,
    target: str = "label",
    test_size: float = 0.2,
    random_state: int = 42,
):
    """Split a dataframe into (X_train, X_test, y_train, y_test)."""
    X = df.drop(columns=[target])
    y = df[target]
    return train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
