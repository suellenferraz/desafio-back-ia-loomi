import { useState, useCallback, useEffect } from 'react';
import { chatService } from '../services/chatService';
import type { Message, ChatState } from '../types/chat';

interface UseChatReturn {
  messages: Message[];
  conversationId: string | null;
  isLoading: boolean;
  error: string | null;
  sendMessage: (content: string) => Promise<void>;
  clearChat: () => void;
}

export const useChat = (): UseChatReturn => {
  const [state, setState] = useState<ChatState>({
    messages: [],
    conversationId: null,
    isLoading: false,
    error: null,
  });

  // Carregar conversationId do localStorage ao montar
  useEffect(() => {
    const savedConversationId = localStorage.getItem('conversation_id');
    if (savedConversationId) {
      setState(prev => ({ ...prev, conversationId: savedConversationId }));
    }
  }, []);

  const sendMessage = useCallback(async (content: string) => {
    if (!content.trim()) return;

    // Adicionar mensagem do usuário imediatamente
    const userMessage: Message = {
      role: 'user',
      content: content.trim(),
      timestamp: new Date(),
    };

    setState(prev => ({
      ...prev,
      messages: [...prev.messages, userMessage],
      isLoading: true,
      error: null,
    }));

    try {
      const response = await chatService.sendMessage({
        message: content.trim(),
        conversation_id: state.conversationId || undefined,
      });

      // Adicionar resposta do assistente
      const assistantMessage: Message = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      // Atualizar conversationId
      const newConversationId = response.conversation_id;
      localStorage.setItem('conversation_id', newConversationId);

      setState(prev => ({
        ...prev,
        messages: [...prev.messages, assistantMessage],
        conversationId: newConversationId,
        isLoading: false,
        error: null,
      }));
    } catch (error: any) {
      setState(prev => ({
        ...prev,
        isLoading: false,
        error: error.message || 'Erro ao enviar mensagem',
      }));
    }
  }, [state.conversationId]);

  const clearChat = useCallback(() => {
    setState({
      messages: [],
      conversationId: null,
      isLoading: false,
      error: null,
    });
    localStorage.removeItem('conversation_id');
  }, []);

  return {
    messages: state.messages,
    conversationId: state.conversationId,
    isLoading: state.isLoading,
    error: state.error,
    sendMessage,
    clearChat,
  };
};
