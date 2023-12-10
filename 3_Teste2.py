import streamlit as st

def mostrar_pagina_teste2():
    st.title("Segunda Página de Teste")
    st.write("Esta é a Segunda Página de Teste")
    # Adicione outros elementos ou gráficos conforme necessário

if __name__ == "__main__":
    mostrar_pagina_teste2()

    st.line_chart(data=df_grafico, x='Mês',
               y=['Soma Despesas', 'Soma Receitas'],
               color= ['#E01631', '#08abf5'],
               markers=True,
               line_shape='linear', 
               labels={'value': 'Mês', 'variable': 'Soma Despesas'}, 
               width=0,
               height=0,
               use_container_width=True)
