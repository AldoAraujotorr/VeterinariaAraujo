import streamlit as st, os, glob, sys, platform, pathlib
st.set_page_config(page_title="Smoke", page_icon="✅", layout="wide")

st.title("✅ Smoke test")
st.write("cwd:", os.getcwd())
st.write("python:", sys.version)
st.write("platform:", platform.platform())
st.write("files:", sorted([p for p in os.listdir(".") if not p.startswith(".")]))
