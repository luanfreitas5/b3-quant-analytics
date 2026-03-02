"""Testes de camada de ingestão e banco."""

import sqlite3

from ingestion.fetch_db import insert_prices, load_returns_with_sql
from processing.clean import clean_prices


def test_insert_prices_and_sql_returns(sample_prices, tmp_db_path):
    """Valida inserção em SQLite e cálculo de retorno via SQL."""
    cleaned = clean_prices(sample_prices)

    with sqlite3.connect(tmp_db_path) as conn:
        conn.execute(
            """
            CREATE TABLE prices (
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

    inserted = insert_prices(cleaned, tmp_db_path)
    assert inserted == len(cleaned)

    returns = load_returns_with_sql(tmp_db_path)
    assert "daily_return" in returns.columns
    assert len(returns) > 0
