import type { User } from '../../types/auth';
import './ChatHeader.css';

interface ChatHeaderProps {
  user: User | null;
  onLogout: () => Promise<void>;
  onClearChat: () => void;
}

export const ChatHeader = ({ user, onLogout, onClearChat }: ChatHeaderProps) => {
  const handleLogout = async () => {
    if (window.confirm('Deseja realmente sair?')) {
      await onLogout();
    }
  };

  const getInitials = (name: string) => {
    return name
      .split(' ')
      .map(n => n[0])
      .join('')
      .toUpperCase()
      .slice(0, 2);
  };

  return (
    <header className="chat-header">
      <div className="chat-header-content">
        <div className="chat-header-left">
          <div className="chat-header-logo">
            <div className="chat-header-logo-icon">🎨</div>
          </div>
          <h1 className="chat-header-title">Tintas AI</h1>
        </div>
        
        <div className="chat-header-right">
          <div className="chat-header-actions">
            <button 
              className="header-button secondary"
              onClick={onClearChat}
              title="Nova conversa"
            >
              Nova Conversa
            </button>
          </div>
          
          {user && (
            <div className="user-avatar" title={user.username}>
              {getInitials(user.username)}
            </div>
          )}
          
          <button 
            className="header-button-icon"
            onClick={handleLogout}
            title="Sair"
          >
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
              <polyline points="16 17 21 12 16 7"></polyline>
              <line x1="21" y1="12" x2="9" y2="12"></line>
            </svg>
          </button>
        </div>
      </div>
    </header>
  );
};
