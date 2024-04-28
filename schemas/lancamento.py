from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

from model.lancamento import Lancamento
from schemas.grupo import SubGrupoViewSchema

class LancamentoSchema(BaseModel):
  """Define os campos de um novo lançamento a ser inserido
  """
  dataDaCompra: Optional[date] = date.today()
  dataDePagamento: Optional[date]
  descricao: str = 'sofá'
  valor: float = 1530.3
  ehCredito: bool = False
  compraNoDebito: Optional[bool]
  quantidadeDeParcelas: Optional[int]
  subGrupoId: int = 19



class LancamentoPathSchema(BaseModel):
  """Define o pathParam idLancamento a ser alterado ou excluído
  """
  idLancamento: int = 1



class LancamentoViewSchema(BaseModel):
  """Define como um lançamento será retornado.
  """
  id: int = 1
  dataDaCompra: date = date.today()
  dataDePagamento: Optional[date]
  descricao: str = 'sofá'
  valor: float = 510.1
  ehCredito: bool = False
  compraNoDebito: Optional[bool]
  numeroParcela: Optional[int]
  subGrupo: SubGrupoViewSchema



def apresenta_lancamento(lancamento: Lancamento):
  """Retorna uma representação do lançamento seguindo o schema definido em LancamentoViewSchema

  Args:
      lancamento (Lancamento): lançamento a crédito ou débito
  """
  return {
    "id": lancamento.id,
    "dataDaCompra": lancamento.dataDaCompra.isoformat(),
    "dataDePagamento": lancamento.dataDePagamento and lancamento.dataDePagamento.isoformat(),
    "descricao": lancamento.descricao,
    "valor": lancamento.valor,
    "ehCredito": lancamento.ehCredito,
    "compraNoDebito": lancamento.compraNoDebito,
    "numeroParcela": lancamento.numeroParcela,
    "subGrupo": {
      "id": lancamento.subGrupoId,
      "descricao": lancamento.subGrupo and lancamento.subGrupo.descricao,
    },
  }



class LancamentosQuery(BaseModel):
  """Define os query params para o Orçamento
  """
  mes: Optional[int] = Field(date.today().month, ge=1, le=12, description='Mês')
  ano: Optional[int] = Field(date.today().year, ge=2021, le=date.today().year, description='Ano')



class LancamentosViewSchema(BaseModel):
  """Define como os lançamentos serão retornados.
  """
  lancamentos:List[LancamentoViewSchema]



def apresenta_lancamentos(lancamentos: List[Lancamento]):
  """Retorna uma representação dos lançamentos levando em consideração o LancamentosViewSchema

  Args:
      lancamentos (List[Lancamento]): lista de lançamentos dentro do mês-ano
  """
  lancamentosList = []
  for lancamento in lancamentos:
    lancamentosList.append(apresenta_lancamento(lancamento))
  return {
    "lancamentos": lancamentosList,
  }
