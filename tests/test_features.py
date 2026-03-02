"""Testes de engenharia de features."""

from features.build_features import build_risk_return_features
from processing.clean import clean_prices
from processing.transform import build_returns_frame


def test_build_risk_return_features_generates_expected_columns(sample_prices):
    """Valida colunas de features de risco."""
    cleaned = clean_prices(sample_prices)
    transformed = build_returns_frame(cleaned)

    features = build_risk_return_features(
        transformed,
        rolling_window=5,
        risk_free_rate_annual=0.12,
        confidence_level=0.95,
    )

    assert "volatility_rolling" in features.columns
    assert "var_historical_rolling" in features.columns
    assert "sharpe_ratio" in features.columns
    assert "adf_pvalue" in features.columns
