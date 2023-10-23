from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker, relationship

engine = create_engine('sqlite:///lista_dev.db')
db_session = scoped_session(sessionmaker(autocommit=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


class Programador(Base):
    __tablename__ = 'programadores'
    id = Column(Integer, primary_key=True)
    nome = Column(String(30), index=True)
    idade = Column(Integer)
    email = Column(String(30), index=True)


class Habilidades(Base):
    __tablename__ = 'habilidades'
    id = Column(Integer, primary_key=True)
    nome = Column(String(30))


class ProgramadorHabilidades(Base):
    __tablename__ = 'programador_habilidades'
    id = Column(Integer, primary_key=True)
    programador_id = Column(Integer, ForeignKey('programadores.id'))
    programador = relationship("Programador")
    habilidades_id = Column(Integer, ForeignKey('habilidades.id'))
    habilidades = relationship("Habilidades")


def init_db():
    Base.metadata.create_all(bind=engine)


if __name__ == '__main__':
    init_db()
