import React, { useState, useEffect } from 'react';
import api from '../api';
import { History, ArrowUpRight, ArrowDownLeft, Edit2, Trash2, Filter, AlertCircle } from 'lucide-react';

export function TransactionHistory({ usuario, cuentas, onDataChanged }) {
  const [transacciones, setTransacciones] = useState([]);
  const [filtroTipo, setFiltroTipo] = useState(''); // '' (todos), 'gasto', 'ingreso'
  const [loading, setLoading] = useState(true);

  // Estado para la edición modal
  const [editingTx, setEditingTx] = useState(null);
  const [editMontoDisplay, setEditMontoDisplay] = useState('');
  const [editCuentaId, setEditCuentaId] = useState('');
  const [editDescripcion, setEditDescripcion] = useState('');
  const [editTipo, setEditTipo] = useState('gasto');
  const [errorEdit, setErrorEdit] = useState('');

  const cargarHistorial = async () => {
    try {
      setLoading(true);
      const url = filtroTipo ? `/transacciones/?tipo=${filtroTipo}` : '/transacciones/';
      const res = await api.get(url);
      
      // Filtrar solo las transacciones del usuario activo
      const userTx = res.data.filter((t) => t.usuario === usuario.id);
      setTransacciones(userTx);
    } catch {
      // Manejo silencioso de carga
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    cargarHistorial();
  }, [usuario.id, filtroTipo]);

  // Mapa para resolver el nombre de la cuenta según su ID de forma transparente
  const getNombreCuenta = (cuentaId) => {
    const cuenta = cuentas.find((c) => c.id === cuentaId);
    return cuenta ? cuenta.nombre : 'Cuenta';
  };

  // Abrir modal de edición prellenando campos
  const handleStartEdit = (tx) => {
    setEditingTx(tx);
    setEditTipo(tx.tipo);
    setEditCuentaId(tx.cuenta);
    setEditDescripcion(tx.descripcion);
    setEditMontoDisplay(Math.round(parseFloat(tx.monto)).toLocaleString('es-CO'));
    setErrorEdit('');
  };

  const handleEditMontoChange = (e) => {
    const rawValue = e.target.value.replace(/\D/g, '');
    if (!rawValue) {
      setEditMontoDisplay('');
      return;
    }
    setEditMontoDisplay(parseInt(rawValue, 10).toLocaleString('es-CO'));
  };

  const handleSaveEdit = async (e) => {
    e.preventDefault();
    if (!editMontoDisplay) return;

    const montoNumerico = parseFloat(editMontoDisplay.replace(/\./g, ''));

    try {
      setErrorEdit('');
      await api.put(`/transacciones/${editingTx.id}/`, {
        monto: montoNumerico,
        cuenta: parseInt(editCuentaId, 10),
        tipo: editTipo,
        descripcion: editDescripcion.trim(),
      });

      setEditingTx(null);
      cargarHistorial();
      onDataChanged(); // Recargar cuentas en el padre para actualizar saldos
    } catch {
      setErrorEdit('No se pudo guardar la modificación.');
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm('¿Deseas eliminar esta transacción? El saldo de la cuenta será reajustado.')) return;

    try {
      await api.delete(`/transacciones/${id}/`);
      cargarHistorial();
      onDataChanged();
    } catch {
      alert('Error al eliminar la transacción.');
    }
  };

  return (
    <div style={styles.card}>
      <div style={styles.header}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <History size={22} color="#8b5cf6" />
          <h3 style={styles.title}>Historial de Movimientos</h3>
        </div>

        {/* Filtros rápidos */}
        <div style={styles.filterContainer}>
          <button
            style={filtroTipo === '' ? styles.activeFilter : styles.inactiveFilter}
            onClick={() => setFiltroTipo('')}
          >
            Todos
          </button>
          <button
            style={filtroTipo === 'gasto' ? styles.activeFilterGasto : styles.inactiveFilter}
            onClick={() => setFiltroTipo('gasto')}
          >
            Gastos
          </button>
          <button
            style={filtroTipo === 'ingreso' ? styles.activeFilterIngreso : styles.inactiveFilter}
            onClick={() => setFiltroTipo('ingreso')}
          >
            Ingresos
          </button>
        </div>
      </div>

      {loading ? (
        <p style={styles.infoText}>Cargando historial...</p>
      ) : transacciones.length === 0 ? (
        <p style={styles.infoText}>No hay registros para mostrar.</p>
      ) : (
        <div style={styles.list}>
          {transacciones.map((tx) => (
            <div key={tx.id} style={styles.txRow}>
              <div style={styles.txLeft}>
                <div style={tx.tipo === 'ingreso' ? styles.badgeIngreso : styles.badgeGasto}>
                  {tx.tipo === 'ingreso' ? <ArrowDownLeft size={20} /> : <ArrowUpRight size={20} />}
                </div>
                <div>
                  <p style={styles.txDesc}>{tx.descripcion}</p>
                  <p style={styles.txSub}>
                    {getNombreCuenta(tx.cuenta)} • {new Date(tx.fecha).toLocaleDateString('es-CO')}
                  </p>
                </div>
              </div>

              <div style={styles.txRight}>
                <span style={tx.tipo === 'ingreso' ? styles.amountIngreso : styles.amountGasto}>
                  {tx.tipo === 'ingreso' ? '+' : '-'}${Math.round(parseFloat(tx.monto)).toLocaleString('es-CO')}
                </span>
                <div style={styles.actions}>
                  <button style={styles.iconBtn} onClick={() => handleStartEdit(tx)}>
                    <Edit2 size={16} color="#94a3b8" />
                  </button>
                  <button style={styles.iconBtn} onClick={() => handleDelete(tx.id)}>
                    <Trash2 size={16} color="#f87171" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Modal de Edición */}
      {editingTx && (
        <div style={styles.modalOverlay}>
          <div style={styles.modalCard}>
            <h3>Editar Transacción</h3>
            <form onSubmit={handleSaveEdit} style={styles.form}>
              <label style={styles.label}>Tipo:</label>
              <select
                value={editTipo}
                onChange={(e) => setEditTipo(e.target.value)}
                style={styles.select}
              >
                <option value="gasto">Gasto</option>
                <option value="ingreso">Ingreso</option>
              </select>

              <label style={styles.label}>Cuenta origen/destino:</label>
              <select
                value={editCuentaId}
                onChange={(e) => setEditCuentaId(e.target.value)}
                style={styles.select}
              >
                {cuentas.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.nombre}
                  </option>
                ))}
              </select>

              <label style={styles.label}>Monto ($):</label>
              <input
                type="text"
                value={editMontoDisplay}
                onChange={handleEditMontoChange}
                style={styles.input}
                required
              />

              <label style={styles.label}>Descripción / Categoría:</label>
              <input
                type="text"
                value={editDescripcion}
                onChange={(e) => setEditDescripcion(e.target.value)}
                style={styles.input}
                required
              />

              {errorEdit && (
                <div style={styles.errorBox}>
                  <AlertCircle size={16} /> {errorEdit}
                </div>
              )}

              <div style={styles.modalActions}>
                <button
                  type="button"
                  style={styles.cancelButton}
                  onClick={() => setEditingTx(null)}
                >
                  Cancelar
                </button>
                <button type="submit" style={styles.saveButton}>
                  Guardar Cambios
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

const styles = {
  card: {
    backgroundColor: '#1e293b',
    borderRadius: '0.75rem',
    padding: '1.5rem',
    border: '1px solid #334155',
    marginTop: '2rem',
    marginBottom: '3rem',
  },
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '1.5rem',
    flexWrap: 'wrap',
    gap: '1rem',
  },
  title: {
    fontSize: '1.2rem',
    fontWeight: 'bold',
  },
  filterContainer: {
    display: 'flex',
    backgroundColor: '#0f172a',
    padding: '4px',
    borderRadius: '0.5rem',
    gap: '4px',
  },
  activeFilter: {
    padding: '0.4rem 0.8rem',
    border: 'none',
    borderRadius: '0.3rem',
    backgroundColor: '#8b5cf6',
    color: '#fff',
    fontWeight: 'bold',
    fontSize: '0.85rem',
    cursor: 'pointer',
  },
  activeFilterGasto: {
    padding: '0.4rem 0.8rem',
    border: 'none',
    borderRadius: '0.3rem',
    backgroundColor: '#ef4444',
    color: '#fff',
    fontWeight: 'bold',
    fontSize: '0.85rem',
    cursor: 'pointer',
  },
  activeFilterIngreso: {
    padding: '0.4rem 0.8rem',
    border: 'none',
    borderRadius: '0.3rem',
    backgroundColor: '#10b981',
    color: '#fff',
    fontWeight: 'bold',
    fontSize: '0.85rem',
    cursor: 'pointer',
  },
  inactiveFilter: {
    padding: '0.4rem 0.8rem',
    border: 'none',
    backgroundColor: 'transparent',
    color: '#94a3b8',
    fontSize: '0.85rem',
    cursor: 'pointer',
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.8rem',
  },
  txRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: '#0f172a',
    padding: '1rem',
    borderRadius: '0.5rem',
    border: '1px solid #334155',
  },
  txLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: '1rem',
  },
  badgeGasto: {
    backgroundColor: 'rgba(239, 68, 68, 0.2)',
    color: '#f87171',
    padding: '0.5rem',
    borderRadius: '50%',
  },
  badgeIngreso: {
    backgroundColor: 'rgba(16, 185, 129, 0.2)',
    color: '#34d399',
    padding: '0.5rem',
    borderRadius: '50%',
  },
  txDesc: {
    fontWeight: 'bold',
    fontSize: '0.95rem',
  },
  txSub: {
    fontSize: '0.8rem',
    color: '#94a3b8',
    marginTop: '0.2rem',
  },
  txRight: {
    display: 'flex',
    alignItems: 'center',
    gap: '1.2rem',
  },
  amountGasto: {
    fontWeight: 'bold',
    color: '#f87171',
    fontSize: '1rem',
  },
  amountIngreso: {
    fontWeight: 'bold',
    color: '#34d399',
    fontSize: '1rem',
  },
  actions: {
    display: 'flex',
    gap: '0.5rem',
  },
  iconBtn: {
    backgroundColor: 'transparent',
    border: 'none',
    cursor: 'pointer',
    padding: '0.3rem',
    borderRadius: '0.3rem',
  },
  infoText: {
    color: '#94a3b8',
    textAlign: 'center',
    padding: '1.5rem',
  },
  modalOverlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.7)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
  },
  modalCard: {
    backgroundColor: '#1e293b',
    padding: '2rem',
    borderRadius: '1rem',
    width: '100%',
    maxWidth: '420px',
    border: '1px solid #475569',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '0.8rem',
    marginTop: '1rem',
  },
  label: {
    fontSize: '0.85rem',
    color: '#cbd5e1',
  },
  input: {
    padding: '0.7rem',
    borderRadius: '0.5rem',
    border: '1px solid #475569',
    backgroundColor: '#0f172a',
    color: '#fff',
    outline: 'none',
  },
  select: {
    padding: '0.7rem',
    borderRadius: '0.5rem',
    border: '1px solid #475569',
    backgroundColor: '#0f172a',
    color: '#fff',
    outline: 'none',
  },
  modalActions: {
    display: 'flex',
    justifyContent: 'flex-end',
    gap: '0.8rem',
    marginTop: '1.2rem',
  },
  cancelButton: {
    padding: '0.6rem 1rem',
    borderRadius: '0.5rem',
    border: '1px solid #475569',
    backgroundColor: 'transparent',
    color: '#cbd5e1',
    cursor: 'pointer',
  },
  saveButton: {
    padding: '0.6rem 1rem',
    borderRadius: '0.5rem',
    border: 'none',
    backgroundColor: '#8b5cf6',
    color: '#fff',
    fontWeight: 'bold',
    cursor: 'pointer',
  },
  errorBox: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.5rem',
    color: '#f87171',
    fontSize: '0.85rem',
  },
};
