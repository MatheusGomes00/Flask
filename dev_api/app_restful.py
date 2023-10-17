from flask import Flask, request
from flask_restful import Resource, Api
from abilities import Habilidades, Handling, abilities_list
import json

app = Flask(__name__)
api = Api(app)

developers = [
    {
        'id': '0',
        'name': 'Matheus',
        'abilities': ['Python', 'Flask']},
    {
        'id': '1',
        'name': 'Pedro',
        'abilities': ['Python', 'Django']}]


class Desenvolvedor(Resource):
    # devolve um desenvolvedor pelo ID, também altera e deleta
    def get(self, id):
        try:
            response = developers[id]
        except IndexError:
            message = "Developer ID {} doesn't exist".format(id)
            response = {'status': 'error', 'message': message}
        except Exception:
            message = 'Unknown error. Find your API administrator'
            response = {'status': 'error', 'message': message}
        return response

    # altera dados de um desenvolvedor pelo ID
    def put(self, id):
        dados = json.loads(request.data)
        for item in dados['abilities']:
            if item not in abilities_list:
                return {"Insira uma habilidade existente na lista": abilities_list}
        developers[id] = dados
        return dados

    # deleta um dev pelo ID
    def delete(self, id):
        developers.pop(id)
        return {'status': 'success', 'message': 'deleted record'}


class DeveloperList(Resource):
    # lista todos os desenvolvedores
    def get(self):
        return developers

    # registrar um novo desenvolvedor
    def post(self):
        dados = json.loads(request.data)
        for item in dados['abilities']:
            if item not in abilities_list:
                return {"Insira uma habilidade existente na lista": abilities_list}
        position = len(developers)
        dados['id'] = position
        developers.append(dados)
        return developers[position]


api.add_resource(Desenvolvedor, '/dev/<int:id>/')
api.add_resource(DeveloperList, '/dev/')
api.add_resource(Habilidades, '/abilities/')
api.add_resource(Handling, '/abilities/<int:id>/')

if __name__ == '__main__':
    app.run(debug=True)
