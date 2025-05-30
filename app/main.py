import streamlit as st
import pandas as pd
import os
from logic import contabilizar_itens

st.title("Gestão de Kits para Colaboradores")

CAMINHO_COLABS = "data/colaboradores.xlsx"
CAMINHO_ESTOQUE = "data/estoque.xlsx"

email_config = {
    "remetente": "conextagsprout@gmail.com",
    "senha": "zvct qlke ypry asbt",  # melhor usar os.environ.get("EMAIL_APP_PASS")
    "destinatario": "conextagsprout@gmail.com"
}

if not os.path.exists(CAMINHO_COLABS) or not os.path.exists(CAMINHO_ESTOQUE):
    st.error("Arquivos .xlsx não encontrados.")
else:
    df_colabs = pd.read_excel(CAMINHO_COLABS, engine="openpyxl")
    df_estoque = pd.read_excel(CAMINHO_ESTOQUE, engine="openpyxl")

    st.subheader("Selecione uma ação:")
    col1, col2, col3 = st.columns(3)
    if col1.button("Ver Estoque"):
        st.subheader("Estoque Atual")
        st.dataframe(df_estoque)
    if col2.button("Ver Colaboradores"):
        st.subheader("Lista de Colaboradores")
        st.dataframe(df_colabs)
    if col3.button("Fazer Requisição"):
        resultado = contabilizar_itens(df_colabs, df_estoque, email_config)
        st.subheader("Resumo da Operação")
        st.write(resultado["mensagem"])
        st.subheader("Itens Necessários")
        st.write(resultado["itens_necessarios"])
        st.subheader("Estoque Restante")
        st.write(resultado["estoque_restante"])
        st.subheader("Itens a Comprar")
        st.write(resultado["itens_a_comprar"])
