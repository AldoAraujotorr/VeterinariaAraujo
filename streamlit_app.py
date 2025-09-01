import streamlit as st
import pandas as pd
from pathlib import Path

# Configuración de página
st.set_page_config(
    page_title="📊 Campaña Veterinaria",
    page_icon="🐾",
    layout="wide"
)

# Cargar datos
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Veterinaria.csv"
    df = pd.read_csv(data_path, sep=";")
    df.columns = [c.strip().upper() for c in df.columns]
    return df

df = load_data()

# Título
st.title("📊 Análisis de la Campaña Veterinaria")
st.caption("Vista rápida + filtros + descarga")

# Vista previa
st.subheader("🔍 Vista previa")
st.dataframe(df.head(20), use_container_width=True)

# Resumen
st.subheader("📈 Resumen (conteos)")
st.write(df.describe(include="all"))

# Columnas disponibles
st.subheader("🗂 Columnas")
st.write(df.columns.tolist())

# Filtros dinámicos (si existen esas columnas)
if "TIPO" in df.columns and "SEXO" in df.columns:
    st.subheader("🎯 Filtros")
    tipo = st.multiselect("Tipo", df["TIPO"].unique())
    sexo = st.multiselect("Sexo", df["SEXO"].unique())
    df_filtrado = df.copy()
    if tipo:
        df_filtrado = df_filtrado[df_filtrado["TIPO"].isin(tipo)]
    if sexo:
        df_filtrado = df_filtrado[df_filtrado["SEXO"].isin(sexo)]
    st.dataframe(df_filtrado, use_container_width=True)

    # Descargar CSV filtrado
    csv = df_filtrado.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Descargar CSV filtrado",
        csv,
        "veterinaria_filtrado.csv",
        "text/csv"
    )
