// src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* BURADA <BrowserRouter> OLMAMALI */}
    <App />
    {/* BURADA </BrowserRouter> OLMAMALI */}
  </React.StrictMode>,
);