import React, { useState, useEffect } from 'react';
import api from '../api';
import { X, Trash2, Save, CreditCard, Wallet, Building2, AlertTriangle, ShieldCheck, Repeat } from 'lucide-react';

export function AccountDetailModal({ cuenta, isOpen, onClose, onAccountUpdated, onAccountDeleted }) {
  const [activeTab, setActiveTab] = useState('general'); // 'general' o 'subscriptions'
  const [nombre, setNombre] = useState('');
  const [tipo, setTipo] = useState('Ahorros');
  const [topeDisplay, setTopeDisplay] = useState('');
  const [gastosMesActual, setGastosMesActual] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (cuenta) {
      setNombre(cuenta.nombre || '');
      setTipo(cuenta.tipo || 'Ahorros');
      
      const tope = parseFloat(cuenta.tope_gasto_mensual || 0);
      setTopeDisplay(tope > 0 ? Math.round(tope).toLocaleString('es-CO') : '');

      // Cargar gastos acumulados del mes para calcular la barra de consumo del presupuesto
      const cargarGastos = async () => {
        try {
          const res = await api.get(`/transacciones/?cuenta=${cuenta.id}&tipo=gasto`);
          const totalGastos = res.data.reduce((acc, t) => acc + parseFloat(t.monto), 0);
          setGastosMesActual(totalGastos);
        } catch {
          // Manejo silencioso
        }
      };
      cargarGastos();
    }
  }, [cuenta]);

  if (!isOpen || !cuenta) return null;

  // Formateador con puntos de miles
  const handleTopeChange = (e) => {
    const rawValue = e.target.value.replace(/\D/g, '');
    if (!rawValue) {
      setTopeDisplay('');
      return;
    }
    const formatted = parseInt(rawValue, 10).toLocaleString('es-CO');
    setTopeDisplay(formatted);
  };

  const handleGuardarCambios = async (e) => {
    e.preventDefault();
    if (!nombre.trim()) return;

    const topeNumerico = topeDisplay ? parseFloat(topeDisplay.replace(/\./g, '')) : 0;

    try {
      setLoading(true);
      setError('');
      await api.put(`/cuentas/${cuenta.id}/`, {
        nombre: nombre.trim(),
        tipo: tipo,
        tope_gasto_mensual: topeNumerico,
      });
      onAccountUpdated();
      onClose();
    } catch {
      setError('No se pudieron guardar los cambios en la cuenta.');
    } finally {
      setLoading(false);
    }
  };

  const handleEliminar = async () => {
    const confirmar = window.confirm(
      `¿Estás seguro de eliminar la cuenta "${cuenta.nombre}"? Se borrarán también todas sus transacciones vinculadas.`
    );
    if (!confirmar) return;

    try {
      setLoading(true);
      await api.delete(`/cuentas/${cuenta.id}/`);
      onAccountDeleted();
      onClose();
    } catch {
      setError('Ocurrió un error al eliminar la cuenta.');
    } finally {
      setLoading(false);
    }
  };

  // Cálculo del consumo del presupuesto
  const topeActual = parseFloat(cuenta.tope_gasto_mensual || 0);
  const porcentajeConsumido = topeActual > 0 ? Math.min(Math.round((gastosMesActual / topeActual) * 100), 100) : 0;
  
  const getBarColor = () => {
    if (porcentajeConsumido >= 100) return '#ef4444'; // Rojo si supera el 100%
    if (porcentajeConsumido >= 80) return '#f59e0b';  // Amarillo advertencia si supera el 80%
    return '#10b981'; // Verde seguro
  };

  return (
    <div style={styles.overlay} onClick={onClose}>
      <div style={styles.modalCard} onClick={(e) => e.stopPropagation()}>
        {/* Cabecera del Modal */}
        <div style={styles.header}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.8rem' }}>
            <div style={styles.iconBadge}>
              {tipo === 'Billetera Digital' ? (
                <Wallet size={22} color="#a855f7" />
              ) : tipo === 'Tarjeta de Crédito' ? (
                <CreditCard size={22} color="#f43f5e" />
              ) : (
                <Building2 size={22} color="#3b82f6" />
              )}
            </div>
            <div>
              <h3 style={styles.modalTitle}>{cuenta.nombre}</h3>
              <span style={styles.subtitle}>Gestión integral de cuenta y presupuestos</span>
            </div>
          </div>
          <button style={styles.closeBtn} onClick={onClose}>
            <X size={20} color="#cbd5e1" />
          </button>
        </div>

        {/* Pestañas de Navegación */}
        <div style={styles.tabsRow}>
          <button
            style={{ ...styles.tabBtn, ...(activeTab === 'general' ? styles.activeTab : {}) }}
            onClick={() => setActiveTab('general')}
          >
            Ajustes y Presupuesto
          </button>
          <button
            style={{ ...styles.tabBtn, ...(activeTab === 'subscriptions' ? styles.activeTab : {}) }}
            onClick={() => setActiveTab('subscriptions')}
          >
            Suscripciones (Próximamente)
          </button>
        </div>

        {activeTab === 'general' ? (
          <div>
            {/* Medidor de Presupuesto / Tope Mensual */}
            {topeActual > 0 ? (
              <div style={styles.budgetCard}>
                <div style={styles.budgetHeader}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    {porcentajeConsumido >= 80 ? (
                      <AlertTriangle size={18} color={getBarColor()} />
                    ) : (
                      <ShieldCheck size={18} color={getBarColor()} />
                    )}
                    <span style={{ fontWeight: 'bold', fontSize: '0.9rem' }}>
                      Consumo del Presupuesto Mensual
                    </span>
                  </div>
                  <span style={{ fontSize: '0.85rem', color: '#cbd5e1' }}>
                    ${Math.round(gastosMesActual).toLocaleString('es-CO')} /${Math.round(topeActual).toLocaleString('es-CO')}
                  </span>
                </div>

                <div style={styles.barBg}>
                  <div style={{ ...styles.barFill, width: `${porcentajeConsumido}%`, backgroundColor: getBarColor() }} />
                </div>

                <p style={{ ...styles.budgetStatusText, color: getBarColor() }}>
                  {porcentajeConsumido >= 100
                    ? '¡Atención! Has alcanzado o superado el tope de gasto establecido para esta cuenta.'
                    : porcentajeConsumido >= 80
                    ? 'Advertencia: Te estás aproximando al límite de gasto mensual.'
                    : `Has consumido el ${porcentajeConsumido}% de tu presupuesto mensual.`}
                </p>
              </div>
            ) : (
              <div style={styles.noBudgetCard}>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#94a3b8' }}>
                  Sin tope de gasto configurado. Define un valor en el campo de abajo para monitorear tus alertas.
                </p>
              </div>
            )}

            {/* Formulario de Edición */}
            <form onSubmit={handleGuardarCambios} style={styles.form}>
              <label style={styles.label}>Nombre de la Cuenta:</label>
              <input
                type="text"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                style={styles.input}
                required
              />

              <label style={styles.label}>Tipo de Cuenta:</label>
              <select value={tipo} onChange={(e) => setTipo(e.target.value)} style={styles.select}>
                <option value="Ahorros">Cuenta de Ahorros</option>
                <option value="Corriente">Cuenta Corriente</option>
                <option value="Billetera Digital">Billetera Digital</option>
                <option value="Tarjeta de Crédito">Tarjeta de Crédito</option>
              </select>

              <label style={styles.label}>Tope Máximo de Gasto Mensual ($):</label>
              <input
                type="text"
                placeholder="Ej: 500.000"
                value={topeDisplay}
                onChange={handleTopeChange}
                style={styles.input}
              />

              {error && <p style={styles.errorText}>{error}</p>}

              <div style={styles.actionsRow}>
                <button
                  type="button"
                  style={styles.deleteBtn}
                  onClick={handleEliminar}
                  disabled={loading}
                >
                  <Trash2 size={16} style={{ marginRight: '6px' }} /> Eliminar Cuenta
                </button>

                <button type="submit" style={styles.saveBtn} disabled={loading}>
                  <Save size={16} style={{ marginRight: '6px' }} /> Guardar Cambios
                </button>
              </div>
            </form>
          </div>
        ) : (
          /* Pestaña Reservada para Suscripciones Futuras */
          <div style={styles.subscriptionsPlaceholder}>
            <Repeat size={40} color="#8b5cf6" />
            <h4 style={{ margin: '0.8rem 0 0.4rem 0' }}>Módulo de Suscripciones Asociadas</h4>
            <p style={{ color: '#94a3b8', fontSize: '0.85rem', textAlign: 'center', maxWidth: '320px' }}>
              Próximamente podrás vincular cobros recurrentes (Netflix, Spotify, gimnasio) a esta cuenta y recibir notificaciones previas a cada débito.
            </p>
          </div>
        )}
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
    backgroundColor: 'rgba(0,0,0,0.75)',
    zIndex: 2500,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  },
  modalCard: {
    backgroundColor: '#1e293b',
    borderRadius: '1rem',
    padding: '1.8rem',
    width: '100%',
    maxWidth: '480px',
    border: '1px solid #334155',
  },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.2rem' },
  iconBadge: { backgroundColor: '#0f172a', padding: '0.6rem', borderRadius: '0.5rem' },
  modalTitle: { fontSize: '1.15rem', margin: 0, color: '#f8fafc' },
  subtitle: { fontSize: '0.8rem', color: '#94a3b8' },
  closeBtn: { backgroundColor: 'transparent', border: 'none', cursor: 'pointer' },
  tabsRow: { display: 'flex', borderBottom: '1px solid #334155', marginBottom: '1.2rem' },
  tabBtn: {
    flex: 1,
    padding: '0.6rem',
    backgroundColor: 'transparent',
    color: '#94a3b8',
    border: 'none',
    borderBottom: '2px solid transparent',
    cursor: 'pointer',
    fontSize: '0.85rem',
  },
  activeTab: { color: '#8b5cf6', borderBottomColor: '#8b5cf6', fontWeight: 'bold' },
  budgetCard: {
    backgroundColor: '#0f172a',
    padding: '1rem',
    borderRadius: '0.6rem',
    border: '1px solid #334155',
    marginBottom: '1.2rem',
  },
  budgetHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.6rem' },
  barBg: { height: '8px', backgroundColor: '#1e293b', borderRadius: '4px', overflow: 'hidden' },
  barFill: { height: '100%', transition: 'width 0.4s ease' },
  budgetStatusText: { fontSize: '0.78rem', marginTop: '0.6rem', marginBottom: 0 },
  noBudgetCard: {
    backgroundColor: '#0f172a',
    padding: '0.8rem 1rem',
    borderRadius: '0.6rem',
    border: '1px dashed #334155',
    marginBottom: '1.2rem',
  },
  form: { display: 'flex', flexDirection: 'column', gap: '0.7rem' },
  label: { fontSize: '0.82rem', color: '#cbd5e1' },
  input: { padding: '0.65rem', borderRadius: '0.5rem', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff', outline: 'none' },
  select: { padding: '0.65rem', borderRadius: '0.5rem', border: '1px solid #475569', backgroundColor: '#0f172a', color: '#fff', outline: 'none' },
  errorText: { color: '#f87171', fontSize: '0.8rem', margin: 0 },
  actionsRow: { display: 'flex', justifyContent: 'space-between', marginTop: '1.2rem', gap: '0.8rem' },
  deleteBtn: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#ef4444',
    color: '#fff',
    border: 'none',
    padding: '0.6rem 1rem',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    fontSize: '0.85rem',
    fontWeight: 'bold',
  },
  saveBtn: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#8b5cf6',
    color: '#fff',
    border: 'none',
    padding: '0.6rem 1rem',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    fontSize: '0.85rem',
    fontWeight: 'bold',
  },
  subscriptionsPlaceholder: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '2.5rem 1rem',
  },
};
