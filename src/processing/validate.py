"""Validações de qualidade de dados."""

from typing import Iterable

import pandas as pd

from exceptions import DataValidationError

REQUIRED_COLUMNS = ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]


def validate_prices_schema(
    df: pd.DataFrame, required_columns: Iterable[str] = REQUIRED_COLUMNS
) -> None:
    """Valida schema mínimo para dados de preços.

    Parameters
    ----------
    df : pd.DataFrame
        Base de preços a ser validada.
    required_columns : Iterable[str], optional
        Colunas obrigatórias esperadas.

    Raises
    ------
    DataValidationError
        Quando faltam colunas obrigatórias ou o DataFrame está vazio.
    """
    if df.empty:
        raise DataValidationError("DataFrame de preços está vazio.")

    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise DataValidationError(f"Colunas obrigatórias ausentes: {missing}")
