import plotly.express as px
import plotly.graph_objects as go

import numpy as np
import pandas as pd
import json


#Leitura da Base de Dados
dataFrame = pd.read_csv("/content/drive/MyDrive/Datasets/Gasolina por estado.csv",sep=";")

#Leitura Da base de Dados das localizações
estados_brasil = json.load(open("/content/drive/MyDrive/Datasets/brazil_geo.json", "r"))

#https://www.kaggle.com/code/jribeiro09/gas-prices-in-brazil-data-analysis/notebook

#Lista de Todos os Estados do Brasil
estadosSiglas = ['AC','AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']


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


#Alocando valores de preço na lista respectiva de seu estado
for contador in range(len(lista)):
    for linha in range(len(dataFrame)):
        if dataFrame['ESTADO'] [linha] == estadosSiglas[contador]:
            lista[contador].append(dataFrame['PREÇO MÉDIO REVENDA'] [linha])

precos = []

#calculo das medias de preço
for i in range(len(lista)):
    soma = sum(lista[i])
    divisor = len(lista[i])
    media = soma/divisor
    precos.append(media)

#criando dicinario

dicionario = {
    'ESTADO': estadosSiglas,
    'MEDIA DE PREÇOS': precos
}

#criando dataFrame com o dicionario
dataFrameMedia = pd.DataFrame(dicionario)

#Criação do grafico de mapa
fig = px.choropleth_mapbox(dataFrameMedia, locations="ESTADO",
                        center={"lat": -16.95, "lon": -47.78}, zoom = 3, color="MEDIA DE PREÇOS",
                        geojson=estados_brasil,color_continuous_scale="Redor", opacity=0.4,
                        hover_data={"MEDIA DE PREÇOS": True,"ESTADO": True})  

#Parte visual do mapa 
fig.update_layout(
    paper_bgcolor ="#242424",
    autosize = True,
    margin = go.Margin(l=0, r = 0, t = 0, b =0),
    showlegend = False,
    mapbox_style="carto-darkmatter"
)

