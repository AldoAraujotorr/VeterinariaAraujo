import streamlit as st
import pandas as pd

# Cargar dataset
df = pd.read_csv("veterinaria_dataset.csv")

st.title("Campañas Veterinarias 🐾")

st.subheader("Vista previa del dataset")
st.dataframe(df.head())

if "Distrito" in df.columns:
    st.subheader("Número de campañas por distrito")
    st.bar_chart(df["Distrito"].value_counts())
