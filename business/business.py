import secrets 
import streamlit as st
import logging
from constants import constants
from infisical_sdk import infisical_requests, InfisicalSDKClient
import string
from datetime import datetime, timedelta
from dotenv import load_dotenv

TIEMPO_LIMITE = 3
load_dotenv("IDs.env")

servidores = {1 : "GNS3",
              2: "SERVER_ADMIN_PASS"}

# Iniciamos el cliente y le pasamos la credenciales que se encuentrarn en IDs.env
client = InfisicalSDKClient(host="https://app.infisical.com")
client.auth.universal_auth.login(
    client_id = constants.Constantes.INFISICAL_CLIENT_ID,
    client_secret = constants.Constantes.INFISICAL_CLIENT_SECRET
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
    },
    "servidor 4": {
        "nombre": "servidor 4",
        "id_infisical": 4,
        "descripcion": "descripcion 4"
    },
    "servidor 5": {
        "nombre": "servidor 5",
        "id_infisical": 5,
        "descripcion": "descripcion 5"
    },
    "servidor 6": {
        "nombre": "servidor 6",
        "id_infisical": 6,
        "descripcion": "descripcion 6"
    },
    "servidor 7": {
        "nombre": "servidor 4",
        "id_infisical": 4,
        "descripcion": "descripcion 4 "
    },
    "servidor 8": {
        "nombre": "servidor 4",
        "id_infisical": 4,
        "descripcion": "descripcion 4 "
    }
}

def setup_logging():
    """Configuracion basica de logging"""
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s',
        level=logging.INFO
    )

def generar_password():
    longitud = 15
    """
    Funcion para generar contraseña con requerimientos estandarizados

    Args:
        None: No recibe nada

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
            project_id = constants.Constantes.INFISICAL_PROJECT_ID,
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

    Return: No regresa
    
    """

    servidor = servidores.get(server)
    client.secrets.update_secret_by_name(
        current_secret_name = servidor,
        secret_value = nuevo_pass,
        project_id= constants.Constantes.INFISICAL_PROJECT_ID,
        environment_slug="dev",
        secret_path="/",
    )
    # print("El password ha sido cambiado correctamente")
    # enviar_notificacion(nuevo_pass, server, usuario)


def obtener_usuarios():
    """
    Funcion que nos permite obtener los usuarios que se encuentran en unarchivo .env

    Args: 
        None: No recibe

    Returns:
        diccionario_usuario (diccionario): usuario, contraseña y rol de los usuarios encontrados    
    """
    usuarios_str = constants.Constantes.USUARIOS
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
                        st.session_state["ultimo_movimiento"] = datetime.now()
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

def sesion_expirada():
    if "ultimo_movimiento" not in st.session_state:
        return True
    
    tiempo_inactivo = datetime.now() - st.session_state["ultimo_movimiento"]
    return tiempo_inactivo > timedelta(minutes=TIEMPO_LIMITE)

def cerrar_sesion():
    st.session_state.clear()
