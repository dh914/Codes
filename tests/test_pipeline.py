from codes.data import load_dataset, train_test_split_df
from codes.models import build_model, train_and_evaluate


def test_iris_baseline_pipeline_runs():
    df = load_dataset("iris")
    X_train, X_test, y_train, y_test = train_test_split_df(df, target="label", random_state=0)
    model = build_model("logreg")
    report = train_and_evaluate(model, X_train, X_test, y_train, y_test)
    assert report.accuracy > 0.8
    assert report.macro_f1 > 0.8


def test_random_forest_runs():
    df = load_dataset("iris")
    X_train, X_test, y_train, y_test = train_test_split_df(df, target="label", random_state=0)
    model = build_model("rf", n_estimators=50)
    report = train_and_evaluate(model, X_train, X_test, y_train, y_test)
    assert report.accuracy > 0.8
