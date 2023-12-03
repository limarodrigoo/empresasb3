import requests
import pandas as pd
from bs4 import BeautifulSoup
from helper import filtros

url = "https://www.fundamentus.com.br/resultado.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")


# Encontrar a tabela pelo ID "resultado"
table = soup.find("table", id="resultado")

if table:
    colunas_desejadas = [
        "Papel",
        "Cotação",
        "P/L",
        "ROE",
        "Dív.Brut/ Patrim.",
        "Cresc. Rec.5a",
        "Liq.2meses",
        "Patrim. Líq",
        "ROIC",
        "P/VP",
        "Div.Yield",
        "Mrg. Líq.",
    ]

    filtro_dict = {
        "P/L": ("<", 15),
        "ROE": (">=", 0.15),
        "Dív.Brut/ Patrim.": ("<=", 1),
        "Cresc. Rec.5a": (">=", 0.1),
        "Liq.2meses": (">=", 2000000),
        "Patrim. Líq": (">", 0),
        "ROIC": (">=", 0.15),
        "Mrg. Líq.": (">=", 0.1),
    }
    data = []
    for row in table.find_all("tr"):
        cols = row.find_all(["td", "th"])
        data.append([col.text.strip() for col in cols])

    # Criar um DataFrame pandas
    df = pd.DataFrame(data[1:], columns=data[0])

    allColumns = list()
    for column in df.columns:
        allColumns.append(column)

    colunas_indesejadas = list(set(colunas_desejadas) ^ set(allColumns))

    for coluna in colunas_indesejadas:
        df.drop(coluna, axis=1, inplace=True)

    for i, coluna in enumerate(colunas_desejadas):
        if i != 0:
            df[coluna] = df[coluna].apply(filtros.limpar_e_converter)
    # Salvar DataFrame em um arquivo Excel

    for coluna, (operacao, valor) in filtro_dict.items():
        if operacao == ">":
            df = df[df[coluna] > valor]
        elif operacao == "<":
            df = df[df[coluna] < valor]
        elif operacao == "==":
            df = df[df[coluna] == valor]
        elif operacao == ">=":
            df = df[df[coluna] >= valor]
        elif operacao == "<=":
            df = df[df[coluna] <= valor]

    df.to_excel("dados_tabela.xlsx", index=False)

    print("Dados da tabela salvos em dados_tabela.xlsx")
else:
    print("Tabela 'resultado' não encontrada.")
