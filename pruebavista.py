import test
import streamlit as st
from dotenv import load_dotenv

load_dotenv("IDs.env")

st.set_page_config(page_title="Gestor de Credenciales", page_icon="🔐")

st.title("🛡️ Central de Contraseñas Seguras")
st.markdown("---")

if "mostrar" not in st.session_state:
    st.session_state.mostrar = None

if st.session_state.mostrar is None:
    st.subheader("🖥️ Seleccione un Servidor")
    col1, col2 = st.columns(2)
    with col1:
        st.info("Servidor GNS3")
        if st.button("Gestionar GNS3"):
            st.session_state.mostrar = "gns3"
            st.rerun()

    with col2:
        st.info("Servidor Docker")
        if st.button("Gestionar Docker"):
            st.session_state.mostrar = "docker"
            st.rerun()

# --- VISTA DETALLADA: GNS3 ---
elif st.session_state.mostrar == "gns3":
    st.subheader("🔑 Credenciales: GNS3")

    if st.toggle("👁️ Revelar Contraseña"):
        try:
            pwd = test.obtener_password_servidor()
            st.code(pwd)
        except Exception as e:
            st.error(f"Error: {e}")
    st.markdown("---")
    st.subheader("Configuracion contraseña")
    if st.button("🔄 Rotar Contraseña (Se notificara por correo)"):
        with st.spinner("Procesando..."):
            nueva = test.generar_password_segura(15)
            test.actualizar_password_en_infisical(nueva)
            test.enviar_notificacion_cambio(nueva)
            st.success("Contraseña rotada y enviada.")

    if st.button("⬅️ Volver"):
        st.session_state.mostrar = None
        st.rerun()

# --- VISTA DETALLADA: DOCKER ---
elif st.session_state.mostrar == "docker":
    st.subheader("🔑 Credenciales: Docker")

    if st.button("👁️ Revelar Contraseña"):
        try:
            pwd = "Contraseña prueba"
            st.code(pwd)
        except Exception as e:
            st.error(f"Error: {e}")

    if st.button("⬅️ Volver", key = 1):
        st.session_state.mostrar = None
        st.rerun()

st.markdown("---")

