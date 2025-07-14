from flask import Flask, render_template, request, jsonify
from chat import get_chatbot_instance

app = Flask(__name__)
c = get_chatbot_instance()

def get_app():
    return app
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def chat():
    user_msg = request.json.get("message")
    reply = c.return_bot_response(user_msg)
    return jsonify({"response": reply})

if __name__ == "__main__":
    app.run(debug=True)