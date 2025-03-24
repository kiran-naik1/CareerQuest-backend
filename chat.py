from flask import Flask, request, jsonify
import requests
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

# Get API details from .env
API_URL = os.getenv("CHATBOT_API_URL")
HEADERS = {"Authorization": f"Bearer {os.getenv('CHATBOT_API_KEY')}"}

def chatbot_response(prompt):
    response = requests.post(API_URL, headers=HEADERS, json={
        "inputs": prompt,
        "parameters": {"max_new_tokens": 150, "temperature": 0.7, "top_p": 0.9}
    })

    if response.status_code != 200:
        return f"Error {response.status_code}: {response.text}"

    try:
        data = response.json()
        if isinstance(data, list):
            data = data[0]
        return data.get("generated_text", "Sorry, I couldn't process that.")
    except requests.exceptions.JSONDecodeError:
        return "Error: Invalid JSON response from API."

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    bot_response = chatbot_response(user_input)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
