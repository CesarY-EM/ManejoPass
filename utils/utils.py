import streamlit as st
import os
from business import business
from datetime import datetime, timedelta

def main():
    st.set_page_config(page_title="Gestor de Credenciales")
    
    if business.verificar_login():

        if business.sesion_expirada():
            business.cerrar_sesion()
            st.rerun()
    
        st.session_state["ultimo_movimiento"] = datetime.now()

        st.sidebar.write(f"Logueado como: **{st.session_state.rol}**")

        if st.sidebar.button("Cerrar Sesión"):
            st.session_state.autenticado = False
            st.rerun()

        st.title("Central de Contraseñas")
        st.markdown("---")

        if "mostrar" not in st.session_state:
            st.session_state.mostrar = None

        if st.session_state.mostrar is None:

            st.subheader("🖥️ Seleccione un Servidor")

            cols = st.columns(len(business.SERVIDORES_CONFIG))

            for i, (key, info) in enumerate(business.SERVIDORES_CONFIG.items()):
                with cols[i]:
                    st.info(f"{info['nombre']}")
                    if st.button(f"Gestionar {key.upper()}", key=f"btn_{key}"):
                        st.session_state.mostrar = key
                        st.rerun()

            if st.session_state.rol == "editor":
                st.markdown("---")
                log_path = "movimientos.log"

                if st.button("🔄 Sincronizar con Disco"):
                    # Forzamos a Python a soltar cualquier versión vieja del archivo
                    if os.path.exists(log_path):
                        os.utime(log_path, None)
                    st.rerun()

                with st.expander("📄 Ver Historial de Auditoría (Logs)"):
                    try:
                        with open("movimientos.log", "r") as f:
                            logs = f.readlines()
                            if logs:
                                for line in reversed(logs[-5:]):
                                    if "ERROR" in line:
                                        st.error(line.strip())
                                    elif "WARNING" in line:
                                        st.warning(line.strip())
                                    else:
                                        st.text(line.strip())
                    except FileNotFoundError:
                        st.write("Aún no hay registros de actividad.")



            # VISTA DETALLADA:
        elif st.session_state.mostrar in business.SERVIDORES_CONFIG:
            srv = business.SERVIDORES_CONFIG[st.session_state.mostrar]

            st.subheader(f"Panel de Control: {srv['nombre']}")

            #Lógica de Contraseña:
            with st.container(border=True):
                if st.toggle("👁️ Revelar Contraseña", key=f"toggle_{st.session_state.mostrar}"):
                    user = st.session_state.get("usuario_logueado", "Desconocido")
                    srv_name = srv['nombre']
                    try:
                        pwd = business.obtener_password_servidor(srv['id_infisical'])
                        st.code(pwd)
                        business.logging.info(f"{user} | Visualizó contraseña | SERVIDOR: {srv_name}")
                    except Exception as e:
                        st.error(f"Error al conectar con la bóveda: {e}")

            # Volver
            if st.button("⬅️ Volver al menú principal"):
                st.session_state.mostrar = None
                st.rerun()

            if st.session_state.rol == "editor":
                st.markdown("---")
                if st.button(f"🔄 Rotar Clave de {srv['nombre']}"):
                    user = st.session_state.get("usuario_logueado", "Desconocido")
                    srv_name = srv['nombre']
                    try:
                        with st.spinner("Ejecutando..."):
                            nueva = business.generar_password()
                            business.cambio_contraseña(nueva, srv["id_infisical"],st.session_state.usuario_logueado)
                            business.logging.warning(f"{user} | Roto la contraseña   | SERVIDOR: {srv_name}")
                            st.success("Proceso completado, se notificara por correo el cambio realizado")
                    except Exception as e:
                        business.logging.error(f"{user} | ERROR EN ROTACIÓN: {e} | SERVIDOR: {srv_name}")
                        st.error("Falló en la rotación.")