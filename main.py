import pandas as pd

#Transforma o arquivo csv em um dataframe
preco_df = pd.read_csv('2004-2021.csv')


def criaTabela(nome, index):
  '''
    Função que retorna uma tabela separada do dataframe original.
  '''
  linhas = preco_df.values.tolist()
  valores = []
  nome = nome.upper().strip()

  for linha in linhas:
    valores.append([linha[int(index)]])

  tabela = pd.DataFrame(valores, columns=[nome])
  return tabela



def precoEstado(estado):
  '''
    Função que retorna o valores da tabela por Estado.
  '''
  estado = estado.upper().strip()
  
  precos_medios = []
  
  #Laço de repetição para verificar o estado e se o produto é a gasolina comum.
  for linha in range(len(preco_df)):
    if preco_df['ESTADO'][linha] == estado:
      if preco_df['PRODUTO'][linha] == 'GASOLINA COMUM':
          precos_medios.append(preco_df['PREÇO MÉDIO REVENDA'][linha]) #adiciona a linha atual depois de passar pelas condições.

  datas_finais = []

  for linha in range(len(preco_df)):
    if preco_df['ESTADO'][linha] == estado:
      if preco_df['PRODUTO'][linha] == 'GASOLINA COMUM':
        data = preco_df['DATA FINAL'][linha]
        if data.startswith("2010"):
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
  
  return print(media)


tabela_estado = precoEstado('DISTRITO FEDERAL')

print(f'A media geral: {media(tabela_estado)}')
print(tabela_estado)