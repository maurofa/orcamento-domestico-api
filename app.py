from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from sqlalchemy import select, insert, or_, and_
from sqlalchemy.orm import Session
import calendar
from dateutil.relativedelta import relativedelta
import math

from model import engine, Grupo, SubGrupo, Lancamento
from schemas.error import *
from schemas.grupo import *
from schemas.lancamento import *

info = Info(title="API do Orçamento Doméstico", version="0.1")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapidDoc")
lancamento_tag = Tag(name="Lançamento", description="Adição, visualização, remoção e alteração de lançamentos de receitas e despesas")
grupo_tag = Tag(name="Grupo e Sub-grupo", description="Listagem de Grupos e Sub-grupos")



@app.get('/', tags=[home_tag])
def home():
  """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
  """
  return redirect('/openapi')



@app.post('/lancamentos', tags=[lancamento_tag],
          responses={"201": LancamentoViewSchema, "400": ErrorSchema, "404": ErrorSchema})
def lancar(form: LancamentoSchema):
  """Faz o lançamento do débito ou crédito

  Returns:
      lancamento: débito ou crédito que foi incluído
  """

  try:
    with Session(engine) as session:
      subGrupoId = form.subGrupoId
      subGrupo = session.query(SubGrupo).filter(SubGrupo.id == subGrupoId).first()
      if not subGrupo:
        error_msg = "Sub-grupo não encontrado pelo id informado: "+ subGrupoId
        return {"message": error_msg}, 404

      if form.quantidadeDeParcelas:
        valor = math.floor(form.valor * 100 / form.quantidadeDeParcelas) / 100
        for i in range(form.quantidadeDeParcelas) :
          if i == 0:
            valorDaPrimeira = valor + (math.floor(form.valor * 100) % form.quantidadeDeParcelas) / 100
            dataDePagamento = form.dataDePagamento
          else:
            dataDePagamento = dataDePagamento + relativedelta(months=1)
          lancamento = session.scalar(
            insert(Lancamento).returning(Lancamento),
            {"dataDaCompra" : form.dataDaCompra,
              "dataDePagamento": dataDePagamento,
              "descricao" : form.descricao,
              "valor" : valorDaPrimeira if i == 0 else valor,
              "ehCredito" : form.ehCredito,
              "compraNoDebito": form.compraNoDebito,
              "numeroParcela" : i + 1,
              "subGrupoId" : subGrupoId}
          )
          if i == 0:
            retorno = apresenta_lancamento(lancamento)
      else:
        lancamento = session.scalar(
            insert(Lancamento).returning(Lancamento),
            {"dataDaCompra" : form.dataDaCompra,
              "dataDePagamento": form.dataDePagamento,
              "descricao" : form.descricao,
              "valor" : form.valor,
              "ehCredito" : form.ehCredito,
              "compraNoDebito": form.compraNoDebito,
              "subGrupoId" : subGrupoId}
          )
        retorno = apresenta_lancamento(lancamento)

      session.commit()
      return retorno, 201

  except Exception as e:
    error_msg = "Não foi possível salvar o novo lançamento."
    print(f"An exception occurred: {str(e)}")
    return {"message": error_msg}, 400



@app.get('/grupos', tags=[grupo_tag],
         responses={"200": ListagemGrupoSchema})
def getGrupos():
  """Devolve a lista de grupos de conta

  Returns:
      Grupos: Lista de grupos de conta.
  """
  with Session(engine) as session:
    stmt = select(Grupo)
    grupos = session.scalars(stmt).all()
    return apresenta_grupos(grupos), 200



@app.get('/lancamentos', tags=[lancamento_tag],
         responses={"200": LancamentosViewSchema, "404": ErrorSchema})
def gerarListaLancamentos(query: LancamentosQuery):
  """Gera o orçamento do mês/ano informado.

  Returns:
      orcamento: lista de lançamentos do mês/ano informado, ou do mês/ano atual.
  """

  with Session(engine) as session:
    mes = query.mes or date.today().month
    ano = query.ano or date.today().year
    inicio = date(ano, mes, 1)
    fim = ultimo_dia_mes(ano, mes)
    stmt = select(Lancamento).where(
      or_(Lancamento.dataDePagamento.between(inicio, fim),
             and_(Lancamento.dataDePagamento == None, Lancamento.dataDaCompra.between(inicio, fim))))
    lancamentos = session.scalars(stmt).all()
    if not lancamentos:
      error_msg = 'Não foi encontrado nenhum lançamento no mês ano informado.'
      return {"message": error_msg}, 404
    return apresenta_lancamentos(lancamentos), 200

def ultimo_dia_mes(ano, mes):
  """Retorna a data referente ao último dia do mês

  Returns:
      A data do último dia do mês no formato date
  """
  (_, ultimoDia) = calendar.monthrange(ano, mes)
  return date(ano, mes, ultimoDia)



@app.put('/lancamentos/<int:idLancamento>/alterar', tags=[lancamento_tag],
         responses={"200": LancamentoViewSchema, "404": ErrorSchema})
def alterarLancamento(path: LancamentoPathSchema, form: LancamentoSchema):
  """Altera um lançamento

  Returns:
      Lancamento: lançamento que foi alterado.
  """
  with Session(engine) as session:
    stmt = select(Lancamento).where(Lancamento.id == path.idLancamento)
    lancamento = session.scalars(stmt).one_or_none()
    subGrupo = session.scalars(select(SubGrupo).where(SubGrupo.id == form.subGrupoId)).one_or_none()
    if not lancamento or not subGrupo:
      error_msg = 'Não foi possível encontrar o lançamento ou o subGrupo com o id informado.'
      return {"message": error_msg}, 404
    lancamento.descricao = form.descricao
    lancamento.dataDaCompra = form.dataDaCompra
    lancamento.dataDePagamento = form.dataDePagamento
    lancamento.compraNoDebito = form.compraNoDebito
    lancamento.valor = form.valor
    lancamento.subGrupo = subGrupo
    lancamento.ehCredito = form.ehCredito
    retorno = apresenta_lancamento(lancamento)
    session.commit()
    return retorno, 200



@app.delete('/lancamentos/<int:idLancamento>/excluir', tags=[lancamento_tag],
            responses={"200": LancamentoViewSchema, "404": ErrorSchema})
def excluirLancamento(path: LancamentoPathSchema):
  """Exclui um lançamento

  Args:
      idLancamento (number): id do lançamento que será excluído.

  Returns:
      Lancamento: lançamento que foi excluído.
  """
  with Session(engine) as session:
    stmt = select(Lancamento).where(Lancamento.id == path.idLancamento)
    lancamento = session.scalars(stmt).one_or_none()
    if not lancamento:
      error_msg = 'Não foi possível encontrar o lançamento com o id informado.'
      return {"message": error_msg}, 404
    retorno = apresenta_lancamento(lancamento)
    session.delete(lancamento)
    session.commit()
    return retorno, 200
