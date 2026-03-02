"""Persistência de datasets de features."""

from pathlib import Path

import pandas as pd


def save_features(df: pd.DataFrame, output_path: Path) -> Path:
    """Salva features em formato CSV.

    Parameters
    ----------
    df : pd.DataFrame
        DataFrame de features.
    output_path : Path
        Caminho de destino do arquivo.

    Returns
    -------
    Path
        Caminho final do arquivo salvo.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    return output_path
