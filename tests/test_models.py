"""Testes de modelos e métricas."""

import numpy as np

from features.build_features import build_risk_return_features
from models.evaluate import evaluate_predictions
from models.train import train_return_model
from processing.clean import clean_prices
from processing.transform import build_returns_frame


def test_evaluate_predictions_returns_metrics_dict():
    """Valida estrutura de métricas de avaliação."""
    y_true = np.array([0.01, -0.01, 0.02])
    y_pred = np.array([0.008, -0.005, 0.01])

    metrics = evaluate_predictions(y_true, y_pred)

    assert set(metrics.keys()) == {"rmse", "mae", "r2", "directional_accuracy"}


def test_train_return_model_produces_artifacts(sample_prices):
    """Valida treinamento e retorno de artefatos."""
    cleaned = clean_prices(sample_prices)
    transformed = build_returns_frame(cleaned)
    features = build_risk_return_features(
        transformed,
        rolling_window=5,
        risk_free_rate_annual=0.10,
        confidence_level=0.95,
    )

    artifacts = train_return_model(features)

    assert artifacts.model is not None
    assert len(artifacts.feature_columns) > 0
    assert len(artifacts.x_test) > 0
