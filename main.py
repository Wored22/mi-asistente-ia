from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Clave API de Gemini (sustituye esta por la tuya si es necesario)
API_KEY = "TU_CLAVE_API_AQUI"

# Función que hace la llamada a Gemini
def llamar_a_gemini(texto_usuario):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={API_KEY}"
    data = {
        "contents": [
            {
                "parts": [{"text": texto_usuario}]
            }
        ]
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()  # Lanza error si el código HTTP no es 200
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

# Ruta raíz para probar que el servidor funciona
@app.route("/")
def home():
    return "Servidor de Mi IA funcionando 🚀"

# Webhook para Dialogflow o Postman
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("🔸 JSON recibido de Dialogflow/Postman:", data)

    try:
        user_input = data["queryResult"]["queryText"]
        respuesta = llamar_a_gemini(user_input)
        print("🔹 Respuesta cruda de Gemini:", respuesta)
        return jsonify({"fulfillmentText": respuesta})
    except Exception as e:
        print("❌ Error de conexión o respuesta:", e)
        print("❌ Cuerpo de respuesta:", data)
        return jsonify({"fulfillmentText": "Lo siento, hubo un error de conexión con Gemini."})

# Ejecutar servidor Flask
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
