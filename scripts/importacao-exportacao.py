import pandas as pd
import plotly
import plotly.express as px

df = pd.read_excel("/content/drive/MyDrive/Datasets/importacoes-exportacoes-petroleo-2000-2022_2(1).xlsx")

#https://www.gov.br/anp/pt-br/centrais-de-conteudo/dados-abertos/importacoes-e-exportacoes


def lista_por_exp_imp(ano):
  exportado = []
  importado = []
  soma_exp, qtd_val_exp, soma_imp, qtd_val_imp = 0, 0, 0, 0

  #Filtrando por ano os valores.
  for linha in range(len(df)):
    if df['ANO'][linha] == ano: 
      exportado.append(df['VALOR_EXPORTAÇÃO'][linha])
      importado.append(df['VALOR_IMPORTAÇÃO'][linha])

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

px.bar(tabela_completa, x='Ano', y=['Média Exportação do Ano', 'Média Importação do Ano'], title='Quantidade Exportada/Importada em Metros Cúbicos (M³)')