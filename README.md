# Sistema de centralización de contraseñas.

Descripción:
Este programa permite tener usuarios con distintos roles para poder ver / rotar la contraseña de algún servidor dependiendo de su rol.

## Requisitos:
    - Lenguaje Python 3.X
    - Acceso a proyecto configurado en Infisical
    - Archivo .env configurado 
## Librerías usadas:
    - os
    - logging
    - streamlit
    - string
    - secrets
    - smtplib
    - python-dotenv
    - infisicalsdk

## Instalación:
    1. Descargar repositorio
    2. Instalar dependencias
    3. Se pueden hacer pruebas pero para crear la pagina y simularlo en consola es necesario poner el comando: streamlit run vistaPagina.py o el nombre de el archivo donde estan los comandos de la pagina

## Funcionamiento:
El programa utiliza variables de entorno para manejar credenciales y datos sensibles.
Por razones de seguridad, el archivo que contiene estas credenciales no se incluye en el repositorio.
Para este codigo en particular se creo un archivo llamado Ids.env, pero puede crear un archivo con otro nombre, siempre que se modifique el código para que lo cargue correctamente.
Este archivo almacenará las credenciales necesarias para la ejecución del sistema.

    1. Se importa la función load_dotenv() desde la librería dotenv.
    2. Se ejecuta load_dotenv(), lo que permite leer las variables definidas en el archivo .env.
    3. Se obtiene el valor de las variables mediante os.getenv().
    4. El sistema utiliza estas variables para autenticación, envío de correos y gestión de usuarios.
Este trae los siguientes datos (se usaran ejemplos)
INFISICAL_CLIENT_ID
INFISICAL_CLIENT_SECRET 
INFISICAL_PROJECT_ID

EMAIL_USER = “ejemplo@gmail.com”
EMAIL_PASS
EMAIL_RECEIVERS = “receptor1@gmail.com,receptor2@gmail.com”

USUARIOS= usuario:contraseña:rol,usuario2:contraseña2:rol2
## Descripción de variables
    • INFISICAL_CLIENT_ID / SECRET / PROJECT_ID
        Credenciales necesarias para autenticación con el servicio externo.
    • EMAIL_USER
        Correo desde el cual se enviarán los mensajes.
    • EMAIL_PASS
        Contraseña o token de aplicación del correo.
    • EMAIL_RECEIVERS
        Lista de correos separados por comas que recibirán notificaciones.
    • USUARIOS
        Lista de usuarios del sistema en formato:
            usuario:contraseña:rol
## Importante
    • Las variables sensibles deben ser obtenidas por el desarrollador autorizado.
    • Nunca se deben subir credenciales reales al repositorio.
    • El archivo .env debe agregarse al archivo .gitignore.

Al momento de correr el programa se abrirá una pagina en el navegador, puede ser de manera local o remoto, streamlit proporciona las direcciones necesarias para probar ambas.
Como primer vista se maneja la validación de los usuarios que se cargaran del archivo .env, cabe mencionar que se contara con un limite de 3 intentos para poder acceder al portal, en caso de llegar al limite se bloqueara y no se podrá intentar de nuevo hasta que otra persona libere el servicio.
Al poder acceder se vera una sección donde debes elegir el servidor el cual quieras ver / rotar su contraseña.
Si rotas la contraseña esta se generara automáticamente asegurándonos de que tenga cierta longitud y al menos; 1 letra mayúscula, 1 letra minúscula, un carácter especial y un un numero.
Al momento de rotarla esta enviara una notificación a los usuarios que estén en el archivo .env (EMAIL_RECEIVERS).

El sistema utiliza Streamlit como framework para convertir el script de Python en una aplicación web interactiva.
## Cuando se ejecuta el programa:
    1. Streamlit inicia un servidor web local.
    2. Genera automáticamente una URL (por ejemplo: http://localhost:8501).
    3. Abre la aplicación en el navegador predeterminado.
    4. Renderiza los componentes visuales (formularios, botones, selectores, mensajes).
    5. Gestiona la interacción del usuario sin necesidad de programar HTML o JavaScript.

Streamlit es el framework utilizado para desarrollar la interfaz web del sistema. Se encarga de levantar un servidor local, renderizar la interfaz gráfica en el navegador y gestionar la interacción del usuario con la aplicación.

## Historial de Logs / Registro de Actividades
### El sistema tiene un tiene un historial de logs donde, por el momento, se almacenan:
    • Contabilización de intentos de inicio de sesión
    • El usuario que accedió al portal
    • Cuando alguien observo la contraseña de algún servidor
    • Cuando alguien roto la contraseña de algún servidor

Los logs se guardan en un archivo llamado movimientos.log donde siguen el siguiente formato:
Fecha (AAAA-MM-DD) | Tipo de log | usuario (Si aplica) | Accion que se hizo | Servidor afectado (Si aplica)
### Logs: 
    • Permiten identificar errores o problemas de uso, como intentos fallidos de inicio de sesión o accesos no autorizados.
    • Facilitan la auditoría de acciones críticas, como la rotación de contraseñas o la visualización de secretos.
    • Ayudan a reproducir pasos de ejecución si ocurre un fallo en la aplicación, facilitando la localización del error.
    • Sirven como herramienta de seguridad, para detectar patrones inusuales o uso indebido del sistema.
    • Permiten realizar seguimiento de cambios y responsabilidad de usuarios.
## Uso de Infisical en el sistema
El sistema utiliza Infisical como herramienta de gestión segura de secretos y credenciales.
### ¿Por qué se utiliza?
### Infisical se emplea para:
    • Almacenar credenciales sensibles de forma segura.
    • Evitar que contraseñas o claves estén expuestas en el código fuente.
    • Centralizar la administración de secretos.
    • Permitir la rotación segura de contraseñas.
    • Reducir riesgos de filtraciones.
El uso de un gestor de secretos como Infisical permite que las credenciales no estén almacenadas directamente en el código, reduciendo significativamente el riesgo de vulnerabilidades.

### El flujo de integración es el siguiente:
    1. La aplicación se autentica contra Infisical utilizando credenciales de cliente configuradas en variables de entorno.
    2. Se establece una sesión segura con el proyecto correspondiente.
    3. El sistema consulta o actualiza secretos según la operación solicitada.
    4. En caso de rotación de contraseña:
        ◦ Se genera una nueva contraseña bajo políticas de complejidad definidas.
        ◦ Se actualiza el secreto en Infisical.
        ◦ Se notifica a los usuarios autorizados vía correo electrónico.
