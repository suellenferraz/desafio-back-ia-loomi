export const config = {
  // URLs padrão - o navegador faz as requisições, então sempre usa localhost
  // ou a URL configurada via variável de ambiente
  backApiUrl: import.meta.env.VITE_BACK_API_URL || 'http://localhost:8000',
  agentApiUrl: import.meta.env.VITE_AGENT_API_URL || 'http://localhost:8001',
};
