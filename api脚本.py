from flask import Flask, request, jsonify
import openai  # 假设你用 OpenAI 作为你的后台模型

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')  # 获取用户的消息
    prompt = f"请根据以下内容回答：{user_input}"
    
    # 连接 OpenAI API（可以换成其他模型API）
    openai.api_key = '你的API密钥'
    response = openai.Completion.create(
        model="gpt-4",  # 你可以根据需要选择模型
        prompt=prompt,
        max_tokens=150
    )

    return jsonify({"response": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(debug=True,port=8000)
