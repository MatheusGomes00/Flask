# Este código em Python é um exemplo de como definir e usar classes que mapeiam tabelas em um banco de dados SQLite usando o SQLAlchemy.
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, relationship
from enum import Enum

"""
A biblioteca enum em Python é usada para criar enumeradores, 
que são uma maneira de representar um conjunto de valores 
nomeados de forma mais legível e amigável. Ela fornece uma 
maneira de definir constantes ou valores fixos que não mudam 
durante a execução de um programa.
"""

# Cria uma conexão com o banco de dados SQLite
engine = create_engine('sqlite:///atividades.db')  # create_engine(mydb:/..., echo=True) --> registra no console todos os comandos SQL executados, !!não usar em produção!!

""" Cria uma sessão com o banco de dados
A sessão é uma interface para executar operações no banco de dados. 
A opção autocommit=False significa que as transações não são confirmadas 
automaticamente; você precisa confirmá-las manualmente com db_session.commit()."""
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

# Cria uma classe base para definição das tabelas
Base = declarative_base()
# Associa a sessão de banco de dados à classe base para que ela possa ser usada posteriormente para consultar o banco de dados.
Base.query = db_session.query_property()


# Define a classe "Pessoas" que mapeia a tabela 'Pessoas' no banco de dados
class Pessoas(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)  #
    idade = Column(Integer)
    """
'primary_key=True' declara a coluna como sendo a chave primária de identificação da tabela.

'index=True' cria um índice na coluna, facilitando a consulta no banco indo direto no item não 
precisando percorrer toda a coluna.
vale ressaltar que, embora os índices acelerem as operações de pesquisa, 
eles tornam as operações de gravação (como inserir novos dados ou alterar dados existentes) mais lentas, 
porque o índice também precisa ser atualizado. Portanto, é uma prática recomendada usar índices apenas 
em colunas que serão frequentemente pesquisadas e filtradas
"""

    def __repr__(self):  # representação em consultas
        return '<Pessoa {}>'.format(self.nome)

    def save(self):  # manipulação
        db_session.add(self)
        db_session.commit()

    def delete(self):  # manipulação
        db_session.delete(self)
        db_session.commit()


class StatusAtividade(Enum):
    PENDENTE = "pendente"
    CONCLUIDO = "concluído"


# Define a classe Atividades que mapeia a tabela 'atividades' no banco de dados
class Atividades(Base):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key=True)
    tarefa = Column(String(80))
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    status = Column(String(20), default=StatusAtividade.PENDENTE.value)
    pessoa = relationship("Pessoas")

    # Métodos para representar e manipular objetos
    def __repr__(self):  # representação
        return '<Pessoa {}>'.format(self.nome)

    def save(self):  # manipulação
        db_session.add(self)
        db_session.commit()

    def delete(self):  # manipulação
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)  # cria as tabelas do banco de dados


if __name__ == '__main__':
    init_db()
