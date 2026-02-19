import os
import logging
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
        st.title("Inicio de sesión")
        usuario_input = st.text_input("Usuario:")
        password = st.text_input("Contraseña:", type="password")

        if st.button("Iniciar sesion"):
            users = obtener_usuarios()
            if usuario_input in users:

                if "intentos" not in st.session_state:
                    st.session_state.intentos = 0

                if st.session_state.intentos >= 3:
                    st.error("Acceso bloqueado. Limite de intentos alcanzado.")
                    st.info("Contacte al administrador del sistema.")
                    logging.warning(f"{usuario_input} | LOGIN: BLOQUEADO POR EXCESO DE INTENTOS")

                else:
                    if password == users[usuario_input]["pass"]:
                        st.session_state["autenticado"] = True
                        st.session_state["rol"] = users[usuario_input]["rol"]
                        st.session_state.usuario_logueado = usuario_input
                        st.session_state.intentos = 0  # Reiniciamos
                        logging.info(f"{usuario_input} | Ha ingresado al portal")
                        st.rerun()
                    else:
                        st.session_state.intentos += 1
                        intentos_restantes = 3 - st.session_state.intentos

                        if st.session_state.intentos >= 3:
                            st.toast("⚠️ Límite de intentos alcanzado")
                            st.error("Has agotado tus 3 intentos.")
                        else:
                            st.warning(f"Contraseña incorrecta. Te quedan {intentos_restantes} intentos.")

                        logging.warning(f"{usuario_input} | LOGIN: FALLIDO (Intento {st.session_state.intentos}/3)")
            else:
                st.toast("El usuario ingresado no existe", icon="⚠️")
        return False
    return True
