"""Fixtures compartilhadas dos testes."""

from pathlib import Path

import pandas as pd
import pytest


@pytest.fixture
def sample_prices() -> pd.DataFrame:
    """Retorna DataFrame sintético de preços para testes."""
    return pd.DataFrame(
        {
            "date": pd.date_range("2024-01-01", periods=40, freq="D").tolist() * 2,
            "ticker": ["PETR4.SA"] * 40 + ["VALE3.SA"] * 40,
            "open": [10.0 + i * 0.1 for i in range(40)] + [20.0 + i * 0.1 for i in range(40)],
            "high": [10.2 + i * 0.1 for i in range(40)] + [20.2 + i * 0.1 for i in range(40)],
            "low": [9.8 + i * 0.1 for i in range(40)] + [19.8 + i * 0.1 for i in range(40)],
            "close": [10.1 + i * 0.1 for i in range(40)] + [20.1 + i * 0.1 for i in range(40)],
            "adj_close": [10.1 + i * 0.1 for i in range(40)] + [20.1 + i * 0.1 for i in range(40)],
            "volume": [1000 + i for i in range(40)] + [2000 + i for i in range(40)],
        }
    )


@pytest.fixture
def tmp_db_path(tmp_path: Path) -> Path:
    """Retorna caminho temporário para banco SQLite."""
    return tmp_path / "test_quant.db"
