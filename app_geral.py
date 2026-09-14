import streamlit as st
import plotly.express as px
from conexao_duckdb import get_connection

from queries import (
    total_obitos,
    obitos_por_ano,
    obitos_por_sexo,
    obitos_por_raca,
    top_causas,
)

def mostrar_geral():

    con = get_connection()

    # ========================================================
    # DADOS
    # ========================================================

    total = total_obitos(con)

    df_ano = obitos_por_ano(con)

    df_sexo = obitos_por_sexo(con)

    df_raca = obitos_por_raca(con)

    df_causas = top_causas(
        con,
        limite=10,
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    st.title(
        "Visão Geral"
    )

    st.caption(
        "Panorama dos óbitos registrados no SIM"
    )

    # ========================================================
    # CARDS
    # ========================================================

    card1, card2, card3 = st.columns(3)

    with card1:

        with st.container(border=True):

            st.metric(
                "Total de óbitos",
                f"{total:,}".replace(",", "."),
            )

    with card2:

        with st.container(border=True):

            ultimo_ano = df_ano["ano"].max()

            valor_ultimo_ano = int(
                df_ano.loc[
                    df_ano["ano"] == ultimo_ano,
                    "obitos",
                ].iloc[0]
            )

            st.metric(
                f"Óbitos em {ultimo_ano}",
                f"{valor_ultimo_ano:,}".replace(
                    ",", "."
                ),
            )

    with card3:

        with st.container(border=True):

            st.metric(
                "Período analisado",
                f"{df_ano['ano'].min()}–{df_ano['ano'].max()}",
            )

    st.write("")

    # ========================================================
    # SEXO + RAÇA/COR
    # ========================================================

    col1, col2 = st.columns(2)

    with col1:

        with st.container(border=True):

            st.subheader(
                "Óbitos por sexo"
            )

            fig = px.bar(
                df_sexo,
                x="SEXO",
                y="obitos",
            )

            fig.update_layout(
                height=350,
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

    with col2:

        with st.container(border=True):

            st.subheader(
                "Óbitos por raça/cor"
            )

            fig = px.bar(
                df_raca,
                x="RACACOR",
                y="obitos",
            )

            fig.update_layout(
                height=350,
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
    # CAUSAS
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "Principais causas básicas de morte"
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
    # EVOLUÇÃO
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "Evolução dos óbitos"
        )

        fig = px.area(
            df_ano,
            x="ano",
            y="obitos",
        )

        fig.update_layout(
            height=400,
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

    con.close()