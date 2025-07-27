// frontend/src/pages/AdminDashboard.jsx
import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';
import { adminService } from '../services/adminService';
import './AdminDashboard.css';
import 'bootstrap-icons/font/bootstrap-icons.css';

// Admin panel için CSS değişkenlerini tanımla
const styles = {
  '--widget-bg': '#ffffff',
  '--bg-color': '#f5f5f5',
  '--text-color': '#333333',
  '--border-color': '#e0e0e0',
  '--hover-color': '#f0f0f0',
  '--turquoise': '#00bcd4',
  '--text-secondary': '#666666',
  '--input-bg': '#ffffff'
};

const AdminDashboard = () => {
  const [models, setModels] = useState([]);
  const [selectedModel, setSelectedModel] = useState(null);
  const [entries, setEntries] = useState([]);
  const [metadata, setMetadata] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [editingEntry, setEditingEntry] = useState(null);

  useEffect(() => {
    const loadModels = async () => {
      try {
        setIsLoading(true);
        const modelList = await adminService.getModels();
        setModels(modelList);
        setError('');
      } catch (err) {
        console.error('API Error:', err);
        setError(err.response?.data?.detail || err.message || 'Modeller yüklenirken hata oluştu.');
      } finally {
        setIsLoading(false);
      }
    };

    loadModels();
  }, []);

  useEffect(() => {
    const loadModelData = async () => {
      if (selectedModel) {
        try {
          setIsLoading(true);
          const [entriesData, metadataData] = await Promise.all([
            adminService.getModelEntries(selectedModel.id),
            adminService.getModelMetadata(selectedModel.id)
          ]);
          setEntries(entriesData);
          setMetadata(metadataData);
        } catch (err) {
          setError('Model verileri yüklenirken hata oluştu.');
          console.error(err);
        } finally {
          setIsLoading(false);
        }
      }
    };

    loadModelData();
  }, [selectedModel]);

  const handleCreate = async (formData) => {
    try {
      await adminService.createEntry(selectedModel.id, formData);
      const updatedEntries = await adminService.getModelEntries(selectedModel.id);
      setEntries(updatedEntries);
    } catch (err) {
      setError('Kayıt oluşturulurken hata oluştu.');
      console.error(err);
    }
  };

  const handleUpdate = async (id, formData) => {
    try {
      await adminService.updateEntry(selectedModel.id, { ...formData, id });
      const updatedEntries = await adminService.getModelEntries(selectedModel.id);
      setEntries(updatedEntries);
      setEditingEntry(null);
    } catch (err) {
      setError('Kayıt güncellenirken hata oluştu.');
      console.error(err);
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Bu kaydı silmek istediğinizden emin misiniz?')) {
      try {
        await adminService.deleteEntry(selectedModel.id, id);
        const updatedEntries = await adminService.getModelEntries(selectedModel.id);
        setEntries(updatedEntries);
      } catch (err) {
        setError('Kayıt silinirken hata oluştu.');
        console.error(err);
      }
    }
  };

  if (isLoading) {
    return <div className="admin-container"><h1>Yükleniyor...</h1></div>;
  }

  if (error) {
    return <div className="admin-container"><h1>{error}</h1></div>;
  }

  const renderForm = (initialData = {}) => {
    if (!metadata) return null;

    return (
      <div className="admin-form">
        <h3>{initialData.id ? 'Kayıt Düzenle' : 'Yeni Kayıt'}</h3>
        <form onSubmit={(e) => {
          e.preventDefault();
          const formData = new FormData(e.target);
          const data = {};
          metadata.fields.forEach(field => {
            data[field.name] = formData.get(field.name);
          });
          
          if (initialData.id) {
            handleUpdate(initialData.id, data);
          } else {
            handleCreate(data);
          }
        }}>
          {metadata.fields.map(field => (
            <div key={field.name} className="form-group">
              <label htmlFor={field.name}>{field.verbose_name}</label>
              {field.choices ? (
                <select
                  name={field.name}
                  defaultValue={initialData[field.name] || ''}
                  required={field.required}
                >
                  <option value="">Seçiniz...</option>
                  {field.choices.map(choice => (
                    <option key={choice.value} value={choice.value}>
                      {choice.label}
                    </option>
                  ))}
                </select>
              ) : (
                <input
                  type={field.type === 'IntegerField' ? 'number' : 'text'}
                  name={field.name}
                  defaultValue={initialData[field.name] || ''}
                  required={field.required}
                />
              )}
              {field.help_text && <small>{field.help_text}</small>}
            </div>
          ))}
          <button type="submit" className="btn-primary">
            {initialData.id ? 'Güncelle' : 'Oluştur'}
          </button>
          {initialData.id && (
            <button type="button" className="btn-secondary" onClick={() => setEditingEntry(null)}>
              İptal
            </button>
          )}
        </form>
      </div>
    );
  };

  if (isLoading) {
    return <div className="admin-container">Yükleniyor...</div>;
  }

  if (error) {
    return <div className="admin-container">{error}</div>;
  }

  return (
    <div className="admin-container" style={styles}>
      <div className="admin-header">
        <h1>Admin Panel</h1>
      </div>

      <div className="admin-content">
        {/* Model Seçici */}
        <div className="model-selector">
          <h2>Modeller</h2>
          <div className="model-list">
            {models.map(model => (
              <button
                key={model.id}
                className={`model-button ${selectedModel?.id === model.id ? 'active' : ''}`}
                onClick={() => setSelectedModel(model)}
              >
                {model.app_label}.{model.model}
              </button>
            ))}
          </div>
        </div>

        {/* Model İçeriği */}
        {selectedModel && metadata && (
          <div className="model-content">
            <div className="model-header">
              <h2>{metadata.verbose_name_plural}</h2>
              <button className="btn-primary" onClick={() => setEditingEntry({})}>
                Yeni Ekle
              </button>
            </div>

            {/* Düzenleme Formu */}
            {editingEntry && renderForm(editingEntry)}

            {/* Veri Tablosu */}
            <div className="table-container">
              <table className="admin-table">
                <thead>
                  <tr>
                    {metadata.fields.map(field => (
                      <th key={field.name}>{field.verbose_name}</th>
                    ))}
                    <th>İşlemler</th>
                  </tr>
                </thead>
                <tbody>
                  {entries.map(entry => (
                    <tr key={entry.id}>
                      {metadata.fields.map(field => (
                        <td key={field.name}>
                          {field.choices
                            ? field.choices.find(c => c.value === entry[field.name])?.label
                            : entry[field.name]}
                        </td>
                      ))}
                      <td className="actions">
                        <button onClick={() => setEditingEntry(entry)}>
                          <i className="bi bi-pencil"></i>
                        </button>
                        <button onClick={() => handleDelete(entry.id)}>
                          <i className="bi bi-trash"></i>
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
