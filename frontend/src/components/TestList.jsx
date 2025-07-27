import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';
import TestRunner from './TestRunner';
import './TestList.css';

const TestList = () => {
    const [tests, setTests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedTest, setSelectedTest] = useState(null);

    useEffect(() => {
        loadTests();
    }, []);

    const loadTests = async () => {
        try {
            setLoading(true);
            const response = await apiClient.get('/tests/');
            if (response.data && Array.isArray(response.data)) {
                setTests(response.data);
                setError(null);
            } else {
                console.error('Beklenmeyen API yanıtı:', response.data);
                setTests([]);
                setError('Testler alınırken bir hata oluştu');
            }
        } catch (err) {
            console.error('Test yükleme hatası:', err.response?.data || err.message);
            setError('Testler yüklenirken bir hata oluştu. Lütfen daha sonra tekrar deneyin.');
            setTests([]);
        } finally {
            setLoading(false);
        }
    };

    if (loading) {
        return (
            <div className="test-list-container">
                <div className="loading">
                    <i className="fas fa-spinner fa-spin"></i> Testler yükleniyor...
                </div>
            </div>
        );
    }
    
    if (error) {
        return (
            <div className="test-list-container">
                <div className="error">
                    <div className="error-icon">⚠️</div>
                    <div className="error-message">{error}</div>
                    <button onClick={loadTests} className="retry-button">
                        Yeniden Dene
                    </button>
                </div>
            </div>
        );
    }

    return (
        <>
            <div className="test-list-container">
                <div className="test-list-header">
                    <h2>Mini Testler</h2>
                </div>
                {tests.length === 0 ? (
                    <div className="no-tests">Henüz test bulunmuyor</div>
                ) : (
                    <div className="test-grid">
                        {tests.map(test => (
                            <div key={test.id} className="test-card">
                                <div className="test-card-header">
                                    <h3>{test.title}</h3>
                                    <span className={`test-type ${test.type}`}>
                                        {test.type === 'practice' ? 'Alıştırma' : 'Deneme'}
                                    </span>
                                </div>
                                <p className="test-description">{test.description}</p>
                                <div className="test-meta">
                                    <span><i className="far fa-clock"></i>{test.duration} dk</span>
                                    <span><i className="far fa-question-circle"></i>{test.questionCount} Soru</span>
                                </div>
                                <button
                                    className="start-test-button"
                                    onClick={() => setSelectedTest(test.id)}
                                >
                                    Testi Başlat
                                </button>
                            </div>
                        ))}
                    </div>
                )}
            </div>

            {selectedTest && (
                <TestRunner
                    testId={selectedTest}
                    onClose={() => setSelectedTest(null)}
                />
            )}
        </>
    );
};

export default TestList;
