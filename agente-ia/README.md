## Estrutura do Projeto

```
agente-ia/
├── app/
│   ├── domain/                      # Camada de Domínio (regras de negócio)
│   │   ├── entities/                # Entidades de domínio
│   │   │   ├── conversation.py      # Entidade Conversation
│   │   │   └── message.py           # Entidade Message
│   │   └── repositories/            # Interfaces de repositórios (ABC)
│   │       └── conversation_repository.py
│   │
│   ├── application/                # Camada de Aplicação (casos de uso)
│   │   ├── agents/                  # Agentes de IA
│   │   │   └── paint_agent.py      # Agente principal de tintas
│   │   ├── services/                # Serviços de aplicação
│   │   │   ├── api_client.py       # Cliente HTTP para back-api
│   │   │   └── embedding_service.py # Serviço de embeddings
│   │   └── tools/                   # Ferramentas do LangChain
│   │       ├── paint_search_tool.py # Tool de busca de tintas (RAG)
│   │       └── visual_generation_tool.py # Tool de geração visual
│   │
│   ├── infrastructure/              # Camada de Infraestrutura
│   │   ├── config/                  # Configurações
│   │   │   └── settings.py          # Settings (Pydantic)
│   │   ├── llm/                     # Integração com LLMs
│   │   │   ├── openai_client.py     # Cliente OpenAI
│   │   │   └── prompt_templates/    # Templates de prompts
│   │   │       └── paint_prompt.py
│   │   ├── logging/                 # Sistema de logging
│   │   │   └── logger.py            # Configuração de logging estruturado
│   │   └── repositories/            # Implementações de repositórios
│   │       └── conversation_repository_impl.py
│   │
│   └── presentation/                # Camada de Apresentação (API)
│       └── api/
│           ├── dependencies/         # Dependency Injection
│           │   └── agent_dependencies.py
│           ├── routes/              # Rotas da API
│           │   ├── chat_routes.py   # Endpoint de chat
│           │   └── health_routes.py # Health checks
│           └── schemas/             # Schemas Pydantic
│               └── chat_schema.py
│
├── main.py                          # Entry point da aplicação
├── requirements.txt                 # Dependências Python
├── Dockerfile                       # Imagem Docker
├── .dockerignore                    # Arquivos ignorados no Docker
└── .env.example                     # Exemplo de variáveis de ambiente
```

## Instalação

### Passo 1: Criar ambiente virtual

```bash
python -m venv venv
```

### Passo 2: Ativar ambiente virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### Passo 3: Instalar dependências

```bash
pip install -r requirements.txt
```

### Passo 4: Configurar variáveis de ambiente

Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

Edite o `.env` e configure:

```env
OPENAI_API_KEY=sua-chave-openai-aqui
OPENAI_MODEL=gpt-4o-mini
OPENAI_EMBEDDING_MODEL=text-embedding-3-small
API_BASE_URL=http://localhost:8000
```

### Passo 5: Verificar se back-api está rodando

O agente-ia depende do back-api estar rodando na porta 8000:

```bash
curl http://localhost:8000/api/v1/health
```

### Passo 6: Iniciar o servidor

```bash
uvicorn main:app --reload --port 8001
```