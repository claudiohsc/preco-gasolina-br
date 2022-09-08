import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


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

fig1 = px.line(tabela_medias, x='Ano', y='Média do Ano', title='Média anual do Preço do Petróleo')   # Gráfico da Média do Ano


fig2 = px.line(preco_petroleo, x='Mês', y='Valor', title='Média mensal do Preço do Petróleo')   #Gráfico da Média por Mês


app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div([
  dbc.Row([
    dbc.Col([
    html.H3("Dashboard Preço do Petróleo.", className='text-center text-primary'),
    html.H5("Dashboard do preço do Petróleo ao longo de 20 anos."),
    html.P("Selecione o ano abaixo:")
    ])
    
  ]),
  dbc.Row([
    dbc.Col([
      dcc.Dropdown(lista_anos, value="2002", id="lista-anos"),
      dcc.Graph(id='grafico-preco',
      figure=fig2)
    

  ], width={'size': 6}),
  dbc.Row([
    
    ])
  ])
    
])


@app.callback(
    Output('grafico-preco', 'figure'),
    Input('lista-anos', 'value')
)


def update_graph(value):
  tabela_ano = valoresAno(preco_petroleo, int(value))

  fig2 = px.bar(tabela_ano, x='Mês', y='Valor', title=f'Média mensal do Preço do Petróleo do ano {value}', template='plotly_dark')   #Gráfico da Média por Mês

  return fig2


if __name__ == '__main__':
    app.run_server(debug=True)