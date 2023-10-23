# classes que vão referenciar as tabelas do banco de dados
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, relationship

# O engine é para ser apenas a ponte de conexão entre o Python e o banco.
engine = create_engine('sqlite:///atividades.db')  # create_engine(mydb:/..., echo=True) --> registra no console todos os comandos SQL executados, !!não usar em produção!!
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Pessoas(Base):
    __tablename__ = 'pessoas'
    id = Column(Integer, primary_key=True)
    nome = Column(String(40), index=True)
    idade = Column(Integer)

    def __repr__(self):  # forma de representar o objeto ao fazer chamadas
        return '<Pessoa {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


class Atividades(Base):
    __tablename__ = 'atividades'
    id = Column(Integer, primary_key=True)
    nome = Column(String(80))
    pessoa_id = Column(Integer, ForeignKey('pessoas.id'))
    pessoa = relationship("Pessoas")

    def __repr__(self):  # forma de representar o objeto ao fazer chamadas
        return '<Pessoa {}>'.format(self.nome)

    def save(self):
        db_session.add(self)
        db_session.commit()

    def delete(self):
        db_session.delete(self)
        db_session.commit()


def init_db():
    Base.metadata.create_all(bind=engine)  # cria o banco de dados


if __name__ == '__main__':
    init_db()
