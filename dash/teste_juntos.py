import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

#Grafico 1
preco_petroleo = pd.read_excel('datasets/Preco_do_petroleo.xlsx')

def mediaAno(dataframe, ano):
  lista_ano = []

  #Filtragem por ano dos valores 
  for linha in range(len(dataframe)):
    if dataframe['Ano'][linha] == ano:
      lista_ano.append(dataframe['Valor'][linha])

  soma_preco = sum(lista_ano)
  qtd_valores = len(lista_ano)
  
  media = soma_preco / qtd_valores
  

  return round(media, 2)   #Media com duas casas decimais           

lista_anos = []
lista_medias = []


#Criando novo dataframe com as médias de cada ano
for ano in range(2002, 2023):
  media_anual = 0
  media_anual = mediaAno(preco_petroleo, ano)

  lista_anos.append(ano) #adicionando os anos em uma lista
  lista_medias.append(media_anual) #adicionando as media em uma lista

medias_anuais = {'Ano': lista_anos,
                 'Média do Ano': lista_medias}

tabela_medias = pd.DataFrame(medias_anuais) #criando dataframe a partir do dicionario

def valoresAno(dataframe, ano):
  valores_mes = []
  lista_meses = []

  #Filtragem de um ano especifico 
  for linha in range(len(dataframe)):
    if dataframe['Ano'][linha] == ano:
      valores_mes.append(dataframe['Valor'][linha])
      lista_meses.append(dataframe['Mês'][linha])
  
  medias_mensais = {'Mês': lista_meses,
                 'Valor': valores_mes}

  tabela_anual = pd.DataFrame(medias_mensais) #criando dataframe a partir do dicionario

  return tabela_anual


fig2 = px.line(preco_petroleo, x='Mês', y='Valor', title='Média mensal do Preço do Petróleo')   #Gráfico da Média por Mês



#Grafico 2
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

fig = px.line(tabela_padrao, x='ANO', y='PREÇO MÉDIO REVENDA', title=f'Preços Médios de Revenda da Gasolina Comum em Distrito Federal.', template="plotly_dark")

lista_estados= []

#buscando todos os estados do dataframe
for linha in range(len(preco_df)):
    if preco_df['ESTADO'][linha] not in lista_estados:
        lista_estados.append(preco_df['ESTADO'][linha])



#Parte do dash: juntado os graficos

#layout funciona com linhas, e cada linha possui 12 colunas.

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
  dbc.Row([
    dbc.Col([
    html.H3("Dashboard Preço do Petróleo e da Gasolina.", className='text-center text-primary'),
    html.H5("Dashboard do preço do Petróleo e da Gasolina ao longo de 20 anos.", className='text-center text-dark')    
    ])
    
  ]),
  dbc.Row([
    dbc.Col([
        html.P("Selecione o ano abaixo:"),
        dcc.Dropdown(lista_anos, value="2002", id="lista-anos", className="mb-3"),
        dcc.Graph(id='grafico-preco',
        figure=fig2)
    

  ], width={'size': 6}),
    dbc.Col([
      html.P("Selecione o Estado abaixo:"),
      dcc.Dropdown(lista_estados, value="DISTRITO FEDERAL", id="lista-estados", className="mb-3"),

      dcc.Graph(
        id='grafico-medias',
        figure=fig)
        ], width={'size': 6})
  ])
      
])

#callback grafico 1
@app.callback(
    Output('grafico-preco', 'figure'),
    Input('lista-anos', 'value')
)


def update_graph(value):
  tabela_ano = valoresAno(preco_petroleo, int(value))

  fig2 = px.bar(tabela_ano, x='Mês', y='Valor', title=f'Média mensal do Preço do Petróleo do ano {value}', template='plotly_dark')   #Gráfico da Média por Mês

  return fig2

#callback grafico 2
@app.callback(
    Output('grafico-medias', 'figure'),
    Input('lista-estados', 'value')
)

def update_graph2(value):
  tabela_filtrada = media_geral_anual(value)

  fig = px.line(tabela_filtrada, x='ANO', y='PREÇO MÉDIO REVENDA', title=f'Preços Médios de Revenda da Gasolina Comum em {value}.', template='plotly_dark')

  return fig


if __name__ == '__main__':
    app.run_server(debug=True)