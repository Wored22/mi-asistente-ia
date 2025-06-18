from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

API_KEY = 1006247776433

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
    app.run(debug=True)
