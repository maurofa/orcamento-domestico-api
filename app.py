from flask import redirect
from flask_openapi3 import OpenAPI, Info, Tag
from flask_cors import CORS
from sqlalchemy import select
import calendar

from model import Session, engine, Grupo, SubGrupo, Lancamento
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



@app.post('/lancar', tags=[lancamento_tag],
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
      lancamento = Lancamento(
          dataDoFato = form.dataDoFato,
          descricao = form.descricao,
          valor = form.valor,
          ehReceita = form.ehReceita,
          quantasParcelas = form.quantasParcelas,
          subGrupo = subGrupo
        )
      session.add(lancamento)
      session.commit()

      return apresenta_lancamento(lancamento), 201

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



@app.get('/grupo/<int:idGrupo>/sub-grupos', tags=[grupo_tag],
         responses={"200": ListagemSubGrupoSchema, "404": ErrorSchema})
def getSubGrupos(path: SubGrupoPath):
  """Devolve a lista de SubGrupos de contas do grupo informado

  Args:
      idGrupo (number): idGrupo pai

  Returns:
      sub-grupo: lista de sub-grupos de conta do grupo informado
  """
  with Session(engine) as session:
    stmt = select(SubGrupo).where(SubGrupo.grupo_id == path.idGrupo)
    subGrupos = session.scalars(stmt).all()
    if not subGrupos:
      error = {"msg": "Sub-grupo não encontrado pelo id informado: "+path.idGrupo}
      return {"message": error}, 404
    return apresenta_sub_grupos(subGrupos), 200





@app.get('/gerar_orcamento', tags=[lancamento_tag],
         responses={"200": OrcamentoViewSchema, "404": ErrorSchema})
def gerarOrcamento(query: OrcamentoQuery):
  """Gera o orçamento do mês/ano informado.

  Returns:
      orcamento: lista de lançamentos do mês/ano informado, ou do mês/ano atual.
  """

  with Session(engine) as session:
    mes = query.mes or date.today().month
    ano = query.ano or date.today().year
    inicio = date(ano, mes, 1)
    (diaDaSemana, ultimoDia) = calendar.monthrange(ano, mes)
    fim = date(ano, mes, ultimoDia)
    stmt = select(Lancamento).where(Lancamento.dataDoFato.between(inicio, fim))
    orcamento = session.scalars(stmt).all()
    if not orcamento:
      error_msg = 'Não foi encontrado nenhum lançamento no mês ano informado.'
      return {"message": error_msg}, 404
    return apresenta_orcamento(orcamento), 200



@app.put('/lancamento/<int:idLancamento>/alterar', tags=[lancamento_tag],
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
    lancamento.dataDoFato = form.dataDoFato
    lancamento.valor = form.valor
    lancamento.quantasParcelas = form.quantasParcelas
    lancamento.ehReceita = form.ehReceita
    lancamento.subGrupo = subGrupo
    session.commit()
    return apresenta_lancamento(lancamento), 200



@app.delete('/lancamento/<int:idLancamento>/excluir', tags=[lancamento_tag],
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
    session.delete(lancamento)
    session.commit()
    return apresenta_lancamento(lancamento), 200
