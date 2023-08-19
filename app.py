from flask import Flask, request, make_response, jsonify

app = Flask(__name__)

@app.route('/')
def home():
  html = """
    <!DOCTYPE html>
    <html>
      <body>
        <p> Documentação em desenvolvimento"" </p>
      </body>
    </html>
  """
  return make_response(html), 200

@app.route('/lancar', methods=['POST'])
def lancar():
  # lendo atributos recebidos via formulário
  lancamento = {}
  lancamento["subGrupo"] = request.form.get("subGrupo")
  lancamento["meioDeMovimentacao"] = request.form.get("meioDeMovimentacao")
  lancamento["data"] = request.form.get("data")
  lancamento["descricao"] = request.form.get("descricao")
  lancamento["valor"] = request.form.get("valor")
  lancamento["quantasParcelas"] = request.form.get("quantasParcelas")

  # imprimindo no console
  print("Salvar lançamento: \n", lancamento)

  # criando JSON
  resposta_json = jsonify(lancamento)

  # criando resposta
  resposta = make_response(resposta_json, 200,)
  resposta.headers["Content-Type"] = "application/json"

  # retornando reposta
  return resposta


