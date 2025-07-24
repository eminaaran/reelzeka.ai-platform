// frontend/src/pages/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../api';
import './AdminDashboard.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // Bu endpoint'i daha sonra oluşturacağız
        const response = await apiClient.get('/api/admin/users/');
        setUsers(response.data);
      } catch (err) {
        setError('Veri yüklenemedi veya yetkiniz yok.');
        console.error(err);
      } finally {
        setIsLoading(false);
      }
    };

    fetchUsers();
  }, []);

  if (isLoading) {
    return <div className="admin-container"><h1>Yükleniyor...</h1></div>;
  }

  if (error) {
    return <div className="admin-container"><h1>{error}</h1></div>;
  }

  return (
    <div className="admin-container">
      <div className="admin-header">
        <h1>Kullanıcı Yönetimi</h1>
      </div>
      <table className="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Kullanıcı Adı</th>
            <th>Email</th>
            <th>Admin mi?</th>
            <th>Katılma Tarihi</th>
            <th>İşlemler</th>
          </tr>
        </thead>
        <tbody>
          {users.map(user => (
            <tr key={user.id}>
              <td>{user.id}</td>
              <td>{user.username}</td>
              <td>{user.email || '-'}</td>
              <td>{user.is_staff ? 'Evet' : 'Hayır'}</td>
              <td>{new Date(user.date_joined).toLocaleDateString()}</td>
              <td className="action-buttons">
                <button className="edit-btn" title="Düzenle"><i className="bi bi-pencil-square"></i></button>
                <button className="delete-btn" title="Sil"><i className="bi bi-trash-fill"></i></button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminDashboard;
