import React from 'react';
import { Bot, User } from 'lucide-react';
import { format } from 'date-fns';
import QuickReplies from './QuickReplies';

interface Message {
  id: string;
  content: string;
  type: 'user' | 'bot';
  timestamp: Date;
  suggestions?: string[];
  quickReplies?: string[];
}

interface ChatMessageProps {
  message: Message;
  onQuickReply: (reply: string) => void;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, onQuickReply }) => {
  const isBot = message.type === 'bot';

  return (
    <div className={`flex ${isBot ? 'justify-start' : 'justify-end'}`}>
      <div className={`flex items-start space-x-2 max-w-xs lg:max-w-md ${isBot ? 'flex-row' : 'flex-row-reverse'}`}>
        {/* Avatar */}
        <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
          isBot 
            ? 'bg-gradient-to-r from-primary-500 to-secondary-500' 
            : 'bg-gray-300'
        }`}>
          {isBot ? (
            <Bot className="w-4 h-4 text-white" />
          ) : (
            <User className="w-4 h-4 text-gray-600" />
          )}
        </div>

        {/* Message Content */}
        <div className={`flex flex-col ${isBot ? 'items-start' : 'items-end'}`}>
          <div className={`px-4 py-2 rounded-lg ${
            isBot 
              ? 'bg-gray-100 text-gray-900' 
              : 'bg-primary-600 text-white'
          }`}>
            <p className="text-sm whitespace-pre-wrap">{message.content}</p>
          </div>
          
          {/* Timestamp */}
          <span className="text-xs text-gray-500 mt-1">
            {format(message.timestamp, 'HH:mm')}
          </span>

          {/* Quick Replies */}
          {isBot && message.quickReplies && message.quickReplies.length > 0 && (
            <div className="mt-2">
              <QuickReplies 
                replies={message.quickReplies} 
                onReply={onQuickReply} 
              />
            </div>
          )}

          {/* Suggestions */}
          {isBot && message.suggestions && message.suggestions.length > 0 && (
            <div className="mt-2">
              <p className="text-xs text-gray-500 mb-1">Suggestions:</p>
              <div className="flex flex-wrap gap-1">
                {message.suggestions.map((suggestion, index) => (
                  <button
                    key={index}
                    onClick={() => onQuickReply(suggestion)}
                    className="text-xs bg-gray-200 hover:bg-gray-300 text-gray-700 px-2 py-1 rounded transition-colors"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ChatMessage; 