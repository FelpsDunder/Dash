import streamlit as st
import pandas as pd
import locale
import plotly.express as px

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

st.set_page_config(layout='wide')

st.title(':rainbow[Dashboard Teste] :heavy_dollar_sign:')

df_data = pd.read_excel("dataset/dados.xlsx")

df_data['DATAEXTRAT'] = pd.to_datetime(df_data['DATAEXTRAT'])
df_data['Mês'] = df_data['DATAEXTRAT'].dt.to_period('M').astype(str)

# Função para calcular despesas e receitas
def calcular_movimentacao(df, tipo_movimentacao):
    filtro = (df['VALORLANCA'] * tipo_movimentacao > 0) & (df['CATEGORIA'] != 'Transferência entre contas')
    dados_filtrados = df[filtro]
    soma_movimentacao = dados_filtrados['VALORLANCA'].sum()
    return soma_movimentacao

# Cálculos diretos
total_despesas = calcular_movimentacao(df_data, -1)
total_receitas = calcular_movimentacao(df_data, 1)
saldo_ano = total_receitas + total_despesas

# Criação do DataFrame para o gráfico
df_grafico = pd.DataFrame({
    'Mês': df_data['Mês'].unique(),
    'Soma Despesas': df_data.loc[df_data['VALORLANCA'] < 0].groupby('Mês')['VALORLANCA'].sum().values,
    'Soma Receitas': df_data.loc[df_data['VALORLANCA'] > 0].groupby('Mês')['VALORLANCA'].sum().values
})

# Formatação dos valores
formatted_despesas = locale.currency(total_despesas, grouping=True)
formatted_receitas = locale.currency(total_receitas, grouping=True)
formatted_saldo = locale.currency(saldo_ano, grouping=True)

# Layout da página
coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric("Despesas", f"{formatted_despesas}")
with coluna2:
    st.metric("Receitas", f"{formatted_receitas}")

st.metric("Saldo", f"{formatted_saldo}")

# Criação do gráfico
fig = px.line(df_grafico, x='Mês', y=['Soma Despesas', 'Soma Receitas'],
              markers=True, line_shape='linear', labels={'value': '', 'variable': 'Soma Receitas'},
              color_discrete_map={'Soma Despesas': '#E01631', 'Soma Receitas': '#6D05FF'})

st.plotly_chart(fig)
