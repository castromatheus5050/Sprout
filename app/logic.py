import pandas as pd
from collections import defaultdict
from email_service import enviar_email_necessidade

def contabilizar_itens(df_colabs, df_estoque, email_config):
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
        enviar_email_necessidade(necessidade_compra, email_config["destinatario"],
                                 email_config["remetente"], email_config["senha"])
        return {
            "itens_necessarios": dict(contagem),
            "estoque_restante": estoque,
            "itens_a_comprar": necessidade_compra,
            "mensagem": "Estoque insuficiente. E-mail enviado ao setor responsável."
        }

    for item, qtd_necessaria in contagem.items():
        estoque[item] = estoque.get(item, 0) - qtd_necessaria

    pd.DataFrame(list(estoque.items()), columns=["Item", "Quantidade"])\
        .to_excel("data/estoque.xlsx", index=False, engine="openpyxl")

    return {
        "itens_necessarios": dict(contagem),
        "estoque_restante": estoque,
        "itens_a_comprar": {},
        "mensagem": "Estoque atualizado com sucesso."
    }
