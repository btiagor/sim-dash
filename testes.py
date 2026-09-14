from queries import total_obitos, obitos_por_ano
from conexao_duckdb import get_connection


def testar_duckdb():
    con = get_connection()

    print("Conexão realizada!")

    print(
        con.sql("""
            SHOW TABLES
        """).df()
    )

    con.close()

def testar_query():

    con = get_connection()

    print("Total de óbitos:")

    total = total_obitos(con)

    print(total)


    print("\nÓbitos por ano:")

    df = obitos_por_ano(con)

    print(df)

    con.close()

if __name__ == "__main__":
    testar_duckdb()
    testar_query()