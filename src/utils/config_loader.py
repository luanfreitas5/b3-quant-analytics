"""Leitura e validação de configurações da aplicação."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from exceptions import ConfigurationError
from utils.helpers import parse_symbols


@dataclass(frozen=True)
class Settings:
    """Estrutura de configurações globais do projeto.

    Parameters
    ----------
    environment : str
        Ambiente de execução (ex.: dev, prod).
    log_level : str
        Nível global de log.
    symbols : list[str]
        Lista de ativos monitorados.
    start_date : str
        Data inicial da coleta.
    end_date : str
        Data final da coleta.
    interval : str
        Intervalo dos candles (ex.: 1d).
    database_url : str
        URL de conexão do banco de dados.
    risk_free_rate_annual : float
        Taxa anual livre de risco para Sharpe.
    rolling_window : int
        Janela para métricas móveis.
    confidence_level : float
        Nível de confiança para VaR.
    root_dir : Path
        Diretório raiz do projeto.
    """

    environment: str
    log_level: str
    symbols: list[str]
    start_date: str
    end_date: str
    interval: str
    database_url: str
    risk_free_rate_annual: float
    rolling_window: int
    confidence_level: float
    root_dir: Path


def load_settings(root_dir: Path) -> Settings:
    """Carrega configurações a partir de variáveis de ambiente.

    Parameters
    ----------
    root_dir : Path
        Diretório raiz do projeto para localizar `.env`.

    Returns
    -------
    Settings
        Objeto imutável com as configurações validadas.

    Raises
    ------
    ConfigurationError
        Quando uma configuração obrigatória estiver ausente ou inválida.
    """
    env_path = root_dir / ".env"
    load_dotenv(env_path)

    symbols_raw = os.getenv("symbols", "")
    symbols = parse_symbols(symbols_raw)
    if not symbols:
        raise ConfigurationError("A variável 'symbols' deve conter ao menos um ativo.")

    database_url = os.getenv("database_url", "sqlite:///data/b3_quant.db")
    if not database_url:
        raise ConfigurationError("A variável 'database_url' não pode estar vazia.")

    try:
        risk_free_rate_annual = float(os.getenv("risk_free_rate_annual", "0.13"))
        rolling_window = int(os.getenv("rolling_window", "21"))
        confidence_level = float(os.getenv("confidence_level", "0.95"))
    except ValueError as exc:
        raise ConfigurationError("Parâmetros numéricos inválidos no .env") from exc

    return Settings(
        environment=os.getenv("environment", "dev"),
        log_level=os.getenv("log_level", "INFO").upper(),
        symbols=symbols,
        start_date=os.getenv("start_date", "2020-01-01"),
        end_date=os.getenv("end_date", "2025-12-31"),
        interval=os.getenv("interval", "1d"),
        database_url=database_url,
        risk_free_rate_annual=risk_free_rate_annual,
        rolling_window=rolling_window,
        confidence_level=confidence_level,
        root_dir=root_dir,
    )
