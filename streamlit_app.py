# --- streamlit_app.py (versión con estilo, sin dependencias extra) ---
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Campaña Veterinaria",
    page_icon="🐾",
    layout="wide"
)

# ====== ESTILO LIGERO (solo CSS) ======
st.markdown("""
<style>
/* colores base */
:root{
  --pri:#2563eb; /* azul */
  --pri2:#1e40af;
}
/* header tipo “hero” */
.hero{
  padding: 1.4rem 1.2rem;
  border-radius: 18px;
  background: linear-gradient(120deg, var(--pri), var(--pri2));
  color: #fff;
  margin-bottom: 1rem;
}
.hero h1{ margin:0 0 .25rem 0; font-size: 2.1rem; }
.hero p{ opacity:.95; margin:0; }

/* tarjetas métricas */
.card{
  border:1px solid #eef2ff; border-radius:16px; padding:1rem;
  background:#fff; box-shadow:0 6px 20px rgba(37,99,235,.08);
}
.card h3{ margin:.15rem 0 .4rem 0; font-size: .95rem; font-weight:600; color:#334155}
.card .v{ font-size:1.6rem; font-weight:700; color:var(--pri) }

/* botones y widgets */
.stButton > button, .stDownloadButton > button{
  background: var(--pri); border:0; color:#fff; border-radius:10px; padding:.55rem .9rem;
}
.stButton > button:hover, .stDownloadButton > button:hover{ background: var(--pri2) }

/* quitar menú/footers */
#MainMenu, footer {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ====== DATOS ======
@st.cache_data
def load_data():
    path = Path(__file__).parent/"Veterinaria.csv"
    df = pd.read_csv(path, sep=";")
    df.columns = [c.strip().upper() for c in df.columns]
    return df

df = load_data()

# ====== CABECERA ======
st.markdown("""
<div class="hero">
  <h1>📊 Análisis de la Campaña Veterinaria</h1>
  <p>Vista rápida • filtros • descarga</p>
</div>
""", unsafe_allow_html=True)

# ====== MÉTRICAS ======
c1,c2,c3,c4 = st.columns(4)
with c1:
    st.markdown('<div class="card"><h3>Registros</h3><div class="v">{:,}</div></div>'.format(len(df)), unsafe_allow_html=True)
with c2:
    col_tipo = next((c for c in df.columns if "MASCOTA_TIPO" in c or c=="TIPO"), None)
    n_tipos = df[col_tipo].nunique() if col_tipo else 0
    st.markdown(f'<div class="card"><h3>Tipos de mascota</h3><div class="v">{n_tipos}</div></div>', unsafe_allow_html=True)
with c3:
    col_raza = next((c for c in df.columns if "RAZA" in c), None)
    n_razas = df[col_raza].nunique() if col_raza else 0
    st.markdown(f'<div class="card"><h3>Razas</h3><div class="v">{n_razas}</div></div>', unsafe_allow_html=True)
with c4:
    col_anio = next((c for c in df.columns if "ANIO" in c or "AÑO" in c), None)
    anios = ", ".join(sorted(map(str, df[col_anio].dropna().unique()))[:3]) if col_anio else "—"
    st.markdown(f'<div class="card"><h3>Años (muestra)</h3><div class="v">{anios}</div></div>', unsafe_allow_html=True)

st.divider()

# ====== SIDEBAR: FILTROS ======
st.sidebar.header("🔎 Filtros")
filtros = {}
col_sexo = next((c for c in df.columns if "SEXO" in c), None)
col_tipo = col_tipo  # ya detectada arriba

if col_tipo:
    tipos = sorted(df[col_tipo].dropna().unique().tolist())
    sel_tipos = st.sidebar.multiselect("Tipo de mascota", tipos)
    if sel_tipos: filtros[col_tipo] = sel_tipos

if col_sexo:
    sexos = sorted(df[col_sexo].dropna().unique().tolist())
    sel_sexos = st.sidebar.multiselect("Sexo", sexos)
    if sel_sexos: filtros[col_sexo] = sel_sexos

df_f = df.copy()
for k, vals in filtros.items():
    df_f = df_f[df_f[k].isin(vals)]

# ====== CUERPO ======
st.subheader("🔍 Vista previa")
st.dataframe(df_f.head(20), use_container_width=True)

st.subheader("📈 Resumen")
st.write(df_f.describe(include="all"))

# Conteos simples (barras) con st.bar_chart, sin librerías extra
cA, cB = st.columns(2)
if col_tipo:
    stt = df_f[col_tipo].value_counts().head(10)
    cA.caption("Top 10 por tipo")
    cA.bar_chart(stt)

if col_sexo:
    sts = df_f[col_sexo].value_counts()
    cB.caption("Distribución por sexo")
    cB.bar_chart(sts)

# ====== DESCARGA ======
csv = df_f.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Descargar CSV filtrado", csv, "veterinaria_filtrado.csv", "text/csv")
