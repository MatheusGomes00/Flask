from flask import Flask, jsonify, request, json
#  'jsonify' permite retornar objetos json

app = Flask(__name__)

"""
    tipagem, int, float, bool...
"""


@app.get("/<int:id>")
def people(id):
    return jsonify({"id": id, "name": "Matheus", "role": "developer"})


# @app.route('/soma/<int:value1>/<int:value2>/')
# def soma(value1, value2):
#     return jsonify({'soma': value1 + value2})

# Para o método POST é possível enviar dados através do ‘body’ da requisição.
@app.route('/soma', methods=['POST', 'GET'])
def soma():
    if request.method == 'POST':
        dados = json.loads(request.data)
        total = sum(dados['valores'])
    elif request.method == 'GET':
        total = 10 + 10
    return jsonify({'soma': total})


if __name__ == '__main__':
    app.run(debug=True)
