from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class StatusTarefa(str, enum.Enum):
    pendente = "pendente"
    em_andamento = "em_andamento"
    concluida = "concluida"


class PrioridadeTarefa(str, enum.Enum):
    baixa = "baixa"
    media = "media"
    alta = "alta"


class Usuario(Base):
    """Um usuário do sistema — dono de zero ou mais tarefas."""
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    senha_hash = Column(String(255), nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)

    tarefas = relationship("Tarefa", back_populates="dono", cascade="all, delete-orphan")


class Tarefa(Base):
    """Uma tarefa, sempre vinculada a um usuário dono."""
    __tablename__ = "tarefas"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)
    descricao = Column(String(500), nullable=True)
    status = Column(Enum(StatusTarefa), default=StatusTarefa.pendente, nullable=False)
    prioridade = Column(Enum(PrioridadeTarefa), default=PrioridadeTarefa.media, nullable=False)
    criado_em = Column(DateTime, default=datetime.utcnow)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"), nullable=False)

    dono = relationship("Usuario", back_populates="tarefas")
