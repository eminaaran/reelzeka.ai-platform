// src/components/Navbar.jsx
import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Dropdown } from 'react-bootstrap';
import apiClient from '../api';
import './Navbar.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

const Navbar = ({ user, setUser }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await apiClient.post('/logout/');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('user');
      setUser(null);
      navigate('/login');
    }
  };

  const UserMenu = () => (
    <Dropdown className="user-menu-dropdown">
      <Dropdown.Toggle id="dropdown-custom-components">
        <div className="user-avatar">{user.username.charAt(0).toUpperCase()}</div>
        <span>{user.username}</span>
      </Dropdown.Toggle>

      <Dropdown.Menu>
        <Dropdown.Item as={Link} to="/profile">
          <i className="bi bi-person-circle"></i> Profil
        </Dropdown.Item>
        <Dropdown.Item as={Link} to="/settings">
          <i className="bi bi-gear"></i> Ayarlar
        </Dropdown.Item>
        <Dropdown.Divider />
        <Dropdown.Item as={Link} to="/premium" className="premium-link">
          <i className="bi bi-gem"></i> Premium'a Geç
        </Dropdown.Item>
        <Dropdown.Divider />
        <Dropdown.Item onClick={handleLogout}>
          <i className="bi bi-box-arrow-right"></i> Çıkış Yap
        </Dropdown.Item>
      </Dropdown.Menu>
    </Dropdown>
  );

  return (
    <nav className="main-navbar">
      <div className="navbar-content">
        <Link className="navbar-brand-custom" to={user ? "/dashboard" : "/"}>
          ReelZeka.ai
        </Link>
        <div>
          {user ? (
            <UserMenu />
          ) : (
            <Link to="/login" className="btn btn-primary">
              Giriş Yap
            </Link>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
