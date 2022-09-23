#Importação das Bibliotecas
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json

#Leitura da Base de Dados
dataFrame = pd.read_csv("precosGasolina.csv",sep=";")

#Leitura Da base de Dados das localizações
estados_brasil = json.load(open("brazil_geo.json", "r"))

#https://www.kaggle.com/code/jribeiro09/gas-prices-in-brazil-data-analysis/notebook

##Inserir codigo do Mapa


#Lista de Todos os Estados do Brasil
estadosSiglas = []

for linha in range(len(dataFrame)):
    if dataFrame['ESTADO'][linha] not in estadosSiglas:
        estadosSiglas.append(dataFrame['ESTADO'][linha])



#Lista para Cada Estado Do Brasil
AC = []
AL = []
AP = []
AM = []
BA = []
CE = []
DF = []
ES = []
GO = []
MA = []
MT = []
MS = []
MG = []
PA = []
PB = []
PR = []
PE = []
PI = []
RJ = []
RN = []
RS = []
RO = []
RR = []
SC = []
SP = []
SE = []
TO = []


#Lista contendo todas as litas de estados
lista = [AC,AL,AP,AM,BA,CE,DF,ES,GO,MA,MT,MS,MG,PA,PB,PR,PE,PI,RJ,RN,RS,RO,RR,SC,SP,SE,TO]

precos = []




#Alocando valores de preço na lista respectiva de seu estado


def leitura(ano):
    for contador in range(len(lista)):
        for linha in range(len(dataFrame)):
           if dataFrame['ESTADO'] [linha] == estadosSiglas[contador] and dataFrame['ANO'] [linha] == ano:
                lista[contador].append(dataFrame['PREÇO'] [linha])


def mediatotal(ano):
    for i in range(len(lista)):
      soma = sum(lista[i])
      divisor = len(lista[i])
      media = soma/divisor
      precos.append(media)


    for z in range(len(precos)):
        precos[z] =  float("%.2f" % precos[z])


    dicionario = {
        'ESTADO': estadosSiglas,
        'MEDIA DE PREÇOS': precos,
        'ANO' : ano
    }


    dataFrameMedia = pd.DataFrame(dicionario)
    global dataFrameFinal 
    dataFrameFinal = dataFrameMedia

   


def clear():
    for i in range(len(lista)):
        lista[i].clear()
    precos.clear()







app = dash.Dash(__name__,external_stylesheets=[dbc.themes.CYBORG])

leitura(2004)
mediatotal(2004)

fig = px.choropleth_mapbox(dataFrameFinal, locations="ESTADO",
                        center={"lat": -16.95, "lon": -47.78}, zoom = 3, color="MEDIA DE PREÇOS",
                        geojson=estados_brasil,color_continuous_scale="Redor", opacity=0.4,
                        hover_data={"MEDIA DE PREÇOS": True,"ESTADO": True}) 

fig.update_layout(
    paper_bgcolor ="#242424",
    autosize = True,
    margin = dict(l = 0, r = 0, t = 0, b = 0),
    showlegend = False,
    mapbox_style="carto-darkmatter"
)


opcoes = []

for linha in range(len(dataFrame)):
    if dataFrame['ANO'][linha] not in opcoes:
        opcoes.append(dataFrame['ANO'][linha])



app.layout = dbc.Container(
    dbc.Row([


        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.H4("Preço Médio Anual da Gasolina",style={}),
        	            html.P("Selecione a Data Desejada",style={}),
                        dcc.Dropdown(opcoes, value = '2004', id = 'botao', style = {"color": "#121212"})
                    ],style={}),         
                ])   
            ],color = "light", inverse= True)
        ],md=4,style={"padding": "25px", "background-color":"#121212"}),


         dbc.Col([
            dcc.Graph(id = 'mapa',
                figure = fig,
                style={"height": "100vh"}
            
            )
        ],md = 8)

    ],class_name='g-0')
    
,fluid = True)




clear()
@app.callback(
    Output('mapa', 'figure'),
    Input('botao','value')
)

def update(value):
    ano = value
    
    leitura(ano)
    mediatotal(ano)
    


    fig = px.choropleth_mapbox(dataFrameFinal, locations="ESTADO",
                        center={"lat": -16.95, "lon": -47.78}, zoom = 3, color="MEDIA DE PREÇOS",
                        geojson=estados_brasil,color_continuous_scale="Redor", opacity=0.4,
                        hover_data={"MEDIA DE PREÇOS": True,"ESTADO": True}) 

    fig.update_layout(
    paper_bgcolor ="#242424",
    autosize = True,
    margin = dict(l = 0, r = 0, t = 0, b = 0),
    showlegend = False,
    mapbox_style="carto-darkmatter")

    clear()
    return fig
    

if __name__ == "__main__":
    app.run_server(debug=True, port=8052)

