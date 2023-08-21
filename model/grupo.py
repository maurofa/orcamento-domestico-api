from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing import Any, List

from model import Base

class Grupo(Base):
  __tablename__ = 'grupo'

  id: Mapped[int] = mapped_column(primary_key=True)
  descricao: Mapped[str] = mapped_column(String(140), unique=True)

  subGrupos: Mapped[List["SubGrupo"]] = relationship(back_populates="grupo", cascade="all, delete-orphan")

class SubGrupo(Base):
  __tablename__ = "sub_grupo"

  id: Mapped[int] = mapped_column( primary_key=True)
  descricao: Mapped[str] = mapped_column(String(140), unique=True)
  grupo_id: Mapped[int] = mapped_column(ForeignKey("grupo.id"))

  grupo: Mapped["Grupo"] = relationship(back_populates="subGrupos")
