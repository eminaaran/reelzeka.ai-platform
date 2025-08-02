// src/pages/Register.jsx
import React, { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import apiClient from '../apiClient';

const Register = ({ setUser }) => {
  const navigate = useNavigate();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [password2, setPassword2] = useState('');
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = useCallback(async (e) => {
    e.preventDefault();
    setError('');

    if (password !== password2) {
      return setError("Şifreler eşleşmiyor.");
    }
    if (password.length < 8) {
        return setError("Şifre en az 8 karakter olmalıdır.");
    }

    setIsLoading(true);

    try {
      const response = await apiClient.post('/register/', { username, password });
      setUser(response.data);
      navigate('/dashboard');
    } catch (err) {
      if (err.response && err.response.data) {
        const errorData = err.response.data;
        const errorMessages = Object.values(errorData).flat().join(' ');
        setError(errorMessages || 'Kayıt başarısız oldu. Lütfen tekrar deneyin.');
      } else {
        setError('Kayıt sırasında bir sunucu hatası oluştu.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [username, password, password2, navigate, setUser]);

  return (
    <div className="auth-form-container">
        <div className="auth-logo">ReelZeka.ai</div>
        <h2 className="auth-title">Hesap Oluştur</h2>
        <p className="auth-subtitle">Yapay zeka destekli öğrenme macerasına katıl.</p>

        {error && <div className="alert-danger">{error}</div>}

        <form onSubmit={handleSubmit} className="auth-form" noValidate>
            <div className="input-group">
              <input 
                type="text" 
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
                placeholder="Şifre"
                value={password} 
                onChange={(e) => setPassword(e.target.value)} 
                required 
                autoComplete="new-password" 
              />
            </div>
            <div className="input-group">
              <input 
                type="password" 
                placeholder="Şifreyi Onayla"
                value={password2} 
                onChange={(e) => setPassword2(e.target.value)} 
                required 
                autoComplete="new-password" 
              />
            </div>
            <button type="submit" className="auth-button" disabled={isLoading}>
                {isLoading ? 'Hesap Oluşturuluyor...' : 'Ücretsiz Kaydol'}
            </button>
        </form>
    </div>
  );
};

export default Register;
