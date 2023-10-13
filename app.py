"""
https://github.com/pydata/pandas-datareader/issues/170 -> onde encontrei uma solução utilizando o yfinance

https://stackoverflow.com/questions/46922260/pycharm-pandas-datareader-not-found -> alguns erros ao utilizar o pandas-datareader
"""
#importação de bibliotecas
import datetime as dt
import yfinance as yf
import pandas_datareader.data as pdr
import pandas as pd
import streamlit as st

#definição do primeiro e último dia
end = dt.datetime.today()
start = dt.datetime(end.year-1,end.month,end.day) #forma dinâmica de saber o dia

#função do yfinance para corrigir os erros do pandas-datareader
yf.pdr_override()

#configurando a página
st.set_page_config(page_title="Dashboard Financeiro",layout="wide")
st.title('Dashboard Financeiro')

#utilizando a estrutura with para criar os containers e colunas.
with st.container():
    st.header('Insira as informações solicitadas abaixo :')

    col1,col2,col3=st.columns(3)

    with col1:
        ativo=st.selectbox('Selecione o ativo desejado:',options=['PETR4.SA','VALE3.SA','MGLU3.SA','ITSA4.SA'])
    with col2:
        data_inicial=st.date_input('Selecione a Data inicial:',start)
    with col3:
        data_final=st.date_input('Selecione a Data final:', end)


# retornando as informações da API
sp500 = pdr.get_data_yahoo(ativo, data_inicial, data_final)
sp500.index = sp500.index.date

# métricas
ult_atualizacao = sp500.index.max() # data da ultima atualizacao
ult_cotacao = round(sp500.loc[sp500.index.max(),'Adj Close'],2) # ultima cotacao encontrada
menor_cotacao = round(sp500['Adj Close'].min(),2) # menor cotacao do periodo
maior_cotacao = round(sp500['Adj Close'].max(),2) # maior cotacao do periodo
prim_cotacacao = round(sp500.loc[sp500.index.min(),'Adj Close'],2) # primeira cotacao encontrada
variacao = round(((ult_cotacao-prim_cotacacao)/prim_cotacacao)*100,2)

#métricas no container
with st.container():
    with col1:
        st.metric(f"última atualização - {ult_atualizacao}","RS {:,.2f}".format(ult_cotacao),f"{variacao}%")
    with col2:
        st.metric("Maior Cotação do período ","RS {:,.2f}".format(maior_cotacao))
    with col3:
        st.metric("Maior Cotação do período ","RS {:,.2f}".format(menor_cotacao))

#gráficos
with st.container():
    st.area_chart(sp500[['Adj Close']])
    st.line_chart(sp500[['Low','Adj Close','High']])


#print(sp500.head(5))
#st.dataframe(sp500.head(10),500,500)
