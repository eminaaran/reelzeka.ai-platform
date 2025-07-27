// src/pages/Dashboard.jsx
import React, { useState, useEffect, useRef } from 'react';
import apiClient from '../apiClient';
import '../base.css';
import './Dashboard.css';
import 'bootstrap-icons/font/bootstrap-icons.css';
import TestList from '../components/TestList';

const TipCard = ({ icon, title, description }) => (
  <div className="tip-card">
    <i className={`bi ${icon} tip-card-icon`}></i>
    <div className="tip-card-content">
      <h5>{title}</h5>
      <p>{description}</p>
    </div>
  </div>
);

const Dashboard = () => {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');
  const [isAiResponding, setIsAiResponding] = useState(false);
  const chatContainerRef = useRef(null);
  const inputRef = useRef(null);
  const [progress, setProgress] = useState(75);

  useEffect(() => {
    setMessages([
      { id: 1, sender: 'ai', text: `Merhaba! Bugün ne öğrenmek istersin?` }
    ]);
    inputRef.current?.focus(); // Sayfa yüklendiğinde input'a odaklan
  }, []);

  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, isAiResponding]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (newMessage.trim() === '' || isAiResponding) return;

    const userMessage = { id: Date.now(), sender: 'user', text: newMessage };
    setMessages(prev => [...prev, userMessage]);
    const currentMessage = newMessage;
    setNewMessage('');
    setIsAiResponding(true);

    try {
      const response = await apiClient.post('/api/rag-query/', { question: currentMessage });
      const aiResponse = { id: Date.now() + 1, sender: 'ai', text: response.data.answer };
      setMessages(prev => [...prev, aiResponse]);
    } catch (error) {
      const errorResponse = { id: Date.now() + 1, sender: 'ai', text: 'Üzgünüm, bir sorun oluştu.' };
      setMessages(prev => [...prev, errorResponse]);
    } finally {
      setIsAiResponding(false);
      inputRef.current?.focus(); // Mesaj gönderildikten sonra input'a tekrar odaklan
    }
  };

  return (
    <div className="dashboard-container">
      {/* SOL SÜTUN */}
      <div className="dashboard-column left-column">
        <div className="widget weekly-goals">
          <h4 className="widget-title">Haftalık Hedefler</h4>
          <div className="progress-ring" style={{ background: `conic-gradient(var(--turquoise) ${progress}%, var(--border-color) 0)` }}>
            <div className="progress-ring-inner">{progress}%</div>
          </div>
        </div>
        <div className="widget study-schedule">
          <h4 className="widget-title">Çalışma Takvimi</h4>
          <ul>
            <li><i className="bi bi-calendar-check"></i> <strong>Yarın:</strong> TYT Matematik Tekrarı</li>
            <li><i className="bi bi-calendar-event"></i> <strong>Cuma:</strong> Paragraf Soru Çözümü</li>
          </ul>
        </div>
        <div className="widget motivation-badge">
           <i className="bi bi-fire"></i>
           <h4>5 Günlük Seri!</h4>
           <p>Harika gidiyorsun!</p>
        </div>
      </div>

      {/* ORTA SÜTUN */}
      <div className="dashboard-column middle-column">
        <div className="chat-container">
          <div className="chat-header">
            <h3>Sohbet Asistanı</h3>
          </div>
          <div className="chat-messages" ref={chatContainerRef}>
            {messages.map(msg => (
              <div key={msg.id} className={`message-bubble ${msg.sender}-message`}>
                {msg.text}
              </div>
            ))}
            {isAiResponding && (
              <div className="message-bubble ai-message">...</div>
            )}
          </div>
          <form className="chat-input-area" onSubmit={handleSendMessage}>
            <input 
              ref={inputRef}
              type="text" 
              placeholder="Merak ettiğin bir konuyu sor..." 
              value={newMessage}
              onChange={(e) => setNewMessage(e.target.value)}
              disabled={isAiResponding}
            />
            <button type="submit" disabled={isAiResponding || newMessage.trim() === ''}>
              <i className="bi bi-send-fill"></i>
            </button>
          </form>
        </div>
      </div>

      {/* SAĞ SÜTUN */}
      <div className="dashboard-column right-column">
        <div className="widget available-tests">
          <h4 className="widget-title">Mevcut Testler</h4>
          <TestList />
        </div>
        <div className="widget yks-quick-tips">
          <h4 className="widget-title">YKS Hızlı İpuçları</h4>
          <div className="tips-grid">
            <TipCard 
              icon="bi-lightbulb" 
              title="Fizik: Net Kuvvet Kuralı"
              description="Bir cisme etki eden net kuvvet, cismin kütlesi ile ivmesinin çarpımına eşittir (F=ma)."
            />
            <TipCard 
              icon="bi-book"
              title="Edebiyat: Teşbih Sanatı"
              description="Anlatımı güçlendirmek için, aralarında ortak özellik bulunan iki varlıktan zayıf olanın güçlü olana benzetilmesidir."
            />
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
