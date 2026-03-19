import telebot
import os
import json
import datetime
import subprocess

from libs.m5config import M5config
from libs.m5bot import M5bot
from libs.m5mysql import M5mysql


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "libs", "config.json")

with open(config_path, "r") as f:
    config = json.load(f)

db_user = config["mysql"]["user"]
db_password = config["mysql"]["password"]

config = M5config()
botconfig = config.get("bot")


bot = telebot.TeleBot(botconfig["token"], parse_mode=None)
print("bot iniciado")

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    print(message.chat.id)
    user = message.from_user.first_name
    print(user)
    bot.reply_to(message, f"Hola, Bienvenido al bot {user}")

@bot.message_handler(commands=["cuanto_cuesta", "cuanto"])
def cuanto_cuesta(message):
    print(message.text)
    texto = message.text.split()
    mysql = M5mysql()
    sql = f"select * from productos_abarrotes where nombre like '%{texto[1]}%'"
    print(sql)
    result = mysql.query(sql)
    respuesta = ""
    for r in result:
        respuesta = respuesta + "\n" + f"{r["nombre"]}: ${r["precio"]}"
    bot.reply_to(message, respuesta)

@bot.message_handler(commands=["acerca_de"])
def send_welcome(message):
    print(message.chat.id)
    photo = open('cd /mnt/c/py/m5bot/mi_foto.jpg', 'rb')
    bot.send_photo(message.chat_id, photo)
    bot.send_photo(message.chat_id, "FILEID")


@bot.message_handler(commands=["ayuda"])
def ayuda(message):
    respuesta = (
        "Comandos disponibles:\n\n"
        "/cuanto ó /cuanto_cuesta (producto) -> muestra el precio del producto\n"
        "/acerca_de ->muestra info respecto al paaco\n"
        "/total_inventario -> muestra el inventario"
    )

    bot.reply_to(message, respuesta)

@bot.message_handler(commands=["acerca_de"])
def ayuda(message):
    respuesta = (
        "Información de yo :)\n\n"
        "Nombre: Paco el chato\n"
        "Carrera: ISIC\n"
        "Semestre: 6to\n"
        "Artista fav: TS\n"
        "Intereses: bd, programming, frontend, guitarras blancas\n"
    )



    bot.reply_to(message, respuesta)
@bot.message_handler(commands=["total_inventario"])
def total_inventario(message):

    mysql = M5mysql()
    sql = "SELECT nombre, stock, precio, (precio * stock) AS total_producto FROM productos_abarrotes"
    result = mysql.query(sql)

    respuesta = "Inventario:\n"
    total_dinero = 0
    for r in result:
        respuesta += (
            "\n---------------------------------\n"
            f"\n{r['nombre']}\n "
            f"Stock: {r['stock']}\n"
            f"Total: ${r['total_producto']}"
        )

        total_dinero += r['total_producto']

    respuesta += f"\n\n*****************************\n Dinero total en inventario: ${total_dinero}"

    bot.reply_to(message, respuesta)

@bot.message_handler(commands=["Estatus_tabla", "status"])
def estatus_tabla(message):
    print(message.chat.id)

    mysql = M5mysql()

    sql = """
    SELECT TABLE_NAME, ENGINE, TABLE_ROWS 
    FROM information_schema.TABLES 
    WHERE TABLE_SCHEMA = 'super_dba' 
    AND TABLE_TYPE = 'BASE TABLE'
    """

    print(sql)

    result = mysql.query(sql)

    if not result:
        bot.reply_to(message, "No se encontraron tablas.")
        return

    respuesta = "Estatus de Tablas:\n"

    for r in result:
        respuesta += f"\n   Tabla: {r['TABLE_NAME']}"
        respuesta += f"\n   Motor: {r['ENGINE']}"
        respuesta += f"\n   Filas: {r['TABLE_ROWS']}\n"

    bot.reply_to(message, respuesta)


