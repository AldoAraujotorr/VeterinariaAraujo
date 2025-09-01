# === app.py (corto y robusto) ===
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Campaña Veterinaria", page_icon="🐾", layout="wide")

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    # ¡Respeta mayúsculas/minúsculas del archivo!
    data_path = Path(__file__).parent / "Veterinaria.csv"
    # Tu CSV usa ; como separador
    df = pd.read_csv(data_path, sep=";")
    # Limpia nombres de columnas (evita problemas de variantes)
    df.columns = [c.strip().upper() for c in df.columns]
    return df

df = load_data()

# --- UI ---
st.title("📊 Análisis de la Campaña Veterinaria")
st.caption("Vista rápida + filtros + descarga")

st.subheader("👀 Vista previa")
st.dataframe(df.head(20), use_container_width=True)

st.subheader("📌 Columnas")
st.write(list(df.columns))

st.subheader("📈 Resumen (conteos)")
with st.expander("Ver top de cada columna"):
    for col in df.columns:
        st.markdown(f"**{col}**")
        st.write(df[col].value_counts().head(10))

# --- FILTROS (si existen) ---
st.subheader("🔎 Filtros")
col_tipo = next((c for c in df.columns if "MASCOTA_TIPO" in c or "TIPO" in c), None)
col_sexo = next((c for c in df.columns if "SEXO" in c), None)

c1, c2 = st.columns(2)
filtros = {}

with c1:
    if col_tipo:
        tipos = sorted(x for x in df[col_tipo].dropna().unique())
        op_tipo = st.selectbox("Tipo de mascota:", ["(Todos)"] + tipos)
        if op_tipo != "(Todos)":
            filtros[col_tipo] = op_tipo

with c2:
    if col_sexo:
        sexos = sorted(x for x in df[col_sexo].dropna().unique())
        op_sexo = st.selectbox("Sexo:", ["(Todos)"] + sexos)
        if op_sexo != "(Todos)":
            filtros[col_sexo] = op_sexo

df_filtrado = df.copy()
for k, v in filtros.items():
    df_filtrado = df_filtrado[df_filtrado[k] == v]

st.write(f"**Registros filtrados:** {len(df_filtrado)}")
st.dataframe(df_filtrado.head(20), use_container_width=True)

# --- DESCARGA ---
@st.cache_data
def _to_csv_bytes(d: pd.DataFrame) -> bytes:
    return d.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Descargar CSV filtrado",
    _to_csv_bytes(df_filtrado),
    file_name="veterinaria_filtrado.csv",
    mime="text/csv",
)

st.info("Si no ves filtros, revisa que existan columnas con palabras como TIPO/SEXO (en cualquier variante).")
# === fin ===
