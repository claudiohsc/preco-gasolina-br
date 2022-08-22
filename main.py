import pandas as pd
import plotly
import plotly.express as px

preco_df = pd.read_csv('2004-2021.csv')


def precoEstado(estado, ano):
  '''
    Função que retorna o valores da tabela de um Estado.
  '''

  estado = estado.upper().strip() #Elimina os espaços e coloca tudo em maiúsculo.
  precos_medios = []
  datas_finais = []
  
  #Laço de repetição para verificar o estado, se o produto é a gasolina comum e se a data é igual ao ano passado.
  for linha in range(len(preco_df)):
    if preco_df['ESTADO'][linha] == estado:
      if preco_df['PRODUTO'][linha] == 'GASOLINA COMUM':
        data = preco_df['DATA FINAL'][linha]
        if data[:4] == str(ano): 
          precos_medios.append(preco_df['PREÇO MÉDIO REVENDA'][linha]) #adiciona a linha atual depois de passar pelas condições.
          datas_finais.append(preco_df['DATA FINAL'][linha])
          

  #Cria um dicionario com todos os valores das listas.
  valores_estado = {'DATA': datas_finais,
                   'PREÇO MÉDIO REVENDA': precos_medios}

  #Transforma o dicionario em um Data Frame.
  tabela_estado = pd.DataFrame(valores_estado)
  return tabela_estado
  

def media(dataframe):
  qtd_valores = 0
  soma_preco = 0

  for linha in range(len(dataframe)):
    soma_preco += dataframe['PREÇO MÉDIO REVENDA'][linha]
    qtd_valores += 1
    
  media = soma_preco / qtd_valores
  
  return media

#criando listas para armezenar os anos e as médias
lista_de_anos = []
lista_de_medias = []

for ano in range(2004, 2022):
  media_anual = 0
  df_estado = precoEstado('DISTRITO FEDERAL', ano) #Cria a tabela de acordo com o ano e o Estado.
  media_anual = media(df_estado)

  lista_de_anos.append(ano) #adiciona os anos em uma lista.
  lista_de_medias.append(media_anual) #adiciona as medias em uma lista.

medias_por_ano = {'ANO': lista_de_anos,
                 'PREÇO MÉDIO REVENDA': lista_de_medias}

tabela_completa = pd.DataFrame(medias_por_ano) #cria um dataframe a partir do dicionario.


fig = px.line(tabela_completa, x='ANO', y='PREÇO MÉDIO REVENDA', title='Preços Médios de Revenda da Gasolina Comum no Distrito Federal.')
fig.show()