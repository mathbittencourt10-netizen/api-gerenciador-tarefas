from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
from app import schemas, crud, models
from app.database import get_db
from app.dependencies import obter_usuario_atual

router = APIRouter(prefix="/tarefas", tags=["Tarefas"])


@router.get("/", response_model=List[schemas.TarefaResponse])
def listar(
    status_filtro: Optional[models.StatusTarefa] = None,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    """Lista as tarefas do usuário autenticado. Use ?status_filtro= para filtrar."""
    return crud.listar_tarefas(db, usuario.id, status_filtro)


@router.post("/", response_model=schemas.TarefaResponse, status_code=status.HTTP_201_CREATED)
def criar(
    tarefa: schemas.TarefaCreate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    """Cria uma nova tarefa vinculada ao usuário autenticado."""
    return crud.criar_tarefa(db, tarefa, usuario.id)


@router.get("/{tarefa_id}", response_model=schemas.TarefaResponse)
def obter(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    """Retorna uma tarefa específica, se pertencer ao usuário autenticado."""
    tarefa = crud.obter_tarefa(db, tarefa_id, usuario.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return tarefa


@router.put("/{tarefa_id}", response_model=schemas.TarefaResponse)
def atualizar(
    tarefa_id: int,
    dados: schemas.TarefaUpdate,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    """Atualiza campos de uma tarefa existente (envie só o que quer mudar)."""
    tarefa = crud.obter_tarefa(db, tarefa_id, usuario.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    return crud.atualizar_tarefa(db, tarefa, dados)


@router.delete("/{tarefa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir(
    tarefa_id: int,
    db: Session = Depends(get_db),
    usuario: models.Usuario = Depends(obter_usuario_atual),
):
    """Remove uma tarefa do usuário autenticado."""
    tarefa = crud.obter_tarefa(db, tarefa_id, usuario.id)
    if not tarefa:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada.")
    crud.excluir_tarefa(db, tarefa)
