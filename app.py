from flask import Flask, render_template, request, jsonify, session
import json
import random
import os
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
app.secret_key = "super_secret_key"  # 用于用户 session

# 读取 prompts 模板
with open("prompts.json", "r", encoding="utf-8") as f:
    prompts_data = json.load(f)

# 聊天记录存储路径
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

def save_chat_log(user_id, user_input, bot_response):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] 用户: {user_input}\n[{timestamp}] 机器人: {bot_response}\n"
    log_file = os.path.join(LOG_DIR, f"chat_{user_id}.txt")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(log_entry)

# 模拟 LLM 生成（你可以替换为实际 API）
def generate_response(user_input, mode):
    template = prompts_data.get(mode, prompts_data["助手"])
    final_prompt = template.replace("{{input}}", user_input)
    replies = [
        f"你说得对，{user_input} 是个不错的策略。在沙漠中水源和遮蔽确实至关重要。",
        f"的确，{user_input} 是沙漠生存的关键一步，我们还可以尝试寻找岩石阴影躲避高温。",
        f"好主意，{user_input} 能帮助我们保存体力。你还想到其他方法了吗？"
    ]
    return random.choice(replies)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/chat")
def chat_ui():
    if "user_id" not in session:
        return "未登录，请先输入昵称。"
    return render_template("index.html", nickname=session.get("nickname", "陌生人"))

@app.route("/set_nickname", methods=["POST"])
def set_nickname():
    nickname = request.form.get("nickname", "未知")
    user_id = str(uuid4())[:8]  # 简短唯一编号
    session["user_id"] = user_id
    session["nickname"] = nickname
    return jsonify({"status": "ok", "redirect": "/chat"})

@app.route("/api/chat", methods=["POST"])
def api_chat():
    user_input = request.json["message"]
    mode = request.json.get("mode", "助手")
    user_id = session.get("user_id", "guest")
    response = generate_response(user_input, mode)
    save_chat_log(user_id, user_input, response)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True, port=8000)
