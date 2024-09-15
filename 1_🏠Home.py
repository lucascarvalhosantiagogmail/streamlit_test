import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path
 
path = Path(__file__).parent


# CARREGAR OS DADOS DA PLANILHA

if "data" not in st.session_state:
    all_sheets = pd.read_excel(path / "dataset"/ "Planilha.xlsx", sheet_name=None)
    df_data = pd.concat(all_sheets.values(), ignore_index=True, join="outer")
    df_data["Licença-Data de validade"] = pd.to_datetime(df_data["Licença-Data de validade"])
    df_data["Licença-Data de emissão"] = pd.to_datetime(df_data["Licença-Data de emissão"])
    st.session_state["data"] = df_data
    
else:
    df_data = st.session_state["data"]
    

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Plataforma Santiago Engenharia",
    page_icon= "https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
    layout="wide")

# LOGO

st.sidebar.image("Santiago.png", caption="Plataforma de Controle")

# TÍTULO

st.title("PLATAFORMA SANTIAGO ENGENHARIA")
st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

st.divider()

# TEXTO

st.header("Seja bem-vindo(a) à nossa Plataforma!")
st.subheader("Para acesso às funcionalidades, faça o seu login.")
st.divider()

st.subheader("Login:")

# DADOS PARA O LOGIN

login = st.text_input("E-mail")
password = st.text_input("Senha", type="password")


if st.button("Entrar"):
    if login =="fulano@fulano.com.br" and password == "123456":
        st.session_state.logged_in=True
        st.session_state.page = "2_📆Controle"
        st.markdown(
            """
            <div style='text-align: center;'>
                <h2 style='color: green;'>Página liberada para acesso. Clique nos menus laterais para acessar.</h2>
                
            </div>
            """,
            unsafe_allow_html=True
        )
        st.session_state.page = "1_🌍Home"    
    
    else:
        st.error("E-mail ou senha incorretos. Tente novamente.")
st.divider()
st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")