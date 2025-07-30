from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)

# 读取提示词
with open("prompts_full.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data.get("message", "")
    # 简单模拟响应（你可替换为真正的 LLM 或规则）
    reply = prompts.get("default_reply", "收到，我会尽力协助你生存。")
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
