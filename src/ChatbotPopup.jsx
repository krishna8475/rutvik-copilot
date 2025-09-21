import React, { useState, useRef, useEffect } from "react";
import logo from "./assets/logo.png";
import "./App.css";

export default function ChatbotPopup() {
  const [isOpen, setIsOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { sender: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const response = await fetch("http://localhost:5000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });

      const data = await response.json();

      if (data.reply) {
        setMessages([...newMessages, { sender: "bot", text: data.reply }]);
      } else {
        setMessages([...newMessages, { sender: "bot", text: "Error: No reply received" }]);
      }
    } catch (err) {
      setMessages([...newMessages, { sender: "bot", text: "Server error" }]);
    }
  };

  return (
    <div className="chatbot-container">
      {/* Main Button */}
      <button className="chatbot-toggle-btn" onClick={() => setIsOpen(!isOpen)}
        title="DealSummery AI"
        >
        
       <img src={logo} alt="logo" className="chat-logo" />
         Copilot
        </button>

      {/* Chat Popup */}
      {isOpen && (
        <div className="chat-popup">
          {/* Header */}
          <div className="chat-header">🤖 Chatbot</div>

          {/* Messages */}
          <div className="chat-messages">
            {messages.map((msg, idx) => (
              <div key={idx} className={msg.sender === "user" ? "chat-message user" : "chat-message bot"}>
                {msg.text}
              </div>
            ))}
            <div ref={messagesEndRef}></div>
          </div>

          {/* Input */}
          <div className="chat-input">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleSend()}
              placeholder="Type a message..."
            />
            <button onClick={handleSend}>Send</button>
          </div>
        </div>
      )}
    </div>
  );
}
