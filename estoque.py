import pandas as pd
import streamlit as st

def formatar(valor):
    formatado = "{:_.0f}".format(valor)
    formatado = formatado.replace('_','.')  # Formata números com pontos
    return formatado

def formatar2(valor):
    formatado = "{:_.0f}".format(valor)
    formatado = formatado.replace('_','')  # Formata números sem pontos
    return formatado

# Função para colorir células negativas de vermelho
st.set_page_config(layout="wide")
st.title("Relatório de estoque")

# URL do Google Sheets para exportar como XLSX
url = "https://docs.google.com/spreadsheets/d/1lelTCCzvoxH2dxciNjRaIEEkV0DLEj9v5u6v8Y8NQa8/export?format=xlsx"

# Carregando o arquivo do Google Sheets
df = pd.read_excel(url)

# Lista de filtros
lista_filtros = ("Saldo", "Dias Estoque - cart")

# Seleção de filtro no sidebar
familia_selecionada = st.sidebar.selectbox("Selecione a Familia", df["Descrição Familia"].unique())
filtro_selecionado = st.sidebar.selectbox("Classificar por: ", lista_filtros)
filtro_codigo = st.sidebar.text_input("Pesquisa por código","")
botao = st.toggle("Exibir itens principais")

# Filtrando os dados com base nos inputs do usuário
if filtro_codigo == "":
    # Exibe por família selecionada
    df_filtered = df[df["Descrição Familia"] == familia_selecionada]
    df_filtered.sort_values(filtro_selecionado, ascending=True, inplace=True)
else:
    # Exibe por código do item
    df_filtered = df[df["Código Item"].apply(formatar2) == filtro_codigo]
    df_filtered.sort_values(filtro_selecionado, ascending=True, inplace=True)




coluna_faturamento = df_filtered["Faturado Mês Qt."]
coluna_meta = df_filtered["Média Trimestre"]

st.data_editor(
    coluna_faturamento,
    column_config={
        "Faturado Mês Qt.": st.column_config.ProgressColumn(
            "Progresso de faturamento",
            help="Progresso em quantidade",
            format=":.0f",
            min_value=0,
            
        ),
    },
    hide_index=True,
)


# Formatação dos valores
df_filtered["Dias Estoque - cart"] = df_filtered["Dias Estoque - cart"].apply(formatar)
df_filtered["Saldo"] = df_filtered["Saldo"].apply(formatar)
df_filtered["Carteira"] = df_filtered["Carteira"].apply(formatar)
df_filtered["Código Item"] = df_filtered["Código Item"].apply(formatar2)
df_filtered["Média Trimestre"] = df_filtered["Média Trimestre"].apply(formatar)

# Definindo os itens específicos para exibição
itens_tubos = ["20001001", "20001002", "20001005", "20001013"]
itens_conexoes_injetadas = ["20002002", "20002037", "20002035", "20002001"]

# Asegurando que os códigos de itens sejam tratados como strings
df["Código Item"] = df["Código Item"].astype(str)


if botao:
    # Filtrando os itens específicos da família "Tubos"
    df_tubos = df[(df["Descrição Familia"] == "TUBOS") & (df["Código Item"].isin(itens_tubos))]

    # Filtrando os itens específicos da família "Conexões Injetadas"
    df_conexoes_injetadas = df[(df["Descrição Familia"] == "CONEXÕES INJETADAS") & (df["Código Item"].isin(itens_conexoes_injetadas))]

    df_tubos.sort_values(filtro_selecionado, ascending=True, inplace=True)
    df_tubos["Dias Estoque - cart"] = df_tubos["Dias Estoque - cart"].apply(formatar)
    df_tubos["Saldo"] = df_tubos["Saldo"].apply(formatar)
    df_tubos["Carteira"] = df_tubos["Carteira"].apply(formatar)
    df_tubos["Média Trimestre"] = df_tubos["Média Trimestre"].apply(formatar)

    df_conexoes_injetadas.sort_values(filtro_selecionado, ascending=True, inplace=True)
    df_conexoes_injetadas["Dias Estoque - cart"] = df_conexoes_injetadas["Dias Estoque - cart"].apply(formatar)
    df_conexoes_injetadas["Saldo"] = df_conexoes_injetadas["Saldo"].apply(formatar)
    df_conexoes_injetadas["Carteira"] = df_conexoes_injetadas["Carteira"].apply(formatar)
    df_conexoes_injetadas["Média Trimestre"] = df_conexoes_injetadas["Média Trimestre"].apply(formatar)
  
    # Verificando se os DataFrames filtrados contém dados
    st.write("Principais Itens - Tubos", df_tubos)
    st.write("Principais Itens - Conexões", df_conexoes_injetadas)

st.dataframe(df_filtered)
