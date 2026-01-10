## Estrutura do Projeto

```
back-api/
├── app/                      # Módulo principal da aplicação
│   ├── domain/              # Camada de Domínio
│   │   └── entities/        # Entidades de negócio
│   │       └── product.py   # Entidade Product (exemplo)
│   ├── application/         # Camada de Aplicação
│   │   └── use_cases/      # Serviços e casos de uso
│   │       └── product_use_cases.py
│   ├── infrastructure/      # Camada de Infraestrutura (estrutura para futuro uso)
│   └── presentation/        # Camada de Apresentação
│       └── api/
│           ├── routes/      # Rotas FastAPI
│           │   └── product_routes.py
│           └── schemas/     # Schemas Pydantic
│               └── product_schema.py
├── main.py                  # Aplicação FastAPI
└── requirements.txt         # Dependências
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
```

## Execução

```bash
# Executar servidor de desenvolvimento
uvicorn main:app --reload

# A API estará disponível em http://localhost:8000
# Documentação interativa em http://localhost:8000/docs
```