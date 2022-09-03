import pandas as pd
import plotly
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


df = pd.read_excel("datasets/ESTADOS_PETROLEO_ATUALIZADO.xlsx")


def tabela_por_estado(df_, estado, ano):                                                
  producao_estado = []
  mes_estado = []                                                                 
                                                                         
  for linha in range(len(df_)):                                                        
    if df_['UF'][linha] == estado:                                                     
      if df_['ANO'][linha] == ano:                                                     
        producao_estado.append(df_['PRODUCAO'][linha])
        mes_estado.append(df_['MES'][linha]) 
  
  
  #([549516, 65544, 98797....], [janeiro, fev, mar, abril.....])
  # foi criado um dicionario das listas criadas la em cima
  dicionario = {'PRODUÇÃO': producao_estado, 'MÊS': mes_estado}


  # foi feito um dataframe pra poder fazer o gráfico mais tarde
  tabela_final = pd.DataFrame(dicionario)

  return tabela_final



tabela_producao = tabela_por_estado(df, 'RIO DE JANEIRO', 2017) #recebe os dois valores: producao e mês


# foi criado o grafico usando o plotly. no eixo x é o mes, no eixo y é a produção 

fig = px.bar(tabela_producao, x='MÊS', y='PRODUÇÃO', title=('PRODUÇÃO DE BARRIS DE PETRÓLEO POR MÊS     ESTADO: RIO DE JANEIRO     ANO: 2017'))



#começo do dash

estados = ["ALAGOAS", "AMAZONAS", "BAHIA", "CEARÁ", "ESPÍRITO SANTO", "PARANÁ",
 "RIO DE JANEIRO", "RIO GRANDE DO NORTE", "SÃO PAULO", "SERGIPE", "MARANHÃO"]

anos = ['2017', '2018', '2019', '2020', '2021']

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Dashboard Produção Nacional de Petróleo."),
    html.H3("Dashboard das médias de Produção Nacional de Petróleo por ano."),
    html.P("Selecione o Estado abaixo:"),
    dcc.Dropdown(estados, value="ALAGOAS", id="lista-estados"),
    dcc.Dropdown(anos, value='2017', id='anos'),

    dcc.Graph(
      id='grafico-producao',
      figure=fig
    )
])

@app.callback(
  Input('lista-estados', 'value'),   
)

def update_state(value):
  estado = value
  
  return estado

@app.callback(
  Output('grafico-producao', 'figure'), 
  Input('anos', 'value')
)

def update_graph(value):
  estado = update_state()
  tabela_estado = tabela_por_estado(df, estado, int(value)) #recebe os dois valores: producao e mês

  fig = px.line(tabela_estado, x='ANO', y='PREÇO MÉDIO REVENDA', title=f'Preços Médios de Revenda da Gasolina Comum em {value}.')

  return fig



if __name__ == '__main__':
    app.run_server(debug=True)