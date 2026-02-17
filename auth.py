import os
import streamlit as st
from dotenv import load_dotenv

load_dotenv("IDs.env")

def obtener_usuarios():
    usuarios_str = os.getenv("USUARIOS")
    diccionario_usuarios = {}

    if usuarios_str:
        lista_usuarios = usuarios_str.split(",")
        for item in lista_usuarios:
            u, p, r = item.split(":")
            diccionario_usuarios[u] = {"pass": p, "rol": r}

    return diccionario_usuarios


def verificar_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False
        st.session_state["rol"] = None

    if not st.session_state["autenticado"]:
        st.title("Acceso Restringido")
        usuario_input = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")

        if st.button("Iniciar sesion"):
            users = obtener_usuarios()
            if usuario_input in users and password == users[usuario_input]["pass"]:
                st.session_state["autenticado"] = True
                st.session_state["rol"] = users[usuario_input]["rol"]
                st.session_state.usuario_logueado = usuario_input
            else:
                st.error("Contraseña incorrecta")

        return False
    return True
