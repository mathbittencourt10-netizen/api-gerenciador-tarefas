from sqlalchemy.orm import Session
from app import models, schemas
from app.security import hash_senha


# ── Usuário ──────────────────────────────────────────────────────────────
def obter_usuario_por_email(db: Session, email: str) -> models.Usuario | None:
    return db.query(models.Usuario).filter(models.Usuario.email == email).first()


def criar_usuario(db: Session, dados: schemas.UsuarioCreate) -> models.Usuario:
    novo = models.Usuario(
        nome=dados.nome,
        email=dados.email,
        senha_hash=hash_senha(dados.senha),
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo


# ── Tarefa ───────────────────────────────────────────────────────────────
def listar_tarefas(db: Session, usuario_id: int, status: str | None = None) -> list[models.Tarefa]:
    query = db.query(models.Tarefa).filter(models.Tarefa.usuario_id == usuario_id)
    if status:
        query = query.filter(models.Tarefa.status == status)
    return query.order_by(models.Tarefa.criado_em.desc()).all()


def obter_tarefa(db: Session, tarefa_id: int, usuario_id: int) -> models.Tarefa | None:
    """Busca a tarefa garantindo que ela pertence ao usuário informado."""
    return (
        db.query(models.Tarefa)
        .filter(models.Tarefa.id == tarefa_id, models.Tarefa.usuario_id == usuario_id)
        .first()
    )


def criar_tarefa(db: Session, dados: schemas.TarefaCreate, usuario_id: int) -> models.Tarefa:
    nova = models.Tarefa(**dados.model_dump(), usuario_id=usuario_id)
    db.add(nova)
    db.commit()
    db.refresh(nova)
    return nova


def atualizar_tarefa(db: Session, tarefa: models.Tarefa, dados: schemas.TarefaUpdate) -> models.Tarefa:
    """Atualiza somente os campos que vieram preenchidos na requisição."""
    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(tarefa, campo, valor)
    db.commit()
    db.refresh(tarefa)
    return tarefa


def excluir_tarefa(db: Session, tarefa: models.Tarefa) -> None:
    db.delete(tarefa)
    db.commit()
