// frontend/src/components/AdminRoute.jsx
import React from 'react';
import { Navigate, Outlet } from 'react-router-dom';

const AdminRoute = ({ user }) => {
  // Kullanıcı giriş yapmış ve admin yetkisine sahip mi?
  if (user && user.is_staff) {
    return <Outlet />; // Evet ise, içindeki sayfayı (AdminDashboard) göster
  }

  // Giriş yapmamışsa veya admin değilse, ana sayfaya yönlendir
  return <Navigate to="/dashboard" replace />;
};

export default AdminRoute;
