import streamlit as st

from app_geral import mostrar_geral
from app_perfil import mostrar_perfil
from app_causas import mostrar_causas
from app_territorio import mostrar_territorio


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="SIM - Mortalidade",
    page_icon="📊",
    layout="wide",
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("SIM")

    st.caption(
        "Sistema de Informação sobre Mortalidade"
    )

    pagina = st.radio(
        "Navegação",
        [
            "Visão Geral",
            "Perfil Demográfico",
            "Causas de Morte",
            "Território",
        ],
    )


# ============================================================
# NAVEGAÇÃO
# ============================================================

if pagina == "Visão Geral":

    mostrar_geral()


elif pagina == "Perfil Demográfico":

    mostrar_perfil()


elif pagina == "Causas de Morte":

    mostrar_causas()


elif pagina == "Território":

    mostrar_territorio()