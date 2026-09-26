from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from app.models import StatusTarefa, PrioridadeTarefa


# ── Usuário ──────────────────────────────────────────────────────────────
class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(..., min_length=6, description="Mínimo de 6 caracteres")


class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: EmailStr
    criado_em: datetime

    class Config:
        from_attributes = True  # permite criar a partir de um objeto SQLAlchemy


# ── Autenticação ─────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: EmailStr
    senha: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ── Tarefa ───────────────────────────────────────────────────────────────
class TarefaCreate(BaseModel):
    titulo: str = Field(..., min_length=1, max_length=150)
    descricao: Optional[str] = Field(None, max_length=500)
    status: StatusTarefa = StatusTarefa.pendente
    prioridade: PrioridadeTarefa = PrioridadeTarefa.media


class TarefaUpdate(BaseModel):
    """Todos os campos são opcionais — permite atualizar só o que for enviado."""
    titulo: Optional[str] = Field(None, min_length=1, max_length=150)
    descricao: Optional[str] = Field(None, max_length=500)
    status: Optional[StatusTarefa] = None
    prioridade: Optional[PrioridadeTarefa] = None


class TarefaResponse(BaseModel):
    id: int
    titulo: str
    descricao: Optional[str]
    status: StatusTarefa
    prioridade: PrioridadeTarefa
    criado_em: datetime
    usuario_id: int

    class Config:
        from_attributes = True
