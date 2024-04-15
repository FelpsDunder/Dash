import streamlit as st
import pandas as pd
import locale
import plotly.express as px

# try
try:
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
except locale.Error:
    # Se a configuração do locale não for suportada, use o padrão 'C' (ou outro que funcione)
    locale.setlocale(locale.LC_ALL, 'C')

st.set_page_config(layout='wide')

st.title(':violet[Dashboard Teste] :heavy_dollar_sign:')

# dados importacao
df_data = pd.read_excel("dados.xlsx")

df_data['DATA'] = pd.to_datetime(df_data['DATA'])
df_data['Mês'] = df_data['DATA'].dt.to_period('M').astype(str)

def calcular_movimentacao(df, tipo_movimentacao):
    return df[(df['VALOR'] * tipo_movimentacao > 0) & (df['CATEGORIA'] != 'Transferência entre contas')]['VALOR'].sum()


# Cálculos diretos
total_despesas = calcular_movimentacao(df_data, -1)
total_receitas = calcular_movimentacao(df_data, 1)

condicao_categoria = df_data['CATEGORIA'] != 'Transferência entre contas'
condicao_valor = df_data['VALOR'] < 0
condicao_valor_2 = df_data['VALOR'] > 0

valor_despesas = df_data.loc[condicao_categoria & condicao_valor].groupby('Mês')['VALOR'].sum().reset_index()
valor_receitas = df_data.loc[condicao_categoria & condicao_valor_2].groupby('Mês')['VALOR'].sum().reset_index()

# Formatando o eixo x (Mês)
valor_despesas['Mês'] = valor_despesas['Mês'].astype(str).str[5:] + '/' + valor_despesas['Mês'].astype(str).str[0:4]
valor_receitas['Mês'] = valor_receitas['Mês'].astype(str).str[5:] + '/' + valor_receitas['Mês'].astype(str).str[0:4]

# Ordenando o DataFrame pelo Mês
valor_despesas = valor_despesas.sort_values('Mês')
valor_receitas = valor_receitas.sort_values('Mês')

df_grafico = pd.DataFrame({
    'Mês': valor_receitas['Mês'],
    'Soma Despesas': valor_despesas['VALOR'],
    'Soma Receitas': valor_receitas['VALOR']
})

# Removendo o símbolo de moeda antes de converter para float
df_grafico['Soma Despesas'] = df_grafico['Soma Despesas'].astype(str).replace(r'[\$,]', '', regex=True).astype(float)
df_grafico['Soma Receitas'] = df_grafico['Soma Receitas'].astype(str).replace(r'[\$,]', '', regex=True).astype(float)

formatted_despesas = f'R$ {total_despesas:,.2f}'
formatted_receitas = f'R$ {total_receitas:,.2f}'

coluna1, coluna2 = st.columns(2)
with coluna1:
    st.metric("Despesas", formatted_despesas)
with coluna2:
    st.metric("Receitas", formatted_receitas)



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
