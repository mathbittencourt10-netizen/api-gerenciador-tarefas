from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import bcrypt
import os

# ⚠️ Em produção, SEMPRE defina SECRET_KEY como variável de ambiente.
# Nunca deixe uma chave fixa no código de um projeto real.
SECRET_KEY = os.getenv("SECRET_KEY", "chave-secreta-apenas-para-desenvolvimento")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_senha(senha: str) -> str:
    """Gera o hash da senha (bcrypt) — nunca armazenamos a senha em texto puro."""
    hash_bytes = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
    return hash_bytes.decode("utf-8")


def verificar_senha(senha_texto: str, senha_hash: str) -> bool:
    """Compara a senha digitada no login com o hash salvo no banco."""
    return bcrypt.checkpw(senha_texto.encode("utf-8"), senha_hash.encode("utf-8"))


def criar_access_token(dados: dict) -> str:
    """Gera um token JWT assinado, válido por ACCESS_TOKEN_EXPIRE_MINUTES."""
    to_encode = dados.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expira})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decodificar_token(token: str) -> Optional[str]:
    """Valida o token e retorna o e-mail (subject) do usuário, ou None se inválido/expirado."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
