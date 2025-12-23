from flask import Flask, render_template, request, jsonify
from flask_cors import CORS  # 1. Import CORS
from chat import get_chatbot_instance

app = Flask(__name__)
CORS(app) # 2. Enable CORS for all routes

c = get_chatbot_instance()

def get_app():
    return app

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat():
    # Adding a small safety check for JSON data
    data = request.get_json()
    if not data:
        return jsonify({"response": "No data received"}), 400
        
    user_msg = data.get("message")
    reply = c.return_bot_response(user_msg)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)
