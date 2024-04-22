from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import Optional

from model import Base
from model.grupo import SubGrupo

class Lancamento(Base):
  __tablename__ = "lancamento"

  id: Mapped[int] = mapped_column(primary_key=True)
  dataDaCompra: Mapped[Optional[date]] = mapped_column(default=date.today())
  dataDePagamento: Mapped[Optional[date]]
  descricao: Mapped[str] = mapped_column(String(140))
  valor: Mapped[float]
  ehCredito: Mapped[bool]
  compraNoDebito: Mapped[Optional[bool]]
  numeroParcela: Mapped[Optional[int]]
  subGrupoId: Mapped[int] = mapped_column(ForeignKey("sub_grupo.id"))

  subGrupo: Mapped["SubGrupo"] = relationship()