@bot.message_handler(commands=["backup"])
def backup_general_log(message):
    try:
        import pymysql
        import os
        import datetime
        import json

        # Leer configuración
        config_path = os.path.join(os.path.dirname(__file__), "libs", "config.json")
        with open(config_path, "r") as f:
            config_local = json.load(f)

        db_user = config_local["mysql"]["user"]
        db_password = config_local["mysql"]["password"]
        db_host = config_local["mysql"]["host"]
        db_port = config_local["mysql"]["port"]

        partes = message.text.split()
        if len(partes) < 2:
            bot.reply_to(message, "❌ Debes indicar la base.\nEjemplo: /backup super_dba")
            return

        base_filtrar = partes[1]

        # Conexión a MySQL (solo para controlar estado del log)
        conn = pymysql.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database="mysql",
            port=db_port,
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor
        )

        with conn.cursor() as cursor:
            # Guardar estado del log
            cursor.execute("SELECT @@GLOBAL.general_log AS log_state")
            old_log_state = cursor.fetchone()['log_state']

            cursor.execute("FLUSH LOGS")

            # Apagar log temporalmente
            cursor.execute("SET GLOBAL general_log = OFF")
            print("🔇 Log general desactivado temporalmente")

            # Leer registros desde el archivo
            log_file = "/var/log/mysql/general.log"
            registros = []
            with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                for linea in f:
                    if base_filtrar in linea:
                        registros.append(linea.strip())

            if not registros:
                bot.reply_to(message, f"⚠️ No hay registros en el log para la base '{base_filtrar}'.")
                cursor.execute(f"SET GLOBAL general_log = {old_log_state}")
                conn.close()
                return

            # Preparar rutas
            ahora = datetime.datetime.now()
            fecha = ahora.strftime("%Y-%m-%d")
            hora = ahora.strftime("%H-%M-%S")
            usuario_telegram = message.from_user.username or "sin_usuario"

            backup_root = "/home/hogolo/mysql_backups"
            destino_dir = os.path.join(backup_root, fecha)
            os.makedirs(destino_dir, exist_ok=True)

            backup_sql = os.path.join(
                destino_dir,
                f"general_{base_filtrar}_{usuario_telegram}_{hora}.sql"
            )

            # Crear archivo SQL
            with open(backup_sql, "w", encoding="utf-8") as f:
                f.write("-- BACKUP GENERAL LOG (desde archivo)\n")
                f.write(f"-- Base filtrada: {base_filtrar}\n")
                f.write(f"-- Fecha: {fecha} {hora}\n")
                f.write(f"-- Usuario Telegram: {usuario_telegram}\n\n")

                f.write("CREATE TABLE IF NOT EXISTS general_log_backup (\n")
                f.write(" linea_log TEXT\n")
                f.write(");\n\n")

                for linea in registros:
                    linea_sql = linea.replace("'", "\\'")
                    f.write(f"INSERT INTO general_log_backup VALUES ('{linea_sql}');\n")

            # Restaurar estado del log
            cursor.execute(f"SET GLOBAL general_log = {old_log_state}")
            print(f"🔊 Log restaurado a: {old_log_state}")

        conn.close()

        bot.reply_to(
            message,
            f"✅ Backup realizado correctamente\n"
            f"📦 Archivo: {backup_sql}\n"
            f"📊 Registros respaldados: {len(registros)}\n"
            f"🧹 general_log sigue activo."
        )

    except pymysql.Error as e:
        bot.reply_to(message, f"❌ Error de MySQL: {str(e)}")
    except Exception as e:
        bot.reply_to(message, f"❌ Error general: {str(e)}")


@bot.message_handler(commands=["buscar"])
def buscar_backup_por_fecha(message):
    try:
        import os

        backup_root = "/home/hogolo/mysql_backups"

        partes = message.text.split()
        if len(partes) < 2:
            bot.reply_to(message, "❌ Debes indicar una fecha.\nEjemplo: /buscar 2026-03-04")
            return

        fecha_buscar = partes[1]
        ruta_fecha = os.path.join(backup_root, fecha_buscar)

        if not os.path.exists(ruta_fecha) or not os.path.isdir(ruta_fecha):
            bot.reply_to(message, f"❌ No existen backups para la fecha {fecha_buscar}")
            return

        # Caso 1: Se proporcionó también el nombre del archivo → enviarlo
        if len(partes) >= 3:
            nombre_archivo = partes[2]
            # Seguridad: evitar rutas relativas maliciosas
            if ".." in nombre_archivo or "/" in nombre_archivo:
                bot.reply_to(message, "❌ Nombre de archivo no válido.")
                return

            ruta_archivo = os.path.join(ruta_fecha, nombre_archivo)
            if not os.path.isfile(ruta_archivo):
                bot.reply_to(message, f"❌ El archivo '{nombre_archivo}' no existe en {fecha_buscar}.")
                return

            # Enviar el archivo como documento
            with open(ruta_archivo, 'rb') as f:
                bot.send_document(message.chat.id, f, caption=f"📁 Backup: {nombre_archivo}")
            return

        # Caso 2: Solo fecha → listar archivos
        archivos = os.listdir(ruta_fecha)
        archivos = [a for a in archivos if os.path.isfile(os.path.join(ruta_fecha, a))]

        if not archivos:
            bot.reply_to(message, f"⚠️ La carpeta existe pero no hay backups en {fecha_buscar}")
            return

        respuesta = f"📂 Backups encontrados para {fecha_buscar}:\n\n"
        for archivo in archivos:
            respuesta += f"• {archivo}\n"
        respuesta += "\nPara descargar uno, usa: /buscar <fecha> <nombre_archivo>"

        bot.reply_to(message, respuesta)

    except Exception as e:
        bot.reply_to(message, f"❌ Error al buscar backups:\n{str(e)}")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
bot.infinity_polling()
#como correr el bot
#python bot.py