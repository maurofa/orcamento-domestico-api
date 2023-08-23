from pydantic import BaseModel
from typing import List
from model.grupo import Grupo, SubGrupo

class GrupoViewSchema(BaseModel):
  """ Define como um grupo será retornado.
  """
  id: int = 1
  descricao: str = 'Alimentação'
  qtdSubGrupos: int = 6

class ListagemGrupoSchema(BaseModel):
  """Define como uma listagem de grupos será retornada.
  """
  grupos:List[GrupoViewSchema]

def apresenta_grupos(grupos: List[Grupo]):
  """Retorna uma representação da lista de grupos seguindo o schema definido em GrupoViewSchema.

  Args:
      grupos (List[Grupo]): Lista com todos os grupos cadastrados.
  """
  resultado = []
  for grupo in grupos:
    resultado.append({
      "id": grupo.id,
      "descricao": grupo.descricao,
      "qtdSubGrupos": len(grupo.subGrupos),
    })

  return {"grupos": resultado}

class SubGrupoPath(BaseModel):
  """Define como o path params para SubGrupo
  """
  idGrupo: int = 1

class SubGrupoViewSchema(BaseModel):
  """ Define como um sub-grupo será retornado.
  """
  id: int = 1
  descricao: str = 'Alimentação'

class ListagemSubGrupoSchema(BaseModel):
  """Define como uma listagem de sub-grupos será retornada.
  """
  subGrupos:List[SubGrupoViewSchema]

def apresenta_sub_grupos(subGrupos: List[SubGrupo]):
  """Retorna uma representação da lista de sub-grupos seguindo o schema definido em GrupoViewSchema.

  Args:
      subGrupos (List[SubGrupo]): Lista com todos os sub-grupos do grupo informado.
  """
  resultado = []
  for subGrupo in subGrupos:
    resultado.append({
      "id": subGrupo.id,
      "descricao": subGrupo.descricao,
    })

  return {"subGrupos": resultado}
