from pydantic import BaseModel, Field
from datetime import date
from typing import Optional, List

from model.lancamento import Lancamento
from schemas.grupo import SubGrupoViewSchema

class LancamentoSchema(BaseModel):
  """Define os campos de um novo lançamento a ser inserido
  """
  dataDoFato: Optional[date] = date.today()
  descricao: str = 'sofá'
  valor: float = 1530.3
  ehReceita: bool = False
  quantasParcelas: Optional[int]=6
  subGrupoId: int = 19



class LancamentoPathSchema(BaseModel):
  """Define o pathParam idLancamento a ser alterado ou excluído
  """
  idLancamento: int = 1



class LancamentoViewSchema(BaseModel):
  """Define como um lançamento será retornado.
  """
  id: int = 1
  dataDoFato: date = date.today()
  descricao: str = 'sofá'
  valor: float = 1530,3
  ehReceita: bool = False
  quantasParcelas: int = 6
  subGrupo: SubGrupoViewSchema



def apresenta_lancamento(lancamento: Lancamento):
  """Retorna uma representação do lançamento seguindo o schema definido em LancamentoViewSchema

  Args:
      lancamento (Lancamento): lançamento a crédito ou débito
  """
  return {
    "id": lancamento.id,
    "dataDoFato": lancamento.dataDoFato,
    "descricao": lancamento.descricao,
    "valor": lancamento.valor,
    "ehReceita": lancamento.ehReceita,
    "subGrupo": {
      "id": lancamento.subGrupoId,
      "descricao": lancamento.subGrupo.descricao,
    },
  }



class OrcamentoQuery(BaseModel):
  """Define os path params para o Orçamento
  """
  mes: Optional[int] = Field(date.today().month, ge=1, le=12, description='Mês')
  ano: Optional[int] = Field(date.today().year, ge=2021, le=date.today().year, description='Ano')



class LancamentoView2Schema(BaseModel):
  """Define como o lançamento será exibido no orçamento
  """
  id: int = 1
  dataDoFato: date = date.today()
  descricao: str = 'sofá'
  valor: float = 255.0
  ehReceita: bool = False
  subGrupo: SubGrupoViewSchema



class OrcamentoViewSchema(BaseModel):
  """Define como um orçamento será retornado.
  """
  orcamento:List[LancamentoView2Schema]
  saldo:float = 100.0
  quantidade:int = 50



def apresenta_orcamento(lancamentos: List[Lancamento]):
  """Retorna uma representação do lançamento levando em consideração o OrcamentoViewSchema

  Args:
      lancamentos (List[Lancamento]): lista de lançamentos dentro do mês-ano
  """
  saldo = 0.0
  quantidade = len(lancamentos)
  orcamento = []
  for lancamento in lancamentos:
    lancamentoDict = {
      "id": lancamento.id,
      "dataDoFato": lancamento.dataDoFato,
      "descricao": lancamento.descricao,
      "valor": lancamento.valor / (lancamento.quantasParcelas or 1),
      "ehReceita": lancamento.ehReceita,
      "subGrupo": {
        "id": lancamento.subGrupoId,
        "descricao": lancamento.subGrupo.descricao,
      },
    }
    orcamento.append(lancamentoDict)
    saldo = saldo + lancamentoDict["valor"] * (1 if lancamento.ehReceita else -1)
  return {
    "orcamento": orcamento,
    "saldo": saldo,
    "quantidade": quantidade,
  }
