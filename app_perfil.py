import streamlit as st
import plotly.express as px
from conexao_duckdb import get_connection


from queries import (
    obitos_por_sexo,
    obitos_por_raca,
    obitos_por_faixa_etaria,
    obitos_por_idade,
)


def mostrar_perfil():

    con = get_connection(
        read_only=True
    )

    # ========================================================
    # DADOS
    # ========================================================

    df_sexo = obitos_por_sexo(con)

    df_raca = obitos_por_raca(con)

    df_faixa = obitos_por_faixa_etaria(con)

    df_idade = obitos_por_idade(con)

    # ========================================================
    # TÍTULO
    # ========================================================

    st.title("Perfil Demográfico")

    st.caption(
        "Distribuição dos óbitos segundo características "
        "demográficas"
    )

    # ========================================================
    # SEXO + RAÇA/COR
    # ========================================================

    col1, col2 = st.columns(2)

    # --------------------------------------------------------
    # SEXO
    # --------------------------------------------------------

    with col1:

        with st.container(border=True):

            st.subheader("Óbitos por sexo")

            fig = px.bar(
                df_sexo,
                x="SEXO",
                y="obitos",
                labels={
                    "SEXO": "Sexo",
                    "obitos": "Óbitos",
                },
                text_auto=True,
            )

            fig.update_layout(
                height=380,
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
    # RAÇA/COR
    # --------------------------------------------------------

    with col2:

        with st.container(border=True):

            st.subheader("Óbitos por raça/cor")

            fig = px.bar(
                df_raca,
                x="RACACOR",
                y="obitos",
                labels={
                    "RACACOR": "Raça/cor",
                    "obitos": "Óbitos",
                },
                text_auto=True,
            )

            fig.update_layout(
                height=380,
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
    # FAIXA ETÁRIA
    # ========================================================

    with st.container(border=True):

        st.subheader("Óbitos por faixa etária")

        st.caption(
            "Distribuição dos óbitos segundo faixa etária"
        )

        fig = px.bar(
            df_faixa,
            x="faixa_etaria",
            y="obitos",
            labels={
                "faixa_etaria": "Faixa etária",
                "obitos": "Óbitos",
            },
            text_auto=True,
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

    st.write("")

    # ========================================================
    # IDADE
    # ========================================================

    with st.container(border=True):

        st.subheader("Distribuição dos óbitos por idade")

        st.caption(
            "Quantidade de óbitos segundo idade em anos"
        )

        fig = px.line(
            df_idade,
            x="idade_anos",
            y="obitos",
            markers=True,
            labels={
                "idade_anos": "Idade",
                "obitos": "Óbitos",
            },
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