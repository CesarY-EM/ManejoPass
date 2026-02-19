# main.py
from business import business
import streamlit as st

# Configuración de página (Debe ir en el archivo que ejecutas)
st.set_page_config(page_title="Portal de Seguridad", layout="wide")

# Invocamos el método principal de la clase 2
if __name__ == "__main__":
    business.main()