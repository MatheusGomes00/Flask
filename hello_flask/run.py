from flask import Flask

# Cria uma instância do aplicativo Flask
app = Flask(__name__)

# Define uma rota (route) para o aplicativo. Neste caso, a rota é "/<numero>".
# A parte "<numero>" entre colchetes é uma variável de rota que pode capturar valores
# numéricos passados na URL e passá-los para a função como um argumento.


@app.route("/<numero>", methods=["GET", "POST"])
def hello(numero):
    return "Hello Word"


if __name__ == "__main__":
    app.run(debug=True)
    # "debug=True"usar somente quando em desenvolvimento, em produção se der
    #  erro é mostrada toda uma trilha do erro, o que não é interessante;
