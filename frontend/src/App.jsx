import React, { useState, useEffect } from 'react';
import { UserSelection } from './components/UserSelection';
import { AccountsManager } from './components/AccountsManager';
import { AnalyticsDashboard } from './components/AnalyticsDashboard';
import { Sidebar } from './components/Sidebar';
import { Menu, LogOut } from 'lucide-react';

export default function App() {
  const [usuario, setUsuario] = useState(null);
  const [activeView, setActiveView] = useState('dashboard'); // 'dashboard' o 'analytics'
  const [sidebarOpen, setSidebarOpen] = useState(false);

  useEffect(() => {
    const sesionGuardada = localStorage.getItem('usuario_activo');
    if (sesionGuardada) {
      setUsuario(JSON.parse(sesionGuardada));
    }
  }, []);

  const handleCerrarSesion = () => {
    localStorage.removeItem('usuario_activo');
    setUsuario(null);
  };

  if (!usuario) {
    return <UserSelection onUserSelect={(u) => setUsuario(u)} />;
  }

  return (
    <div style={styles.appContainer}>
      {/* Menú Lateral Desplegable */}
      <Sidebar
        activeView={activeView}
        setActiveView={setActiveView}
        isOpen={sidebarOpen}
        setIsOpen={setSidebarOpen}
        usuario={usuario}
        onLogout={handleCerrarSesion}
      />

      {/* Navbar Superior */}
      <header style={styles.navbar}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button style={styles.menuBtn} onClick={() => setSidebarOpen(true)}>
            <Menu size={22} color="#f8fafc" />
          </button>
          <h1 style={styles.title}>Panel Financiero</h1>
        </div>

        <div style={styles.userSection}>
          <span style={styles.userName}>Usuario: {usuario.nombre}</span>
          <button onClick={handleCerrarSesion} style={styles.logoutButton}>
            <LogOut size={16} style={{ marginRight: '6px' }} /> Salir
          </button>
        </div>
      </header>

      {/* Contenido Dinámico */}
      <main style={styles.mainContent}>
        {activeView === 'dashboard' ? (
          <AccountsManager usuario={usuario} />
        ) : (
          <AnalyticsDashboard
            usuario={usuario}
            onBackToMain={() => setActiveView('dashboard')}
          />
        )}
      </main>
    </div>
  );
}

const styles = {
  appContainer: {
    backgroundColor: '#0f172a',
    minHeight: '100vh',
    width: '100vw',
    color: '#f8fafc',
    fontFamily: 'system-ui, sans-serif',
    boxSizing: 'border-box',
  },
  navbar: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '1.2rem 2rem',
    backgroundColor: '#1e293b',
    borderBottom: '1px solid #334155',
    width: '100%',
    boxSizing: 'border-box',
  },
  menuBtn: {
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
  },
  title: {
    fontSize: '1.3rem',
    fontWeight: 'bold',
  },
  userSection: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  userName: {
    fontSize: '0.95rem',
    color: '#cbd5e1',
  },
  logoutButton: {
    display: 'flex',
    alignItems: 'center',
    padding: '0.5rem 0.9rem',
    backgroundColor: '#ef4444',
    color: '#fff',
    border: 'none',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    fontSize: '0.85rem',
    fontWeight: 'bold',
  },
  mainContent: {
    maxWidth: '100%', // Ampliado para abarcar mejor pantallas anchas
    width: '100%',       // Ocupa el 95% del viewport de manera fluida
    boxSizing: 'border-box',
    padding: '1.5rem 2rem',
  },
};
