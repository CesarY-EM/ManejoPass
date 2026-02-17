import os
import smtplib
import secrets
import string
from email.message import EmailMessage
from dotenv import load_dotenv
from infisical_sdk import infisical_requests, InfisicalSDKClient

load_dotenv("IDs.env")

servidores = {1 : "GNS3",
              2: "SERVER_ADMIN_PASS"}

# Iniciamos el cliente y le pasamos la credenciales que se encuentrarn en IDs.env
client = InfisicalSDKClient(host="https://app.infisical.com")
client.auth.universal_auth.login(
    client_id=os.getenv("INFISICAL_CLIENT_ID"),
    client_secret=os.getenv("INFISICAL_CLIENT_SECRET")
)

#Confirmacion de autentificacion
print("✅ Autenticación exitosa")

# Funcion para generar nueva contraseña
def generar_password(longitud=15):
    minusculas = string.ascii_lowercase
    mayusculas = string.ascii_uppercase
    numeros = string.digits
    especiales = "!@#$%^&*()-_=+"


    #Nos aseguramos que la contraseña al menos tenga un caracter enminuscula, mayuscula, digito y un especial
    password = [
        secrets.choice(minusculas),
        secrets.choice(mayusculas),
        secrets.choice(numeros),
        secrets.choice(especiales)
    ]

    #Creamos de donde se agarrara el complemento de la contraseña
    todos_los_caracteres = minusculas + mayusculas + numeros + especiales

    #Rellenamos lo que falta de la contraseña
    for _ in range(longitud - len(password)):
        password.append(secrets.choice(todos_los_caracteres))

    #Una vez que ya tenemos la contraseña mezclamos para mas seguridad
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)

#Metodo para contener la contraseña actual del servidor
def obtener_password_servidor(server):
    servidor = servidores.get(server)
    try:
        secret = client.secrets.get_secret_by_name(
            secret_name = servidor, #Nombre del servidor el cual queremos saber su contraseña
            project_id = os.getenv("INFISICAL_PROJECT_ID"), # ID del proyecto que se encuentra en infisical
            environment_slug = "dev", #environment donde se creo el proyecto
            secret_path = "/"
        )
        return secret.secretValue

    except Exception as e:
        print(f"Error al obtener secreto: {e}")
        return None


#Funcion que se encarga de enviar la notificacion por correo cuando se rote la contraseña
#El parametro sera la nueva contraseña y el servidor para agregarlos al correo
def enviar_notificacion(nueva_contra, server, usuario):
    servidor = servidores.get(server)
    user = os.getenv("EMAIL_USER") # Usuario que enviara el correo
    password = os.getenv("EMAIL_PASS") # Contraseña de dispositivo, este lo obtenemos en configuracion de tu cuenta de google
    receiver = os.getenv("EMAIL_RECEIVERS") # Usuario que recibira el correo (pueden ser varios)

    msg = EmailMessage()
    msg.set_content(f"""
        Hola,
        Se ha realizado una rotación de contraseña exitosa en tu servidor de: {servidor}.
        La nueva contraseña es: {nueva_contra}.
        La persona que solicito el cambio fue: {usuario}
        Este cambio ya ha sido actualizado automáticamente en Infisical.
        """)

    msg['Subject'] = 'Rotación de Contraseña Exitosa'
    msg['From'] = user
    msg['To'] = receiver.split(",")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(user, password)
            smtp.send_message(msg)
            print("📧 Correo de notificación enviado correctamente.")
    except Exception as e:
        print(f"❌ Error al enviar el correo: {e}")

# Metodo para cambiar la contraseña del servidor
def cambio_contraseña(nuevo_pass, server, usuario):
    servidor = servidores.get(server)
    client.secrets.update_secret_by_name(
        current_secret_name = servidor, #Nombre del servidor donde queremos rotar la contraseña
        secret_value = nuevo_pass, #nueva contraseña
        project_id=os.getenv("INFISICAL_PROJECT_ID"),
        environment_slug="dev",
        secret_path="/",
    )
    print("El password ha sido cambiado correctamente")
    enviar_notificacion(nuevo_pass, server, usuario)

if __name__ == "__main__":
    #password_nuevo = generar_password(15)
    #cambio_contraseña(password_nuevo, 2, "Cesar")
    #print(obtener_password_servidor(1))
    print ("Prueba")
