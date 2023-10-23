from models import Pessoas


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
    pessoa = Pessoas.query.filter_by(nome='Gomes').first()  # first() pega o primeiro registro
    pessoa.nome = 'Pedro'
    pessoa.save()


def exclui_pessoa():  # Exclui dados na tabela pessoas
    pessoa = Pessoas.query.filter_by(nome='Gomes').first()
    pessoa.delete()


if __name__ == '__main__':
    # insere_pessoas()
    # altera_pessoa()
    exclui_pessoa()
    consulta_pessoas()
