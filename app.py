
from flask import Flask, render_template, request, jsonify
import json
from mock_llm import generate_response

app = Flask(__name__)

with open("prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data["message"]
    role = data["role"]
    task = data["task"]
    responses = generate_response(user_input, role, task, prompts)
    return jsonify(responses)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
