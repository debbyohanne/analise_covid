#Vamos instalar o streamlit antes, senão vai dar erro.
#Pra isso aperto ctrl + shift + p pra poder mudar o ambiente do Run daqui pro do ambiente virtual.

#Mas como não aconteceu nada quando eu rodo pelo run, eu precisei colocar no terminal de comando: streamlit run app.py
#Agoraaaaa sim abriu o browser com o meu título.

#Copiando o endereço Network URL, eu consigo abrir essa aplicação em outros dispositivos, por exemplo o celular. 

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np  #entrou por causa do código unique que me retorna um array numpy

def carrega_dados(caminho):
    dados = pd.read_csv(caminho)
    return dados

#como estado tem um parâmetro definido por default, ele tem que vir por último: 
def grafico_comparativo(dados_2019, dados_2020, causa, estado='BRASIL'):

    if estado == 'BRASIL':
        #aqui então só vou classificar por tipo da doença
        total_2019 = dados_2019.groupby('tipo_doenca').sum()
        total_2020 = dados_2020.groupby('tipo_doenca').sum()
        lista = [int(total_2019.loc[causa]),int(total_2020.loc[causa])]
    else:
        #classificando por uf e tipo de doença
        total_2019 = dados_2019.groupby(['uf','tipo_doenca']).sum()
        total_2020 = dados_2020.groupby(['uf','tipo_doenca']).sum()
        
        #fazendo uma lista com o total por tipo da doença
        lista = [int(total_2019.loc[estado,causa]),int(total_2020.loc[estado,causa])]

    #criando um dataframe com os dados que fizemos no loc. 
    dados = pd.DataFrame({'Total': lista,
                            'Ano':[2019,2020]})

    #plotando o gráfico de maneira que não dê erro na nossa aplicação... 
    #é como se eu tivesse que fazer um subplot dentro do plot. 
    fig, ax = plt.subplots()
    ax = sns.barplot(x='Ano',y='Total',data=dados)
    ax.set_title(f'Óbitos por {causa} = {estado}')
 
    return fig

def main():
    obitos_2019 = carrega_dados('dados\obitos-2019.csv')
    obitos_2020 = carrega_dados('dados\obitos-2020.csv')
 
    tipo_doenca = obitos_2020['tipo_doenca'].unique()
    estado = np.append(obitos_2020['uf'].unique(), 'BRASIL')

    st.title("Análise de Óbitos 2019-2020")

    #você pode ver as funções mágicas sobre os markdowns na própria documentação. 
    st.markdown('Este trabalho analisa dados dos **óbitos 2019-2020**')
    #st.dataframe(obitos_2019) #essa parte me faz ter a visualização da tabela dos dados.

    opcao_1 = st.sidebar.selectbox('Selecione o tipo de doença', tipo_doenca)
    opcao_2 = st.sidebar.selectbox('Selecione o estado', estado)

    figura = grafico_comparativo(obitos_2019, obitos_2020,opcao_1,opcao_2)

    #pra renderizar a figura:
    st.pyplot(figura)


#quando eu iniciar, vou rodar a função main. 
if __name__=='__main__':
    main()
