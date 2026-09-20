import React, { useState, useEffect } from 'react';
import api from '../api';
import { Wallet, TrendingUp, TrendingDown, AlertTriangle, ArrowLeft, PieChart, Filter } from 'lucide-react';

export function AnalyticsDashboard({ usuario, onBackToMain }) {
  const [reporte, setReporte] = useState(null);
  const [cuentas, setCuentas] = useState([]);
  const [selectedCuenta, setSelectedCuenta] = useState(''); // '' es "Todas las cuentas"
  const [loading, setLoading] = useState(true);

  // Cargar lista de cuentas del usuario para el filtro
  useEffect(() => {
    const cargarCuentas = async () => {
      try {
        const res = await api.get('/cuentas/');
        const userCuentas = res.data.filter((c) => c.usuario === usuario.id);
        setCuentas(userCuentas);
      } catch {
        // Manejo silencioso
      }
    };
    cargarCuentas();
  }, [usuario.id]);

  // Cargar reporte financiero según la cuenta seleccionada
  useEffect(() => {
    const cargarReporte = async () => {
      try {
        setLoading(true);
        let url = `/transacciones/reporte-analitico/?usuario=${usuario.id}`;
        if (selectedCuenta) {
          url += `&cuenta=${selectedCuenta}`;
        }
        const res = await api.get(url);
        setReporte(res.data);
      } catch {
        // Manejo silencioso
      } finally {
        setLoading(false);
      }
    };
    cargarReporte();
  }, [usuario.id, selectedCuenta]);

  const { resumen_general, desglose_categorias } = reporte || {};
  const totalGastos = resumen_general?.total_gastos || 1;

  return (
    <div style={styles.container}>
      <div style={styles.headerRow}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <button style={styles.backBtn} onClick={onBackToMain}>
            <ArrowLeft size={18} style={{ marginRight: '6px' }} /> Volver al Inicio
          </button>
          <h2 style={styles.pageTitle}>Panel de Reportes y Estadísticas</h2>
        </div>

        {/* Filtro por Cuenta */}
        <div style={styles.filterBox}>
          <Filter size={18} color="#94a3b8" />
          <select
            value={selectedCuenta}
            onChange={(e) => setSelectedCuenta(e.target.value)}
            style={styles.selectFilter}
          >
            <option value="">Todas las Cuentas (General)</option>
            {cuentas.map((c) => (
              <option key={c.id} value={c.id}>
                {c.nombre} ({c.tipo})
              </option>
            ))}
          </select>
        </div>
      </div>

      {loading ? (
        <p style={styles.loadingText}>Cargando reporte analítico...</p>
      ) : (
        <>
          {/* Tarjetas de Métricas */}
          <div style={styles.metricsGrid}>
            <div style={styles.metricCard}>
              <div style={styles.cardHeader}>
                <span style={styles.metricTitle}>
                  {selectedCuenta ? 'Saldo Disponible en Cuenta' : 'Balance Total (Todas)'}
                </span>
                <Wallet color="#38bdf8" size={20} />
              </div>
              <p style={styles.metricAmount}>
                ${Math.round(resumen_general?.balance_total || 0).toLocaleString('es-CO')}
              </p>
            </div>

            <div style={styles.metricCard}>
              <div style={styles.cardHeader}>
                <span style={styles.metricTitle}>Ingresos Totales</span>
                <TrendingUp color="#34d399" size={20} />
              </div>
              <p style={styles.metricAmountIngreso}>
                ${Math.round(resumen_general?.total_ingresos || 0).toLocaleString('es-CO')}
              </p>
            </div>

            <div style={styles.metricCard}>
              <div style={styles.cardHeader}>
                <span style={styles.metricTitle}>Gastos Totales</span>
                <TrendingDown color="#f87171" size={20} />
              </div>
              <p style={styles.metricAmountGasto}>
                ${Math.round(resumen_general?.total_gastos || 0).toLocaleString('es-CO')}
              </p>
            </div>

            <div style={styles.metricCard}>
              <div style={styles.cardHeader}>
                <span style={styles.metricTitle}>Gastos Hormiga Estimados</span>
                <AlertTriangle color="#fbbf24" size={20} />
              </div>
              <p style={styles.metricAmountWarning}>
                ${Math.round(resumen_general?.gastos_hormiga_estimados || 0).toLocaleString('es-CO')}
              </p>
            </div>
          </div>

          {/* Desglose de Gastos por Categoría */}
          <div style={styles.sectionCard}>
            <div style={styles.sectionHeader}>
              <PieChart size={20} color="#8b5cf6" />
              <h3 style={{ margin: 0 }}>Distribución de Gastos por Categoría</h3>
            </div>

            {desglose_categorias && desglose_categorias.length > 0 ? (
              <div style={styles.categoryList}>
                {desglose_categorias.map((cat, idx) => {
                  const porcentaje = Math.round((cat.monto / totalGastos) * 100);
                  return (
                    <div key={idx} style={styles.categoryRow}>
                      <div style={styles.categoryInfo}>
                        <span style={styles.categoryName}>{cat.categoria}</span>
                        <span style={styles.categoryAmount}>
                          ${Math.round(cat.monto).toLocaleString('es-CO')} ({porcentaje}%)
                        </span>
                      </div>
                      <div style={styles.barBg}>
                        <div style={{ ...styles.barFill, width: `${porcentaje}%` }} />
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p style={styles.loadingText}>No hay datos de gastos registrados para el filtro seleccionado.</p>
            )}
          </div>
        </>
      )}
    </div>
  );
}

const styles = {
  container: { marginTop: '1.5rem', marginBottom: '3rem' },
  headerRow: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    flexWrap: 'wrap',
    gap: '1rem',
    marginBottom: '1.5rem',
  },
  pageTitle: { fontSize: '1.4rem', fontWeight: 'bold' },
  backBtn: {
    display: 'flex',
    alignItems: 'center',
    backgroundColor: '#334155',
    color: '#f8fafc',
    border: 'none',
    padding: '0.5rem 1rem',
    borderRadius: '0.5rem',
    cursor: 'pointer',
    fontSize: '0.85rem',
  },
  filterBox: {
    display: 'flex',
    alignItems: 'center',
    gap: '0.6rem',
    backgroundColor: '#1e293b',
    padding: '0.4rem 0.8rem',
    borderRadius: '0.5rem',
    border: '1px solid #334155',
  },
  selectFilter: {
    backgroundColor: 'transparent',
    color: '#f8fafc',
    border: 'none',
    outline: 'none',
    fontSize: '0.9rem',
    cursor: 'pointer',
  },
  loadingText: { color: '#94a3b8', marginTop: '1rem', textAlign: 'center' },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))',
    gap: '1.2rem',
    marginBottom: '2rem',
  },
  metricCard: {
    backgroundColor: '#1e293b',
    padding: '1.25rem',
    borderRadius: '0.75rem',
    border: '1px solid #334155',
  },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  metricTitle: { fontSize: '0.85rem', color: '#94a3b8' },
  metricAmount: { fontSize: '1.5rem', fontWeight: 'bold', color: '#38bdf8', marginTop: '0.5rem' },
  metricAmountIngreso: { fontSize: '1.5rem', fontWeight: 'bold', color: '#34d399', marginTop: '0.5rem' },
  metricAmountGasto: { fontSize: '1.5rem', fontWeight: 'bold', color: '#f87171', marginTop: '0.5rem' },
  metricAmountWarning: { fontSize: '1.5rem', fontWeight: 'bold', color: '#fbbf24', marginTop: '0.5rem' },
  sectionCard: {
    backgroundColor: '#1e293b',
    borderRadius: '0.75rem',
    padding: '1.5rem',
    border: '1px solid #334155',
  },
  sectionHeader: { display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.2rem' },
  categoryList: { display: 'flex', flexDirection: 'column', gap: '1.2rem' },
  categoryRow: { display: 'flex', flexDirection: 'column', gap: '0.4rem' },
  categoryInfo: { display: 'flex', justifyContent: 'space-between', fontSize: '0.95rem' },
  categoryName: { color: '#f8fafc', fontWeight: '500' },
  categoryAmount: { color: '#94a3b8' },
  barBg: { height: '10px', backgroundColor: '#0f172a', borderRadius: '5px', overflow: 'hidden' },
  barFill: { height: '100%', backgroundColor: '#8b5cf6', borderRadius: '5px', transition: 'width 0.4s ease' },
};
