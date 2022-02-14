import pandas as pd

# Importando arquivos com nomes masculinos e femininos
nomes_f = pd.read_json('https://guilhermeonrails.github.io/nomes_ibge/nomes-f.json') # DataFrame
nomes_m = pd.read_json('https://guilhermeonrails.github.io/nomes_ibge/nomes-m.json') # DataFrame

# Gera uma amostra de nomes dentro do conjunto baixado
print(nomes_f.sample(10))

# Une os DataFrames nomes_f e nomes_m em uma única coleção. O tipo do objeto resultado é List
frames = [nomes_f, nomes_m]

# Criando um DataFrame contendo apenas o nome dos 2 DataFrames originais
nomes = pd.concat(frames)['nome'].to_frame()
print(type(nomes))
