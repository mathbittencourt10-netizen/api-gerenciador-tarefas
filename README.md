# ✅ API de Gerenciamento de Tarefas

API REST desenvolvida com **FastAPI**, com autenticação via **JWT** e persistência em banco
de dados relacional. Cada usuário se cadastra, faz login e gerencia apenas suas próprias tarefas.

Inclui documentação interativa automática — dá para testar todos os endpoints direto pelo
navegador, sem precisar do Postman.

---

## 🚀 Funcionalidades

- ✅ Cadastro e login de usuários com senha criptografada (bcrypt)
- ✅ Autenticação via token JWT
- ✅ CRUD completo de tarefas (criar, listar, editar, excluir)
- ✅ Cada usuário só acessa suas próprias tarefas
- ✅ Filtro de tarefas por status
- ✅ Validação automática de dados (Pydantic)
- ✅ Documentação interativa em `/docs` (Swagger UI)

---

## 🛠️ Tecnologias

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=python&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-000000?style=for-the-badge&logo=jsonwebtokens&logoColor=white)

---

## 📁 Estrutura do projeto

```
api-gerenciador-tarefas/
├── app/
│   ├── main.py                 # Ponto de entrada da aplicação
│   ├── database.py             # Configuração da conexão (SQLite/PostgreSQL)
│   ├── models.py                # Modelos SQLAlchemy (Usuario, Tarefa)
│   ├── schemas.py                # Schemas Pydantic (validação e resposta)
│   ├── security.py               # Hash de senha e geração/validação de JWT
│   ├── crud.py                   # Operações de banco de dados
│   ├── dependencies.py           # Dependency de autenticação
│   └── routers/
│       ├── auth.py               # Rotas de registro e login
│       └── tarefas.py            # Rotas CRUD de tarefas
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚙️ Como executar

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/api-gerenciador-tarefas.git
cd api-gerenciador-tarefas
```

### 2. Crie um ambiente virtual (recomendado)
```bash
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/macOS
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Execute a API
```bash
uvicorn app.main:app --reload
```

### 5. Acesse a documentação interativa
Abra no navegador: **http://127.0.0.1:8000/docs**

> Por padrão, o projeto usa SQLite — nenhuma configuração de banco é necessária.
> Para usar PostgreSQL, veja o arquivo `.env.example`.

---

## 🔑 Como testar a autenticação pelo Swagger

1. Em `/docs`, abra **POST /auth/registrar** e crie uma conta
2. Abra **POST /auth/login** e informe e-mail/senha — copie o `access_token` retornado
3. Clique no botão **Authorize** (cadeado, no topo direito) e cole o token
4. Agora todas as rotas de `/tarefas` podem ser testadas autenticado

---

## 📚 Endpoints principais

| Método | Rota | Descrição | Autenticação |
|---|---|---|---|
| POST | `/auth/registrar` | Cria uma nova conta | Não |
| POST | `/auth/login` | Autentica e retorna o token JWT | Não |
| GET | `/tarefas/` | Lista as tarefas do usuário | Sim |
| POST | `/tarefas/` | Cria uma nova tarefa | Sim |
| GET | `/tarefas/{id}` | Retorna uma tarefa específica | Sim |
| PUT | `/tarefas/{id}` | Atualiza uma tarefa | Sim |
| DELETE | `/tarefas/{id}` | Exclui uma tarefa | Sim |

---

## 🧪 Testando via terminal (exemplo com curl)

```bash
# Registrar
curl -X POST http://127.0.0.1:8000/auth/registrar \
  -H "Content-Type: application/json" \
  -d '{"nome": "Seu Nome", "email": "voce@email.com", "senha": "senha123"}'

# Login
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "voce@email.com", "senha": "senha123"}'

# Criar tarefa (substitua SEU_TOKEN pelo access_token retornado no login)
curl -X POST http://127.0.0.1:8000/tarefas/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer SEU_TOKEN" \
  -d '{"titulo": "Minha primeira tarefa", "prioridade": "alta"}'
```

---

## 🔮 Possíveis melhorias futuras

- Testes automatizados com `pytest`
- Paginação na listagem de tarefas
- Deploy em nuvem (Render, Railway ou Fly.io)

---

## 👨‍💻 Autor

**Matheus Bittencourt**  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/matheus-bittencourt-3b31a3177)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)](https://github.com/mathbittencourt10-netizen)
