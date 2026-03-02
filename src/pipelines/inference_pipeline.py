"""Pipeline de inferência para uso em lote."""

import json
import logging
from pathlib import Path

import pandas as pd

from models import load_model, predict_next_return
from utils import Settings

LOGGER = logging.getLogger(__name__)


def run_inference_pipeline(settings: Settings, model_path: Path, input_path: Path) -> Path:
    """Executa inferência em lote com modelo treinado.

    Parameters
    ----------
    settings : Settings
        Configurações da aplicação.
    model_path : Path
        Caminho do modelo serializado.
    input_path : Path
        Arquivo CSV com as features de entrada.

    Returns
    -------
    Path
        Caminho do arquivo de predições gerado.
    """
    model = load_model(model_path)
    metadata_path = model_path.parent / "model_metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    feature_columns = metadata["feature_columns"]

    data = pd.read_csv(input_path)
    predictions = predict_next_return(model, data, feature_columns)

    output = data.copy()
    output["predicted_return_t1"] = predictions

    output_path = settings.root_dir / "reports" / "metrics" / "batch_predictions.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output.to_csv(output_path, index=False)

    LOGGER.info("Inferência concluída. Arquivo salvo em %s", output_path)
    return output_path
