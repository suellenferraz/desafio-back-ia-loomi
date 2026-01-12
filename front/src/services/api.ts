import axios from 'axios';
import type { AxiosInstance, AxiosError } from 'axios';
import { config } from '../config/env';

// Criar instâncias do axios para cada API
export const backApi: AxiosInstance = axios.create({
  baseURL: config.backApiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const agentApi: AxiosInstance = axios.create({
  baseURL: config.agentApiUrl,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token nas requisições do back-api
backApi.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('auth_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros
const handleError = (error: AxiosError) => {
  if (error.response) {
    // Erro com resposta do servidor
    const status = error.response.status;
    const data = error.response.data as { detail?: string };
    
    switch (status) {
      case 401:
        // Token inválido ou expirado
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user');
        window.location.href = '/login';
        throw new Error('Sessão expirada. Faça login novamente.');
      case 403:
        throw new Error(data.detail || 'Acesso negado.');
      case 404:
        throw new Error('Recurso não encontrado.');
      case 500:
        throw new Error('Erro interno do servidor. Tente novamente.');
      default:
        throw new Error(data.detail || 'Erro ao processar requisição.');
    }
  } else if (error.request) {
    // Erro de rede
    throw new Error('Erro de conexão. Verifique sua internet.');
  } else {
    throw new Error('Erro ao processar requisição.');
  }
};

backApi.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(handleError(error));
  }
);

agentApi.interceptors.response.use(
  (response) => response,
  (error) => {
    return Promise.reject(handleError(error));
  }
);
