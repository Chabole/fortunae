import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import concurrent.futures 
import json
from tqdm.contrib import tzip
from tqdm.contrib.concurrent import thread_map


'''
Created on Tue  30 Jan 10:34:42 2022
@author: Arthur Chabole

contact: arthur.chabole@unesp.br
contact: chabole.arthur@gmail.com

__version__0.0.9
__Release__25/03/2022

'''

def __connection_stocks(ATIVO):
    try:
        if '34' in ATIVO: #BDRs
            url = f'https://statusinvest.com.br/bdrs/{ATIVO}'
        else: #ações em geral
            url = f'https://statusinvest.com.br/acoes/{ATIVO}'
        html = requests.get(url)
    except:
        pass
    return html

def __connection_FIIs(ATIVO):
    try:
        url = f'https://statusinvest.com.br/fundos-imobiliarios/{ATIVO}'
        html = requests.get(url)
    except:
        pass
    return html

def full_word(x):
    if x == '-' or x == '-%' or x==' -':    
        x = str(x.replace("-","NaN"))
    return x

def Beatifulfy_data(tabela_df):
        
    #Tratando os valores para floats
    for coluna in range(len(tabela_df.columns)):
        index = tabela_df.columns[coluna]
        
        try:            
            tabela_df[index] = tabela_df[index].apply(lambda x: (full_word(x)))
        except:
            pass
        
        try:            
            tabela_df[index] = tabela_df[index].apply(lambda x: (x.replace("%","")))
        except:
            pass
        
        try:
            tabela_df[index] = tabela_df[index].apply(lambda x: (x.replace(".","")))    
        except:
            pass
        
        try:
            tabela_df[index] = tabela_df[index].apply(lambda x: (x.replace(",",".")))    
        except:
            pass
    
        try:
            tabela_df[index] = tabela_df[index].astype(float)
        except:
            pass
    
    tabela_df = tabela_df.fillna(0)
    return tabela_df

def __format_num(num):
    try:
        num = num.replace('.', '')
    except:
        pass
    try:
        num = num.replace(',', '.')
    except:
        pass
    try:
        num = num.replace('%', '')
    except:
        pass
    try:
        num = num.replace('-%', '0')
    except:
        pass
    try:
        num = num.replace('-', '0')
    except:
        pass
    try:
        return float(num)
    except:
        return num

def __search_stocks(html, ATIVO):
    sopa = bs(html.text, 'html.parser')
    #Coletando dados de preço e adicionais
    dic = {}
    dic['Ativo'] = ATIVO.upper()

    #segmentação
    new_conjunto = sopa.find_all(attrs={"card bg-main-gd-h white-text rounded ov-hidden pt-0 pb-0"}) 
    for bloco in new_conjunto:
        indicadores = bloco.find_all(attrs={"sub-value"}) 
        valores = bloco.find_all(attrs={"value"})
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = (valor.text)

    new_conjunto = sopa.find_all(attrs={"info"}) #cada indicador
    for bloco in new_conjunto:
        indicadores = bloco.find_all(attrs={"title m-0"}) #nome do indicador
        valores = bloco.find_all(attrs={"value"})
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = (valor.text)
            #dic[indicador.text] = __format_num(valor.text)

    #Coletando dados indicadores fundamentalistas
    conjunto = sopa.find_all(attrs={"w-50 w-sm-33 w-md-25 w-lg-16_6 mb-2 mt-2 item"})
    for bloco in conjunto:
        indicadores = bloco.find_all(attrs={"title m-0 uppercase"}, limit=30) #nome do indicador
        valores = bloco.find_all(attrs={"value d-block lh-4 fs-4 fw-700"}) #valor do indicador 
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = (valor.text)

    #Coletando dados indicadores fundamentalistas
    conjunto = sopa.find_all(attrs={"w-50 w-sm-33 w-md-25 w-lg-50 mb-2 mt-2 item"}) 
    for bloco in conjunto:
        indicadores = bloco.find_all(attrs={"title m-0 uppercase"}, limit=150) #nome do indicador
        valores = bloco.find_all(attrs={"value d-block lh-4 fs-4 fw-700"}) #valor do indicador 
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = (valor.text)
    return dic

