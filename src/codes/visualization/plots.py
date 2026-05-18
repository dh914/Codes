from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay


def plot_confusion(y_true, y_pred, labels: Sequence | None = None, ax=None):
    disp = ConfusionMatrixDisplay.from_predictions(y_true, y_pred, display_labels=labels, ax=ax)
    return disp.figure_


def plot_feature_importance(names: Sequence[str], importances: Sequence[float], top_n: int = 20):
    order = np.argsort(importances)[::-1][:top_n]
    fig, ax = plt.subplots(figsize=(8, max(3, 0.3 * len(order))))
    ax.barh([names[i] for i in order][::-1], [importances[i] for i in order][::-1])
    ax.set_xlabel("Importance")
    ax.set_title(f"Top {len(order)} feature importances")
    fig.tight_layout()
    return fig
