"""Funções auxiliares reutilizáveis."""

from pathlib import Path
from typing import Iterator, List, Sequence, TypeVar

T = TypeVar("T")


def ensure_directory(path: Path) -> Path:
    """Garante que um diretório exista.

    Parameters
    ----------
    path : Path
        Caminho do diretório a ser garantido.

    Returns
    -------
    Path
        Caminho do diretório criado ou já existente.
    """
    path.mkdir(parents=True, exist_ok=True)
    return path


def chunked(items: Sequence[T], size: int) -> Iterator[List[T]]:
    """Divide uma sequência em blocos de tamanho fixo.

    Parameters
    ----------
    items : Sequence[T]
        Itens de entrada.
    size : int
        Tamanho do bloco.

    Yields
    ------
    Iterator[List[T]]
        Blocos contendo subconjuntos da sequência.

    Raises
    ------
    ValueError
        Quando `size` for menor ou igual a zero.
    """
    if size <= 0:
        raise ValueError("O tamanho do bloco deve ser maior que zero.")

    for index in range(0, len(items), size):
        yield list(items[index : index + size])


def parse_symbols(symbols: str) -> List[str]:
    """Converte string de símbolos separados por vírgula em lista limpa.

    Parameters
    ----------
    symbols : str
        Símbolos separados por vírgula.

    Returns
    -------
    List[str]
        Lista de símbolos normalizados.
    """
    return [symbol.strip().upper() for symbol in symbols.split(",") if symbol.strip()]
