from pydantic import BaseModel
from typing import List
from model.grupo import Grupo, SubGrupo

class SubGrupoViewSchema(BaseModel):
  """ Define como um sub-grupo será retornado.
  """
  id: int = 1
  descricao: str = 'Alimentação'

class GrupoViewSchema(BaseModel):
  """ Define como um grupo será retornado.
  """
  id: int = 1
  descricao: str = 'Alimentação'
  subGrupos: List[SubGrupoViewSchema]

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
    subGrupos = []

    for subGrupo in grupo.subGrupos:
      subGrupos.append({"id": subGrupo.id, "descricao": subGrupo.descricao})

    resultado.append({
      "id": grupo.id,
      "descricao": grupo.descricao,
      "subGrupos": subGrupos,
    })

  return {"grupos": resultado}
