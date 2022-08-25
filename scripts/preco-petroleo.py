import pandas as pd
import plotly
import plotly.express as px



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

fig1 = px.line(tabela_medias, x='Ano', y='Média do Ano', title='Média anual do Preço do Petróleo')   # Gráfico da Média do Ano
fig1.show()

fig2 = px.line(preco_petroleo, x='Mês', y='Valor', color='Ano', title='Média mensal do Preço do Petróleo')   #Gráfico da Média por Mês
fig2.show()