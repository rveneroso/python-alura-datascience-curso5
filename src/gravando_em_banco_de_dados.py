import pandas as pd
import numpy as np
import seaborn as sns
from sqlalchemy import create_engine
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
# plt.show()

# Lista vazia que conterá os números de matrículos
todas_matriculas = []
# Gera um ndarray com 20 números aleatórios
x = np.random.rand(20)
# Calcula a probabilidade de ocorrência de um número no total (acho que é isso).
prob = x / sum(x)

# Iterage por cada linha do DataFrame
for index, row in nomes.iterrows():
  id = row.id_aluno
  matriculas = row.matriculas
  # Faz um for que vai até a quantidade de matrículas do aluno em questão.
  for i in range(matriculas):
    # Escolhe o id de um curso para associar ao aluno
    mat = [id, np.random.choice(cursos.index, p = prob)]
    # Adiciona a associação aluno / curso à lista todas_matriculas
    todas_matriculas.append(mat)

# Cria um DataFrame a partir da lista todas_matriculas
matriculas = pd.DataFrame(todas_matriculas, columns = ['id_aluno', 'id_curso'])

# Conta quantos alunos estão associados a cada um dos cursos. Para isso, o agrupamento é feito no DataFrame
# matriculas mas o join para obter o nome do curso é feito com o DataFrame cursos com base no variável
# nome_do_curso.
matriculas_por_curso = matriculas.groupby('id_curso').count().join(cursos['nome_do_curso']).rename(columns={'id_aluno':'quantidade_de_alunos'})

# engine é do tipo <class 'sqlalchemy.engine.base.Engine'>
engine = create_engine("mysql+pymysql://root:My_Sql_D4t4b4s3@localhost/python_data_science?charset=utf8mb4")

matriculas_por_curso.to_sql('matriculas', engine, if_exists='replace')

# Executando uma query no banco de dados
query = 'select * from matriculas where quantidade_de_alunos < 20'
resultado = pd.read_sql(query, engine) # Essa consulta retorna um DataFrame

# Buscando todos os registros de um tabela. A leitura abaixo também retorna um DataFrame
resultado = pd.read_sql_table('matriculas', engine, columns=['nome_do_curso', 'quantidade_de_alunos'])

# Fazendo uma consulta utilizando o método query do pandas
resultado = resultado.query('quantidade_de_alunos > 60')
resultado.to_sql('mais60alunos', con=engine, if_exists='replace')