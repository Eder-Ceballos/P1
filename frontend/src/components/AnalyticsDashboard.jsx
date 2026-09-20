import React, { useState, useEffect } from 'react';
import api from '../api';
import { Wallet, TrendingUp, TrendingDown, AlertTriangle, ArrowLeft, PieChart } from 'lucide-react';

export function AnalyticsDashboard({ usuario, onBackToMain }) {
  const [reporte, setReporte] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const cargarReporte = async () => {
      try {
        setLoading(true);
        const res = await api.get(`/transacciones/reporte-analitico/?usuario=${usuario.id}`);
        setReporte(res.data);
      } catch {
        // Manejo de error silencioso
      } finally {
        setLoading(false);
      }
    };
    cargarReporte();
  }, [usuario.id]);

  if (loading) {
    return <p style={styles.loadingText}>Cargando reporte analítico...</p>;
  }

  const { resumen_general, desglose_categorias } = reporte || {};
  const totalGastos = resumen_general?.total_gastos || 1;

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <button style={styles.backBtn} onClick={onBackToMain}>
          <ArrowLeft size={18} style={{ marginRight: '6px' }} /> Volver al Inicio
        </button>
        <h2>Panel de Reportes y Estadísticas</h2>
      </div>

      {/* Tarjetas resumen */}
      <div style={styles.metricsGrid}>
        <div style={styles.metricCard}>
          <div style={styles.cardHeader}>
            <span style={styles.metricTitle}>Balance Total</span>
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
          <p style={styles.loadingText}>No hay datos de gastos registrados.</p>
        )}
      </div>
    </div>
  );
}

const styles = {
  container: { marginTop: '1.5rem' },
  header: { display: 'flex', alignItems: 'center', gap: '1rem', marginBottom: '1.5rem' },
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
  loadingText: { color: '#94a3b8', marginTop: '1rem' },
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))',
    gap: '1rem',
    marginBottom: '2rem',
  },
  metricCard: {
    backgroundColor: '#1e293b',
    padding: '1.2rem',
    borderRadius: '0.75rem',
    border: '1px solid #334155',
  },
  cardHeader: { display: 'flex', justifyContent: 'space-between', alignItems: 'center' },
  metricTitle: { fontSize: '0.85rem', color: '#94a3b8' },
  metricAmount: { fontSize: '1.4rem', fontWeight: 'bold', color: '#38bdf8', marginTop: '0.5rem' },
  metricAmountIngreso: { fontSize: '1.4rem', fontWeight: 'bold', color: '#34d399', marginTop: '0.5rem' },
  metricAmountGasto: { fontSize: '1.4rem', fontWeight: 'bold', color: '#f87171', marginTop: '0.5rem' },
  metricAmountWarning: { fontSize: '1.4rem', fontWeight: 'bold', color: '#fbbf24', marginTop: '0.5rem' },
  sectionCard: {
    backgroundColor: '#1e293b',
    borderRadius: '0.75rem',
    padding: '1.5rem',
    border: '1px solid #334155',
  },
  sectionHeader: { display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.2rem' },
  categoryList: { display: 'flex', flexDirection: 'column', gap: '1rem' },
  categoryRow: { display: 'flex', flexDirection: 'column', gap: '0.4rem' },
  categoryInfo: { display: 'flex', justifyContent: 'space-between', fontSize: '0.9rem' },
  categoryName: { color: '#f8fafc', fontWeight: '500' },
  categoryAmount: { color: '#94a3b8' },
  barBg: { height: '8px', backgroundColor: '#0f172a', borderRadius: '4px', overflow: 'hidden' },
  barFill: { height: '100%', backgroundColor: '#8b5cf6', borderRadius: '4px' },
};
