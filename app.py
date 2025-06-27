from flask import Flask, render_template, request, jsonify
from chat import Chat

app = Flask(__name__)
c = Chat()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    bot_response = c.response(user_message)
    print(bot_response)

    return jsonify({'response': bot_response})

def get_app():
    return app

if __name__ == '__main__':
    app.run(debug=True)