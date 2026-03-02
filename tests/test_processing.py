"""Testes de limpeza e transformação."""

import pandas as pd

from processing.clean import clean_prices
from processing.transform import build_returns_frame


def test_clean_prices_removes_duplicates(sample_prices):
    """Valida remoção de duplicatas por data e ticker."""
    duplicated = sample_prices.copy()
    duplicated = pd.concat([duplicated.iloc[:10], duplicated.iloc[:10]], ignore_index=True)
    result = clean_prices(duplicated)

    assert result.duplicated(subset=["date", "ticker"]).sum() == 0


def test_build_returns_frame_adds_return_columns(sample_prices):
    """Valida criação de colunas de retorno."""
    cleaned = clean_prices(sample_prices)
    transformed = build_returns_frame(cleaned)

    assert "daily_return" in transformed.columns
    assert "log_return" in transformed.columns
