import streamlit as st
import pandas as pd
from datetime import datetime
import webbrowser
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import plotly.express as px 
import plotly.graph_objects as go
from pathlib import Path

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Plataforma Santiago Engenharia",
    page_icon= "https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll",
    layout="wide"
)

# Função JavaScript para manipular o localStorage
local_storage_script = """
<script>
    function getLoginState() {
        return localStorage.getItem("logged_in") === "true";
    }

    function clearLoginState() {
        localStorage.removeItem("logged_in");
    }

    document.addEventListener('DOMContentLoaded', (event) => {
        const loggedIn = getLoginState();
        if (!loggedIn) {
            window.parent.postMessage("logged_out", "*");
        }
    });
</script>
"""

# Incluir o JavaScript no Streamlit
st.components.v1.html(local_storage_script, height=0)

# Função para verificar se o usuário está logado
def is_logged_in():
    return st.session_state.get('logged_in', False)

# Função para limpar o login no localStorage
def logout():
    st.session_state['logged_in'] = False
    st.components.v1.html('<script>clearLoginState();</script>', height=0)

# Verificação de login
if not is_logged_in():
    st.subheader("Você precisa fazer login para acessar este menu")
    st.subheader("Volte para a página inicial")
    st.stop()  # Interrompe o código se não estiver logado

else:
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(8)
    with col1:
        st.subheader("Logoff")
    with col2:
        if st.button("Sair"):
            logout()
            st.write("Você foi desconectado. Clique [aqui](#/1_🌍Home) para voltar à página inicial.")


    path = Path(__file__).parent.parent


    # TÍTULO DA PÁGINA
    st.title("CONTROLE DE LICENÇAS")
    st.header("Empresa: Engenharia LTDA")
    st.logo("https://img1.wsimg.com/isteam/ip/0cdba6f5-2fc0-4aaf-b030-d8df637187a2/blob-46e0c21.png/:/rs=w:134,h:100,cg:true,m/cr=w:134,h:100/qt=q:100/ll")

# CARREGAR OS DADOS DA PLANILHA

    if "data" in st.session_state:
        df_data = st.session_state["data"]
        df_data = df_data.dropna(subset=["Cidade",
                                        "Licença",
                                        "Código Licença",
                                        "Licença-Data de emissão",
                                        "Licença-Data de validade",
                                        "Status da licença",
                                        "Dias restantes",                                  
                                        ])
        df_data = df_data[(df_data["Cidade"] != "") &
                        (df_data["Licença"] != "") &
                        (df_data["Código Licença"] != "") &
                        (df_data["Licença-Data de emissão"] != "") &
                        (df_data["Licença-Data de validade"] != "") &
                        (df_data["Status da licença"] != "") &
                        (df_data["Dias restantes"] != "") ]
        df_data = df_data[["Cidade",
                        "Licença",
                        "Código Licença",
                        "Licença-Data de emissão",
                        "Licença-Data de validade",
                        "Status da licença",
                        "Dias restantes"]]
    
    # DESCRITIVO INICIAL
        st.subheader("Número de Licenças: 2")
        st.subheader("Código da licença 1: L-1234")
        st.subheader("Código da licença 2: L-5678")

    # INSERIR OPÇÃO PARA ESCOLHA DA LICENÇA
        licenca = df_data["Código Licença"].unique()
        licenca_selecionada = st.sidebar.selectbox("Licenças", licenca)

        df_filtrado = df_data[df_data["Código Licença"] == licenca_selecionada]

        contagem_por_data = df_filtrado.groupby("Licença-Data de validade")["Código Licença"].count().reset_index()

        st.divider()

        st.header(f"Licença {licenca_selecionada}")

        if not df_filtrado.empty:
            col1, col2 = st.columns(2)
            col1.metric(label="Data de emissão da licença:", value=df_filtrado["Licença-Data de emissão"].iloc[0].strftime("%d/%m/%Y"))
            col2.metric(label="Data da validade da licença:", value=df_filtrado["Licença-Data de validade"].iloc[0].strftime("%d/%m/%Y"))
        
            col1, col2 = st.columns(2)

            col1.metric(label="Dias para vencimento:", value=int(df_filtrado["Dias restantes"].iloc[0]))
            col2.metric(label="Status:", value=df_filtrado["Status da licença"].iloc[0])
        else:
            st.warning("Não há licença para a condição selecionada.")

        st.divider()

    # VENCIMENTO

        st.subheader("Vencimento")

    # CRIANDO CORES DAS BARRAS DO GRÁFICO

        df_filtrado["Cor"] = df_filtrado["Status da licença"].map({
            "Dentro do prazo": "green",
            "Vencida": "red",
            "Renovar": "yellow"
    })

    # 1º GRÁFICO

        contagem_por_data = contagem_por_data.merge(df_filtrado[["Licença-Data de validade", "Cor"]].drop_duplicates(), on="Licença-Data de validade", how="left") 



        fig = px.bar(
            contagem_por_data,
            x="Licença-Data de validade",
            y="Código Licença",
            color="Cor",
            labels={"Licença-Data de validade": "Data de Validade", "Quantidade de licenças": "Número de Licenças"},
            template="plotly_dark",
            color_discrete_map={"green":"green","red":"red","yellow":"yellow"}
    )

    #CONFIGURANDO O TAMANHO DO GRÁFICO
        fig.update_layout(
            width=600,
            height=400
    )

        col1, col2, col3 = st.columns([1, 2, 1])

        with col2:
            st.plotly_chart(fig)

        st.divider()


    else:
        st.write("Dados não correlacionados")

    # FUNÇÃO QUE DEFINE A PARA A LOGO

    st.sidebar.image("Santiago.png", caption="Plataforma de Controle")
    st.sidebar.markdown("Desenvolvido por Santiago Engenharia (https://santiagoengenharia.com)")


 
 