from pathlib import Path

import duckdb


DB_PATH = Path("data/database/sim.duckdb")


def get_connection(read_only: bool = False):
    """
    Cria uma conexão com o banco DuckDB.
    """

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    return duckdb.connect(
        str(DB_PATH),
        read_only=read_only
    )