import React, { useState, useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import Login from './Login';
import Register from './Register';
import AnimatedBackground from '../components/AnimatedBackground';
import styles from './LandingPage.module.css';

const LandingPage = ({ setUser }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const [isFlipped, setIsFlipped] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    const mode = params.get('mode');
    if (mode === 'register') {
        setIsFlipped(true);
    } else {
        setIsFlipped(false);
    }
  }, [location.search]);

  const handleToggle = () => {
    setIsFlipped(!isFlipped);
    const newMode = !isFlipped ? 'register' : 'login';
    navigate(`/?mode=${newMode}`, { replace: true });
  };

  return (
    <AnimatedBackground>
        <div className={styles.heroContent}>
          <h1 className={styles.heroHeadline}>Potansiyelini Keşfet. <br/> YKS'ye Yapay Zeka ile Hakim Ol.</h1>
          <p className={styles.heroSubheadline}>Her derste, her adımda senin için kişiselleştirilmiş çalışma partnerin.</p>
        </div>

        <div className={`${styles.authCardFlipper} ${isFlipped ? styles.isFlipped : ''}`}>
            <div className={styles.authCardFront}>
                <Login setUser={setUser} />
                <p className={styles.authToggleLink}>
                    Hesabın yok mu?{' '}
                    <span onClick={handleToggle}>
                    Kayıt Ol
                    </span>
                </p>
            </div>
            <div className={styles.authCardBack}>
                <Register setUser={setUser} />
                <p className={styles.authToggleLink}>
                    Zaten bir hesabın var mı?{' '}
                    <span onClick={handleToggle}>
                    Giriş Yap
                    </span>
                </p>
            </div>
        </div>
    </AnimatedBackground>
  );
};

export default LandingPage;
