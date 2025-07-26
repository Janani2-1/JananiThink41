import React from 'react';

interface QuickRepliesProps {
  replies: string[];
  onReply: (reply: string) => void;
}

const QuickReplies: React.FC<QuickRepliesProps> = ({ replies, onReply }) => {
  return (
    <div className="flex flex-wrap gap-2">
      {replies.map((reply, index) => (
        <button
          key={index}
          onClick={() => onReply(reply)}
          className="px-3 py-1 bg-white border border-primary-300 text-primary-700 rounded-full text-sm hover:bg-primary-50 hover:border-primary-400 transition-colors"
        >
          {reply}
        </button>
      ))}
    </div>
  );
};

export default QuickReplies; 