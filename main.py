from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

API_KEY = "AIzaSyBhbZufwycOVzlwcIQYjGY0cSX4Ewim8Cs"

def llamar_a_gemini(texto_usuario):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=" + API_KEY
    data = {
        "contents": [
            {
                "parts": [{"text": texto_usuario}]
            }
        ]
    }
    response = requests.post(url, json=data)
    respuesta = response.json()
    try:
        return respuesta['candidates'][0]['content']['parts'][0]['text']
    except:
        return "Lo siento, no pude procesar eso."

@app.route("/")
def home():
    return "Servidor de Mi IA funcionando 🚀"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    user_input = data["queryResult"]["queryText"]
    respuesta = llamar_a_gemini(user_input)
    return jsonify({"fulfillmentText": respuesta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)