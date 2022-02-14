import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
np.random.seed(123)

# Importando arquivos com nomes masculinos e femininos
nomes_f = pd.read_json('https://guilhermeonrails.github.io/nomes_ibge/nomes-f.json') # DataFrame
nomes_m = pd.read_json('https://guilhermeonrails.github.io/nomes_ibge/nomes-m.json') # DataFrame

# Une os DataFrames nomes_f e nomes_m em uma única coleção. O tipo do objeto resultado é List
frames = [nomes_f, nomes_m]

# Criando um DataFrame contendo apenas o nome dos 2 DataFrames originais
nomes = pd.concat(frames)['nome'].to_frame()
total_alunos = len(nomes)

# Cria o atributo id_aluno e atribui, para cada aluno, um id aleatório.
nomes['id_aluno'] = np.random.permutation(total_alunos) + 1

# Cria uma lista de domínios fictícios a serem usados na criação de email dos alunos
dominios = ['@dominiodoemmail.com.br', '@servicodoemail.com']
# Cria a variável 'domínio' no DataFrame que será preenchida de forma aleatória com um dos dois possíveis
# valores de domínio presentes na lista criada acima.
nomes['dominio'] = np.random.choice(dominios, total_alunos)
# Cria mais uma variável no DataFrame. A nova variável se chama 'email' e seu valor será a concatenação
# do nome do aluno em letras minúsculas com o valor da variável 'domínio' criada na etapa anterior.
nomes['email'] = nomes.nome.str.cat(nomes.dominio).str.lower()

url = 'http://tabela-cursos.herokuapp.com/index.html'
cursos = pd.read_html(url) # Retorna uma lista
cursos = cursos[0] # Converte de list para DataFrame

# Os nomes das colunas no DataFrame estarão como definidos na página html. Assim, vamos renomear 'Nome do curso'
# para nome_do_curso
cursos.rename(columns={'Nome do curso' : 'nome_do_curso'}, inplace=True)

# Criando a variável id para os cursos
cursos['id'] = cursos.index + 1

# Gera quantidades aleatórias de matrículos para os alunos. No comando abaixo:
# random.exponential: gera números aleatórios com crescimento exponencial.
# np.ceil: não permite que seja gerado um valor zero.
# a multiplicação por 1.5 é para gerar um número ainda maior de matrículas
nomes['matriculas'] = np.ceil(np.random.exponential(size=total_alunos) * 1.5).astype(int)

# Gera um histograma da distribuição da quantidade de matrículas
sns.distplot(nomes.matriculas)
plt.show()

# Apresentando as quantidades exatas de números de matrículas
print(nomes.matriculas.value_counts())
