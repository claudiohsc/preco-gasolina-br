import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

preco_df = pd.read_csv('datasets/2004-2021.csv')

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
        if data[:4] == str(ano):   #comparando data com o ano
          precos_medios.append(preco_df['PREÇO MÉDIO REVENDA'][linha]) #adiciona o preço atual depois de passar pelas condições.
          datas_finais.append(preco_df['DATA FINAL'][linha]) #adiciona a data atual depois de passar pelas condições.
          

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
    soma_preco += dataframe['PREÇO MÉDIO REVENDA'][linha] #soma_preço = soma_preço + dataframe['PREÇO MÉDIO REVENDA'][linha]
    qtd_valores += 1
    
  media = soma_preco / qtd_valores
  
  return media


def media_geral_anual(estado):
  #criando listas para armezenar os anos e as médias
  lista_de_anos = []
  lista_de_medias = []

  for ano in range(2004, 2022):
    media_anual = 0
    df_estado = precoEstado(estado, ano) #Cria a tabela de acordo com o ano e o Estado.
    media_anual = media(df_estado)

    lista_de_anos.append(ano) #adiciona os anos em uma lista.
    lista_de_medias.append(media_anual) #adiciona as medias em uma lista.

  medias_por_ano = {'ANO': lista_de_anos,
                  'PREÇO MÉDIO REVENDA': lista_de_medias}

  tabela_completa = pd.DataFrame(medias_por_ano) #cria um dataframe a partir do dicionario.

  return tabela_completa

tabela_padrao = media_geral_anual('DISTRITO FEDERAL')

fig = px.line(tabela_padrao, x='ANO', y='PREÇO MÉDIO REVENDA', title=f'Preços Médios de Revenda da Gasolina Comum em Distrito Federal.')

lista_estados = ['ACRE', 'ALAGOAS', 'AMAPA', 'AMAZONAS', 'BAHIA', 'CEARA','DISTRITO FEDERAL', 'ESPIRITO SANTO',
'GOIAS', 'MARANHAO', 'MATO GROSSO', 'MATO GROSSO DO SUL', 'MINAS GERAIS', 'PARA', 'PARAIBA', 'PARANA', 
'PERNAMBUCO', 'PIAUI', 'RIO DE JANEIRO', 'RIO GRANDE DO NORTE', 'RIO GRANDE DO SUL', 'RONDONIA', 'RORAIMA', 'SANTA CATARINA', 'SAO PAULO', 'SERGIPE', 'TOCANTINS']

#Parte dashboard

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Gasolina no Brasil."),
    html.H3("Dashboard das médias dos preços da gasolina por Estado."),
    html.P("Selecione o Estado abaixo:"),
    dcc.Dropdown(lista_estados, value="DISTRITO FEDERAL", id="lista-estados"),

    dcc.Graph(
      id='grafico-medias',
      figure=fig
    )
])


@app.callback(
    Output('grafico-medias', 'figure'),
    Input('lista-estados', 'value')
)

def update_graph(value):
  tabela_filtrada = media_geral_anual(value)

  fig = px.line(tabela_filtrada, x='ANO', y='PREÇO MÉDIO REVENDA', title=f'Preços Médios de Revenda da Gasolina Comum em {value}.')

  return fig


if __name__ == '__main__':
    app.run_server(debug=True)