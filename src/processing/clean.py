"""Limpeza e padronização de dados brutos."""

import logging

import pandas as pd

LOGGER = logging.getLogger(__name__)


def clean_prices(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpeza e otimização de memória em base de preços.

    Parameters
    ----------
    df : pd.DataFrame
        Dados de preços de entrada.

    Returns
    -------
    pd.DataFrame
        Base limpa, ordenada e com tipos ajustados.

    Notes
    -----
    - Remove duplicatas por (`ticker`, `date`).
    - Ordena temporalmente por ativo.
    - Converte `ticker` para tipo categórico para reduzir memória.
    """
    clean_df = df.copy()
    clean_df["date"] = pd.to_datetime(clean_df["date"], errors="coerce")
    clean_df = clean_df.dropna(subset=["date", "ticker", "close"])

    clean_df = clean_df.drop_duplicates(subset=["ticker", "date"], keep="last")
    clean_df = clean_df.sort_values(["ticker", "date"]).reset_index(drop=True)

    if "ticker" in clean_df.columns:
        clean_df["ticker"] = clean_df["ticker"].astype("category")

    for column in ["open", "high", "low", "close", "adj_close", "volume"]:
        if column in clean_df.columns:
            clean_df[column] = pd.to_numeric(clean_df[column], errors="coerce", downcast="float")

    clean_df = clean_df.dropna(subset=["close"])
    LOGGER.info("Limpeza concluída: %s linhas após tratamento.", len(clean_df))
    return clean_df
