"""Ponto de entrada CLI para o projeto B3 Quant Analytics."""

import argparse
import logging
from pathlib import Path

from pipelines import run_inference_pipeline, run_training_pipeline
from utils import load_settings, setup_logging

LOGGER = logging.getLogger(__name__)


def build_parser() -> argparse.ArgumentParser:
    """Cria parser de argumentos de linha de comando.

    Returns
    -------
    argparse.ArgumentParser
        Parser configurado com subcomandos do projeto.
    """
    parser = argparse.ArgumentParser(description="B3 Quant Analytics CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("run", help="Executa pipeline completo de treinamento")

    infer_parser = subparsers.add_parser("infer", help="Executa inferência em lote")
    infer_parser.add_argument("--model-path", required=True, help="Caminho do modelo .joblib")
    infer_parser.add_argument("--input-path", required=True, help="Caminho do CSV de entrada")

    return parser


def main() -> None:
    """Executa o fluxo principal da aplicação baseado no subcomando informado."""
    project_root = Path(__file__).resolve().parents[1]
    settings = load_settings(project_root)
    setup_logging(project_root, settings.log_level)

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "run":
        metrics = run_training_pipeline(settings)
        LOGGER.info("Métricas finais: %s", metrics)
    elif args.command == "infer":
        run_inference_pipeline(
            settings=settings,
            model_path=Path(args.model_path),
            input_path=Path(args.input_path),
        )


if __name__ == "__main__":
    main()
