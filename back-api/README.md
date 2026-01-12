## Estrutura do Projeto da API de CRUD para tintas, usuários e serviço de Auth

```
back-api/
├── app/                          # Módulo principal da aplicação
│   ├── domain/                   # Camada de Domínio (regras de negócio)
│   │   ├── entities/            # Entidades de domínio puras
│   │   │   ├── paint.py        # Entidade Paint (Tinta)
│   │   │   ├── user.py         # Entidade User (Usuário)
│   │   │   ├── session.py      # Entidade Session (Sessão)
│   │   │   └── product.py      # Entidade Product (exemplo/legado)
│   │   └── repositories/       # Interfaces de repositórios (ABC)
│   │       ├── paint_repository.py
│   │       ├── user_repository.py
│   │       └── session_repository.py
│   │
│   ├── application/             # Camada de Aplicação (casos de uso)
│   │   └── use_cases/          # Lógica de negócio isolada
│   │       ├── paint_use_cases.py
│   │       ├── auth_use_cases.py
│   │       ├── session_use_cases.py
│   │       └── product_use_cases.py
│   │
│   ├── infrastructure/          # Camada de Infraestrutura (detalhes técnicos)
│   │   ├── database/           # SQLAlchemy
│   │   │   ├── connection.py   # Conexão com banco
│   │   │   └── models/         # Models SQLAlchemy
│   │   │       ├── paint_model.py
│   │   │       ├── user_model.py
│   │   │       └── session_model.py
│   │   ├── repositories/       # Implementações dos repositórios
│   │   │   ├── paint_repository_impl.py
│   │   │   ├── user_repository_impl.py
│   │   │   └── session_repository_impl.py
│   │   ├── services/           # Serviços técnicos
│   │   │   ├── auth_service.py  # JWT, bcrypt
│   │   │   └── health_service.py
│   │   └── config/             # Configurações
│   │       └── settings.py     # Pydantic Settings
│   │
│   └── presentation/           # Camada de Apresentação (API)
│       └── api/
│           ├── routes/         # Endpoints FastAPI
│           │   ├── paint_routes.py    # CRUD Tintas
│           │   ├── account_routes.py  # Auth (signup, login, logout)
│           │   ├── user_routes.py     # Admin Users
│           │   ├── health_routes.py   # Health check
│           │   └── product_routes.py   # Exemplo (legado)
│           ├── schemas/         # Schemas Pydantic
│           │   ├── paint_schema.py
│           │   ├── auth_schema.py
│           │   ├── health_schema.py
│           │   └── product_schema.py
│           └── dependencies/   # Dependency Injection
│               └── auth_dependencies.py
│
├── alembic/                     # Migrations do banco de dados
│   ├── versions/               # Arquivos de migration
│   │   ├── efc272891e25_create_paints_table.py
│   │   ├── 82c0fb5a6b8f_create_users_table.py
│   │   └── 36646653677f_create_sessions_table.py
│   └── env.py                  # Configuração Alembic
│
├── main.py                      # Aplicação FastAPI
├── alembic.ini                  # Configuração Alembic
├── requirements.txt             # Dependências Python
├── Dockerfile                   # Imagem Docker
└── .dockerignore                # Arquivos ignorados no Docker
```

## Instalação

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual (Windows)
venv\Scripts\activate

# Ativar ambiente virtual (Linux/Mac)
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Utilize o .env.example como modelo para criar .env na raiz de back-api, configurando:
DB_URL=postgresql://postgres:senha@localhost:5432/tintas_db?options=-c timezone=UTC
'''
Para criar 'SECURITY_SECRET_KEY', abra o cmd e coloque 'python -c "import secrets; print(secrets.token_urlsafe(32))"'
'''
SECURITY_SECRET_KEY=sua_chave_secreta_minimo_32_caracteres
SECURITY_ALGORITHM=HS256
SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Execução

```bash
# Executar upgrade head
alembic upgrade head
```

```bash
# Executar servidor de desenvolvimento
uvicorn main:app --reload

# A API estará disponível em http://localhost:8000
# Documentação interativa em http://localhost:8000/docs
```