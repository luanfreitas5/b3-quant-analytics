"""Transformações para análise temporal de retornos."""

import numpy as np
import pandas as pd


def build_returns_frame(df: pd.DataFrame) -> pd.DataFrame:
    """Constrói colunas de retorno simples e logarítmico por ativo.

    Parameters
    ----------
    df : pd.DataFrame
        Base de preços limpa contendo `ticker`, `date` e `close`.

    Returns
    -------
    pd.DataFrame
        Base com colunas `daily_return` e `log_return`.
    """
    transformed = df.copy().sort_values(["ticker", "date"]).reset_index(drop=True)

    transformed["daily_return"] = transformed.groupby("ticker", observed=True)["close"].pct_change()
    transformed["log_return"] = transformed.groupby("ticker", observed=True)["close"].transform(
        lambda series: np.log(series / series.shift(1))
    )

    return transformed
