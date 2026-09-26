from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db
from app.security import verificar_senha, criar_access_token

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/registrar", response_model=schemas.UsuarioResponse, status_code=status.HTTP_201_CREATED)
def registrar(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    """Cria uma nova conta. O e-mail deve ser único."""
    if crud.obter_usuario_por_email(db, usuario.email):
        raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado.")
    return crud.criar_usuario(db, usuario)


@router.post("/login", response_model=schemas.Token)
def login(dados: schemas.LoginRequest, db: Session = Depends(get_db)):
    """Autentica o usuário e retorna um token JWT para uso nas rotas protegidas."""
    usuario = crud.obter_usuario_por_email(db, dados.email)
    if not usuario or not verificar_senha(dados.senha, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha inválidos.")

    token = criar_access_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}
