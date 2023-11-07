from flask import Flask, request
from flask_restful import Resource, Api
from models import Pessoas, Atividades, StatusAtividade

app = Flask(__name__)
api = Api(app)

"""
neste projeto as 'response' são tratadas em formato JSON, 
as 'response' das requisições HTTP precisam estar em formato JSON, 
basicamente a sintaxe do dicionário ex.: 
string == "'nome': 'Matheus'"
lista == response = [1, 2, 3, 4, 5]      
dicionário == response = {"nome":"Matheus"}
"""


class Pessoa(Resource):
    # filtra a pessoa pelo nome passado na URN
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            response = {
                'nome': pessoa.nome,
                'idade': pessoa.idade,
                'id': pessoa.id
            }
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
        return response

    # altera pessoa pelo body, nome passado como atributo pela URN
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        try:
            pessoa.nome = dados['nome']
            pessoa.idade = dados['idade']
            pessoa.save()
            response = {
                'id': pessoa.id,
                'nome': pessoa.nome,
                'idade': pessoa.idade
            }
            return response
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
            return response

    # deleta pessoa, pelo nome passado como atributo na URN
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            mensagem = f"Pessoa {pessoa.nome} excluída com sucesso"
            pessoa.delete()
            return {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {
                'status': 'error',
                'mensagem': 'Pessoa não encontrada'
            }
        return response


class ListaPessoas(Resource):
    # mostra todas as pessoas cadastradas
    def get(self):
        pessoas = Pessoas.query.first()  # não é recomendado o uso do .all() em banco de dados grandes, é inviável, a consulta deve ser parametrizada...
        if pessoas:
            pessoas = Pessoas.query.all()
            response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
            return response
        else:
            response = {"status": "erro", "mensagem": "Não há pessoas cadastradas."}
            return response

    # criar pessoa, passada pelo body
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {
            'id': pessoa.id,
            'nome': pessoa.nome,
            'idade': pessoa.idade
        }
        return response


class ListaAtividades(Resource):
    # mostra atividades, filtrando pelo nome da pessoa
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        # print(type(pessoa))
        if pessoa is not None:
            atividades = Atividades.query.filter_by(pessoa_id=pessoa.id).all()
            response = [{'id': i.id, 'tarefa': i.tarefa, 'pessoa': i.pessoa.nome, 'status': i.status} for i in atividades]
            return response
        else:
            response = {
                "status": "error",
                "erro": "usuário não encontrado"
            }
            return response


class ConsultarAlterarStatus(Resource):
    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        response = {'tarefa': atividade.tarefa, 'Status': atividade.status}
        return response

    def put(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        atividade.status = StatusAtividade.CONCLUIDO.value
        atividade.save()
        response = {
            "Id": atividade.id,
            "Tarefa": atividade.tarefa,
            "Status": atividade.status
                    }
        return response


class InsereAtividades(Resource):
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(nome=dados['pessoa']).first()
        atividade = Atividades(tarefa=dados['tarefa'], pessoa=pessoa)
        atividade.save()
        response = {
            'pessoa': atividade.pessoa.nome,
            'tarefa': atividade.tarefa,
            'id': atividade.id
        }
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ListaAtividades, '/atividades/<string:nome>/')
api.add_resource(InsereAtividades, '/atividades/')
api.add_resource(ConsultarAlterarStatus, '/status/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
