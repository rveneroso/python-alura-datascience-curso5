import html5lib
import lxml
import pandas as pd

url = 'http://tabela-cursos.herokuapp.com/index.html'
cursos = pd.read_html(url) # Retorna uma lista
cursos = cursos[0] # Converte de list para DataFrame

# Os nomes das colunas no DataFrame estarão como definidos na página html. Assim, vamos renomear 'Nome do curso'
# para nome_do_curso
cursos.rename(columns={'Nome do curso' : 'nome_do_curso'}, inplace=True)

# Criando a variável id para os cursos
cursos['id'] = cursos.index + 1

# Define que o DataFrame cursos será indexado pelo id e não mais pelo index original
cursos = cursos.set_index('id')
print(cursos)

