import pandas as pd
import streamlit as st

def formatar(valor):
    formatado = "{:_.0f}".format(valor)
    formatado = formatado.replace('_','.')
    return formatado

st.set_page_config(layout="wide")
st.title("Relatório de estoque")
url = "https://docs.google.com/spreadsheets/d/1lelTCCzvoxH2dxciNjRaIEEkV0DLEj9v5u6v8Y8NQa8/export?format=xlsx"
#uploaded_file = st.file_uploader("Escolha um arquivo do excel", type=["xlsx"])
lista_filtros = ("Saldo", "Dias Estoque - cart")

if url is not None:
    df = pd.read_excel(url) 
    st.write("### Dados datasul CPP0780")
   
    familia_selecionada = st.sidebar.selectbox("Selecione a Familia", df["Descrição Familia"].unique())
    filtro_selecionado = st.sidebar.selectbox("Classificar por: ", lista_filtros)
   
    df_filtered = df[df["Descrição Familia"] == familia_selecionada]
    df_filtered.sort_values(filtro_selecionado, ascending=True, inplace=True)
    
    df_filtered["Dias Estoque - cart"] = df_filtered["Dias Estoque - cart"].apply(formatar)
    df_filtered["Saldo"] = df_filtered["Saldo"].apply(formatar)
    df_filtered
