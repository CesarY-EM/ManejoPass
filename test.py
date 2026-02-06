import os
import smtplib
import secrets
import string
from email.message import EmailMessage
from dotenv import load_dotenv
from infisical_sdk import infisical_requests, InfisicalSDKClient

load_dotenv("IDs.env")

client = InfisicalSDKClient(host="https://app.infisical.com")
client.auth.universal_auth.login(
    client_id=os.getenv("INFISICAL_CLIENT_ID"),
    client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
)
print("✅ Autenticación exitosa")

def generar_password_segura(longitud=15):
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

def obtener_password_servidor():
    try:
        secret = client.secrets.get_secret_by_name(
            secret_name = "SERVER_ADMIN_PASS",
            project_id = os.getenv("INFISICAL_PROJECT_ID"),
            environment_slug = "dev",
            secret_path = "/"
        )
        return secret.secretValue

    except Exception as e:
        print(f"Error al obtener secreto: {e}")
        return None

def enviar_notificacion(nueva_contra):
    user = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")
    receiver = os.getenv("EMAIL_RECEIVER")

    msg = EmailMessage()
    msg.set_content(f"""
        Hola,
        Se ha realizado una rotación de contraseña exitosa en tus servidores.
        La nueva contraseña es: {nueva_contra}
        Este cambio ya ha sido actualizado automáticamente en Infisical.
        """)

    msg['Subject'] = 'Rotación de Contraseña Exitosa'
    msg['From'] = user
    msg['To'] = receiver

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
            print("📧 Correo de notificación enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")

def cambio_contraseña(nuevo_pass):
    client.secrets.update_secret_by_name(
        current_secret_name = "SERVER_ADMIN_PASS",
        secret_value = nuevo_pass,
        project_id=os.getenv("INFISICAL_PROJECT_ID"),
        environment_slug="dev",
        secret_path="/",
    )


if __name__ == "__main__":
    password_nuevo = generar_password_segura(15)
    cambio_contraseña(password_nuevo)
    enviar_notificacion(password_nuevo)
