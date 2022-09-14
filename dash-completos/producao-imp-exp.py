import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

#Grafico 1 - Producao Nacional
df_producao = pd.read_excel("datasets/ESTADOS_PETROLEO_ATUALIZADO.xlsx")


def tabela_por_estado(dataframe, estado, ano):                                                
  producao_estado = []
  mes_estado = []                                                                 
                                                                         
  for linha in range(len(dataframe)):                                                        
    if dataframe['UF'][linha] == estado:                                                     
      if dataframe['ANO'][linha] == ano:                                                     
        producao_estado.append(dataframe['PRODUCAO'][linha])
        mes_estado.append(dataframe['MES'][linha]) 
  
  
  #([549516, 65544, 98797....], [janeiro, fev, mar, abril.....])
  # foi criado um dicionario das listas criadas la em cima
  dicionario = {'PRODUÇÃO': producao_estado, 'MÊS': mes_estado}


  # foi feito um dataframe pra poder fazer o gráfico mais tarde
  tabela_final = pd.DataFrame(dicionario)

  return tabela_final



# armazenando anos e estados,
estados = []
anos = []

for linha in range(len(df_producao)):
    if df['UF'][linha] not in estados:
        estados.append(df_producao['UF'][linha])

for linha in range(len(df_producao)):
    if df_producao['ANO'][linha] not in anos:
        anos.append(df_producao['ANO'][linha])


tabela_producao = tabela_por_estado(df_producao, 'RIO DE JANEIRO', 2017) #recebe os dois valores: producao e mês

# foi criado o grafico usando o plotly. no eixo x é o mes, no eixo y é a produção 
fig = px.bar(tabela_producao, x='MÊS', y='PRODUÇÃO', title=('PRODUÇÃO DE BARRIS DE PETRÓLEO POR MÊS     ESTADO: RIO DE JANEIRO     ANO: 2017'))







#Grafico 2 - Importacao e exportacao

df_exp_imp = pd.read_excel("datasets/importacoes-exportacoes-petroleo-2000-2022_2(1).xlsx")


def lista_por_exp_imp(ano):
  exportado = []
  importado = []
  soma_exp, qtd_val_exp, soma_imp, qtd_val_imp = 0, 0, 0, 0

  #Filtrando por ano os valores.
  for linha in range(len(df_exp_imp)):
    if df_exp_imp['ANO'][linha] == ano: 
      exportado.append(df_exp_imp['VALOR_EXPORTAÇÃO'][linha])
      importado.append(df_exp_imp['VALOR_IMPORTAÇÃO'][linha])

  #realizando a média dos valores de exportação
  soma_exp = sum(exportado)
  qtd_val_exp = len(exportado)
  
  media_exp = soma_exp / qtd_val_exp

  #realizando a média dos valores de importação
  soma_imp = sum(importado)
  qtd_val_imp = len(importado)
  
  media_imp = soma_imp / qtd_val_imp

  return round(media_exp, 2), round(media_imp, 2)  #(82837.22, 183819)   #Medias com duas casas decimais   

lista_anos = []
lista_medias_exp = []
lista_medias_imp = []

for ano in range(2000, 2023):
  media_anual = 0
  media_anual = lista_por_exp_imp(ano) #realizando a media para cada ano

  lista_anos.append(ano) #adicionando os anos em uma lista
  lista_medias_exp.append(media_anual[0]) #adicionando as medias em uma lista
  lista_medias_imp.append(media_anual[1])

#criando dicionario para transformar em dataframe
medias_anuais = {'Ano': lista_anos,
                 'Média Exportação do Ano': lista_medias_exp,
                 'Média Importação do Ano': lista_medias_imp}

tabela_completa = pd.DataFrame(medias_anuais)

fig1 = px.bar(tabela_completa, x='Ano', y=['Média Exportação do Ano', 'Média Importação do Ano'], title='Quantidade Exportada/Importada em Metros Cúbicos (M³)')





#começo do dash




app = Dash(__name__)

app.layout = html.Div([
    dbc.Row([
      html.H1("Dashboard Produção Nacional, Importação e Exportação de Petróleo no Brasil."),
      html.H3("Dashboard das médias de Produção Nacional de Petróleo por ano.")
    ]),
    dbc.Row([
      dbc.Col([
        html.P("Selecione o Estado abaixo:"),
      dcc.Dropdown(estados, value="ALAGOAS", id="lista-estados"),
      dcc.Dropdown(anos, value='2017', id='anos'),

      dcc.Graph(
        id='grafico-producao',
        figure={})
      ]),
      dbc.Col([
        html.P("Selecione o Estado abaixo:"),
    
        dcc.Graph(
        id='grafico-medias',
        figure=fig1)
      ])
    ])
    
])

#Callback grafico 1 - Producao
@app.callback(
  Output('grafico-producao', 'figure'), 
  Input('lista-estados', 'value'),
  Input('anos', 'value')
)

def update_graph(lista_estados, ano):
  
  tabela_estado = tabela_por_estado(df, lista_estados, int(ano)) #recebe os dois valores: producao e mês
  
  fig = px.bar(tabela_estado, x='MÊS', y='PRODUÇÃO', title=f'Preços Médios de Revenda da Gasolina Comum em {lista_estados}.')

  return fig


if __name__ == '__main__':
    app.run_server(debug=True)