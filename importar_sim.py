from ingestion_sim import carregar_sim
from transformation_sim import transformar_sim
from conexao_duckdb import get_connection


ARQUIVO = "data/raw/base_sim_do.xlsx"
ARQUIVO_CID = "data/raw/codigoCID.xlsx"


def main():
    print("Carregando SIM...")

    df = carregar_sim(ARQUIVO)
    df_cid = carregar_sim(ARQUIVO_CID)

    print(f"{len(df):,} registros carregados.")

    print("Transformando dados...")

    df = transformar_sim(df, df_cid)

    print("Gravando no DuckDB...")

    con = get_connection()

    con.register("df_sim", df)

    con.execute("""
        CREATE OR REPLACE TABLE sim AS
        SELECT *
        FROM df_sim
    """)

    con.close()

    print("Importação concluída.")


if __name__ == "__main__":
    main()