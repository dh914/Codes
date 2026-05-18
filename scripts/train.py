"""CLI entry point: train and evaluate a model from a YAML config."""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from codes.data import load_dataset, train_test_split_df
from codes.models import build_model, train_and_evaluate


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a model from a YAML config.")
    parser.add_argument("--config", type=Path, required=True, help="Path to YAML config")
    args = parser.parse_args()

    cfg = yaml.safe_load(args.config.read_text())

    ds_cfg = cfg["dataset"]
    df = load_dataset(name=ds_cfg.get("name", "iris"), path=ds_cfg.get("path"))
    X_train, X_test, y_train, y_test = train_test_split_df(
        df,
        target=ds_cfg.get("target", "label"),
        test_size=ds_cfg.get("test_size", 0.2),
        random_state=ds_cfg.get("random_state", 42),
    )

    m_cfg = cfg["model"]
    model = build_model(kind=m_cfg.get("kind", "logreg"), **(m_cfg.get("params") or {}))
    report = train_and_evaluate(model, X_train, X_test, y_train, y_test)

    print(f"accuracy = {report.accuracy:.4f}")
    print(f"macro_f1 = {report.macro_f1:.4f}")
    print(report.detail)


if __name__ == "__main__":
    main()
