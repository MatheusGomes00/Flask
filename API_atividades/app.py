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
    # consultar pessoa pelo nome passado na URN
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        print(pessoa)
        try:
            response = {'nome': pessoa.nome, 'idade': pessoa.idade, 'id': pessoa.id}
        except AttributeError:
            response = {'status': 'error', 'mensagem': 'Pessoa não encontrada'}
        return response

    # alterar pessoa pelo body, nome passado como atributo pela URN
    def put(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        dados = request.json
        try:
            pessoa.nome = dados['nome'], pessoa.idade = dados['idade'], pessoa.save()
            response = {'id': pessoa.id, 'nome': pessoa.nome, 'idade': pessoa.idade}
        except AttributeError:
            response = {'status': 'error', 'mensagem': 'Pessoa não encontrada'}
        return response

    # deletar pessoa, pelo nome passado como atributo na URN
    def delete(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        try:
            mensagem = f"Pessoa {pessoa.nome} excluída com sucesso"
            pessoa.delete()
            response = {'status': 'sucesso', 'mensagem': mensagem}
        except AttributeError:
            response = {'status': 'error', 'mensagem': 'Pessoa não encontrada'}
        return response


class ListaPessoas(Resource):
    # consultar pessoas cadastradas
    def get(self):
        pessoas = Pessoas.query.first()  # não é recomendado o uso do .all() em banco de dados grandes, é inviável, a consulta deve ser parametrizada...
        if pessoas:
            pessoas = Pessoas.query.all()
            response = [{'id': i.id, 'nome': i.nome, 'idade': i.idade} for i in pessoas]
        else:
            # response = {"status": "erro", "mensagem": "Não há pessoas cadastradas."}
            response = "Não há pessoas cadastradas."
        return response

    # criar pessoa, passada pelo body
    def post(self):
        dados = request.json
        pessoa = Pessoas(nome=dados['nome'], idade=dados['idade'])
        pessoa.save()
        response = {'id': pessoa.id, 'nome': pessoa.nome, 'idade': pessoa.idade}
        return response


class ConsultarAtividade(Resource):
    # consultar atividades, filtrando pelo nome da pessoa
    def get(self, nome):
        pessoa = Pessoas.query.filter_by(nome=nome).first()
        # print(type(pessoa))
        if pessoa is not None:
            atividades = Atividades.query.filter_by(pessoa_id=pessoa.id).all()
            response = [{'id': i.id, 'tarefa': i.tarefa, 'pessoa': i.pessoa.nome, 'status': i.status} for i in atividades]
        else:
            response = {"status": "error", "erro": "usuário não encontrado"}
        return response


class ConsultarAlterarStatus(Resource):
    # consultar atividade por ID
    def get(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        try:
            response = {'tarefa': atividade.tarefa, 'Status': atividade.status}
        except AttributeError:
            response = {"status": "error", "mensagem": "ID não encontrado"}
        return response

    # alterar status atividade, por ID
    def put(self, id):
        atividade = Atividades.query.filter_by(id=id).first()
        try:
            atividade.status = StatusAtividade.CONCLUIDO.value
            atividade.save()
            response = {"Id": atividade.id, "Tarefa": atividade.tarefa, "Status": atividade.status}
        except AttributeError:
            response = {"status": "error", "mensagem": "ID não encontrado"}
        return response


class InsereAtividades(Resource):
    # criar atividade, filtrando pelo ID da pessoa passado no body
    def post(self):
        dados = request.json
        pessoa = Pessoas.query.filter_by(id=dados['pessoa']).first()
        try:
            atividade = Atividades(tarefa=dados['tarefa'], pessoa=pessoa)
            atividade.save()
            response = {'pessoa': atividade.pessoa.nome, 'tarefa': atividade.tarefa, 'id': atividade.id}
        except AttributeError:
            response = {"status": "error", "mensagem": "Pessoa não encontrada"}
        return response


api.add_resource(Pessoa, '/pessoa/<string:nome>/')
api.add_resource(ListaPessoas, '/pessoa/')
api.add_resource(ConsultarAtividade, '/atividades/<string:nome>/')
api.add_resource(InsereAtividades, '/atividades/')
api.add_resource(ConsultarAlterarStatus, '/status/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
