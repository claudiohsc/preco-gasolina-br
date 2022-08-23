import pandas as pd
import plotly
import plotly.express as px


def lista_por_estado(df_, estado, ano):                                                
  producao_estado = []
  mes_estado = []                                                                 
                                                                         
  for linha in range(len(df_)):                                                        
    if df_['UF'][linha] == estado:                                                     
      if df_['ANO'][linha] == ano:                                                     
        producao_estado.append(df_['PRODUCAO'][linha])
        mes_estado.append(df_['MES'][linha]) 
                                 
  return producao_estado, mes_estado   #([549516, 6544, 997], [janeiro, fev, mar, abril])


producao_e_mes = lista_por_estado(df, 'RIO DE JANEIRO', 2017) #recebe os dois valores: producao e mês

producao_por_estado = producao_e_mes[0] #recebe somente a producao
                                                                      
mes_por_estado= producao_e_mes[1] #recebe somente os meses        


# foi criado um dicionario das listas criadas la em cima
dicionario = {'PRODUÇÃO': producao_por_estado, 'MÊS': mes_por_estado}
	

# foi feito um dataframe pra poder fazer o gráfico mais tarde
df = pd.DataFrame(dicionario)
	

# foi criado o grafico usando o plotly. no eixo x é o mes, no eixo y é a produção 

px.bar(dicionario, x='MÊS', y='PRODUÇÃO', title=('PRODUÇÃO DE BARRIS DE PETRÓLEO POR MÊS     ESTADO: RIO DE JANEIRO     ANO: 2017'))
