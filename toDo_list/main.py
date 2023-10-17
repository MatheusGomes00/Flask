from flask import Flask, request, jsonify, json

app = Flask(__name__)

tasks = [{
    'id': '0',
    'responsável': 'Matheus',
    'tarefa': 'finalizar a lista de tarefas',
    'status': 'pendente'}, {
    'id': '1',
    'responsável': 'Pedro',
    'tarefa': 'estudar InglÊs',
    'status': 'em andamento'
}]


@app.route('/tasks', methods=['POST', 'GET'])
def listar_incluir():
    if request.method == 'GET':
        return jsonify(tasks)
    elif request.method == 'POST':
        dados = json.loads(request.data)
        tasks.append(dados)
        return jsonify({'status': 'success', 'message': 'task added'})


@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def consultar_alterar_deletar(id):
    if request.method == 'GET':
        return jsonify(tasks[id])
    elif request.method == 'PUT':
        dados = json.loads(request.data)
        task = tasks[id]
        task['status'] = dados
        return jsonify({'status': 'success', 'message': 'task status modified'})
    elif request.method == 'DELETE':
        tasks.pop(id)
        return jsonify({'status': 'success', 'message': 'deleted task'})


if __name__ == '__main__':
    app.run(debug=True)
