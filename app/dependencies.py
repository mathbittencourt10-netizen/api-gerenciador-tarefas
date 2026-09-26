from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.security import decodificar_token
from app import crud, models

security_scheme = HTTPBearer()


def obter_usuario_atual(
    credenciais: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: Session = Depends(get_db),
) -> models.Usuario:
    erro_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = decodificar_token(credenciais.credentials)
    if email is None:
        raise erro_credenciais

    usuario = crud.obter_usuario_por_email(db, email)
    if usuario is None:
        raise erro_credenciais

    return usuario
