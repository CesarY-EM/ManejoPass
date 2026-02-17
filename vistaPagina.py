from platformdirs import user_state_dir
from streamlit import spinner

import test
import auth
import streamlit as st

SERVIDORES_CONFIG = {
    "servidor 1": {
        "nombre": "Servidor 1",
        "id_infisical": 1,
        "descripcion": "Entorno de simulación de redes"
    },
    "servidor 2": {
        "nombre": "Servidor 2",
        "id_infisical": 2,
        "descripcion": "Contenedores de servicios core"
    },
    "servidor 3": {
        "nombre": "servidor 3",
        "id_infisical": 3,
        "descripcion": "Perímetro de seguridad"
    }
}

st.set_page_config(page_title="Gestor de Credenciales", page_icon="🔐")

if auth.verificar_login():
    st.sidebar.write(f"Logueado como: **{st.session_state.rol}**")

    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.autenticado = False
        st.rerun()

    st.title("🛡️ Central de Contraseñas")
    st.markdown("---")

    if "mostrar" not in st.session_state:
        st.session_state.mostrar = None

    if st.session_state.mostrar is None:
        st.subheader("🖥️ Seleccione un Servidor")

        cols = st.columns(len(SERVIDORES_CONFIG))

        for i, (key, info) in enumerate(SERVIDORES_CONFIG.items()):
            with cols[i]:
                st.info(f"{info['nombre']}")
                if st.button(f"Gestionar {key.upper()}", key=f"btn_{key}"):
                    st.session_state.mostrar = key
                    st.rerun()

        # VISTA DETALLADA:
    elif st.session_state.mostrar in SERVIDORES_CONFIG:
        srv = SERVIDORES_CONFIG[st.session_state.mostrar]

        st.subheader(f"Panel de Control: {srv['nombre']}")

        #Lógica de Contraseña
        with st.container(border=True):
            if st.toggle("👁️ Revelar Contraseña", key=f"toggle_{st.session_state.mostrar}"):
                try:
                    pwd = test.obtener_password_servidor(srv['id_infisical'])
                    st.code(pwd)
                except Exception as e:
                    st.error(f"Error al conectar con la bóveda: {e}")

        # Volver
        if st.button("⬅️ Volver al menú principal"):
            st.session_state.mostrar = None
            st.rerun()

        if st.session_state.rol == "editor":
            st.markdown("---")
            if st.button(f"🔄 Rotar Clave de {srv['nombre']}"):
                with st.spinner("Ejecutando..."):
                    nueva = test.generar_password()
                    test.cambio_contraseña(nueva, srv["id_infisical"],st.session_state.usuario_logueado)
                    st.success("Proceso completado, se notificara por correo el cambio realizado")