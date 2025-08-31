 import pandas as pd
import streamlit as st
from pathlib import Path

st.title("📊 Análisis de la Campaña Veterinaria")

# Cargar datos
@st.cache_data
def load_data():
    data_path = Path(__file__).parent / "Veterinaria.csv"  # ojo: mismo nombre que en GitHub
    return pd.read_csv(data_path, sep=";")  # tu CSV está separado por ;

df = load_data()

# Mostrar vista previa
st.subheader("👀 Vista previa de los datos")
st.dataframe(df.head())

# Información general
st.subheader("📌 Columnas del dataset")
st.write(list(df.columns))

# Descripción estadística
st.subheader("📈 Resumen estadístico")
st.write(df.describe(include="all"))

# Filtro por tipo de mascota
st.subheader("🐶🐱 Filtrar por tipo de mascota")
tipos = df["MASCOTA_TIPO"].unique()
opcion = st.selectbox("Selecciona un tipo de mascota:", tipos)
st.write(df[df["MASCOTA_TIPO"] == opcion].head(20))