def __search_FIIs(html, ATIVO):
    sopa = bs(html.text, 'html.parser')
    conjunto = sopa.find_all(attrs={"info"})  #cada indicador
    #conjunto = html.find_all(attrs={"info"}) #cada indicador
    dic = {}
    dic['Ativo'] = ATIVO.upper()
    for bloco in conjunto:
        indicadores = bloco.find_all(attrs={"title m-0"}) #nome do indicador
        valores = bloco.find_all(attrs={"value"})         
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = (valor.text)
    return dic

def __get_json(path):

    # Opening JSON file
    file = open(path)

    # returns JSON object as
    data = json.load(file) # a dictionary

    tabela=[]
    for i in data:
        tabela.append(data[i])

    # Closing file
    file.close()
    return pd.DataFrame(tabela, columns=["Ativos"])

def get_stocks(ativos):
    '''
    Carrega os dados financeiros de ações no brasil e BDR's .
    
    Parameters
    -----------
    ativos: list or str 
        Lista ou string com o código do fundos imobiliarios para buscar. Ex: 'mglu3'
    
    Example
    -----------
    >>> import fortunae as ft
    >>> import pandas as pd

    Ver lista de ações internas

    >>> ações_lista = ft.br_stocks()
    
    Procurar dados financeiros da lista de ações

    >>> df_ações = ft.get_stocks(ações_lista)

    Gravando dados em um excel

    >>> df_ações.to_excel('exemplo.xlsx')
    '''
    tabela = []     
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = thread_map(__connection_stocks, ativos)

        for result, ativo in tzip(results, ativos):
            tabela.append(__search_stocks(result, ativo))

    df = Beatifulfy_data(pd.DataFrame(tabela))
    return df

def get_fiis(ativos):
    '''
    Carrega os dados financeiros de fundos imobiliarios.
    
    Parameters
    -----------
    ativos: list or str 
        Lista ou string com o código do fundos imobiliarios para buscar. Ex: 'hglg11'
    
    Example
    -----------
    >>> import fortunae as ft
    >>> import pandas as pd

    Ver lista de ações internas

    >>> fiis_lista = ft.br_fiis()
    
    Procurar dados financeiros da lista de ações

    >>> df_fiis = ft.get_FIIS(fiis_lista)

    Gravando dados em um excel

    >>> df_fiis.to_excel('exemplo.xlsx')
    '''
    tabela = []     
    with concurrent.futures.ThreadPoolExecutor() as executor:
        #results = executor.map(__connection_FIIs, ativos)
        results = thread_map(__connection_FIIs, ativos)

        for result, ativo in tzip(results, ativos):
            tabela.append(__search_FIIs(result, ativo))

    df = Beatifulfy_data(pd.DataFrame(tabela))
    return df

def br_stocks():
    return __get_json('codigos_acoes.json').iloc[0:]['Ativos']

def br_fiis():
    return __get_json('codigos_fiis.json').iloc[0:]['Ativos']

# ----------------- EXEMPLO DE UTILIZAÇÃO ---------------

'''#import fortunae as ft
import pandas as pd
import time 

start = time.time()

#Pegando a lista de ações
ações = br_stocks() #473 ações
fiis = br_fiis()    #250 fundos

#Scraping dados dos ativos usando mult-threads
df_ações = get_stocks(ações)
df_fiis = get_fiis(fiis)

#Gravando os resultados
with pd.ExcelWriter('D:/outputs_final.xlsx') as writer:  
    df_ações.to_excel(writer, sheet_name='acoes')
    df_fiis.to_excel(writer, sheet_name='FIIs')
    
print(f'Tempo de processamento gasto {(time.time() - start):.3f}s')
'''
# ---------------------------------------------------------