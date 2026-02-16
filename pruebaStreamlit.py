from platformdirs import user_state_dir

import test
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv("IDs.env")

st.set_page_config(page_title="Gestor de Credenciales", page_icon="🔐")


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
        st.title("🔒 Acceso Restringido")
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

if verificar_login():
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

        # VISTA DETALLADA: GNS3
    elif st.session_state.mostrar == "gns3":
        if st.button("Volver al Menú", key="regresar_gns3"):
            st.session_state.mostrar = None
            st.rerun()

        st.subheader("🔑 Credenciales: Servidor GNS3")

        with st.container(border=True):
            if st.toggle("👁️ Revelar Contraseña"):
                try:
                    pwd = test.obtener_password_servidor(2)
                    st.info("Contraseña actual en bóveda:")
                    st.code(pwd)
                except Exception as e:
                    st.error(f"Error al conectar con Infisical: {e}")
            else:
                st.write("La contraseña está oculta. Usa el interruptor para verla.")

        st.markdown("---")

        #Acciones
        if st.session_state.rol == "editor":
            st.subheader("⚙️ Configuración y Seguridad")
            st.warning("Cuidado: La rotación actualizará los servidores y notificará al equipo.")

            if st.button("🔄 Ejecutar Rotación Inmediata", use_container_width=True):
                with st.spinner("Generando nueva clave y actualizando sistemas..."):
                    try:
                        usuario_actual = st.session_state.get("usuario_logueado", "admin")
                        nueva = test.generar_password()
                        test.cambio_contraseña(nueva, 2)
                        test.enviar_notificacion(nueva,2, usuario_actual)
                        st.success("✅ ¡Proceso completado! Clave actualizada y correos enviados.")
                    except Exception as e:
                        st.error(f"Fallo en el proceso de rotación: {e}")
        else:
            st.info("🔒 Tu perfil (Lector) no tiene permisos para realizar cambios en este servidor.")

    elif st.session_state.mostrar == "docker":
        if st.button("Volver al Menú", key="regresar_docker"):
            st.session_state.mostrar = None
            st.rerun()

        st.subheader("🔑 Credenciales: Servidor DOCKER")

        with st.container(border=True):
            if st.toggle("👁️ Revelar Contraseña"):
                try:
                    pwd = test.obtener_password_servidor(2)
                    st.info("Contraseña actual en bóveda:")
                    st.code(pwd)
                except Exception as e:
                    st.error(f"Error al conectar con Infisical: {e}")
            else:
                st.write("La contraseña está oculta. Usa el interruptor para verla.")

        st.markdown("---")

        #Acciones
        if st.session_state.rol == "editor":
            st.subheader("⚙️ Configuración y Seguridad")
            st.warning("Cuidado: La rotación actualizará los servidores y notificará al equipo.")

            if st.button("🔄 Ejecutar Rotación Inmediata", use_container_width=True):
                with st.spinner("Generando nueva clave y actualizando sistemas..."):
                    try:
                        nueva = test.generar_password()
                        test.cambio_contraseña(nueva)
                        test.enviar_notificacion(nueva)
                        st.success("✅ ¡Proceso completado! Clave actualizada y correos enviados.")
                    except Exception as e:
                        st.error(f"Fallo en el proceso de rotación: {e}")
        else:
            st.info("🔒 Tu perfil (Lector) no tiene permisos para realizar cambios en este servidor.")