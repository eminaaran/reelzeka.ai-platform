import React, { useState, useEffect } from 'react';
import apiClient from '../apiClient';
import './TestRunner.css';

const TestRunner = ({ testId, onClose }) => {
    const [questions, setQuestions] = useState([]);
    const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
    const [answers, setAnswers] = useState({});
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [showResults, setShowResults] = useState(false);
    const [results, setResults] = useState(null);
    const [startTime, setStartTime] = useState(null);
    const [tempMessage, setTempMessage] = useState(null); // Yeni durum

    useEffect(() => {
        const fetchTest = async () => {
            try {
                const response = await apiClient.get(`/tests/${testId}/`);
                setQuestions(response.data.questions);
                setLoading(false);
                setStartTime(Date.now()); // Test başladığında zamanı kaydet
            } catch (err) {
                console.error('Test yükleme hatası:', err);
                setError('Sorular yüklenirken bir hata oluştu.');
                setLoading(false);
            }
        };

        fetchTest();
    }, [testId]);

    const handleAnswer = (questionId, option) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: option.text // Sadece şıkkın metin değerini kaydet
        }));
    };

    const handlePrevQuestion = () => {
        setCurrentQuestionIndex(prev => Math.max(0, prev - 1));
    };

    const handleNextQuestion = () => {
        setCurrentQuestionIndex(prev => Math.min(questions.length - 1, prev + 1));
    };

    const handleSubmit = async () => {
        try {
            const response = await apiClient.post(`/tests/${testId}/submit/`, {
                answers: answers,
                duration_taken: Math.floor((Date.now() - startTime) / 1000)
            });
            setTempMessage('Test kaydedildi!'); // Başarı mesajını ayarla
            setTimeout(() => {
                setResults(response.data);
                setShowResults(true);
                setTempMessage(null); // Mesajı temizle
            }, 1500); // 1.5 saniye sonra sonuçları göster
        } catch (err) {
            console.error("Test gönderme hatası:", err);
            if (err.response) {
                console.error("Backend hata yanıtı:", err.response.data);
                console.error("Backend hata durumu:", err.response.status);
            }
            setError('Test gönderilirken bir hata oluştu.'); // Hata mesajını koru
            setTempMessage(null); // Herhangi bir önceki mesajı temizle
        }
    };

    if (loading) {
        return (
            <div className="modal-overlay">
                <div className="test-modal">
                    <div className="loading">Yükleniyor...</div>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="modal-overlay">
                <div className="test-modal">
                    <div className="error">{error}</div>
                    <button onClick={onClose} className="close-button">✕</button>
                </div>
            </div>
        );
    }

    if (showResults) {
        return (
            <div className="modal-overlay">
                <div className="test-modal">
                    <div className="modal-header">
                        <h2>Test Sonuçları</h2>
                        <button onClick={onClose} className="close-button">✕</button>
                    </div>
                    <div className="results-container">
                        <div className="score">{results.score}%</div>
                        <div className="results-summary">
                            {results.totalQuestions} sorudan {results.correctAnswers} doğru
                        </div>
                        <button className="review-button" onClick={() => setShowResults(false)}>
                            Soruları Gözden Geçir
                        </button>
                    </div>
                </div>
            </div>
        );
    }

    const currentQuestion = questions[currentQuestionIndex];

    if (!currentQuestion) {
        return (
            <div className="modal-overlay">
                <div className="test-modal">
                    <div className="error">Bu testte henüz soru bulunmuyor veya yüklenemedi.</div>
                    <button onClick={onClose} className="close-button">✕</button>
                </div>
            </div>
        );
    }

    const progress = ((currentQuestionIndex + 1) / questions.length) * 100;

    return (
        <div className="modal-overlay">
            <div className="test-modal">
                {tempMessage && <div className="temp-message">{tempMessage}</div>} {/* Mesajı burada göster */}
                <div className="modal-header">
                    <h2>Mini Test</h2>
                    <button onClick={onClose} className="close-button">✕</button>
                </div>

                <div className="progress-bar">
                    <div className="progress-fill" style={{ width: `${progress}%` }} />
                </div>

                <div className="question-container">
                    <div className="question">
                        <div className="question-text">{currentQuestion.text}</div>
                        <div className="options">
                            {currentQuestion.options.map((option, index) => (
                                <div
                                    key={index}
                                    className={`option ${answers[currentQuestion.id] === option.text ? 'selected' : ''}`}
                                    onClick={() => handleAnswer(currentQuestion.id, option)}
                                    tabIndex="0"
                                    role="button"
                                >
                                    {option.text}
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                <div className="test-controls">
                    <button
                        className="nav-button prev-button"
                        onClick={handlePrevQuestion}
                        disabled={currentQuestionIndex === 0}
                    >
                        Önceki Soru
                    </button>
                    {currentQuestionIndex === questions.length - 1 ? (
                        <button className="nav-button submit-button" onClick={handleSubmit} disabled={!answers[currentQuestion.id]}>
                            Testi Bitir
                        </button>
                    ) : (
                        <button className="nav-button next-button" onClick={handleNextQuestion} disabled={!answers[currentQuestion.id]}>
                            Sonraki Soru
                        </button>
                    )}
                </div>
            </div>
        </div>
    );
};

export default TestRunner;
