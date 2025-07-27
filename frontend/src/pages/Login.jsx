// src/pages/Login.jsx
import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import apiClient from '../apiClient';
import './Login.css';

const Login = ({ setUser }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    const getCsrfToken = async () => {
      console.log("Login Sayfası: CSRF token alımı başlatılıyor...");
      try {
        await apiClient.get('/csrf/');
        console.log("Login Sayfası: CSRF token başarıyla alındı.");
      } catch (err) {
        console.error("Login Sayfası: CSRF token alınamadı:", err);
        setError("Güvenlik anahtarı alınamadı. Lütfen sayfayı yenileyin.");
      }
    };
    getCsrfToken();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    console.log("Login Sayfası: handleSubmit çağrıldı.");
    setIsLoading(true);
    setError('');

    try {
      console.log("Login Sayfası: Giriş isteği gönderiliyor...");
      console.log("Login Sayfası: Kullanıcı Adı:", username);
      console.log("Login Sayfası: Şifre (gönderilmiyor, sadece varlığı kontrol ediliyor):");
      const response = await apiClient.post('/login/', { username, password });
      console.log("Login Sayfası: Giriş başarılı oldu:", response.data);
      setUser(response.data);
      navigate('/dashboard');
    } catch (err) {
      console.error("Login Sayfası: Giriş hatası:", err);
      if (err.response && err.response.data) {
        setError(err.response.data.error || 'Giriş başarısız. Lütfen kullanıcı adı veya şifrenizi kontrol edin.');
      } else {
        setError('Giriş sırasında bir sunucu hatası oluştu.');
      }
    } finally {
      setIsLoading(false);
      console.log("Login Sayfası: isLoading: false olarak ayarlandı.");
    }
  };

  return (
    <div className="login-page-container">
      <div className="login-card">
        <div className="login-logo">ReelZeka.ai</div>
        <h1 className="login-title">Tekrar Hoş Geldiniz!</h1>
        <p className="login-subtitle">Devam etmek için giriş yapın</p>

        {error && <div className="alert-danger">{error}</div>}

        <form onSubmit={handleSubmit} className="login-form" noValidate>
          <div className="input-group">
            <input
              type="text"
              id="username"
              placeholder="Kullanıcı Adı"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              autoComplete="username"
            />
          </div>
          <div className="input-group">
            <input
              type="password"
              id="password"
              placeholder="Şifre"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              autoComplete="current-password"
            />
          </div>
          <button type="submit" className="login-button" disabled={isLoading}>
            {isLoading ? 'Giriş Yapılıyor...' : 'Giriş Yap'}
          </button>
        </form>

        <div className="login-footer-links">
          <Link to="/forgot-password">Şifrenizi mi unuttunuz?</Link>
          <span>|</span>
          <Link to="/register">Hesabınız yok mu? Kaydolun</Link>
        </div>
      </div>
    </div>
  );
};

export default Login;