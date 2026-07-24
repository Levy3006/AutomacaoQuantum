import pandas as pd


def validar(df,cat):
    #Verificar se todas as colunas existem
    if df.shape[0] <= 15 and cat != 'INDICADORES':
        raise ValueError("Inconsistência no número de linhas do relatório (Abaixo de 15 linhas)")
        
        
    #Verificar se numero de linhas está consistente