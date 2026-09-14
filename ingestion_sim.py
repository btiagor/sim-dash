from pathlib import Path

import pandas as pd


def carregar_sim(caminho: str | Path) -> pd.DataFrame:
    """
    Carrega a base do SIM a partir de um arquivo XLSX.
    """

    caminho = Path(caminho)

    if not caminho.exists():
        raise FileNotFoundError(
            f"Arquivo não encontrado: {caminho}"
        )

    return pd.read_excel(caminho)