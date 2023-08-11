import plotly.express as px
import streamlit as st

st.set_page_config(page_title="CEREM-APP", page_icon="https://raw.githubusercontent.com/IMTEmil/ceremapp/main/cerema_icon2.ico", layout="wide")

st.title("Bienvenue sur l'outil de visualisation de MELBA.")

button_file_uploader = st.file_uploader("Veuillez charger le fichier CSV à visualiser.", type=["csv"], accept_multiple_files=False)


st.subheader("Define a custom colorscale")
df = px.data.iris()
fig = px.scatter(
    df,
    x="sepal_width",
    y="sepal_length",
    color="sepal_length",
    color_continuous_scale="reds",
)

tab1, tab2 = st.tabs(["Streamlit theme (default)", "Plotly native theme"])
with tab1:
    st.plotly_chart(fig, theme="streamlit", use_container_width=True)
with tab2:
    st.plotly_chart(fig, theme=None, use_container_width=True)
