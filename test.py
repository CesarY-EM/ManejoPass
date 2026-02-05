import os
from dotenv import load_dotenv
from infisical import *
from infisical_sdk import infisical_requests, InfisicalSDKClient
load_dotenv("IDs.env")

# 2. Inicializamos el cliente
# El SDK suele manejar internamente el login con las credenciales que le pases
client = InfisicalSDKClient(
    client_id=os.getenv("INFISICAL_CLIENT_ID"),
    client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
)

def obtener_password_servidor():
    try:
        # 3. Usamos el cliente para traer el secreto
        # Nota: Los nombres de los métodos pueden variar levemente según la versión,
        # pero usualmente es .get_secret() o .secrets.get()
        secret = client.get_secret(
            name="SERVER_ADMIN_PASS",
            project_id=os.getenv("INFISICAL_PROJECT_ID"),
            environment="dev"
        )
        return secret.value
    except Exception as e:
        print(f"Error al obtener secreto: {e}")
        return None

# Prueba de fuego
password_actual = obtener_password_servidor()
if password_actual:
    print("✅ Conexión con Infisical exitosa.")