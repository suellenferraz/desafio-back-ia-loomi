import { useEffect, useRef } from 'react';
import type { Message } from '../../types/chat';
import { MessageItem } from './MessageItem';
import './MessageList.css';

interface MessageListProps {
  messages: Message[];
  isLoading: boolean;
}

export const MessageList = ({ messages, isLoading }: MessageListProps) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll automático para última mensagem
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div className="message-list" id="message-list">
      {messages.length === 0 && !isLoading && (
        <div className="empty-state">
          <div className="empty-state-icon">🎨</div>
          <h2 className="empty-state-title">Bem-vindo ao Tintas AI</h2>
          <p className="empty-state-description">
            Como posso ajudá-lo hoje?
          </p>
          <p className="empty-state-hint">
            Escolha uma sugestão abaixo ou escreva sua própria pergunta
          </p>
        </div>
      )}
      
      {messages.map((message, index) => (
        <MessageItem key={index} message={message} />
      ))}
      
      {isLoading && (
        <div className="loading-indicator">
          <div className="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <span className="loading-text">IA está pensando...</span>
        </div>
      )}
      <div ref={messagesEndRef} />
    </div>
  );
};
