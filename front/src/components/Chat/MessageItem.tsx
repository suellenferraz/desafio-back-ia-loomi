import type { Message } from '../../types/chat';
import './MessageItem.css';

interface MessageItemProps {
  message: Message;
}

// Função melhorada para renderizar markdown e detectar URLs de imagem
const renderMarkdown = (text: string): { html: string; imageUrl: string | null } => {
  let imageUrl: string | null = null;
  let cleanText = text;
  
  // 1. Remover padrões problemáticos de markdown vazio ANTES de processar
  // Remove [Veja aqui](), [texto](), [imagem]() etc.
  cleanText = cleanText.replace(/\[([^\]]*)\]\(\)/g, '');
  // Remove ![texto](), ![imagem]() etc.
  cleanText = cleanText.replace(/!\[([^\]]*)\]\(\)/g, '');
  
  // 2. Detectar formato markdown de imagem: ![alt](url)
  const markdownImageRegex = /!\[([^\]]*)\]\((https?:\/\/[^\)]+)\)/g;
  const markdownMatch = markdownImageRegex.exec(text);
  
  if (markdownMatch) {
    imageUrl = markdownMatch[2]; // URL está no segundo grupo
    // Remover o markdown completo do texto
    cleanText = cleanText.replace(markdownImageRegex, '').trim();
  } else {
    // 3. Fallback: Detectar URLs diretas (mesmo sem extensão de arquivo)
    // URLs do Azure Blob Storage têm parâmetros de query, não extensão
    const urlRegex = /(https?:\/\/[^\s\)]+)/g;
    const urlMatch = text.match(urlRegex);
    
    if (urlMatch) {
      // Verificar se é uma URL de imagem (contém indicadores de imagem)
      const imageIndicators = ['blob.core.windows.net', 'dalle', 'image', 'img-', '.png', '.jpg', '.jpeg', '.gif', '.webp'];
      const isImageUrl = urlMatch.some(url => 
        imageIndicators.some(indicator => url.toLowerCase().includes(indicator))
      );
      
      if (isImageUrl) {
        imageUrl = urlMatch[0];
        // Remover URL do texto
        cleanText = cleanText.replace(urlRegex, '').trim();
      }
    }
  }
  
  // Limpar espaços duplos e quebras de linha extras
  cleanText = cleanText.replace(/\s+/g, ' ').trim();
  
  // Converter **texto** para <strong>texto</strong>
  let html = cleanText.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  // Converter *texto* para <em>texto</em>
  html = html.replace(/\*(.*?)\*/g, '<em>$1</em>');
  // Converter quebras de linha
  html = html.replace(/\n/g, '<br />');
  
  return { html, imageUrl };
};

export const MessageItem = ({ message }: MessageItemProps) => {
  const isUser = message.role === 'user';
  const { html, imageUrl } = renderMarkdown(message.content);

  return (
    <div className={`message-item ${isUser ? 'user' : 'assistant'}`}>
      <div className="message-content">
        {imageUrl && (
          <div className="message-image">
            <img src={imageUrl} alt="Simulação visual" loading="lazy" />
          </div>
        )}
        <div 
          className="message-text"
          dangerouslySetInnerHTML={{ __html: html }}
        />
        {message.timestamp && (
          <div className="message-timestamp">
            {new Date(message.timestamp).toLocaleTimeString('pt-BR', {
              hour: '2-digit',
              minute: '2-digit',
            })}
          </div>
        )}
      </div>
    </div>
  );
};
