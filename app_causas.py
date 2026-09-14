import streamlit as st
import plotly.express as px

from conexao_duckdb import get_connection

from queries import (
    top_causas,
    causas_por_sexo,
    causas_por_ano,
)


def mostrar_causas():

    con = get_connection(
        read_only=True
    )

    # ========================================================
    # DADOS
    # ========================================================

    df_causas = top_causas(
        con,
        limite=10,
    )

    df_sexo = causas_por_sexo(
        con,
        limite=10,
    )

    df_ano = causas_por_ano(
        con,
        limite=5,
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    st.title("Causas de Morte")

    st.caption(
        "Análise das principais causas básicas de morte"
    )

    # ========================================================
    # TOP 10
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "10 principais causas básicas de morte"
        )

        df_plot = df_causas.sort_values(
            "obitos",
            ascending=True,
        )

        fig = px.bar(
            df_plot,
            x="obitos",
            y="CAUSABAS",
            orientation="h",
            labels={
                "CAUSABAS": "Causa básica",
                "obitos": "Óbitos",
            },
            text_auto=True,
        )

        fig.update_layout(
            height=500,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.write("")

    # ========================================================
    # CAUSAS + SEXO
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "Principais causas por sexo"
        )

        fig = px.bar(
            df_sexo[
                df_sexo["CAUSABAS"].isin(
                    df_causas["CAUSABAS"]
                )
            ],
            x="CAUSABAS",
            y="obitos",
            color="SEXO",
            barmode="group",
            labels={
                "CAUSABAS": "Causa básica",
                "obitos": "Óbitos",
                "SEXO": "Sexo",
            },
        )

        fig.update_layout(
            height=450,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.write("")

    # ========================================================
    # EVOLUÇÃO DAS CAUSAS
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "Evolução das principais causas"
        )

        fig = px.line(
            df_ano,
            x="ano",
            y="obitos",
            color="CAUSABAS",
            markers=True,
            labels={
                "ano": "Ano",
                "obitos": "Óbitos",
                "CAUSABAS": "Causa básica",
            },
        )

        fig.update_layout(
            height=450,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
        )

    st.write("")

    # ========================================================
    # TABELA
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "Ranking das causas"
        )

        st.dataframe(
            df_causas,
            use_container_width=True,
            hide_index=True,
        )

    con.close()