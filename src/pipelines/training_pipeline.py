"""Pipeline principal de treino e análise quantitativa."""

import json
import logging
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from features import build_risk_return_features, save_features
from ingestion import (
    fetch_market_data,
    initialize_database,
    insert_prices,
    load_returns_with_sql,
)
from models import (
    evaluate_predictions,
    predict_next_return,
    save_model,
    train_return_model,
)
from processing import build_returns_frame, clean_prices, validate_prices_schema
from utils.config_loader import Settings

LOGGER = logging.getLogger(__name__)


def _generate_outputs(feature_df: pd.DataFrame, metrics: dict, root_dir: Path) -> None:
    """Gera artefatos analíticos em `reports/`."""
    figures_dir = root_dir / "reports" / "figures"
    metrics_dir = root_dir / "reports" / "metrics"
    figures_dir.mkdir(parents=True, exist_ok=True)
    metrics_dir.mkdir(parents=True, exist_ok=True)

    corr = feature_df.pivot_table(index="date", columns="ticker", values="daily_return").corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, cmap="coolwarm", center=0)
    plt.title("Correlação de Retornos Diários")
    plt.tight_layout()
    plt.savefig(figures_dir / "correlation_heatmap.png", dpi=120)
    plt.close()

    metrics_path = metrics_dir / "model_metrics.json"
    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def run_training_pipeline(settings: Settings) -> dict:
    """Executa pipeline de ingestão, engenharia de features e modelagem.

    Parameters
    ----------
    settings : Settings
        Configurações centralizadas do projeto.

    Returns
    -------
    dict
        Métricas de desempenho do modelo.
    """
    raw_df = fetch_market_data(
        symbols=settings.symbols,
        start_date=settings.start_date,
        end_date=settings.end_date,
        interval=settings.interval,
    )

    validate_prices_schema(raw_df)
    cleaned = clean_prices(raw_df)
    transformed = build_returns_frame(cleaned)

    db_path = initialize_database(settings.database_url, settings.root_dir)
    insert_prices(cleaned, db_path)
    sql_returns = load_returns_with_sql(db_path)

    feature_input = transformed.merge(
        sql_returns[["date", "ticker", "daily_return"]],
        on=["date", "ticker"],
        how="left",
        suffixes=("", "_sql"),
    )
    feature_input["daily_return"] = feature_input["daily_return_sql"].combine_first(
        feature_input["daily_return"]
    )
    feature_input = feature_input.drop(columns=["daily_return_sql"])

    feature_df = build_risk_return_features(
        df=feature_input,
        rolling_window=settings.rolling_window,
        risk_free_rate_annual=settings.risk_free_rate_annual,
        confidence_level=settings.confidence_level,
    )

    save_features(feature_df, settings.root_dir / "data" / "processed" / "features.csv")

    artifacts = train_return_model(feature_df)
    predictions = predict_next_return(artifacts.model, artifacts.x_test, artifacts.feature_columns)
    metrics = evaluate_predictions(artifacts.y_test.to_numpy(), predictions)

    save_model(
        artifacts.model,
        artifacts.feature_columns,
        metrics,
        settings.root_dir / "models",
    )
    _generate_outputs(feature_df, metrics, settings.root_dir)

    LOGGER.info("Pipeline finalizado com métricas: %s", metrics)
    return metrics
