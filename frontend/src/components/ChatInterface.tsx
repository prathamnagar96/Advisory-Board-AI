'use client';

import { useState, useEffect } from 'react';
import { Send, Mic, Search } from 'lucide-react';
import { askTaxQuestion, getToken } from '@/lib/api';

type Message = { id: string; text: string; isUser: boolean; timestamp: string; loading?: boolean };

export default function ChatInterface({ className }: { className?: string }) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // Mock initial message from the AI advisor
  useEffect(() => {
    setMessages([
      {
        id: 'msg_0',
        text: "Hello! I'm your Advisory Board AI assistant. I can help you with tax queries, document analysis, and financial planning. How can I assist you today?",
        isUser: false,
        timestamp: new Date().toISOString()
      }
    ]);
  }, []);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = {
      id: `msg_${Date.now()}`,
      text: input,
      isUser: true,
      timestamp: new Date().toISOString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const token = getToken();
      if (!token) {
        await new Promise(resolve => setTimeout(resolve, 700));
        throw new Error('Login required for live AI answers.');
      }

      const apiResponse = await askTaxQuestion(input);

      setMessages(prev => [
        ...prev,
        {
          id: `msg_${Date.now() + 1}`,
          text: apiResponse.answer,
          isUser: false,
          timestamp: new Date().toISOString()
        }
      ]);
    } catch (error: any) {
      setMessages(prev => [
        ...prev,
        {
          id: `msg_${Date.now() + 1}`,
          text: error?.message || "I ran into a hiccup. Try again in a moment.",
          isUser: false,
          timestamp: new Date().toISOString()
        }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col h-full ${className || ''}`}>
      <div className="flex items-center justify-between border-b border-gray-200 px-4 py-3">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-xl">A</span>
          </div>
          <div>
            <h3 className="text-lg font-semibold text-gray-900">Chat with AI Advisor</h3>
            <p className="text-xs text-gray-500">Ask me anything about taxes, investments, or financial planning</p>
          </div>
        </div>
        <div className="flex items-center space-x-2 text-sm text-gray-500">
          <Search className="h-4 w-4" />
          <span className="cursor-pointer hover:text-gray-700">Search chats</span>
        </div>
      </div>

      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div key={message.id} className="flex max-w-[80%]">
            {message.isUser ? (
              <>
                <div className="ml-auto flex flex-col">
                  <div className="flex items-end space-x-2">
                    <p className="text-sm text-white bg-blue-500 px-3 py-2 rounded-bl-lg rounded-br-lg rounded-tl-lg">
                      {message.text}
                    </p>
                    <span className="text-xs text-gray-400">
                      {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </span>
                  </div>
                </div>
              </>
            ) : (
              <>
                <div className="flex items-start space-x-2">
                  <div className="w-8 h-8 flex items-center justify-center rounded-full bg-blue-50 flex-shrink-0">
                    <span className="text-blue-600 text-bold">A</span>
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-start space-x-2">
                      <p className="text-sm text-gray-900 bg-white px-3 py-2 rounded-bl-lg rounded-br-lg rounded-tr-lg border border-gray-200">
                        {message.text}
                      </p>
                      <span className="text-xs text-gray-400">
                        {new Date(message.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                  </div>
                </div>
              </>
            )}
          </div>
        ))}
        {isLoading && (
          <div className="flex items-start space-x-2">
            <div className="w-8 h-8 flex items-center justify-center rounded-full bg-blue-50 flex-shrink-0">
              <span className="text-blue-600 text-bold">A</span>
            </div>
            <div className="flex flex-col">
              <div className="flex items-start space-x-2">
                <p className="text-sm text-gray-900 bg-white px-3 py-2 rounded-bl-lg rounded-br-lg rounded-tr-lg border border-gray-200">
                  Thinking...
                </p>
                <span className="text-xs text-gray-400">
                  {new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      <div className="border-t border-gray-200 px-4 py-3 flex items-center space-x-3">
        <div className="flex-1">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask your tax question..."
            className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
            rows={2}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
              }
            }}
          />
        </div>
        <div className="flex items-center space-x-2">
          <Mic className="h-5 w-5 text-gray-400 hover:text-gray-600 cursor-pointer" onClick={() => {/* Voice input would go here */ }} />
          <button
            onClick={sendMessage}
            disabled={isLoading || !input.trim()}
            className={`px-4 py-2 rounded-lg text-white font-medium ${isLoading || !input.trim()
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700'
              }`}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}