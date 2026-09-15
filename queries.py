from conexao_duckdb import get_connection
import pandas as pd


# =========================
# VISÃO GERAL
# =========================


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
            DS_SEXO AS SEXO,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY DS_SEXO
        ORDER BY obitos DESC
    """).df()


def obitos_por_raca(con) -> pd.DataFrame:
    """
    Retorna os óbitos agrupados por raça/cor.
    """

    return con.sql("""
        SELECT
            DS_RACACOR AS RACACOR,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY DS_RACACOR
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

def obitos_por_faixa_etaria(con) -> pd.DataFrame:

    return con.sql("""
        SELECT
            CASE
                WHEN idade_anos < 1 THEN 'Menor de 1 ano'
                WHEN idade_anos BETWEEN 1 AND 4 THEN '1 a 4 anos'
                WHEN idade_anos BETWEEN 5 AND 14 THEN '5 a 14 anos'
                WHEN idade_anos BETWEEN 15 AND 24 THEN '15 a 24 anos'
                WHEN idade_anos BETWEEN 25 AND 44 THEN '25 a 44 anos'
                WHEN idade_anos BETWEEN 45 AND 64 THEN '45 a 64 anos'
                WHEN idade_anos >= 65 THEN '65 anos ou mais'
                ELSE 'Ignorado'
            END AS faixa_etaria,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY faixa_etaria
        ORDER BY
            CASE faixa_etaria
                WHEN 'Menor de 1 ano' THEN 1
                WHEN '1 a 4 anos' THEN 2
                WHEN '5 a 14 anos' THEN 3
                WHEN '15 a 24 anos' THEN 4
                WHEN '25 a 44 anos' THEN 5
                WHEN '45 a 64 anos' THEN 6
                WHEN '65 anos ou mais' THEN 7
                ELSE 8
            END
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
            DS_CAUSABAS AS CAUSABAS,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY DS_CAUSABAS
        ORDER BY obitos DESC
        LIMIT {limite}
    """).df()


def causas_por_sexo(con, limite=10):

    return con.sql(f"""
        WITH top_causas AS (
            SELECT
                DS_CAUSABAS,
                COUNT(*) AS total
            FROM sim
            WHERE DS_CAUSABAS IS NOT NULL
            GROUP BY DS_CAUSABAS
            ORDER BY total DESC
            LIMIT {limite}
        )

        SELECT
            CAST(s.DS_CAUSABAS AS VARCHAR) AS DS_CAUSABAS,
            CAST(s.DS_SEXO AS VARCHAR) AS SEXO,
            COUNT(*) AS obitos
        FROM sim s
        INNER JOIN top_causas t
            ON s.DS_CAUSABAS = t.DS_CAUSABAS
        WHERE s.SEXO IS NOT NULL
        GROUP BY
            s.DS_CAUSABAS,
            s.DS_SEXO
        ORDER BY
            obitos DESC
    """).df()



def causas_por_ano(
    con,
    limite: int = 10,
) -> pd.DataFrame:

    return con.sql(f"""
        WITH top AS (

            SELECT
                CAUSABAS,
                COUNT(*) AS total
            FROM sim
            WHERE CAUSABAS IS NOT NULL
            GROUP BY CAUSABAS
            ORDER BY total DESC
            LIMIT {limite}

        )

        SELECT
            YEAR(s.DTOBITO) AS ano,
            s.CAUSABAS,
            COUNT(*) AS obitos

        FROM sim s

        INNER JOIN top
            ON s.CAUSABAS = top.CAUSABAS

        WHERE s.DTOBITO IS NOT NULL

        GROUP BY
            ano,
            s.CAUSABAS

        ORDER BY
            ano,
            obitos DESC
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
            CAST(CODMUNRES AS VARCHAR) AS CODMUNRES,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY CAST(CODMUNRES AS VARCHAR)
        ORDER BY obitos DESC
    """).df()


def obitos_por_municipio_ocorrencia(con) -> pd.DataFrame:
    """
    Retorna os óbitos por município de ocorrência.
    """

    return con.sql("""
        SELECT
            CAST(CODMUNOCOR AS VARCHAR) AS CODMUNOCOR,
            COUNT(*) AS obitos
        FROM sim
        GROUP BY CAST(CODMUNOCOR AS VARCHAR)
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

