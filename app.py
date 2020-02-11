from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

def checar_cartao(f):
    wraps(f)
    def validacoes(*args, **kwargs):
        dados = request.get_json()
        if not dados.get("status"):
            response = {"aprovado":False,
            "novoLimite":dados.get("limit"),
            "motivo":"Cartao bloqueado"}
            return jsonify(response)

        if dados.get("limit") < dados.get("transaction").get("amount"):
            response = {"aprovado":False,
            "novoLimite":dados.get("limit"),
            "motivo":"Compra acima do limite"}
            return jsonify(response)
        return f(*args, **kwargs)

    return(validacoes)

@app.route("/api/transaction",methods=["POST"])
@checar_cartao
def transacao():
    card = request.get_json()   
    novo_limite = card.get("limit") - card.get("transaction").get("amount")
    response = {"aprovado":True,"novoLimite":novo_limite}
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)