import streamlit as st
import pandas as pd
from pathlib import Path

# ---------- CONFIG DE PÁGINA ----------
st.set_page_config(page_title="Campaña Veterinaria", page_icon="🐾", layout="wide")

# ---------- ESTILO (VERDE) ----------
st.markdown("""
<style>
:root { --pri:#1B7F5E; --pri-2:#25A06E; --pri-3:#E8F7F1; }
[data-testid="stAppViewContainer"] { background: linear-gradient(180deg, var(--pri-3) 0%, #ffffff 35%); }
h1, h2, h3 { color: var(--pri) !important; }
.block-container { padding-top: 2rem; }
.stButton>button, .stDownloadButton>button {
  background-color: var(--pri) !important; color: #fff !important; border: 0; border-radius: 10px;
}
div[data-baseweb="select"]>div { border-radius: 10px!important; }
</style>
""", unsafe_allow_html=True)

# ---------- CARGA DE DATOS ----------
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Veterinaria.csv"   # nombre EXACTO del CSV
    df = pd.read_csv(data_path, sep=";", dtype=str)         # tu CSV usa ;
    df.columns = [c.strip().upper() for c in df.columns]    # normaliza nombres
    return df

df = load_data()

# ---------- TÍTULO ----------
st.title("📊 Análisis de la Campaña Veterinaria")
st.caption("Vista general de registros, columnas, conteos y filtros interactivos.")

# ---------- VISTA PREVIA ----------
st.subheader("👀 Vista previa de los datos")
st.dataframe(df.head(), use_container_width=True)

# ---------- COLUMNAS ----------
st.subheader("📌 Columnas del dataset")
st.write(list(df.columns))

# ---------- RESUMEN (conteos) ----------
st.subheader("📈 Resumen de conteos por columna")
with st.expander("Ver top valores por columna"):
    for col in df.columns:
        st.markdown(f"**{col}**")
        st.write(df[col].value_counts().head(10))

# ---------- FILTROS ----------
st.subheader("🔎 Filtros")
col_tipo, col_sexo = None, None

for c in ["MASCOTA_TIPO","MASCOTA TIPO","TIPO_MASCOTA","TIPO","MASCOTA"]:
    if c in df.columns: col_tipo = c; break
for c in ["MASCOTA_SEXO","SEXO_MASCOTA","SEXO","SEXO MASCOTA"]:
    if c in df.columns: col_sexo = c; break

c1, c2 = st.columns(2)
filtros = {}

with c1:
    if col_tipo:
        tipos = sorted([x for x in df[col_tipo].dropna().unique()])
        op_tipo = st.selectbox("Tipo de mascota:", ["(Todos)"] + tipos)
        if op_tipo != "(Todos)":
            filtros[col_tipo] = op_tipo

with c2:
    if col_sexo:
        sexos = sorted([x for x in df[col_sexo].dropna().unique()])
        op_sexo = st.selectbox("Sexo:", ["(Todos)"] + sexos)
        if op_sexo != "(Todos)":
            filtros[col_sexo] = op_sexo

df_filtrado = df.copy()
for k,v in filtros.items():
    df_filtrado = df_filtrado[df_filtrado[k] == v]

st.write(f"**Registros filtrados:** {len(df_filtrado):,}")
st.dataframe(df_filtrado.head(20), use_container_width=True)

# ---------- DESCARGA ----------
@st.cache_data
def _to_csv_bytes(_df: pd.DataFrame) -> bytes:
    return _df.to_csv(index=False).encode("utf-8")

st.download_button("⬇️ Descargar CSV filtrado", _to_csv_bytes(df_filtrado),
                   file_name="veterinaria_filtrado.csv", mime="text/csv")

st.info("Si no ves filtros, revisa que existan columnas como TIPO / SEXO (en cualquier variante).")


