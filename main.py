from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Clave API de Gemini, se obtiene desde variables de entorno
API_KEY = os.environ.get("GEMINI_API_KEY")

# Verifica si la clave existe, si no lanza un error
if not API_KEY:
    raise ValueError("❌ No se encontró la variable de entorno 'GEMINI_API_KEY'. Configúrala en Render.")

# URL actualizada para Gemini 2.0 Flash
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={API_KEY}"

# Función que hace la llamada a Gemini
def llamar_a_gemini(texto_usuario):
    data = {
        "contents": [
            {
                "parts": [{"text": texto_usuario}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, json=data)
        response.raise_for_status()
        respuesta = response.json()
        print("🔹 Respuesta cruda de Gemini:", respuesta)
        return respuesta['candidates'][0]['content']['parts'][0]['text']
    except requests.exceptions.RequestException as e:
        print("❌ Error de conexión o respuesta:", e)
        try:
            print("❌ Cuerpo de respuesta:", response.text)
        except:
            print("❌ No se pudo acceder a response.text")
        return "Lo siento, hubo un error de conexión con Gemini."
    except Exception as e:
        print("❌ Error inesperado:", e)
        return "Lo siento, ocurrió un error inesperado."

# Ruta raíz simple
@app.route("/", methods=["GET"])
def home():
    return "Servidor de Mi IA funcionando 🚀"

# Webhook para Dialogflow
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🔸 JSON recibido:", data)

    try:
        user_input = data.get("queryResult", {}).get("queryText", "")
        respuesta = llamar_a_gemini(user_input)
        return jsonify({"fulfillmentText": respuesta})
    except Exception as e:
        print("❌ Error en el webhook:", e)
        return jsonify({"fulfillmentText": "Lo siento, hubo un error de conexión con Gemini."})

# Ejecutar servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
