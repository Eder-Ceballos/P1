import React from 'react';
import { Home, BarChart3, Bot, LogOut, X } from 'lucide-react';

export function Sidebar({ activeView, setActiveView, isOpen, setIsOpen, usuario, onLogout }) {
  if (!isOpen) return null;

  const navItems = [
    { id: 'dashboard', label: 'Inicio / Cuentas', icon: Home },
    { id: 'analytics', label: 'Reportes y Estadísticas', icon: BarChart3 },
    { id: 'ai-assistant', label: 'Asistente IA (Próximamente)', icon: Bot, disabled: true },
  ];

  return (
    <div style={styles.overlay} onClick={() => setIsOpen(false)}>
      <div style={styles.sidebar} onClick={(e) => e.stopPropagation()}>
        <div style={styles.header}>
          <h2 style={styles.brand}>Finanzas App</h2>
          <button style={styles.closeBtn} onClick={() => setIsOpen(false)}>
            <X size={20} color="#cbd5e1" />
          </button>
        </div>

        <nav style={styles.nav}>
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                disabled={item.disabled}
                onClick={() => {
                  if (!item.disabled) {
                    setActiveView(item.id);
                    setIsOpen(false);
                  }
                }}
                style={{
                  ...styles.navItem,
                  ...(isActive ? styles.activeNavItem : {}),
                  ...(item.disabled ? styles.disabledNavItem : {}),
                }}
              >
                <Icon size={18} style={{ marginRight: '10px' }} />
                {item.label}
              </button>
            );
          })}
        </nav>

        <div style={styles.footer}>
          <p style={styles.userText}>{usuario?.nombre}</p>
          <button style={styles.logoutBtn} onClick={onLogout}>
            <LogOut size={16} style={{ marginRight: '8px' }} /> Salir
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    width: '100vw',
    height: '100vh',
    backgroundColor: 'rgba(0,0,0,0.6)',
    zIndex: 2000,
  },
  sidebar: {
    width: '260px',
    height: '100%',
    backgroundColor: '#1e293b',
    borderRight: '1px solid #334155',
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    padding: '1.5rem',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '2rem',
  },
  brand: {
    fontSize: '1.2rem',
    fontWeight: 'bold',
    color: '#8b5cf6',
  },
  closeBtn: {
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
  },
  nav: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
    flex: 1,
  },
  navItem: {
    display: 'flex',
    alignItems: 'center',
    padding: '0.75rem 1rem',
    borderRadius: '0.5rem',
    backgroundColor: 'transparent',
    color: '#cbd5e1',
    border: 'none',
    cursor: 'pointer',
    textAlign: 'left',
    fontSize: '0.9rem',
    fontWeight: '500',
  },
  activeNavItem: {
    backgroundColor: '#8b5cf6',
    color: '#ffffff',
    fontWeight: 'bold',
  },
  disabledNavItem: {
    color: '#64748b',
    cursor: 'not-allowed',
  },
  footer: {
    borderTop: '1px solid #334155',
    paddingTop: '1rem',
  },
  userText: {
    fontSize: '0.85rem',
    color: '#94a3b8',
    marginBottom: '0.5rem',
  },
  logoutBtn: {
    display: 'flex',
    alignItems: 'center',
    width: '100%',
    padding: '0.6rem',
    backgroundColor: '#ef4444',
    color: '#fff',
    border: 'none',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    fontSize: '0.85rem',
    fontWeight: 'bold',
  },
};
