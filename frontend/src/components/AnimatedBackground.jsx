import React from 'react';
import styles from './AnimatedBackground.module.css';
import { FiBarChart2, FiMessageSquare, FiCalendar, FiCheckSquare } from 'react-icons/fi';

const AnimatedBackground = ({ children }) => {
  return (
    <div className={styles.animatedBackgroundContainer}>
      {/* Floating UI Snippets */}
      <div className={`${styles.snippet} ${styles.snippet1}`}>
          <FiBarChart2 /> İlerleme Takibi
          <div className={styles.graphBar}></div>
      </div>
      <div className={`${styles.snippet} ${styles.snippet2}`}>
          <FiMessageSquare /> Fizik konusunda nasıl yardımcı olabilirim?
      </div>
      <div className={`${styles.snippet} ${styles.snippet3}`}>
          <FiCheckSquare /> Örnek Test Sorusu
      </div>
      <div className={`${styles.snippet} ${styles.snippet4}`}>
          <FiCalendar /> Çalışma Planı
      </div>
      
      {/* Sayfa içeriğini buraya yerleştir */}
      <div className={styles.contentContainer}>
        {children}
      </div>
    </div>
  );
};

export default AnimatedBackground;
