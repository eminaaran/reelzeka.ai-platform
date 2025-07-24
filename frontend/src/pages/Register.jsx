// src/pages/Register.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import apiClient from '../api';
import './Register.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const Register = ({ setUser }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState(''); // Şifre onayı için
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // CSRF token'ı almak için
  useEffect(() => {
    apiClient.get('/csrf/').catch(err => console.error("CSRF token alınamadı:", err));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    if (password !== password2) {
      setError("Şifreler eşleşmiyor.");
      setIsLoading(false);
      return;
    }

    if (password.length < 8) {
        setError("Şifre en az 8 karakter olmalıdır.");
        setIsLoading(false);
        return;
    }

    try {
      const response = await apiClient.post('/register/', {
        username,
        password,
      });
      
      setUser(response.data); 
      navigate('/dashboard');
      
    } catch (err) {
      if (err.response && err.response.data) {
        const errorData = err.response.data;
        const errorMessages = Object.values(errorData).flat().join(' ');
        setError(errorMessages || 'Kayıt başarısız oldu. Lütfen tekrar deneyin.');
      } else {
        setError('Kayıt sırasında bir hata oluştu.');
      }
      console.error("Register error:", err);
    } finally {
        setIsLoading(false);
    }
  };

  return (
    <div className="login-page-container"> {/* Login sayfasından gelen ana sarmalayıcı */}
      {/* SOL SÜTUN */}
      <div className="login-column left-column">
        <div className="welcome-content">
          <h1 className="welcome-title">ReelZeka'ya Katıl!</h1>
          <p className="welcome-subtitle">YKS için yapay zeka destekli çalışma arkadaşın.</p>
          <ul className="feature-list">
            <li><i className="bi bi-lightbulb"></i> Akıllı Soru Üretici</li>
            <li><i className="bi bi-calendar-check"></i> Kişiselleştirilmiş Çalışma Planı</li>
            <li><i className="bi bi-chat-dots"></i> Anlık Sohbet Yardımı</li>
            <li><i className="bi bi-graph-up-arrow"></i> Haftalık İlerleme Takibi</li>
          </ul>
        </div>
      </div>

      {/* ORTA SÜTUN (ANA ODAK) */}
      <div className="login-column middle-column">
        <div className="login-form-wrapper">
          <div className="mascot-icon">
            <i className="bi bi-person-plus-fill"></i>
          </div>
          <h2>Hesap Oluştur</h2>
          {error && <div className="alert alert-danger">{error}</div>}
          <form onSubmit={handleSubmit} className="login-form" noValidate>
            <div className="input-group">
              <label htmlFor="username">Kullanıcı Adı</label>
              <input type="text" id="username" value={username} onChange={(e) => setUsername(e.target.value)} required autoComplete="username" />
            </div>
            <div className="input-group">
              <label htmlFor="password">Şifre</label>
              <input type="password" id="password" value={password} onChange={(e) => setPassword(e.target.value)} required autoComplete="new-password" />
            </div>
            <div className="input-group">
              <label htmlFor="password2">Şifreyi Onayla</label>
              <input type="password" id="password2" value={password2} onChange={(e) => setPassword2(e.target.value)} required autoComplete="new-password" />
            </div>
            <button type="submit" className="login-button" disabled={isLoading}>
              {isLoading ? 'Hesap Oluşturuluyor...' : 'Hesap Oluştur'}
            </button>
          </form>
        </div>
        <div className="signup-footer">
          <p>Zaten bir hesabın var mı? <Link to="/login">Buradan giriş yap</Link></p>
        </div>
      </div>

      {/* SAĞ SÜTUN */}
      <div className="login-column right-column">
        <div className="mockup-container">
          <div className="mockup-card card-1">
            <p><strong>Hedef:</strong> +50 Net</p>
            <div className="progress-bar">
              <div className="progress" style={{width: '75%'}}></div>
            </div>
          </div>
          <div className="mockup-card card-2">
            <i className="bi bi-book"></i>
            <p><strong>Sıradaki Konu:</strong> Fonksiyonlar</p>
          </div>
          <div className="mockup-card card-3">
            <i className="bi bi-chat-quote-fill"></i>
            <p>"Bu konuyu anlamadım, daha basit anlatır mısın?"</p>
          </div>
           <div className="mockup-card card-4">
            <i className="bi bi-check-circle-fill"></i>
            <p>Günlük 50 soru hedefin tamamlandı!</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;