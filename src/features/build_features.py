"""Criação de features quantitativas de risco e retorno."""

import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import adfuller


def _annualized_sharpe(returns: pd.Series, risk_free_rate_annual: float) -> float:
    """Calcula Sharpe anualizado de uma série de retornos."""
    clean = returns.dropna()
    if clean.empty or clean.std(ddof=0) == 0:
        return np.nan

    daily_rf = (1 + risk_free_rate_annual) ** (1 / 252) - 1
    excess = clean - daily_rf
    return np.sqrt(252) * (excess.mean() / clean.std(ddof=0))


def build_risk_return_features(
    df: pd.DataFrame,
    rolling_window: int,
    risk_free_rate_annual: float,
    confidence_level: float,
) -> pd.DataFrame:
    """Constrói métricas de risco e retorno por ativo.

    Parameters
    ----------
    df : pd.DataFrame
        Base com retornos diários e logarítmicos.
    rolling_window : int
        Janela para volatilidade e VaR móveis.
    risk_free_rate_annual : float
        Taxa livre de risco anual usada no Sharpe.
    confidence_level : float
        Nível de confiança para VaR histórico.

    Returns
    -------
    pd.DataFrame
        DataFrame com features para modelagem e análise.

    Notes
    -----
    Inclui métricas de estacionariedade simples (p-valor ADF)
    para cada ativo como recurso analítico adicional.
    """
    feature_df = df.copy().sort_values(["ticker", "date"]).reset_index(drop=True)

    grouped = feature_df.groupby("ticker", observed=True)
    feature_df["volatility_rolling"] = (
        grouped["daily_return"].rolling(rolling_window).std().reset_index(level=0, drop=True)
    ) * np.sqrt(252)

    alpha = 1 - confidence_level
    feature_df["var_historical_rolling"] = (
        grouped["daily_return"]
        .rolling(rolling_window)
        .quantile(alpha)
        .reset_index(level=0, drop=True)
    )

    sharpe_by_ticker = (
        feature_df.groupby("ticker", observed=True)["daily_return"]
        .apply(lambda returns: _annualized_sharpe(returns, risk_free_rate_annual))
        .rename("sharpe_ratio")
    )
    feature_df = feature_df.merge(sharpe_by_ticker, on="ticker", how="left")

    adf_values = {}
    for ticker, ticker_df in feature_df.groupby("ticker", observed=True):
        series = ticker_df["daily_return"].dropna()
        adf_values[ticker] = adfuller(series)[1] if len(series) > 20 else np.nan

    feature_df["adf_pvalue"] = feature_df["ticker"].map(adf_values)

    return feature_df
