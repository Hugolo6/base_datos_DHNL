import requests


TOKEN = "8413133141:AAFObHI07nV8KxRc9PZDlo7JpafP3me4Vis"
CHAT_ID = "7255322769"

# 📩 Mensaje a enviar
mensaje = "Hola 👋 mensaje enviado desde Python"

# URL del endpoint
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

# Parámetros GET
params = {
    "chat_id": CHAT_ID,
    "text": mensaje
}

# Petición GET
response = requests.get(url, params=params)

# Mostrar respuesta
print("Status:", response.status_code)
print("Respuesta:", response.json())
