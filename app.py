from flask import Flask, request, make_response, jsonify
from datetime import date

from model import Session, engine
from model.grupo import Grupo
from model.grupo import SubGrupo
from model.lancamento import Lancamento

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
  """Faz o lançamento do débito ou crédito

  Returns:
      lancamento: débito ou crédito que foi incluído
  """

  try:
    with Session(engine) as session:
      subGrupoId = int(request.form.get("subGrupoId"))
      subGrupo = session.query(SubGrupo).filter(SubGrupo.id == subGrupoId).first()
      print(request.form)
      quantasParcelas = request.form.get("quantasParcelas") and int(request.form.get("quantasParcelas")) or None
      lancamento = Lancamento(
          descricao = request.form.get("descricao"),
          valor = float(request.form.get("valor")),
          ehReceita = bool(request.form.get("ehReceita")),
          quantasParcelas = quantasParcelas,
          subGrupo = subGrupo
        )
      session.add(lancamento)
      session.commit()

      lancamento_dict = {}
      lancamento_dict["data"] = lancamento.dataDoFato
      lancamento_dict["descricao"] = lancamento.descricao
      lancamento_dict["valor"] = lancamento.valor
      lancamento_dict["id"] = lancamento.id
      lancamento_dict["ehReceita"] = lancamento.ehReceita
      lancamento_dict["subGrupoId"] = lancamento.subGrupoId
      lancamento_dict["quantasParcelas"] = lancamento.quantasParcelas
      resposta_json = jsonify(lancamento_dict)
      resposta = make_response(resposta_json, 201,)

      print("Salvo o lançamento:\n", lancamento_dict)

  except Exception as e:
    error = {"msg": "Não foi possível salvar o novo lançamento."}
    print(f"An exception occurred: {str(e)}")
    resposta_json = jsonify(error)
    resposta = make_response(resposta_json, 400,)

  resposta.headers["Content-Type"] = "application/json"

  return resposta

@app.route('/gerar_orcamento', methods=['GET'])
def gerarOrcamento():
  """Gera o orçamento do mês/ano informado. Caso não seja informado pega o mês/ano atual

  Returns:
      orcamento: lista de lançamentos do mês/ano informado, ou do mês/ano atual.
  """
  mes = request.args.get('mes')
  ano = request.args.get('ano')
  print('{}/{}'.format(mes, ano))

  orcamento = []

  resposta_json = jsonify(orcamento)

  resposta = make_response(resposta_json, 200,)
  resposta.headers["Content-Type"] = "application/json"

  return resposta

@app.route('/grupos', methods=['GET'])
def getGrupos():
  """Devolve a lista de grupos de conta existentes

  Returns:
      Grupos: Lista de grupos de conta existentes.
  """
  grupos = []

  resposta_json = jsonify(grupos)

  resposta = make_response(resposta_json, 200,)
  resposta.headers["Content-Type"] = "application/json"

  return resposta

@app.route('/grupo/<idGrupo>/sub-grupos', methods=['GET'])
def getSubGrupos(idGrupo):
  """Devolve a lista de SubGrupos de contas

  Args:
      idGrupo (number): idGrupo pai

  Returns:
      sub-grupo: lista de sub-grupos de conta do grupo informado
  """
  subGrupos = []

  resposta_json = jsonify(subGrupos)

  resposta = make_response(resposta_json, 200,)
  resposta.headers["Content-Type"] = "application/json"

  return resposta

@app.route('/alterar')
def alterarLancamento():
  """Altera um lançamento

  Returns:
      Lancamento: lançamento que foi alterado.
  """
  lancamento = {}
  lancamento["id"] = request.form.get("id")
  lancamento["subGrupo"] = request.form.get("subGrupo")
  lancamento["meioDeMovimentacao"] = request.form.get("meioDeMovimentacao")
  lancamento["data"] = request.form.get("data")
  lancamento["descricao"] = request.form.get("descricao")
  lancamento["valor"] = request.form.get("valor")
  lancamento["quantasParcelas"] = request.form.get("quantasParcelas")

  print("Alterar lançamento: \n", lancamento)

  resposta_json = jsonify(lancamento)

  resposta = make_response(resposta_json, 200,)
  resposta.headers["Content-Type"] = "application/json"

  return resposta

@app.route('/lancamento/<idLancamento>/excluir')
def excluirLancamento(idLancamento):
  """Exclui um lançamento

  Args:
      idLancamento (number): id do lançamento que será excluído.

  Returns:
      Lancamento: lançamento que foi excluído.
  """
  lancamento = {}
  lancamento["id"] = idLancamento

  print("Excluir lancamento de id: ", idLancamento)

  resposta_json = jsonify(lancamento)

  resposta = make_response(resposta_json, 200,)
  resposta.headers["Content-Type"] = "application/json"

  return resposta
