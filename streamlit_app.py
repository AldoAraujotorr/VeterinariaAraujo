import streamlit as st, os
st.title("✅ Smoke test")
st.write("cwd:", os.getcwd())
st.write("Archivos en raíz:", sorted(os.listdir(".")))
