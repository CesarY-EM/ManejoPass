import os

class Constantes():
    """
    Clase de constantes del plugin de contraseñas
    """
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    ATH_DB_USUARIOS = os.path.join(BASE_DIR, ".env")
    PATH_LOG_AUDITORIA = os.path.join(BASE_DIR, "movimientos.log")

    INFISICAL_CLIENT_ID = "8fc3ad29-8344-4b88-86c8-6ff17c2fa800"
    INFISICAL_CLIENT_SECRET = "050e4c967422d279b94d2fee808b06cbcf3e4cb80dac32bf84928b3f033ed8f0"
    INFISICAL_PROJECT_ID = "2ac5ac2d-9c99-4d73-bff9-eec4dc86a187"

    #SMTP
    EMAIL_USER = "al2212005959@azc.uam.mx"
    EMAIL_PASS = "aumq nqjn bbbh vror"
    EMAIL_RECEIVERS = "hunter.cm98@gmail.com,al2212005959@azc.uam.mx"

    #Credeciales
    # Formato: USUARIO:PASSWORD:ROL
    USUARIOS = "admin:admin123:editor,viewer:view123:lector"

    SERVIDORES_CONFIG = {
        "GNS3": {
            "IP": "XXX.XXX.X.X",
            "ID_INFISICAL": 2,
            "DESC": "Simulador de red corporativa"
        },
        "DOCKER": {
            "IP": "XXX.XXX.X.X",
            "ID_INFISICAL": 5,
            "DESC": "Servidor de microservicios"
        }
    }