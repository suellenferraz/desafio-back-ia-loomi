# Frontend - Chat com IA Tintas Suvinil

Interface web em React + TypeScript para interagir com o agente de IA especializado em tintas.

## 🚀 Tecnologias

- **React 18** com TypeScript
- **Vite** como build tool
- **React Router** para navegação
- **Axios** para requisições HTTP
- **CSS puro** (sem bibliotecas de UI)

## 📋 Pré-requisitos

- Node.js 18+ e npm
- Backend rodando:
  - `back-api` na porta 8000
  - `agente-ia` na porta 8001

## 🔧 Instalação

1. Instale as dependências:
```bash
npm install
```

2. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```

Edite o arquivo `.env` se necessário:
```env
VITE_BACK_API_URL=http://localhost:8000
VITE_AGENT_API_URL=http://localhost:8001
```

## 🏃 Executando

### Desenvolvimento

```bash
npm run dev
```

O frontend estará disponível em `http://localhost:5173`

### Build para produção

```bash
npm run build
```

Os arquivos estarão em `dist/`

### Preview da build

```bash
npm run preview
```

## 📁 Estrutura do Projeto

```
front/
├── src/
│   ├── components/       # Componentes reutilizáveis
│   │   ├── Chat/        # Componentes do chat
│   │   └── Login/       # Componentes de login
│   ├── hooks/           # Custom hooks
│   │   ├── useAuth.ts   # Hook de autenticação
│   │   └── useChat.ts   # Hook do chat
│   ├── pages/           # Páginas da aplicação
│   ├── services/        # Serviços de API
│   │   ├── api.ts       # Configuração do Axios
│   │   ├── authService.ts
│   │   └── chatService.ts
│   ├── types/           # Tipos TypeScript
│   ├── config/          # Configurações
│   └── App.tsx          # Componente principal
├── public/              # Arquivos estáticos
└── package.json
```

## 🔐 Autenticação

### Login

O frontend se conecta ao endpoint `POST /api/v1/account/login` do `back-api`.

**Importante**: O backend atual retorna apenas `UserResponseSchema` e define um cookie httpOnly. Para funcionar corretamente com `localStorage`, o backend precisa retornar o token JWT no body da resposta.

**Solução temporária**: O frontend gera um token temporário baseado no user ID. Para produção, ajuste o backend para retornar o token no body do login.

### Logout

O frontend chama `DELETE /api/v1/account/logout` e limpa os dados locais.

### Proteção de Rotas

Rotas protegidas verificam autenticação e roles (RBAC) antes de permitir acesso.

## 💬 Chat

### Funcionalidades

- Envio de mensagens para o agente de IA
- Persistência de `conversation_id` no localStorage
- Exibição de mensagens em ordem cronológica
- Indicador de loading durante processamento
- Suporte básico a markdown (negrito, itálico, quebras de linha)
- Scroll automático para última mensagem
- Diferenciação visual entre mensagens do usuário e assistente

### Endpoint

O chat se conecta ao endpoint `POST /api/v1/chat` do `agente-ia`.

**Payload**:
```json
{
  "message": "texto da mensagem",
  "conversation_id": "uuid-opcional"
}
```

**Response**:
```json
{
  "response": "resposta do agente",
  "conversation_id": "uuid",
  "reasoning": "raciocínio (opcional)",
  "tools_used": ["tool1", "tool2"]
}
```

## 🎨 Estilos

Todos os estilos são CSS puro, organizados por componente:
- `components/Chat/*.css`
- `components/Login/*.css`
- `App.css` e `index.css` para estilos globais

## 🔒 RBAC (Role-Based Access Control)

O frontend verifica roles do usuário para controlar acesso:

- **user**: Acesso ao chat
- **admin**: Acesso ao chat + telas administrativas (futuro)
- **super_admin**: Acesso completo (futuro)

## ⚠️ Notas Importantes

### CORS

O backend precisa ter CORS configurado para permitir requisições do frontend. Adicione no `back-api/main.py` e `agente-ia/main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # ou seu frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Token JWT

O backend atual define cookie httpOnly, mas o frontend precisa do token no header `Authorization`. Ajuste o backend para retornar o token no body do login ou implemente uma solução alternativa.

## 🐛 Troubleshooting

### Erro de CORS

Verifique se o CORS está configurado no backend e se a URL do frontend está na lista de origens permitidas.

### Token não funciona

Verifique se o backend retorna o token no body do login. Se não, ajuste o backend ou use a solução temporária implementada.

### Chat não responde

Verifique se:
1. O `agente-ia` está rodando na porta 8001
2. A variável `VITE_AGENT_API_URL` está correta
3. O backend está acessível

## 📝 Scripts Disponíveis

- `npm run dev` - Inicia servidor de desenvolvimento
- `npm run build` - Cria build de produção
- `npm run preview` - Preview da build
- `npm run lint` - Executa ESLint

## 📄 Licença

Este projeto faz parte do desafio técnico da Loomi.
