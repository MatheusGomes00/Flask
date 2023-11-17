from models import Pessoas, Usuarios


def insere_pessoas():  # Insere dados na tabela Pessoas
    pessoa = Pessoas(nome='Matheus', idade=26)
    pessoa.save()
    print(pessoa)


def consulta_pessoas():  # Realiza consulta na tabela Pessoas
    pessoas = Pessoas.query.all()
    print(pessoas)
    # pessoa = Pessoas.query.filter_by(nome='Matheus').first()
    # print(pessoa.idade)


def altera_pessoa():  # Altera dados na tabela Pessoas
    pessoa = Pessoas.query.filter_by(nome='Matheus').first()  # first() pega o primeiro registro/ocorrência
    pessoa.nome = 'Pedro'
    pessoa.save()


def exclui_pessoa():  # Exclui dados na tabela pessoas
    pessoa = Pessoas.query.filter_by(nome='Matheus').first()
    pessoa.delete()


def insere_usuario(login, senha):
    usuario = Usuarios(login=login, senha=senha)
    usuario.save()


def consulta_todos_usuarios():
    usuarios = Usuarios.query.all()
    print(usuarios)


if __name__ == '__main__':
    # insere_usuario('matheus', '1234')
    # insere_usuario('gomes', '4321')
    consulta_todos_usuarios()
    # insere_pessoas()
    # altera_pessoa()
    # exclui_pessoa()
    # consulta_pessoas()
