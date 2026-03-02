"""Persistência e consultas SQL para dados de mercado."""

import logging
import sqlite3
from pathlib import Path
from typing import Optional

import pandas as pd

LOGGER = logging.getLogger(__name__)


def _resolve_sqlite_path(database_url: str, root_dir: Path) -> Path:
    """Resolve caminho local SQLite a partir de uma URL simples.

    Parameters
    ----------
    database_url : str
        URL de banco no formato `sqlite:///caminho/arquivo.db`.
    root_dir : Path
        Diretório raiz do projeto.

    Returns
    -------
    Path
        Caminho absoluto do arquivo SQLite.
    """
    if database_url.startswith("sqlite:///"):
        relative_path = database_url.replace("sqlite:///", "", 1)
        return (root_dir / relative_path).resolve()
    return (root_dir / "data" / "b3_quant.db").resolve()


def initialize_database(database_url: str, root_dir: Path) -> Path:
    """Cria estrutura de tabelas no banco relacional.

    Parameters
    ----------
    database_url : str
        URL do banco.
    root_dir : Path
        Diretório raiz do projeto.

    Returns
    -------
    Path
        Caminho efetivo do banco SQLite.
    """
    db_path = _resolve_sqlite_path(database_url, root_dir)
    db_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS prices (
                date TEXT NOT NULL,
                ticker TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                adj_close REAL,
                volume REAL,
                PRIMARY KEY (date, ticker)
            )
            """
        )
        conn.execute("CREATE INDEX IF NOT EXISTS idx_prices_ticker_date ON prices (ticker, date)")

    LOGGER.info("Banco inicializado em %s", db_path)
    return db_path


def insert_prices(df: pd.DataFrame, db_path: Path) -> int:
    """Insere ou atualiza preços históricos na tabela `prices`.

    Parameters
    ----------
    df : pd.DataFrame
        Dados com colunas padrão de OHLCV.
    db_path : Path
        Caminho do arquivo SQLite.

    Returns
    -------
    int
        Quantidade de linhas processadas.

    Raises
    ------
    ValueError
        Quando o DataFrame de entrada estiver vazio.
    """
    if df.empty:
        raise ValueError("DataFrame de preços está vazio.")

    payload = df.copy()
    payload["date"] = pd.to_datetime(payload["date"]).dt.strftime("%Y-%m-%d")

    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            """
            INSERT OR REPLACE INTO prices(date, ticker, open, high, low, close, adj_close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            payload[
                ["date", "ticker", "open", "high", "low", "close", "adj_close", "volume"]
            ].itertuples(index=False, name=None),
        )
        conn.commit()

    LOGGER.info("Persistidas %s linhas em prices.", len(payload))
    return len(payload)


def load_prices(db_path: Path, ticker: Optional[str] = None) -> pd.DataFrame:
    """Carrega dados de preços do banco para DataFrame.

    Parameters
    ----------
    db_path : Path
        Caminho do arquivo SQLite.
    ticker : Optional[str], optional
        Filtro opcional por ativo.

    Returns
    -------
    pd.DataFrame
        Dados de preços ordenados por ativo e data.
    """
    query = "SELECT * FROM prices"
    params = ()
    if ticker:
        query += " WHERE ticker = ?"
        params = (ticker,)
    query += " ORDER BY ticker, date"

    with sqlite3.connect(db_path) as conn:
        df = pd.read_sql_query(query, conn, params=params, parse_dates=["date"])

    return df


def load_returns_with_sql(db_path: Path) -> pd.DataFrame:
    """Calcula retornos via SQL avançado com CTE e window function.

    Parameters
    ----------
    db_path : Path
        Caminho do banco SQLite.

    Returns
    -------
    pd.DataFrame
        DataFrame com preços e retorno diário logarítmico.

    Notes
    -----
    A consulta utiliza `LAG` para acessar o fechamento anterior
    e CTE para estruturar etapas de cálculo.
    """
    query = """
    WITH ordered_prices AS (
        SELECT
            date,
            ticker,
            close,
            LAG(close) OVER (PARTITION BY ticker ORDER BY date) AS previous_close
        FROM prices
    ),
    returns_cte AS (
        SELECT
            date,
            ticker,
            close,
            previous_close,
            CASE
                WHEN previous_close IS NULL OR previous_close = 0 THEN NULL
                ELSE (close / previous_close) - 1
            END AS daily_return
        FROM ordered_prices
    )
    SELECT *
    FROM returns_cte
    ORDER BY ticker, date
    """

    with sqlite3.connect(db_path) as conn:
        result = pd.read_sql_query(query, conn, parse_dates=["date"])

    return result
