import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';
import './QuickTest.css';

const QuickTest = () => {
    const [tests, setTests] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        loadTests();
    }, []);

    const loadTests = async () => {
        try {
            setLoading(true);
            const response = await apiClient.get('/tests/');
            const data = response.data;
            console.log('Loaded tests:', data); // Debug için

            // Sadece practice tipindeki testleri al ve en son 5 testi göster
            const practiceTests = Array.isArray(data) ? data
                .filter(test => test.type === 'practice')
                .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                .slice(0, 5) : [];

            console.log('Filtered practice tests:', practiceTests); // Debug için
            setTests(practiceTests);
            setError(null);
        } catch (err) {
            setError('Testler yüklenirken bir hata oluştu.');
            console.error('Test yükleme hatası:', err);
        } finally {
            setLoading(false);
        }
    };

    if (loading) return <div className="loading">Yükleniyor...</div>;
    if (error) return <div className="error">{error}</div>;

    return (
        <div className="quick-test-container">
            <h4 className="widget-title">
                <i className="bi bi-lightning-charge"></i>
                Hızlı Test
            </h4>
            <div className="quick-test-list">
                {tests.map(test => (
                    <div key={test.id} className="quick-test-item">
                        <div className="quick-test-info">
                            <h5>{test.title}</h5>
                            <div className="quick-test-meta">
                                <span><i className="bi bi-clock"></i> {test.duration} dk</span>
                                <span><i className="bi bi-question-circle"></i> {test.questions_count} soru</span>
                            </div>
                        </div>
                        <button className="quick-test-button">
                            <i className="bi bi-play-fill"></i>
                        </button>
                    </div>
                ))}
                {tests.length === 0 && (
                    <div className="no-tests">
                        Henüz hızlı test bulunmuyor.
                    </div>
                )}
            </div>
        </div>
    );
};

export default QuickTest;
