// src/pages/Login.jsx
import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../apiClient';

const Login = ({ setUser }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');

    try {
      const response = await apiClient.post('/login/', { username, password });
      setUser(response.data);
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.error || 'Giriş başarısız. Lütfen kullanıcı adı veya şifrenizi kontrol edin.');
      } else {
        setError('Giriş sırasında bir sunucu hatası oluştu.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-form-container">
        <div className="auth-logo">ReelZeka.ai</div>
        <h2 className="auth-title">Tekrar Hoş Geldiniz!</h2>
        <p className="auth-subtitle">Devam etmek için giriş yapın</p>

        {error && <div className="alert-danger">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form" noValidate>
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
          <button type="submit" className="auth-button" disabled={isLoading}>
            {isLoading ? 'Giriş Yapılıyor...' : 'Giriş Yap'}
          </button>
        </form>
    </div>
  );
};

export default Login;