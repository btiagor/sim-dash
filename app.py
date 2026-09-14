import streamlit as st
from conexao_duckdb import get_connection
import plotly.express as px

from queries import (
    total_obitos,
    obitos_por_ano,
    obitos_por_sexo,
    obitos_por_raca,
    top_causas,
)


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="SIM - Mortalidade",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# CONEXÃO COM BANCO
# ============================================================

con = get_connection()


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # --------------------------------------------------------
    # LOGO
    # --------------------------------------------------------

    logo = st.container(
        height=180,
        border=True,
    )

    with logo:

        # st.image(
        #     "assets/logo_sim.jpeg?text=SIM",
        #     width='stretch',
        # )
        st.image(
            "assets/logo_sim.jpeg",
            use_container_width=True,
        )

    st.write("")

    # --------------------------------------------------------
    # MENU
    # --------------------------------------------------------

    st.button(
        "Visão Geral",
        width='stretch'
    )

    st.button(
        "Perfil Demográfico",
        width='stretch'
    )

    st.button(
        "Causas de Morte",
        width='stretch'
    )

    st.button(
        "Território",
        width='stretch'
    )


# ============================================================
# CONSULTAS
# ============================================================

total = total_obitos(con)

df_ano = obitos_por_ano(con)

df_sexo = obitos_por_sexo(con)

df_raca = obitos_por_raca(con)

df_causas = top_causas(
    con,
    limite=10,
)


# ============================================================
# ÁREA PRINCIPAL
# ============================================================

st.title("Sistema de Informação sobre Mortalidade")

st.caption(
    "Painel de monitoramento dos óbitos registrados no SIM"
)


# ============================================================
# PREPARAÇÃO DOS INDICADORES
# ============================================================

# Último ano disponível
ultimo_ano = df_ano["ano"].max()

# Óbitos do último ano
obitos_ultimo_ano = int(
    df_ano.loc[
        df_ano["ano"] == ultimo_ano,
        "obitos",
    ].iloc[0]
)


# Variação em relação ao ano anterior
anos = sorted(
    df_ano["ano"].dropna().unique()
)

if len(anos) >= 2:

    ano_anterior = anos[-2]

    obitos_ano_anterior = int(
        df_ano.loc[
            df_ano["ano"] == ano_anterior,
            "obitos",
        ].iloc[0]
    )

    variacao = (
        (obitos_ultimo_ano - obitos_ano_anterior)
        / obitos_ano_anterior
    ) * 100

else:

    variacao = None


# ============================================================
# 1. CARDS SUPERIORES
# ============================================================

card1, card2, card3 = st.columns(3)


with card1:

    with st.container(border=True):

        st.metric(
            label="Total de óbitos",
            value=f"{total:,}".replace(",", "."),
        )


with card2:

    with st.container(border=True):

        st.metric(
            label=f"Óbitos em {ultimo_ano}",
            value=f"{obitos_ultimo_ano:,}".replace(",", "."),
        )


with card3:

    with st.container(border=True):

        if variacao is not None:

            st.metric(
                label="Variação anual",
                value=f"{variacao:.1f}%".replace(".", ","),
                delta=f"{ano_anterior} → {ultimo_ano}",
                delta_color="inverse",
            )

        else:

            st.metric(
                label="Variação anual",
                value="N/D",
            )


st.write("")


# ============================================================
# 2. FIG1 + FIG2
# ============================================================

fig1_col, fig2_col = st.columns(2)


# ------------------------------------------------------------
# FIG1 — SEXO
# ------------------------------------------------------------

with fig1_col:

    with st.container(border=True):

        st.subheader("Óbitos por sexo")

        st.caption(
            "Distribuição dos óbitos segundo sexo"
        )

        fig1 = px.bar(
            df_sexo,
            x="SEXO",
            y="obitos",
            labels={
                "SEXO": "Sexo",
                "obitos": "Óbitos",
            },
        )

        fig1.update_layout(
            height=350,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig1,
            width='stretch'
        )


# ------------------------------------------------------------
# FIG2 — RAÇA/COR
# ------------------------------------------------------------

with fig2_col:

    with st.container(border=True):

        st.subheader("Óbitos por raça/cor")

        st.caption(
            "Distribuição dos óbitos segundo raça/cor"
        )

        fig2 = px.bar(
            df_raca,
            x="RACACOR",
            y="obitos",
            labels={
                "RACACOR": "Raça/cor",
                "obitos": "Óbitos",
            },
        )

        fig2.update_layout(
            height=350,
            margin=dict(
                l=20,
                r=20,
                t=20,
                b=20,
            ),
        )

        st.plotly_chart(
            fig2,
            width='stretch'
        )


st.write("")


# ============================================================
# 3. FIG3 — PRINCIPAIS CAUSAS
# ============================================================

with st.container(border=True):

    st.subheader(
        "Principais causas básicas de morte"
    )

    st.caption(
        "10 principais causas segundo a causa básica registrada"
    )

    # Ordena para deixar a barra horizontal
    df_causas_plot = df_causas.sort_values(
        "obitos",
        ascending=True,
    )

    fig3 = px.bar(
        df_causas_plot,
        x="obitos",
        y="CAUSABAS",
        orientation="h",
        labels={
            "CAUSABAS": "Causa básica",
            "obitos": "Óbitos",
        },
    )

    fig3.update_layout(
        height=450,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )

    st.plotly_chart(
        fig3,
        width='stretch'
    )


# ============================================================
# 4. EVOLUÇÃO TEMPORAL
# ============================================================

with st.container(border=True):

    st.subheader(
        "Evolução dos óbitos"
    )

    st.caption(
        "Quantidade de óbitos por ano"
    )

    fig4 = px.area(
        df_ano,
        x="ano",
        y="obitos",
        labels={
            "ano": "Ano",
            "obitos": "Óbitos",
        },
    )

    fig4.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )

    st.plotly_chart(
        fig4,
        width='stretch'
    )


# ============================================================
# FOOTER
# ============================================================

st.write("")

footer_left, footer_center, footer_right = st.columns(
    [1, 2, 1]
)

with footer_center:

    st.caption(
        "Dashboard SIM • Sistema de Informação sobre Mortalidade"
    )