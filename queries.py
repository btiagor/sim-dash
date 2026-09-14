from conexao_duckdb import get_connection
import pandas as pd


# =========================
# VISÃO GERAL
# =========================

# con = get_connection()

def total_obitos(con) -> int:
    resultado = con.sql("""
        SELECT COUNT(*) AS total
        FROM sim
    """).fetchone()

    return resultado[0]


def obitos_por_ano(con) -> pd.DataFrame:

    return con.sql("""
        SELECT
            YEAR(DTOBITO) AS ano,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY ano
        ORDER BY ano
    """).df()


# =========================
# PERFIL
# =========================

def obitos_por_sexo(con) -> pd.DataFrame:
    """
    Retorna os óbitos agrupados por sexo.
    """

    return con.sql("""
        SELECT
            SEXO,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY SEXO
        ORDER BY obitos DESC
    """).df()


def obitos_por_raca(con) -> pd.DataFrame:
    """
    Retorna os óbitos agrupados por raça/cor.
    """

    return con.sql("""
        SELECT
            RACACOR,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY RACACOR
        ORDER BY obitos DESC
    """).df()


def obitos_por_idade(con) -> pd.DataFrame:
    """
    Retorna a distribuição dos óbitos por idade.
    """

    return con.sql("""
        SELECT
            idade_anos,
            COUNT(*) AS obitos
        FROM sim
        WHERE idade_anos IS NOT NULL
        GROUP BY idade_anos
        ORDER BY idade_anos
    """).df()


# =========================
# CAUSAS
# =========================

def top_causas(
        con,   
        limite: int = 10,
) -> pd.DataFrame:
    """
    Retorna as principais causas básicas de morte.
    """

    return con.sql(f"""
        SELECT
            CAUSABAS,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY CAUSABAS
        ORDER BY obitos DESC
        LIMIT {limite}
    """).df()

# =========================
# TERRITÓRIO
# =========================

def obitos_por_municipio_residencia(con) -> pd.DataFrame:
    """
    Retorna os óbitos por município de residência.
    """

    return con.sql("""
        SELECT
            CODMUNRES,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY CODMUNRES
        ORDER BY obitos DESC
    """).df()


def obitos_por_municipio_ocorrencia(con) -> pd.DataFrame:
    """
    Retorna os óbitos por município de ocorrência.
    """

    return con.sql("""
        SELECT
            CODMUNOCOR,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY CODMUNOCOR
        ORDER BY obitos DESC
    """).df()


def fluxo_residencia_ocorrencia(con) -> pd.DataFrame:
    """
    Retorna o fluxo entre município de residência
    e município de ocorrência.
    """

    return con.sql("""
        SELECT
            CODMUNRES,
            CODMUNOCOR,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY
            CODMUNRES,
            CODMUNOCOR
        ORDER BY obitos DESC
    """).df()