import { useAuth } from '../../hooks/useAuth';
import { useChat } from '../../hooks/useChat';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { ChatHeader } from './ChatHeader';
import './ChatContainer.css';
import './ChatSuggestions.css';

export const ChatContainer = () => {
  const { user, logout } = useAuth();
  const { messages, isLoading, error, sendMessage, clearChat } = useChat();

  const suggestions = [
    "Quero pintar meu quarto",
    "Tinta para fachada externa",
    "Qual cor combina com sala?",
    "Tinta lavável para cozinha"
  ];

  const handleSuggestionClick = (suggestion: string) => {
    sendMessage(suggestion);
  };

  return (
    <div className="chat-container">
      <ChatHeader user={user} onLogout={logout} onClearChat={clearChat} />
      
      <div className="chat-content">
        <MessageList messages={messages} isLoading={isLoading} />
        
        {error && (
          <div className="chat-error" role="alert">
            {error}
          </div>
        )}
        
        {messages.length === 0 && !isLoading && (
          <div className="chat-suggestions">
            {suggestions.map((suggestion, index) => (
              <button
                key={index}
                className="suggestion-button"
                onClick={() => handleSuggestionClick(suggestion)}
                disabled={isLoading}
              >
                {suggestion}
              </button>
            ))}
          </div>
        )}
        
        <ChatInput onSendMessage={sendMessage} disabled={isLoading} />
      </div>
    </div>
  );
};
