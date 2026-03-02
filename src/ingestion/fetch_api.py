"""Coleta de dados de mercado via API pública."""

import logging
from typing import List

import pandas as pd
import yfinance as yf
from tqdm import tqdm

from exceptions import DataIngestionError

LOGGER = logging.getLogger(__name__)


def fetch_market_data(
    symbols: List[str],
    start_date: str,
    end_date: str,
    interval: str = "1d",
) -> pd.DataFrame:
    """Baixa dados históricos de ativos via Yahoo Finance.

    Parameters
    ----------
    symbols : List[str]
        Lista de ativos no formato Yahoo (ex.: PETR4.SA).
    start_date : str
        Data inicial da coleta.
    end_date : str
        Data final da coleta.
    interval : str, optional
        Frequência temporal dos dados, por padrão "1d".

    Returns
    -------
    pd.DataFrame
        DataFrame consolidado com colunas OHLCV e símbolo.

    Raises
    ------
    DataIngestionError
        Quando nenhum dado válido é retornado.
    """
    all_data: List[pd.DataFrame] = []

    for symbol in tqdm(symbols, desc="Baixando ativos", unit="ativo", colour="green"):
        try:
            data = yf.download(
                tickers=symbol,
                start=start_date,
                end=end_date,
                interval=interval,
                auto_adjust=False,
                progress=False,
            )
        except Exception as exc:
            LOGGER.error("Falha ao baixar %s: %s", symbol, exc)
            continue

        if data.empty: # type: ignore
            LOGGER.warning("Sem dados para o ativo %s no período informado.", symbol)
            continue

        data = data.reset_index()  # type: ignore
        if "Date" not in data.columns:
            data = data.rename(columns={data.columns[0]: "Date"})

        data.columns = [str(column[0]).lower().replace(" ", "_") for column in data.columns]
        data["ticker"] = symbol
        all_data.append(data)

    if not all_data:
        raise DataIngestionError("Nenhum dado de mercado foi coletado.")

    result = pd.concat(all_data, ignore_index=True)
    result = result.rename(
        columns={
            "date": "date",
            "open": "open",
            "high": "high",
            "low": "low",
            "close": "close",
            "adj_close": "adj_close",
            "volume": "volume",
        }
    )
    result["date"] = pd.to_datetime(result["date"])

    LOGGER.info("Coleta finalizada com %s linhas.", len(result))
    return result
