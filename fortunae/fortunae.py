import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import concurrent.futures 
import json

'''
Created on Tue  30 Jan 10:34:42 2022
@author: Arthur Chabole

contact: arthur.chabole@unesp.br
contact: chabole.arthur@gmail.com

__version__0.0.5
__Release__31/01/2022

'''

def __connection_stocks(ATIVO):
    try:
        url = f'https://statusinvest.com.br/acoes/{ATIVO}'
        html = requests.get(url)
        print(f'Sucesso no download: ativo {ATIVO.upper()}')
    except:
        print(f'Erro no download: ativo {ATIVO.upper()}')
    return html

def __connection_FIIs(ATIVO):
    try:
        url = f'https://statusinvest.com.br/fundos-imobiliarios/{ATIVO}'
        html = requests.get(url)
        print(f'Sucesso no download: ativo {ATIVO.upper()}')
    except:
        print(f'Erro no download: ativo {ATIVO.upper()}')
    return html

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
    new_conjunto = sopa.find_all(attrs={"info"}) #cada indicador
    dic = {}
    dic['Ativo'] = ATIVO.upper()
    for bloco in new_conjunto:
        indicadores = bloco.find_all(attrs={"title m-0"}) #nome do indicador
        valores = bloco.find_all(attrs={"value"})
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = __format_num(valor.text)

    #Coletando dados indicadores fundamentalistas
    conjunto = sopa.find_all(attrs={"w-50 w-sm-33 w-md-25 w-lg-16_6 mb-2 mt-2 item"})
    
    for bloco in conjunto:
        indicadores = bloco.find_all(attrs={"title m-0 uppercase"}, limit=30) #nome do indicador
        valores = bloco.find_all(attrs={"value d-block lh-4 fs-4 fw-700"}) #valor do indicador 
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = __format_num(valor.text)
    return dic

def __search_FIIs(html, ATIVO):
    sopa = bs(html.text, 'html.parser')
    conjunto = sopa.find_all(attrs={"info"}) #cada indicador
    dic = {}
    dic['Ativo'] = ATIVO.upper()
    for bloco in conjunto:
        indicadores = bloco.find_all(attrs={"title m-0"}) #nome do indicador
        valores = bloco.find_all(attrs={"value"})         
        for valor, indicador in zip(valores, indicadores):
            dic[indicador.text] = __format_num(valor.text)
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
    Carrega os dados financeiros de ações.
    
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
        results = executor.map(__connection_stocks, ativos)

        for result, ativo in zip(results, ativos):
            tabela.append(__search_stocks(result, ativo))
    return pd.DataFrame(tabela)

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
        results = executor.map(__connection_FIIs, ativos)

        for result, ativo in zip(results, ativos):
            tabela.append(__search_FIIs(result, ativo))
    return pd.DataFrame(tabela)

def br_stocks():
    return __get_json('codigos_acoes.json').iloc[0:]['Ativos']

def br_fiis():
    return __get_json('codigos_fiis.json').iloc[0:]['Ativos']

# ----------------- EXEMPLO DE UTILIZAÇÃO ---------------
'''
import fortunae as ft
import pandas as pd
import time 

start = time.time()

#Pegando a lista de ações
ações = ft.br_stocks() #473 ações
fiis = ft.br_fiis()    #250 fundos

#Scraping dados usando threads
df_ações = ft.get_stocks(ações)
df_fiis = ft.get_fiis(fiis)

#Gravando os resultados
with pd.ExcelWriter('outputs.xlsx') as writer:  
    df_ações.to_excel(writer, sheet_name='acoes')
    df_fiis.to_excel(writer, sheet_name='FIIs')
    
print(f'Tempo de processamento gasto {(time.time() - start):.3f}s')
'''
# ---------------------------------------------------------