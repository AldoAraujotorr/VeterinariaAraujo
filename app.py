import streamlit as st
import pandas as pd
from pathlib import Path

# --- Cargar datos ---
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Veterinaria.csv"
    return pd.read_csv(data_path, sep=";")  # usa ; porque tu CSV está separado por punto y coma

df = load_data()

# --- Título ---
st.title("📊 Análisis de la Campaña Veterinaria")

# Vista previa
st.subheader("👀 Vista previa de los datos")
st.dataframe(df.head())

# Información general
st.subheader("📌 Columnas del dataset")
st.write(list(df.columns))

# Resumen estadístico
st.subheader("📈 Resumen estadístico")
st.write(df.describe(include="all"))

# Filtro por tipo de mascota
st.subheader("🐶🐱 Filtrar por tipo de mascota")
tipos = df["MASCOTA_TIPO"].unique()
opcion = st.selectbox("Selecciona un tipo de mascota:", tipos)
st.write(df[df["MASCOTA_TIPO"] == opcion].head(20))


