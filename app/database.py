from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

# SQLite por padrão — funciona sem nenhuma configuração externa.
# Para usar PostgreSQL, defina a variável de ambiente DATABASE_URL, por exemplo:
#   postgresql://usuario:senha@localhost:5432/tarefas_db
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./tarefas.db")

# SQLite precisa desse argumento extra quando usado com múltiplas threads (padrão do Uvicorn)
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency do FastAPI: abre uma sessão por requisição e garante o fechamento."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
