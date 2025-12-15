import React, { useState, useRef, useEffect } from 'react';
import { sendMessage } from '../api/client';
import { Send, Bot, User, Loader2 } from 'lucide-react';

interface Message {
    id: string;
    role: 'user' | 'bot';
    content: string;
    timestamp: Date;
}

export const ChatInterface: React.FC = () => {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: '1',
            role: 'bot',
            content: 'Hello! I am your AI assistant. How can I help you today?',
            timestamp: new Date()
        }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        const userMessage: Message = {
            id: Date.now().toString(),
            role: 'user',
            content: input,
            timestamp: new Date()
        };

        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        try {
            const response = await sendMessage(userMessage.content);
            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'bot',
                content: response.response,
                timestamp: new Date()
            };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            console.error("Failed to send message", error);
            const errorMessage: Message = {
                id: (Date.now() + 1).toString(),
                role: 'bot',
                content: "Sorry, I encountered an error simulating the response. Please try again.",
                timestamp: new Date()
            };
            setMessages(prev => [...prev, errorMessage]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="chat-interface">
            {/* Header */}
            <header className="chat-header">
                <h1>AI Assistant</h1>
                <p>Powered by Root Agent</p>
            </header>

            {/* Messages Area */}
            <div className="messages-area custom-scrollbar">
                <div className="messages-list">
                    {messages.map((msg) => (
                        <div
                            key={msg.id}
                            className={`message-row ${msg.role === 'user' ? 'message-row-user' : ''}`}
                        >
                            <div className="avatar">
                                {msg.role === 'user' ? <User size={18} /> : <Bot size={18} />}
                            </div>

                            <div className="message-bubble">
                                <p>{msg.content}</p>
                                <span className="timestamp">
                                    {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                        </div>
                    ))}
                    {isLoading && (
                        <div className="message-row">
                            <div className="avatar bot-avatar">
                                <Bot size={18} />
                            </div>
                            <div className="message-bubble loading-bubble">
                                <Loader2 className="spinner" size={20} />
                            </div>
                        </div>
                    )}
                    <div ref={messagesEndRef} />
                </div>
            </div>

            {/* Input Area */}
            <form onSubmit={handleSend} className="input-area">
                <div className="input-wrapper">
                    <input
                        type="text"
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        placeholder="Type your message..."
                        disabled={isLoading}
                        className="chat-input"
                    />
                    <button
                        type="submit"
                        disabled={!input.trim() || isLoading}
                        className="send-button"
                    >
                        <Send size={20} />
                    </button>
                </div>
            </form>
        </div>
    );
};
