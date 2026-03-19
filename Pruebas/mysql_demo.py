import mysql.connector
import requests
TOKEN = "8413133141:AAFObHI07nV8KxRc9PZDlo7JpafP3me4Vis"
CHAT_ID = "7255322769"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
# conexión
conn = mysql.connector.connect(
    host="localhost",
    user="dba",
    password="123456789",
    database="Abarrotes",
    port=3309
)

# cursor con diccionario (ESTO ES EL "assoc")
cursor = conn.cursor(dictionary=True)

# consulta2
cursor.execute("SELECT * FROM productos_abarrotes limit 5")

# obtener todos los registros
rows = cursor.fetchall()

# recorrer resultados
for row in rows:
    print(row["id"], row["nombre"])
    print(row)   # imprime dict completo
    params = {
        "chat_id": CHAT_ID,
        "text": f"{row["nombre"]} -> {row["precio"]}"
    }
    response = requests.get(url,params=params)

# cerrar
cursor.close()
conn.close()
