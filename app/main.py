from fastapi import FastAPI
from app.database import Base, engine
from app.routers import auth, tarefas

# Cria as tabelas no banco de dados, caso ainda não existam
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Gerenciamento de Tarefas",
    description=(
        "API REST para gerenciar tarefas pessoais, com autenticação via JWT. "
        "Cada usuário só acessa suas próprias tarefas."
    ),
    version="1.0.0",
)

app.include_router(auth.router)
app.include_router(tarefas.router)


@app.get("/", tags=["Status"])
def raiz():
    """Rota de status — confirma que a API está no ar."""
    return {"mensagem": "API de Tarefas no ar! Acesse /docs para testar interativamente."}
