from flask import Flask, jsonify, request, json

app = Flask(__name__)

developers = [
    {
        'id': '0',
        'name': 'Matheus',
        'abilities': ['Python', 'Flask']},
    {
        'id': '1',
        'name': 'Pedro',
        'abilities': ['Python', 'Django']}]


# devolve um desenvolvedor pelo ID, também altera e deleta
@app.route('/dev/<int:id>/', methods=['GET', 'PUT', 'DELETE'])
def developer(id):
    if request.method == 'GET':
        try:
            response = developers[id]
        except IndexError:
            message = "Developer ID {} doesn't exist".format(id)
            response = {'status': 'error', 'message': message}
        except Exception:
            message = 'Unknown error. Find your API administrator'
            response = {'status': 'error', 'message': message}
        return jsonify(response)
    elif request.method == 'PUT':
        dados = json.loads(request.data)
        developers[id] = dados
        return jsonify(dados)
    elif request.method == 'DELETE':
        developers.pop(id)
        return jsonify({'status': 'success', 'message': 'deleted record'})


# lista todos os desenvolvedores e permite registrar um novo desenvolvedor
@app.route('/dev/', methods=['POST', 'GET'])
def developer_list():
    if request.method == 'POST':
        dados = json.loads(request.data)
        position = len(developers)
        dados['id'] = position
        developers.append(dados)
        # return jsonify({'status': 'success', 'message': 'record inserted'})
        return jsonify(developers[position])
    elif request.method == 'GET':
        return jsonify(developers)


if __name__ == '__main__':
    app.run(debug=True)
