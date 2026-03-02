"""Configuração de logging do projeto."""

import logging
from datetime import datetime
from pathlib import Path

from utils.helpers import ensure_directory


def setup_logging(root_dir: Path, level: str = "INFO") -> logging.Logger:
    """Configura logging em arquivo e console.

    Parameters
    ----------
    root_dir : Path
        Diretório raiz do projeto.
    level : str, optional
        Nível de log desejado, por padrão "INFO".

    Returns
    -------
    logging.Logger
        Logger raiz configurado.

    Notes
    -----
    O arquivo de log é salvo em `logs/` com formato
    `YYYY-MM-DD_HH-MM-SS_NIVEL.log`.
    """
    normalized_level = level.upper()
    numeric_level = getattr(logging, normalized_level, logging.INFO)

    logs_dir = ensure_directory(root_dir / "logs")
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = logs_dir / f"{timestamp}_{normalized_level}.log"

    logger = logging.getLogger()
    logger.handlers.clear()
    logger.setLevel(numeric_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(numeric_level)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(numeric_level)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.info("Logging inicializado em %s", log_file)

    return logger
