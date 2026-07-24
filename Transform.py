
import pandas as pd
from validacaoFinal import validar
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=UserWarning, module="openpyxl")

indicador_classes = {
    "CDI":      ["RENDA FIXA", "RENDA FIXA LIQUIDEZ", "LONG AND SHORT", "MULTIMERCADO", "MULTIMERCADOS OUTROS", "FIDC"],
    "IBOVESPA": ["RENDA VARIÁVEL", "EXTERIOR"],
    "IFIX":     ["IMOBILIÁRIOS"]
}

relacao_categoria_classificacao = {
'INDICADORES'           :'Indicadores',
'RENDA FIXA'	        :'Renda Fixa LP',
'RENDA FIXA LIQUIDEZ'	:'RF Liquidez',
'LONG AND SHORT' 	    :'FIM Long Short',
'MULTIMERCADO'	        :'Multimercado',
'MULTIMERCADO EXT'	    :'Multimercado Ext',
'FIDC'	                :'FIDC',
'RENDA VARIÁVEL'	    :['Renda Variável','Ações Dividendos','Ações Livre'],   
'EXTERIOR'	            :'Exterior',
'IMOBILIÁRIOS'	        :'Imobiliários'
}
def add_categoria(relacao, cat, df):
    categoria = relacao[cat]
    if cat != "RENDA VARIÁVEL":
        df['Categoria'] = categoria
    else:
        for c in categoria:
            df.loc[df['Classificação Anbima'] == c, 'Categoria'] = c
            
        sem_categoria = df['Classificação Anbima'].isin(categoria) == False
        df.loc[sem_categoria, 'Categoria'] = 'Ações Outros'
#condicao, coluna em que o valor sera aplicado, e o valor a ser aplicado    
def concatena_bases(b1,b2):
    return pd.concat([b1,b2],ignore_index=True)

def valida_indicadores(df,cat):
    if cat == 'INDICADORES':
        try:
            set(['CDI','IBOVESPA','IFIX','105% DO CDI','ÍNDICE IPCA + 5,00%','ÍNDICE INPC + 5,25%']) in set(df['Fundo'])
           
        except ValueError:
                print("Erro: Alguns indicadores não foram localizados.")
                
def lista_e_retorna_endereço_INDICADORES():
    dirPrincipal =  Path(__file__).parent
    subdirs = [subdir for subdir in dirPrincipal.iterdir() if subdir.is_dir() and "RelatoriosTratados" in subdir.name]
    novoDirPrincipal = subdirs[0]
    arquivos = [arq for arq in novoDirPrincipal.iterdir() if "INDICADORES - " in arq.name]
    if not subdirs:
        raise FileNotFoundError("Pasta RelatoriosTratados não encontrada")
    if not arquivos:
        raise FileNotFoundError("Arquivo INDICADORES não encontrado")
    return arquivos[0]
     
def sobe_indicador_linha1(classe, df, dic):
    nome_indicador = ''
    for indicador, classes in dic.items():
        if classe in classes:
            nome_indicador = indicador
            break
        
    if not nome_indicador:
        print(f"Aviso: Classe '{classe}' não mapeada no dicionário.")
        return df

    try:
        indice_indicador = encontra_linha_por_valor(nome_indicador, df)
        linha_topo = df.loc[[indice_indicador]]
        df_sem_indicador = df.drop(indice_indicador)
        df = pd.concat([linha_topo, df_sem_indicador], ignore_index=True)
    except ValueError:  # era IndexError — semântica correta para "valor não encontrado"
        print(f"Aviso: Indicador '{nome_indicador}' não foi localizado nesta planilha.")
        
    return df

def encontra_linha_por_valor(texto, df):
    condicao_texto = df.iloc[:, 0].astype(str).str.contains(texto, na=False, regex=False)  # regex=False evita quebra com caracteres especiais
    
    resultado = df[condicao_texto]
    if resultado.empty:
        raise ValueError(f"Texto '{texto}' não encontrado na primeira coluna.")  # era IndexError
        
    return resultado.index[0]

def nomeResumido(cat,df):
        if cat !='INDICADORES':
            df['Ativo'] =  df['Fundo'].str.split().str[:4].str.join(' ')
            
