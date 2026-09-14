import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Dashboard",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# DADOS MOCK
# ============================================================

np.random.seed(42)

df1 = pd.DataFrame({
    "Categoria": ["A", "B", "C", "D", "E"],
    "Valor": [20, 35, 28, 50, 42],
})

df2 = pd.DataFrame({
    "Categoria": ["A", "B", "C", "D", "E"],
    "Valor": [15, 25, 45, 30, 55],
})

df3 = pd.DataFrame({
    "Período": range(1, 21),
    "Valor": np.random.randn(20).cumsum(),
})


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    # Mock da logo
    logo = st.container(height=180, border=True)

    with logo:
        st.image(
            "https://via.placeholder.com/180x120.png?text=LOGO",
            use_container_width=True,
        )

    st.write("")

    st.button(
        "Visão Geral",
        use_container_width=True,
    )

    st.button(
        "Análises",
        use_container_width=True,
    )

    st.button(
        "Configurações",
        use_container_width=True,
    )


# ============================================================
# ÁREA PRINCIPAL
# ============================================================

# ------------------------------------------------------------
# 1. CARDS SUPERIORES
# ------------------------------------------------------------

card1, card2, card3 = st.columns(3)

with card1:
    with st.container(border=True):
        st.metric(
            label="Métrica 1",
            value="1.234",
            delta="12,5%",
        )


with card2:
    with st.container(border=True):
        st.metric(
            label="Métrica 2",
            value="5.678",
            delta="8,2%",
        )


with card3:
    with st.container(border=True):
        st.metric(
            label="Métrica 3",
            value="9.101",
            delta="15,3%",
        )


st.write("")


# ------------------------------------------------------------
# 2. FIG1 + FIG2
# ------------------------------------------------------------

fig1_col, fig2_col = st.columns(2)


with fig1_col:

    with st.container(border=True):

        st.subheader("FIG1")
        st.caption("Título da Visualização")

        fig1 = px.bar(
            df1,
            x="Categoria",
            y="Valor",
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
            use_container_width=True,
        )


with fig2_col:

    with st.container(border=True):

        st.subheader("FIG2")
        st.caption("Título da Visualização")

        fig2 = px.line(
            df2,
            x="Categoria",
            y="Valor",
            markers=True,
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
            use_container_width=True,
        )


st.write("")


# ------------------------------------------------------------
# 3. FIG3 — LARGURA TOTAL
# ------------------------------------------------------------

with st.container(border=True):

    st.subheader("FIG3")
    st.caption("Título da Visualização")

    fig3 = px.area(
        df3,
        x="Período",
        y="Valor",
    )

    fig3.update_layout(
        height=400,
        margin=dict(
            l=20,
            r=20,
            t=20,
            b=20,
        ),
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
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
        "Desenvolvido por fulano de tal"
    )