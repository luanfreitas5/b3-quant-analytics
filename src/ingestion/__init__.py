"""Módulos de ingestão de dados."""

from ingestion.fetch_api import fetch_market_data
from ingestion.fetch_db import (
    initialize_database,
    insert_prices,
    load_prices,
    load_returns_with_sql,
)

__all__ = [
    "fetch_market_data",
    "initialize_database",
    "insert_prices",
    "load_prices",
    "load_returns_with_sql",
]
