__author__ = 'Cesar Yair Espinosa Martinez'
__copyright__ = 'Copyright 2026 UNINET. Todos los derechos Reservados'
__version__ = '1.0.0'
__email__ = 'cesaryaem@gmail.com'
__status__ = 'DEVELOPMENT'

import secrets 
import streamlit as st
import logging
import test
import os
from infisical_sdk import infisical_requests, InfisicalSDKClient
import string
from dotenv import load_dotenv

load_dotenv("IDs.env")

servidores = {1 : "GNS3",
              2: "SERVER_ADMIN_PASS"}

# Iniciamos el cliente y le pasamos la credenciales que se encuentrarn en IDs.env
client = InfisicalSDKClient(host="https://app.infisical.com")
client.auth.universal_auth.login(
    client_id=os.getenv("INFISICAL_CLIENT_ID"),
    client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
)

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

def generar_password():
    longitud = 15
    """
    Funcion para generar contraseña con un requerimientos estandarizados

    Returns:
        string: nueva contraseña generada 
    """

    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    numeros = string.digits
    especiales = "!@#$%^&*()-_=+"

    password = [
        secrets.choice(minusculas),
        secrets.choice(mayusculas),
        secrets.choice(numeros),
        secrets.choice(especiales)
    ]

    todos_los_caracteres = minusculas + mayusculas + numeros + especiales

    for _ in range(longitud - len(password)):
        password.append(secrets.choice(todos_los_caracteres))

    secrets.SystemRandom().shuffle(password)

    return ''.join(password)


def obtener_password_servidor(server):
    """
    Funcion que se encarga de obtener la contraseña actual del servidor deseado

    Args:
        server (string): id del servidor del cual queremos obtener la contraseña actual

    Returns:
        secret.value (string): contraseña obtenida del servidor
    """

    servidor = servidores.get(server)
    try:
        secret = client.secrets.get_secret_by_name(
            secret_name = servidor,
            project_id = os.getenv("INFISICAL_PROJECT_ID"),
            environment_slug = "dev",
            secret_path = "/"
        )
        return secret.secretValue

    except Exception as e:
        print(f"Error al obtener secreto: {e}")
        return None


def cambio_contraseña(nuevo_pass, server, usuario):
    """
    Funcion que se encarga de cambiar la contraseña

    Args: 
        nuevo_pass (string): nueva contraseña que se pondra en el servidor deseado
        server (int): id del servidor donde se quiere rotar la contraseña
        usuario (string): cadena que nos indica que usuario solicito el cambio de contraseña
    
    """

    servidor = servidores.get(server)
    client.secrets.update_secret_by_name(
        current_secret_name = servidor,
        secret_value = nuevo_pass,
        project_id=os.getenv("INFISICAL_PROJECT_ID"),
        environment_slug="dev",
        secret_path="/",
    )
    # print("El password ha sido cambiado correctamente")
    # enviar_notificacion(nuevo_pass, server, usuario)

def obtener_usuarios():
    """
    Funcion que nos permite obtener los usuarios que se encuentran en unarchivo .env

    Returns:
        diccionario_usuario (diccionario): usuario, contraseña y rol de los usuarios encontrados    
    """
    usuarios_str = os.getenv("USUARIOS")
    diccionario_usuarios = {}

    if usuarios_str:
        lista_usuarios = usuarios_str.split(",")
        for item in lista_usuarios:
            u, p, r = item.split(":")
            diccionario_usuarios[u] = {"pass": p, "rol": r}

    return diccionario_usuarios


def verificar_login():
    """
    Funcion que la valida a los usuarios en la base

    Returns:
        (boolean) = Si se pudo validar el usuario o no
    """

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


def main():
    st.set_page_config(page_title="Gestor de Credenciales")

    if verificar_login():
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

            cols = st.columns(len(SERVIDORES_CONFIG))

            for i, (key, info) in enumerate(SERVIDORES_CONFIG.items()):
                with cols[i]:
                    st.info(f"{info['nombre']}")
                    if st.button(f"Gestionar {key.upper()}", key=f"btn_{key}"):
                        st.session_state.mostrar = key
                        st.rerun()

            if st.session_state.rol == "editor":
                st.markdown("---")
                log_path = "movimiento.log"

                if st.button("🔄 Sincronizar con Disco"):
                    # Forzamos a Python a soltar cualquier versión vieja del archivo
                    if os.path.exists(log_path):
                        os.utime(log_path, None)  # Actualiza la fecha del archivo para engañar al sistema
                    st.rerun()

                with st.expander("📄 Ver Historial de Auditoría (Logs)"):
                    try:
                        with open("movimientos.log", "r") as f:
                            logs = f.readlines()
                            if logs:
                                for line in reversed(logs[5:]):
                                    if "ERROR" in line:
                                        st.error(line.strip())
                                    elif "WARNING" in line:
                                        st.warning(line.strip())
                                    else:
                                        st.text(line.strip())
                    except FileNotFoundError:
                        st.write("Aún no hay registros de actividad.")



            # VISTA DETALLADA:
        elif st.session_state.mostrar in SERVIDORES_CONFIG:
            srv = SERVIDORES_CONFIG[st.session_state.mostrar]

            st.subheader(f"Panel de Control: {srv['nombre']}")

            #Lógica de Contraseña:
            with st.container(border=True):
                if st.toggle("👁️ Revelar Contraseña", key=f"toggle_{st.session_state.mostrar}"):
                    user = st.session_state.get("usuario_logueado", "Desconocido")
                    srv_name = srv['nombre']
                    try:
                        pwd = test.obtener_password_servidor(srv['id_infisical'])
                        st.code(pwd)
                        logging.info(f"{user} | Visualizó contraseña | SERVIDOR: {srv_name}")
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
                            nueva = test.generar_password()
                            test.cambio_contraseña(nueva, srv["id_infisical"],st.session_state.usuario_logueado)
                            logging.warning(f"{user} | Roto la contraseña   | SERVIDOR: {srv_name}")
                            st.success("Proceso completado, se notificara por correo el cambio realizado")
                    except Exception as e:
                        logging.error(f"{user} | ERROR EN ROTACIÓN: {e} | SERVIDOR: {srv_name}")
                        st.error("Falló en la rotación.")