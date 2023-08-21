from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import Optional

from model import Base
from model.grupo import SubGrupo

class Lancamento(Base):
  __tablename__ = "lancamento"

  id: Mapped[int] = mapped_column(primary_key=True)
  dataDoFato: Mapped[Optional[date]] = mapped_column(default=date.today())
  descricao: Mapped[str] = mapped_column(String(140))
  valor: Mapped[float]
  ehReceita: Mapped[bool]
  quantasParcelas: Mapped[Optional[int]]
  subGrupoId: Mapped[Optional[int]] = mapped_column(ForeignKey("sub_grupo.id"))

  subGrupo: Mapped["SubGrupo"] = relationship()
