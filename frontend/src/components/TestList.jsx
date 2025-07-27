import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';
import './TestList.css';

const TestList = () => {
    const [tests, setTests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [filter, setFilter] = useState('all'); // 'all', 'practice', 'mock'

    useEffect(() => {
        loadTests();
    }, []);

    const loadTests = async () => {
        try {
            setLoading(true);
            const response = await apiClient.get('/tests/');
            const data = response.data;
            console.log('Loaded all tests:', data); // Debug için
            setTests(Array.isArray(data) ? data : []);
            setError(null);
        } catch (err) {
            setError('Testler yüklenirken bir hata oluştu.');
            console.error('Test yükleme hatası:', err);
        } finally {
            setLoading(false);
        }
    };

    const filteredTests = tests.filter(test => {
        if (filter === 'all') return true;
        return test.type === filter;
    });

    if (loading) return <div className="loading">Testler yükleniyor...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="test-list-container">
            <div className="test-list-header">
                <h2>Testler</h2>
                <div className="test-filters">
                    <button 
                        className={filter === 'all' ? 'active' : ''} 
                        onClick={() => setFilter('all')}
                    >
                        Tümü
                    </button>
                    <button 
                        className={filter === 'practice' ? 'active' : ''} 
                        onClick={() => setFilter('practice')}
                    >
                        Alıştırmalar
                    </button>
                    <button 
                        className={filter === 'mock' ? 'active' : ''} 
                        onClick={() => setFilter('mock')}
                    >
                        Denemeler
                    </button>
                </div>
            </div>

            <div className="test-grid">
                {filteredTests.map(test => (
                    <div key={test.id} className="test-card">
                        <div className="test-card-header">
                            <h3>{test.title}</h3>
                            <span className={`test-type ${test.type}`}>
                                {test.type === 'practice' ? 'Alıştırma' : 'Deneme'}
                            </span>
                        </div>
                        <p className="test-description">{test.description}</p>
                        <div className="test-meta">
                            <span>
                                <i className="bi bi-clock"></i>
                                {test.duration} dakika
                            </span>
                            <span>
                                <i className="bi bi-question-circle"></i>
                                {test.questions_count} soru
                            </span>
                        </div>
                        <button className="start-test-button">
                            Teste Başla
                        </button>
                    </div>
                ))}
            </div>

            {filteredTests.length === 0 && (
                <div className="no-tests">
                    Bu kategoride henüz test bulunmuyor.
                </div>
            )}
        </div>
    );
};

export default TestList;
