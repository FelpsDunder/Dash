import streamlit as st
import pandas as pd
import locale
import plotly.express as px

try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # Se a configuração do locale não for suportada, use o padrão 'C' (ou outro que funcione)
    locale.setlocale(locale.LC_ALL, 'C')

st.set_page_config(layout='wide')

st.title(':rainbow[Dashboard Teste] :heavy_dollar_sign:')
 #dados importacao
df_data = pd.read_excel("dados.xlsx")

df_data['DATAEXTRAT'] = pd.to_datetime(df_data['DATAEXTRAT'])
df_data['Mês'] = df_data['DATAEXTRAT'].dt.to_period('M').astype(str)

def calcular_movimentacao(df, tipo_movimentacao):
    filtro = (df['VALORLANCA'] * tipo_movimentacao > 0) & (df['CATEGORIA'] != 'Transferência entre contas')
    dados_filtrados = df[filtro]
    soma_movimentacao = dados_filtrados['VALORLANCA'].sum()
    return soma_movimentacao

# Cálculos diretos
total_despesas = calcular_movimentacao(df_data, -1)
total_receitas = calcular_movimentacao(df_data, 1)
saldo_ano = total_receitas + total_despesas

condicao_categoria = df_data['CATEGORIA'] != 'Transferência entre contas'
condicao_valor = df_data['VALORLANCA'] < 0
condicao_valor_2 = df_data['VALORLANCA'] > 0

valor_despesas = df_data.loc[condicao_categoria & condicao_valor].groupby('Mês')['VALORLANCA'].sum().reset_index()
valor_receitas = df_data.loc[condicao_categoria & condicao_valor_2].groupby('Mês')['VALORLANCA'].sum().reset_index()

# Formatando o eixo x (Mês)
valor_despesas['Mês'] = valor_despesas['Mês'].astype(str).str[5:] + '/' + valor_despesas['Mês'].astype(str).str[0:4] 
valor_receitas['Mês'] = valor_receitas['Mês'].astype(str).str[5:] + '/' + valor_receitas['Mês'].astype(str).str[0:4]

# Ordenando o DataFrame pelo Mês
valor_despesas = valor_despesas.sort_values('Mês')
valor_receitas = valor_receitas.sort_values('Mês')

df_grafico = pd.DataFrame({
    'Mês': valor_despesas['Mês'],
    'Soma Despesas': valor_despesas['VALORLANCA'],
    'Soma Receitas': valor_receitas['VALORLANCA']
})

# Removendo o símbolo de moeda antes de converter para float
df_grafico['Soma Despesas'] = df_grafico['Soma Despesas'].astype(str).replace('[\$,]', '', regex=True).astype(float)
df_grafico['Soma Receitas'] = df_grafico['Soma Receitas'].astype(str).replace('[\$,]', '', regex=True).astype(float)

formatted_despesas = locale.currency(total_despesas, grouping=True)
formatted_receitas = locale.currency(total_receitas, grouping=True)
formatted_saldo = locale.currency(saldo_ano, grouping=True)

coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric("Despesas", f"{formatted_despesas}")
with coluna2:
    st.metric("Receitas", f"{formatted_receitas}")

st.metric("Saldo", f"{formatted_saldo}")

fig = px.line(df_grafico, x='Mês', y=['Soma Despesas', 'Soma Receitas'],
              markers=True, line_shape='linear', labels={'value': '', 'variable': ''},
              color_discrete_map={'Soma Despesas': '#E01631', 'Soma Receitas': '#6D05FF'})

# Adicionando a formatação de moeda ao eixo y
fig.update_yaxes(
    tickprefix="R$ ",
    tickformat=",.2f"
)

fig.update_traces(texttemplate='%{text:$,.2s}', textposition='top center')
st.plotly_chart(fig)
