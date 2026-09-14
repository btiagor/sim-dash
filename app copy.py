# 06 etapas para construir dashboards com streamlit
import numpy as np
import streamlit as st
import seaborn as sns
import plotly.express as px
import pandas as pd
from charts import rotina_plot_dispersao_titanic, fig3
from io import StringIO

# import logging
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)

# ------------- Carregar Dataset do Titanic ------------- 
df = sns.load_dataset("titanic")
st.title("Primeiro Dashboard")
st.set_page_config(
    page_title="Meu Dashboard",
    layout="wide"
)

# ------------------------------ SIDEBAR --------------------------------------

# Using object notation
add_selectbox = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("Email", "Home phone", "Mobile phone")
)

# Using "with" notation
with st.sidebar:
    add_radio = st.radio(
        "Choose a shipping method",
        ("Standard (5-15 days)", "Express (2-5 days)")
    )


# Seção #1 ------------------------------------------------------------------------------
st.header("Seção #1")

uploaded_file = st.file_uploader("Selecione seu arquivo: ")

if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()

    # To convert to a string based IO:
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))

    # To read file as string:
    string_data = stringio.read()

    # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.dataframe(dataframe)

# ---------------------
start_value, end_value = st.select_slider(
    "Selecione o intervalo de idade das pessoas do Titanic.",
    options=sorted(df["age"].dropna().unique()),
    value=( 10, 30),
)

print(f"Você selecionou idade entre {start_value} e {end_value}")
# logger.debug(
#     "Você selecionou idade entre %s e %s",
#     start_value,
#     end_value
# )

# ---------------------------------------------------


with st.container():
    st.write("This is inside the container")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))


# ----------------------------------------------------------


c1 , c2 = st.columns(2)

with c1:
    st.plotly_chart(rotina_plot_dispersao_titanic(df, start_value, end_value))

with c2:
    # Calcula matriz de correlação
    titn = df.filter(['survived', 'pclass', 'sibsp', 'parch', 'fare'])
    corr_matrix = titn.corr()

    # Criar o gráfico de heatmap usando Plotly Express
    fig2 = px.imshow(corr_matrix, x=corr_matrix.columns, y=corr_matrix.columns, color_continuous_scale='greens', text_auto=True) # se tirarmos text_auto, fica sem o número

    # configura o título do gráfico
    fig2.update_layout(title_text="Gráfico de Correlação - Titanic Dataset")

    st.plotly_chart(fig2)


# Seção #3 ------------------------------------------------------------------------------
st.header("Seção #3")

md = st.text_area('Type in your markdown string (without outer quotes)',
                  "Happy Streamlit-ing! :balloon:")

st.code(f"""
import streamlit as st

st.markdown('''{md}''')
""")

st.markdown(md)

st.header("Seção #4 , nova!")

st.pyplot(fig3)