// src/App.jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet, Link } from 'react-router-dom';
import apiClient from './apiClient';

// Sayfalar ve bileşenler

import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import AdminDashboard from './pages/AdminDashboard';
import Navbar from './components/Navbar';
import AdminRoute from './components/AdminRoute'; // AdminRoute'u import et
import LandingPage from './pages/LandingPage'; // LandingPage'i import et

// Korumalı Rota Bileşeni
const PrivateRoute = ({ user }) => {
  return user ? <Outlet /> : <Navigate to="/" replace />;
};

// Admin sayfası için özel düzen
const AdminLayout = () => (
  <>
    <Outlet />
  </>
);

// Navbar'ı içeren genel sayfa düzeni
const MainLayout = ({ user, setUser }) => (
  <>
    <Navbar user={user} setUser={setUser} />
    <Outlet /> {/* Bu kısımda iç içe olan rotalar render edilecek */}
  </>
);

// ANA UYGULAMA BİLEŞENİ
function App() {
  const [user, setUser] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const checkUserAuth = async () => {
      try {
        // Önce CSRF cookie'sini almayı garanti et
        await apiClient.get('/csrf/');
        // Sonra kimlik kontrolü yap
        const response = await apiClient.get('/check-auth/');
        setUser(response.data);
      } catch (error) {
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    };
    checkUserAuth();
  }, []);

  return (
    <Router>
      {isLoading ? (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh', fontSize: '1.5rem' }}>Yükleniyor...</div>
      ) : (
        <Routes>
          {/* Ana giriş ve kayıt sayfası artık LandingPage */}
          <Route path="/" element={<LandingPage setUser={setUser} />} />

          {/* Eski rotalar kaldırıldı */}

          {/* Admin rotası - Navbar içermez */}
          <Route element={<AdminLayout />}>
            <Route element={<AdminRoute user={user} isLoading={false} />}>
              <Route path="/admin" element={<AdminDashboard />} />
            </Route>
          </Route>

          {/* Navbar GEREKTİREN, korumalı rotalar */}
          <Route element={<MainLayout user={user} setUser={setUser} />}>
            <Route element={<PrivateRoute user={user} isLoading={false} />}>
              <Route path="/dashboard" element={<Dashboard user={user} />} />
              {/* Diğer korumalı rotalar buraya */}
            </Route>
          </Route>

          {/* 404 Sayfası */}
          <Route path="*" element={
            <div className="text-center mt-5">
              <h2>404 - Sayfa Bulunamadı</h2>
              <Link to="/">Ana Sayfaya Dön</Link>
            </div>
          } />
        </Routes>
      )}
    </Router>
  );
}

export default App;
