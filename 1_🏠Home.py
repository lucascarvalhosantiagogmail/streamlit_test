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


# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Plataforma Santiago Engenharia",
    page_icon= "https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
    layout="wide")

# Função JavaScript para manipular o localStorage
local_storage_script = """
<script>
    function getLoginState() {
        return localStorage.getItem("logged_in") === "true";
    }

    function setLoginState(value) {
        localStorage.setItem("logged_in", value);
    }

    function clearLoginState() {
        localStorage.removeItem("logged_in");
    }

    document.addEventListener('DOMContentLoaded', (event) => {
        const loggedIn = getLoginState();
        if (loggedIn) {
            window.parent.postMessage("logged_in", "*");
        }
    });
</script>
"""

# Incluir o JavaScript no Streamlit
st.components.v1.html(local_storage_script, height=0)

# Verificar o estado de login no JavaScript
login_state_js = """
<script>
    const isLoggedIn = getLoginState();
    window.parent.postMessage(isLoggedIn ? 'logged_in' : 'logged_out', '*');
</script>
"""

st.components.v1.html(login_state_js, height=0)

# Função para verificar se o usuário está logado
def is_logged_in():
    return st.session_state.get('logged_in', False)

# Função para salvar o login no localStorage
def login():
    st.session_state['logged_in'] = True
    st.components.v1.html('<script>setLoginState(true);</script>', height=0)

# Função para limpar o login no localStorage
def logout():
    st.session_state['logged_in'] = False
    st.components.v1.html('<script>clearLoginState();</script>', height=0)

# CARREGAR OS DADOS DA PLANILHA

if "data" not in st.session_state:
    all_sheets = pd.read_excel(path / "dataset"/ "Planilha.xlsx", sheet_name=None)
    df_data = pd.concat(all_sheets.values(), ignore_index=True, join="outer")
    df_data["Licença-Data de validade"] = pd.to_datetime(df_data["Licença-Data de validade"])
    df_data["Licença-Data de emissão"] = pd.to_datetime(df_data["Licença-Data de emissão"])
    st.session_state["data"] = df_data
    
else:
    df_data = st.session_state["data"]

# Verificar estado de login
if is_logged_in():
        
    # LOGO

    st.sidebar.image("Santiago.png", caption="Plataforma de Controle")

    # TÍTULO

    st.title("PLATAFORMA SANTIAGO ENGENHARIA")
    st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

    st.divider()

    # TEXTO

    st.header("Seja bem-vindo(a) à nossa Plataforma!")

    if st.button("Logout"):
        logout()
        st.write("Você foi deslogado. Recarregue a página para realizar o login novamente.")
else:
    st.title("PLATAFORMA SANTIAGO ENGENHARIA")
    st.header("Seja bem-vindo(a) à nossa Plataforma!")
    st.subheader("Para acesso às funcionalidades, faça o seu login.")
    st.divider()

st.subheader("Login:")

# DADOS PARA O LOGIN

login_input = st.text_input("E-mail")
password = st.text_input("Senha", type="password")


if st.button("Entrar"):
    if login_input =="fulano@fulano.com.br" and password == "123456":
        login()
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