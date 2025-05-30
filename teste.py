import streamlit as st
import pandas as pd
from collections import defaultdict
import os
import smtplib
from email.mime.text import MIMEText

# Função de envio de e-mail usando Gmail com senha de app
def enviar_email_necessidade(itens, destinatario):
    corpo = "Precisamos repor os seguintes itens:\n\n"
    for item, quantidade in itens.items():
        corpo += f"- {item}: {quantidade} unidades\n"
    corpo += "\nPor favor, providenciar o quanto antes."

    msg = MIMEText(corpo)
    msg['Subject'] = 'Reposição de Estoque Necessária'
    msg['From'] = 'conextagsprout@gmail.com'
    msg['To'] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login("conextagsprout@gmail.com", "zvct qlke ypry asbt")
            server.send_message(msg)
    except Exception as e:
        print("Erro ao enviar e-mail:", e)

# Função principal
def contabilizar_itens(df_colabs, df_estoque):
    contagem = defaultdict(int)

    for _, row in df_colabs.iterrows():
        categoria = row["Categoria de Kit"]
        tamanho = row["Tamanho da Camisa"]

        if pd.isna(categoria) or pd.isna(tamanho):
            continue

        contagem[f"Mochila {categoria}"] += 1
        contagem[f"Caderno {categoria}"] += 1
        contagem[f"Caneta {categoria}"] += 1
        contagem[f"Camiseta {tamanho}"] += 1

    estoque = dict(zip(df_estoque['Item'], df_estoque['Quantidade']))
    necessidade_compra = {}

    for item, qtd_necessaria in contagem.items():
        qtd_em_estoque = estoque.get(item, 0)
        if qtd_em_estoque < qtd_necessaria:
            necessidade_compra[item] = qtd_necessaria - qtd_em_estoque

    if necessidade_compra:
        enviar_email_necessidade(necessidade_compra, 'conextagsprout@gmail.com')
        return {
            "itens_necessarios": dict(contagem),
            "estoque_restante": estoque,
            "itens_a_comprar": necessidade_compra,
            "mensagem": "Estoque insuficiente. Reposição necessária para os itens indicados. E-mail enviado para o setor responsável."
        }

    for item, qtd_necessaria in contagem.items():
        estoque[item] = estoque.get(item, 0) - qtd_necessaria

    df_estoque_atualizado = pd.DataFrame(list(estoque.items()), columns=["Item", "Quantidade"])
    df_estoque_atualizado.to_excel("estoque.xlsx", index=False, engine="openpyxl")

    return {
        "itens_necessarios": dict(contagem),
        "estoque_restante": estoque,
        "itens_a_comprar": {},
        "mensagem": "Estoque atualizado com sucesso."
    }

# Interface Streamlit
st.title("Gestão de Kits para Colaboradores")

caminho_padrao_colabs = "colaboradores.xlsx"
caminho_padrao_estoque = "estoque.xlsx"

if not os.path.exists(caminho_padrao_colabs) or not os.path.exists(caminho_padrao_estoque):
    st.error("Arquivos 'colaboradores.xlsx' e/ou 'estoque.xlsx' não encontrados no diretório atual.")
else:
    df_colabs = pd.read_excel(caminho_padrao_colabs, engine="openpyxl")
    df_estoque = pd.read_excel(caminho_padrao_estoque, engine="openpyxl")

    st.subheader("Selecione uma ação:")
    col1, col2, col3 = st.columns(3)

    with col1:
        ver_estoque = st.button("Ver Estoque")
    with col2:
        ver_colaboradores = st.button("Ver Colaboradores")
    with col3:
        fazer_requisicao = st.button("Fazer Requisição")

    if ver_estoque:
        st.subheader("Estoque Atual")
        st.dataframe(df_estoque)

    if ver_colaboradores:
        st.subheader("Lista de Colaboradores")
        st.dataframe(df_colabs)

    if fazer_requisicao:
        resultado = contabilizar_itens(df_colabs, df_estoque)

        st.subheader("Resumo da Operação")
        st.write(resultado["mensagem"])

        st.subheader("Itens Necessários")
        st.write(resultado["itens_necessarios"])

        st.subheader("Estoque Restante")
        st.write(resultado["estoque_restante"])

        st.subheader("Itens a Comprar")
        st.write(resultado["itens_a_comprar"])
