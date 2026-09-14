# import streamlit as st

# from conexao_duckdb import get_connection

# from queries import (
#     obitos_por_municipio_residencia,
#     obitos_por_municipio_ocorrencia,
#     fluxo_residencia_ocorrencia,
# )


# def mostrar_territorio():

#     con = get_connection(
#         read_only=True
#     )

#     df_residencia = (
#         obitos_por_municipio_residencia(con)
#     )

#     df_ocorrencia = (
#         obitos_por_municipio_ocorrencia(con)
#     )

#     df_fluxo = (
#         fluxo_residencia_ocorrencia(con)
#     )

#     st.title(
#         "Território"
#     )

#     st.caption(
#         "Distribuição territorial e fluxo dos óbitos"
#     )

#     # mapas e demais visualizações...

#     con.close()

import streamlit as st
import plotly.express as px

from conexao_duckdb import get_connection

from queries import (
    obitos_por_municipio_residencia,
    obitos_por_municipio_ocorrencia,
    fluxo_residencia_ocorrencia,
)


def mostrar_territorio():

    con = get_connection(
        read_only=True
    )

    # ========================================================
    # DADOS
    # ========================================================

    df_residencia = (
        obitos_por_municipio_residencia(con)
    )

    df_ocorrencia = (
        obitos_por_municipio_ocorrencia(con)
    )

    df_fluxo = (
        fluxo_residencia_ocorrencia(con)
    )

    # ========================================================
    # TÍTULO
    # ========================================================

    st.title("Território")

    st.caption(
        "Distribuição dos óbitos segundo município "
        "de residência e ocorrência"
    )

    # ========================================================
    # TOP MUNICÍPIOS
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # RESIDÊNCIA
    # --------------------------------------------------------

    with col1:

        with st.container(border=True):

            st.subheader(
                "Óbitos por município de residência"
            )

            df_plot = (
                df_residencia
                .head(10)
                .sort_values("obitos")
            )

            fig = px.bar(
                df_plot,
                x="obitos",
                y="CODMUNRES",
                orientation="h",
                labels={
                    "CODMUNRES": "Município",
                    "obitos": "Óbitos",
                },
                text_auto=True,
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

    # --------------------------------------------------------
    # OCORRÊNCIA
    # --------------------------------------------------------

    with col2:

        with st.container(border=True):

            st.subheader(
                "Óbitos por município de ocorrência"
            )

            df_plot = (
                df_ocorrencia
                .head(10)
                .sort_values("obitos")
            )

            fig = px.bar(
                df_plot,
                x="obitos",
                y="CODMUNOCOR",
                orientation="h",
                labels={
                    "CODMUNOCOR": "Município",
                    "obitos": "Óbitos",
                },
                text_auto=True,
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
    # FLUXO
    # ========================================================

    with st.container(border=True):

        st.subheader(
            "Fluxo entre município de residência e ocorrência"
        )

        st.caption(
            "Principais combinações entre residência e local "
            "de ocorrência dos óbitos"
        )

        df_fluxo_plot = df_fluxo.head(20).copy()

        df_fluxo_plot["fluxo"] = (
            df_fluxo_plot["CODMUNRES"].astype(str)
            + " → "
            + df_fluxo_plot["CODMUNOCOR"].astype(str)
        )

        df_fluxo_plot = (
            df_fluxo_plot
            .sort_values("obitos")
        )

        fig = px.bar(
            df_fluxo_plot,
            x="obitos",
            y="fluxo",
            orientation="h",
            labels={
                "fluxo": "Residência → ocorrência",
                "obitos": "Óbitos",
            },
            text_auto=True,
        )

        fig.update_layout(
            height=650,
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

    # ========================================================
    # TABELAS
    # ========================================================

    with st.expander(
        "Ver dados por município"
    ):

        tab1, tab2 = st.tabs(
            [
                "Residência",
                "Ocorrência",
            ]
        )

        with tab1:

            st.dataframe(
                df_residencia,
                use_container_width=True,
                hide_index=True,
            )

        with tab2:

            st.dataframe(
                df_ocorrencia,
                use_container_width=True,
                hide_index=True,
            )

    con.close()