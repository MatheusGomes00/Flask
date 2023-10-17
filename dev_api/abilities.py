from flask_restful import Resource
from flask import request
import json

abilities_list = ['Python', 'Flask', 'Django', 'Java', 'PHP', 'Ruby', 'JS', 'elixir']


class Habilidades(Resource):
    # retorna a lista de habilidades
    def get(self):
        return abilities_list

    # adiciona uma nova habilidade na lista
    def post(self):
        new_skill = json.loads(request.data)
        abilities_list.append(new_skill)
        return abilities_list


class Handling(Resource):
    # altera um item da lista de acordo com ID
    def put(self, id):
        skill_change = json.loads(request.data)
        abilities_list[id] = skill_change
        return abilities_list

    # deleta um item da lista de acordo com ID
    def delete(self, id):
        abilities_list.pop(id)
        return abilities_list
