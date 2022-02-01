# fortunae
 Fortunae quer ser tornar uma biblioteca de análise financeira. Voltada pra importação de indicadores fundamentalistas de ações ou fundos imobiliarios usando multithreading. Usando a biblioteca `current.future` e `threads` para acelerar a coleta de dados automatizada e massiva.

## Download

Computer Version:

[![Windows](https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/seu-usuario/seu-repositorio/releases)
[![Linux](https://img.shields.io/badge/Linux-FF6600?style=for-the-badge&logo=linux&logoColor=white)](https://github.com/seu-usuario/seu-repositorio/releases)
[![Mac OS](https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=macos&logoColor=F0F0F0)](https://github.com/seu-usuario/seu-repositorio/releases)

## Instalação

Você pode instalar fortunae via `pip`

```md
pip install fortunae
```
## Extraindo dados de ações
Verificando indicadores fundamentalistas de ações

```python
import fortunae as ft

ações = ['mglu3', 'bbas3', 'cash3']
df_ações = ft.get_stocks(ações)
```
O `df_ações` será um dataframe com os ativos e seus indicadores.

## Extraindo dados de fundos imobiliarios

Verificando indicadores fundamentalistas de fundos imobiliarios.

```python
import fortunae as ft

fiis = ['hglg11', 'knri11', 'bcff11']
df_fiis = ft.get_fiis(fiis)
```
O `df_fiis` será um dataframe com os ativos e seus indicadores.

## Verificando lista de ativos
Verificando lista de ações
```python
import fortunae as ft

ações_lista = ft.br_stocks()
```
Verificando lista de fundos imobiliarios
```python
import fortunae as ft

ações_lista = ft.br_fiis()
```

### Support Ou Contato

[![Instagram Badge](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/arthurchabole/)
[![Twitter Badge](https://img.shields.io/badge/Twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/Arthur__Chabole)
[![Linkedin](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/arthur-chabole-1589a8149/)
