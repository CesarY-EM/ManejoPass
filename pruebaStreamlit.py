import test
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv("IDs.env")

st.set_page_config(page_title="Gestor de Credenciales", page_icon="🔐")

st.title("🛡️ Central de Contraseñas Seguras")
st.markdown("---")


def verificar_login():
    if "autenticado" not in st.session_state:
        st.session_state["autenticado"] = False

    if not st.session_state["autenticado"]:
        st.title("🔒 Acceso Restringido")
        password_input = st.text_input("Introduce la Clave Maestra:", type="password")

        if st.button("Entrar"):
            if password_input == os.getenv("MASTER_PASSWORD"):
                st.session_state["autenticado"] = True
                st.rerun()  # Recarga la página ya autenticado
            else:
                st.error("❌ Contraseña incorrecta")
        return False
    return True


# --- CUERPO DEL PORTAL ---
if verificar_login():

    st.subheader("🔑 Contraseña Actual")
    col1, col2 = st.columns([3, 1])

    with col1:
        if st.button("Revelar Secreto de Infisical"):
            try:
                st.code(test.obtener_password_servidor())  # Ejemplo de lo que traería
                st.info("Esta es la contraseña activa en el servidor.")
            except Exception as e:
                st.error(f"Error al conectar: {e}")

    st.markdown("---")
    # st.subheader("🔄 Acciones de Seguridad")
    st.sidebar.success("Sesión Iniciada")
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state["autenticado"] = False
        st.rerun()

    st.title("🛡️ Centro de Mando:")

    if st.button("Generar y Rotar Nueva Contraseña"):
        with st.spinner("Generando, actualizando Infisical y enviando correo..."):
            nueva = test.generar_password_segura(15)
            test.cambio_contraseña(nueva)
            test.enviar_notificacion(nueva)
            st.success("¡Proceso completado!")
            st.balloons()
            st.write(f"**Nueva clave:** `{nueva}`")