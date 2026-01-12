# 🎨 Tintas Suvinil AI

Sistema de recomendação inteligente de tintas Suvinil, construído com **FastAPI**, **PostgreSQL** e **LangChain**, com foco em **agentes de IA**, **RAG (Retrieval-Augmented Generation)** e **geração visual com DALL-E**.

---

## 📋 Índice

- [Visão Geral](#visão-geral)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Como Executar](#como-executar)
  - [1. Clonar o projeto](#1-clonar-o-projeto)
  - [2. Configurar variáveis de ambiente](#2-configurar-variáveis-de-ambiente)
  - [3. Executar com Docker Compose](#3-executar-com-docker-compose)
  - [4. Popular banco de dados](#4-popular-banco-de-dados)
- [Funcionalidades](#funcionalidades)
- [API Endpoints](#api-endpoints)
- [Arquitetura e Decisões Técnicas](#arquitetura-e-decisões-técnicas)
- [Organização e Metodologia](#organização-e-metodologia)
- [Uso de IA no Desenvolvimento](#uso-de-ia-no-desenvolvimento)
- [O que foi priorizado](#o-que-foi-priorizado)
- [O que eu melhoraria com mais tempo](#o-que-eu-melhoraria-com-mais-tempo)
- [Variáveis de Ambiente](#variáveis-de-ambiente)
- [Health Checks](#health-checks)
- [Documentação Adicional](#documentação-adicional)

---

## Visão Geral

O sistema é um **Assistente Inteligente** que atua como especialista virtual em tintas Suvinil, ajudando pessoas a escolherem o produto ideal com base em contexto, dúvidas e preferências. A solução utiliza:

- **Agente Orquestrador** com raciocínio explicável e escolha inteligente de ferramentas
- **RAG (Retrieval-Augmented Generation)** para busca contextual de produtos
- **Geração Visual** com DALL-E para simulações de ambientes
- **Arquitetura de Microserviços** com Clean Architecture e DDD
- **Observabilidade Completa** do processo de decisão

### Exemplo de Interação

**Usuário:** "Quero pintar meu quarto, mas prefiro algo que seja fácil de limpar e sem cheiro forte. Tem alguma sugestão?"

**IA:** "Sugiro o tom Cinza Urbano da linha Suvinil Fosco Completo. É lavável, resistente à limpeza e tem tecnologia sem odor. O que acha?"

**Usuário:** "Quero pintar minha varanda de azul claro. Como ficaria?"

**IA:** "Para sua varanda, recomendo a Suvinil Fachada Protegida Azul Sereno. É resistente à chuva, tem proteção UV e antimofo, perfeita para ambientes externos. O que acha dessa opção?"
*[Imagem gerada automaticamente]*

---

## Arquitetura

```txt
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │────▶│  Back-API   │────▶│ PostgreSQL  │
│   (React)   │     │  (FastAPI)  │     │  (pgvector) │
└──────┬──────┘     └──────┬──────┘     └─────────────┘
       │                  │
       │                  │
       ▼                  ▼
┌─────────────┐     ┌─────────────┐
│  Agente-IA  │────▶│   OpenAI    │
│  (FastAPI)  │     │  (GPT/DALL-E│
└─────────────┘     └─────────────┘
```

### Componentes

1. **Frontend (React + TypeScript)**
   - Interface de chat moderna e responsiva
   - Autenticação JWT
   - Exibição de imagens geradas
   - Dark mode premium

2. **Back-API (FastAPI)**
   - CRUD de tintas, usuários e sessões
   - Autenticação e RBAC (JWT)
   - Busca semântica com embeddings (pgvector)
   - ETL Pipeline para popular banco

3. **Agente-IA (FastAPI)**
   - Agente LangChain com ferramentas especializadas
   - RAG para busca contextual
   - Geração visual com DALL-E
   - Memória de conversa persistente

4. **Banco de Dados (PostgreSQL + pgvector)**
   - Armazenamento de tintas com embeddings
   - Persistência de conversas
   - Suporte a busca vetorial

### Fluxo de Processamento

1. Usuário envia mensagem via frontend
2. Frontend autentica e envia para Agente-IA
3. Agente analisa contexto e decide qual ferramenta usar:
   - `retrieve_paint_context`: Busca tintas usando RAG
   - `visual_generation_tool`: Gera imagem com DALL-E
4. Agente consulta Back-API para dados de tintas
5. Resposta é formatada e retornada com reasoning e tools_used
6. Frontend exibe resposta e imagens automaticamente

---

## Tecnologias

### Backend
* **Python 3.11**
* **FastAPI** - Framework web assíncrono
* **SQLAlchemy 2.0** - ORM
* **Alembic** - Migrações de banco
* **PostgreSQL 15** - Banco relacional
* **pgvector** - Extensão para busca vetorial
* **Pydantic** - Validação de dados

### IA e ML
* **LangChain** - Framework para agentes
* **OpenAI API** - GPT-4o-mini, text-embedding-3-small, DALL-E 3
* **AsyncOpenAI** - Cliente assíncrono

### Frontend
* **React 18** - Framework UI
* **TypeScript** - Tipagem estática
* **Vite** - Build tool
* **Axios** - Cliente HTTP
* **React Router** - Roteamento

### Infraestrutura
* **Docker & Docker Compose** - Containerização
* **Nginx** - Servidor web para frontend

---

## Pré-requisitos

* **Docker** e **Docker Compose** instalados
* **Git** para clonar o repositório
* **Chave da API OpenAI** (`OPENAI_API_KEY`)

---

## Como Executar

### 1. Clonar o projeto

```bash
git clone <url-do-repositório>
cd desafio-back-ia-loomi
```

### 2. Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto (ou configure as variáveis no sistema):

```env
OPENAI_API_KEY=sua-chave-openai-aqui
```

**Nota:** As outras variáveis já estão configuradas no `docker-compose.yml` com valores padrão. Para produção, ajuste conforme necessário.

### 3. Executar com Docker Compose

```bash
# Subir todos os serviços (db, back-api, agente-ia, front)
docker-compose up --build

# Ou em modo detached (background)
docker-compose up --build -d

# Ver logs
docker-compose logs -f

# Parar todos os serviços
docker-compose down
```

A aplicação ficará disponível em:

* **Frontend:** `http://localhost:3000`
* **Back-API:** `http://localhost:8000`
* **Agente-IA:** `http://localhost:8001`
* **Swagger Back-API:** `http://localhost:8000/docs`
* **Swagger Agente-IA:** `http://localhost:8001/docs`

### 4. Popular banco de dados

Após subir os serviços, execute o pipeline ETL para popular o banco:

```bash
# Entrar no container do back-api
docker-compose exec back-api bash

# Executar o pipeline
python -m pipelines.runner
```

O pipeline irá:
1. Extrair dados de tintas (web scraping ou CSV)
2. Transformar e enriquecer os dados
3. Gerar embeddings automaticamente
4. Carregar no banco de dados

**Importante:** O pipeline requer `OPENAI_API_KEY` configurada para gerar embeddings.

---

## Funcionalidades

### 🤖 Agente IA Especializado

* **Raciocínio Explícito**: Processo de decisão transparente e auditável
* **Escolha Inteligente de Ferramentas**: Seleção automática baseada em contexto
* **Observabilidade Completa**: Logs estruturados de todo o processo
* **Memória de Conversa**: Contexto mantido entre interações

### 🔍 RAG (Retrieval-Augmented Generation)

* **Busca Semântica**: Utiliza embeddings para encontrar tintas relevantes
* **Contexto Enriquecido**: Respostas baseadas em dados reais do catálogo
* **Embeddings Automáticos**: Geração automática ao criar/atualizar tintas

### 🎨 Geração Visual

* **Simulações de Ambiente**: Geração de imagens com DALL-E 3
* **Contexto Inteligente**: Prompts otimizados baseados no ambiente (interno/externo)
* **Exibição Automática**: Imagens exibidas automaticamente no chat

### 🔐 Autenticação e Segurança

* **JWT Authentication**: Tokens seguros com expiração configurável
* **RBAC (Role-Based Access Control)**: Controle de acesso por roles (user, admin, super_admin)
* **Validação de Prompts**: Proteção contra prompt injection
* **Sessões Persistentes**: Gerenciamento de sessões no banco

### 📊 Observabilidade

* **Logs Estruturados**: Logs em JSON para fácil parsing
* **Reasoning Explicável**: Cada resposta inclui o raciocínio do agente
* **Tools Tracking**: Rastreamento de quais ferramentas foram utilizadas
* **Métricas de Performance**: Tempo de processamento e tamanho de respostas

---

## API Endpoints

### Back-API (`http://localhost:8000`)

#### Autenticação (`/api/v1/account`)

* `POST /signup` - Criar conta
* `POST /login` - Login (retorna JWT)
* `PUT /password` - Alterar senha
* `DELETE /logout` - Logout

#### Tintas (`/api/v1/paints`)

* `POST /` - Criar tinta (admin)
* `GET /{paint_id}` - Buscar tinta por ID
* `GET /` - Listar todas as tintas
* `PUT /{paint_id}` - Atualizar tinta (admin)
* `DELETE /{paint_id}` - Deletar tinta (admin)
* `POST /search` - Busca semântica (RAG)

#### Usuários (`/api/v1/users`) - Admin

* `POST /` - Criar usuário
* `GET /` - Listar usuários
* `PUT /{user_id}/activation` - Ativar usuário
* `DELETE /{user_id}/activation` - Desativar usuário
* `PUT /{user_id}/password` - Definir senha
* `PUT /{user_id}/roles/admin` - Conceder admin
* `DELETE /{user_id}/roles/admin` - Revogar admin

#### Health (`/api/v1/health`)

* `GET /` - Health check

### Agente-IA (`http://localhost:8001`)

#### Chat (`/api/v1/chat`)

* `POST /` - Enviar mensagem ao agente

**Request:**
```json
{
  "message": "Quero pintar meu quarto de azul",
  "conversation_id": "uuid-opcional",
  "user_id": "uuid-do-usuario"
}
```

**Response:**
```json
{
  "response": "Sugiro o tom Azul Sereno...",
  "conversation_id": "uuid",
  "reasoning": "Busquei tintas na base de dados usando busca semântica",
  "tools_used": ["retrieve_paint_context"]
}
```

#### Health (`/api/v1/health`)

* `GET /` - Health check
* `GET /ready` - Readiness check

---

## Arquitetura e Decisões Técnicas

### Clean Architecture + DDD

O projeto segue **Clean Architecture** e **Domain-Driven Design** de forma pragmática, inspirado em referências como o [fastapi-clean-example](https://github.com/ivan-borovets/fastapi-clean-example).

**Camadas:**

1. **Domain**: Regras de negócio puras, entidades e interfaces de repositórios
2. **Application**: Casos de uso, serviços de aplicação e agentes
3. **Infrastructure**: Implementações técnicas (banco, LLMs, logging)
4. **Presentation**: Controllers, rotas e schemas da API

**Benefícios:**
* Baixo acoplamento entre camadas
* Testabilidade facilitada
* Facilidade de evolução e manutenção
* Separação clara de responsabilidades

### Microserviços

**Decisão:** Separar `back-api` e `agente-ia` em serviços distintos.

**Motivação:**
* Escalabilidade independente
* Tecnologias diferentes (backend tradicional vs. IA)
* Isolamento de falhas
* Demonstração de conhecimento em arquitetura distribuída

**Trade-off:** Mais complexidade de deploy e comunicação entre serviços, mas alinhado a cenários reais.

### LangChain para Agentes

**Decisão:** Utilizar LangChain em vez de implementação customizada.

**Motivação:**
* Framework maduro e amplamente utilizado
* Facilita implementação de agentes com ferramentas
* Suporte nativo a memória e observabilidade
* Acelera desenvolvimento

**Alternativa descartada:** Implementação do zero (muito tempo e complexidade).

### RAG com Embeddings

**Decisão:** Busca semântica usando embeddings OpenAI e pgvector.

**Motivação:**
* Respostas baseadas em dados reais do catálogo
* Busca por similaridade semântica (não apenas palavras-chave)
* Escalável para grandes volumes de dados

**Implementação:**
* Embeddings gerados automaticamente ao criar/atualizar tintas
* Busca vetorial usando distância cosseno
* Integração transparente no agente

### DALL-E 3 para Geração Visual

**Decisão:** DALL-E 3 para simulações visuais.

**Motivação:**
* Diferencial valorizado no desafio
* Integração com ecossistema OpenAI
* Qualidade de imagem superior

**Implementação:**
* Prompts otimizados por ambiente (interno/externo)
* Tool especializada no LangChain
* Exibição automática no frontend

---

## Organização e Metodologia

### Gestão de Projeto

Para a gestão do projeto, utilizei o **GitHub Projects (Backlog)** integrado às issues, que serviram como base para a definição e organização das atividades. As issues foram categorizadas por meio de **labels**, permitindo uma visão clara do escopo e das responsabilidades envolvidas.

**Labels criadas:**
* `agente` - Tarefas relacionadas ao serviço de IA
* `back` - Tarefas relacionadas ao back-api
* `front` - Tarefas relacionadas ao frontend
* `documentação` - Tarefas de documentação
* `infraestrutura` - Tarefas de Docker, deploy, etc.
* `review` - Tarefas de revisão e refatoração

### GitFlow

A estratégia de versionamento seguiu o **GitFlow**, com a branch `main` como principal, a partir da qual foi criada a branch `develop`. Dentro da `develop`, organizei branches de feature específicas para cada frente do projeto:

* `feature/back-api` - Desenvolvimento da API principal
* `feature/agente-ia` - Desenvolvimento do agente de IA
* `feature/front` - Desenvolvimento do frontend

O desenvolvimento ocorreu de forma incremental nessas branches, com integração contínua na `develop` e, após validação e estabilidade, o merge final para a `main`.

### Gestão Ágil

A organização do trabalho seguiu uma abordagem ágil pragmática, sem a adoção formal de cerimônias do Scrum, mas inspirada em seus princípios. As demandas foram organizadas e priorizadas de forma incremental, permitindo foco nas entregas essenciais dentro do prazo do desafio, além de flexibilidade para adaptação ao longo do processo.

**Kanban no GitHub Projects:**

* **To Do** - Tarefas planejadas
* **Doing** - Tarefas em execução
* **Waiting for Test** - Aguardando testes
* **In Functional Test** - Em teste funcional
* **Done** - Concluídas
* **Close** - Fechadas

Essa estrutura proporcionou clareza sobre o estado das tarefas, facilitando o acompanhamento da evolução do projeto e a identificação de gargalos.

### Interpretação do Desafio

No início do processo, enfrentei uma limitação técnica relacionada à indisponibilidade do arquivo CSV com dados de exemplo. Como isso ocorreu durante o final de semana e não foi possível obter suporte imediato, optei por manter o andamento do pipeline. Como alternativa, concebi um **pipeline próprio para geração de dados**, inspirado no site de tintas da Suvinil, permitindo dar continuidade ao desenvolvimento sem bloquear o progresso.

A primeira etapa do projeto consistiu na interpretação detalhada do desafio. Anotei manualmente meu entendimento inicial e, em seguida, utilizei o ChatGPT como orientador para brainstorming, possibilitando uma definição objetiva das tarefas e prioridades.

---

## Uso de IA no Desenvolvimento

### Ferramentas Utilizadas

#### ChatGPT (OpenAI)

**Uso Principal:** Scrum Master virtual e orientador estratégico

**Aplicações:**
* Organização do projeto e definição de issues
* Brainstorming de soluções arquiteturais
* Refinamento de requisitos e escopo
* Estruturação de textos e documentação
* Orientação em boas práticas (Clean Architecture, DDD, SOLID)

**Exemplo de Prompt:**
```
"Me ajude a seguir todos os passos, sendo um orientador para ter brainstorming."
```

#### Cursor

**Uso Principal:** Desenvolvimento acelerado e validação técnica

**Aplicações:**
* Acesso direto às documentações e projetos de referência
* Comparação de soluções e validação de abordagens
* Geração de código seguindo padrões do projeto
* Refatoração e melhoria de código existente
* Aumento significativo de produtividade

**Benefício:** Permite acesso contextual a documentações e projetos de referência, facilitando comparação de soluções e validação de abordagens técnicas.

### Como foi Utilizado

As ferramentas de IA foram usadas como **parceiras de desenvolvimento**, não como geradoras automáticas do projeto inteiro:

* **ChatGPT** ajudou principalmente em:
  * Planejamento estratégico e organização
  * Estruturação de arquitetura e decisões técnicas
  * Revisão e refinamento de documentação
  * Orientação em conceitos novos (DDD, Clean Architecture)

* **Cursor** foi fundamental para:
  * Acelerar escrita de código repetitivo
  * Validar padrões e boas práticas
  * Comparar com projetos de referência
  * Refatorar código existente

### Validação do Código Gerado

Todo código sugerido por IA foi:
* **Revisado manualmente** antes de entrar no projeto
* **Adaptado ao padrão do código existente** (nomes, estrutura, estilo)
* **Validado com**:
  * Execução local e testes manuais
  * Verificação de logs e endpoints
  * Revisão de arquitetura e boas práticas

**Responsabilidade:** A responsabilidade final pelo design, pelas decisões de arquitetura e pela implementação é minha. Nenhum trecho foi "copiado às cegas".

### Referências Utilizadas

* [fastapi-clean-example](https://github.com/ivan-borovets/fastapi-clean-example) - Referência principal para Clean Architecture com FastAPI

---

## O que foi priorizado

1. **Funcionalidades Core do Desafio**
   * Agente IA com ferramentas e memória
   * RAG com embeddings e busca semântica
   * Geração visual com DALL-E
   * Autenticação e RBAC

2. **Arquitetura Sólida**
   * Clean Architecture e DDD aplicados de forma pragmática
   * Separação em microserviços
   * Dependency Injection
   * Interfaces e abstrações

3. **Observabilidade**
   * Logs estruturados em JSON
   * Reasoning explicável nas respostas
   * Tracking de ferramentas utilizadas
   * Métricas de performance

4. **Frontend Completo (Plus)**
   * Interface moderna e responsiva
   * Dark mode premium
   * Exibição automática de imagens
   * Experiência de usuário fluida

5. **Documentação**
   * READMEs por serviço
   * Estrutura clara e organizada
   * Exemplos de uso

---

## O que eu melhoraria com mais tempo

Se tivesse mais tempo para evoluir este projeto, eu focaria em:

1. **Testes Automatizados**
   * Testes unitários para casos de uso
   * Testes de integração para APIs
   * Testes end-to-end para fluxos completos
   * Cobertura de código

2. **Cache e Performance**
   * Cache de embeddings para reduzir custos
   * Cache de respostas do agente
   * Otimização de queries no banco
   * Rate limiting

3. **Segurança Avançada**
   * Validação mais robusta de prompt injection
   * Rate limiting por usuário
   * Auditoria de ações administrativas
   * Criptografia de dados sensíveis

4. **Monitoramento e Alertas**
   * Integração com Prometheus/Grafana
   * Alertas para falhas e degradação
   * Dashboard de métricas de negócio
   * Tracing distribuído

5. **Melhorias no Agente**
   * Fine-tuning de prompts baseado em feedback
   * A/B testing de diferentes prompts
   * Suporte a múltiplos idiomas
   * Personalização por perfil de usuário

6. **CI/CD**
   * Pipeline de CI com testes automáticos
   * Deploy automatizado
   * Versionamento de APIs
   * Rollback automático

---

## Variáveis de Ambiente

### Back-API

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `DB_URL` | URL de conexão PostgreSQL | `postgresql://postgres:postgres@db:5432/tintas_db` |
| `SECURITY_SECRET_KEY` | Chave secreta para JWT | (configurar) |
| `SECURITY_ALGORITHM` | Algoritmo JWT | `HS256` |
| `SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES` | Expiração do token | `30` |
| `OPENAI_API_KEY` | Chave da API OpenAI | (obrigatório) |

### Agente-IA

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `OPENAI_API_KEY` | Chave da API OpenAI | (obrigatório) |
| `OPENAI_MODEL` | Modelo GPT | `gpt-4o-mini` |
| `OPENAI_EMBEDDING_MODEL` | Modelo de embeddings | `text-embedding-3-small` |
| `API_BASE_URL` | URL do back-api | `http://back-api:8000` |
| `DB_URL` | URL de conexão PostgreSQL | `postgresql://postgres:postgres@db:5432/tintas_db` |

### Frontend

| Variável | Descrição | Padrão |
|----------|-----------|--------|
| `VITE_BACK_API_URL` | URL do back-api | `http://localhost:8000` |
| `VITE_AGENT_API_URL` | URL do agente-ia | `http://localhost:8001` |

---

## Health Checks

* **Back-API:** `http://localhost:8000/api/v1/health`
* **Agente-IA:** `http://localhost:8001/api/v1/health`
* **Agente-IA (Readiness):** `http://localhost:8001/api/v1/health/ready`

---

## Documentação Adicional

Cada serviço possui seu próprio README com detalhes específicos:

* [`back-api/README.md`](./back-api/README.md) - Documentação da API principal
* [`agente-ia/README.md`](./agente-ia/README.md) - Documentação do agente de IA
* [`front/README.md`](./front/README.md) - Documentação do frontend

---

## Autor

Desenvolvido por Suellen Rayssa Barbosa Ferraz.

---

## Licença

Este projeto é privado e destinado apenas para avaliação técnica.