def transform_sheet(sheet_name, final_sheet_name, dat, cat,pastaGPT):
    
    print("Iniciando Tratamento ...")
    print(f"Processando categoria: {cat}")#{str(cat).upper()}")
    df = pd.read_excel(sheet_name)
    df[df.columns[0]] = df[df.columns[0]].str.upper()
    
    df = df.rename(columns={
        'Nome': 'Fundo',
        'Retorno': 'Retorno 12 Meses', 
        'Unnamed: 18': 'Retorno 24 Meses', 
        'Unnamed: 19': 'Retorno 36 Meses', 
        'Sharpe - CDI': 'Sharpe 12 Meses', 
        'Unnamed: 21': 'Sharpe 24 Meses',
        'Unnamed: 22': 'Sharpe 36 Meses'
    })
    
    df = df.drop([0, 1]).reset_index(drop=True)
    
    # Removendo texto ao final da planilha com tratamento de erro nativo
    texto_remover = "AS INFORMAÇÕES FORAM OBTIDAS"
    try:
        idx_remover = encontra_linha_por_valor(texto_remover, df)
        df = df.iloc[:idx_remover] # Uso do .iloc garante fatiamento estrito por posição
    except IndexError:
        print("Aviso: Texto de rodapé não encontrado. Nenhuma linha deletada ao final.")
    
    valida_indicadores(df,cat)
    # =========== Tratamento de Numéricos ===============
    add_categoria(relacao_categoria_classificacao,cat,df)
    
    #Addiociona nome resumido do fundo a uma nova coluna
    nomeResumido(cat,df)
    
    colunas_percentuais = ['Sharpe 36 Meses', 'Sharpe 24 Meses', 'Sharpe 12 Meses', 'Retorno 12 Meses',
                           'Retorno 24 Meses', 'Retorno 36 Meses', 'Patrimônio Líquido', 'Número de Cotistas']
        
    df[colunas_percentuais] = df[colunas_percentuais].apply(pd.to_numeric, errors='coerce')
    
    # Tratamento de Datas (errors='coerce' evita quebras se houver strings residuais inválidas)
    df['Início do Fundo']  = pd.to_datetime(df['Início do Fundo'], errors='coerce').dt.strftime('%d/%m/%Y')
    df['Data de Registro'] = pd.to_datetime(df['Data de Registro'], errors='coerce').dt.strftime('%d/%m/%Y')
    
    if cat != "INDICADORES":
        df = concatena_bases(pd.read_excel(lista_e_retorna_endereço_INDICADORES()),df)
        df['Posição'] = df['Posição'] = str(dat)[:2] + "/" + str(dat)[2:4] + "/" + str(dat)[4:]
    if cat != 'RENDA VARIÁVEL' and cat != 'INDICADORES':
        df = df.drop(columns = ['Retorno 36 Meses','Sharpe 36 Meses'])
    try:
    # Move o indicador para a primeira linha de forma limpa
        df = sobe_indicador_linha1(cat, df, indicador_classes)
             
    except Exception as e:
        print(f"Erro ao subir indicador para 1º Linha: {e}")
    try:
        validar(df,cat)
    except Exception as e:
        print(f"Erro de validação ( Motivo provável: linhas insuficientes ): {e}")
        raise
    df = df.dropna(subset=['Fundo', 'CNPJ'], how='all')    
    nome = f"{final_sheet_name} - {dat}.xlsx"
    df.to_excel(nome, index=False)
    print(f"Salvo com sucesso: {str(nome).split("\\")[-1]}")
    #if cat != "INDICADORES":
    pasta_destino = Path(r'Z:\APLICAÇÕES GERIN\Automação Quantum\RelatoriosGPT') / dat
    if not pasta_destino.is_dir():
        pasta_destino.mkdir(parents=True, exist_ok=True)
    nomegpt = f"Dados_Fundos {cat}.xlsx"
    pastaGPT = Path(pastaGPT) 
    
    df.to_excel(pasta_destino / nomegpt,index=False)
    print(f"Salvo com sucesso: {nomegpt}")
    return df