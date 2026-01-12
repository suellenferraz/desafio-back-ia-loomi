import { agentApi } from './api';
import type { ChatRequest, ChatResponse } from '../types/chat';

export const chatService = {
  /**
   * Envia mensagem para o agente de IA
   */
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    try {
      const response = await agentApi.post<ChatResponse>('/api/v1/chat', request);
      return response.data;
    } catch (error: any) {
      throw new Error(error.message || 'Erro ao enviar mensagem');
    }
  },
};
