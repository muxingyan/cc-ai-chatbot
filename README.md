# 沙漠生存助手 Chatbot 项目

这是一个可部署在 Render 平台上的 Flask 聊天机器人项目，主题为“沙漠求生任务”。

## 🛠 功能

- 基于 Web 的聊天界面（HTML+Flask）
- 沙漠求生主题引导 + AI 响应
- 可切换为真实 LLM 接入（例如本地模型 / API）

## 🚀 Render 部署方法

1. 创建 Git 仓库并推送此项目代码
2. 登录 [https://render.com](https://render.com)
3. 新建 Web Service：
   - Runtime: Python
   - Start Command: `gunicorn app:app`
   - Build Command: `pip install -r requirements.txt`
4. 等待自动部署并访问公开链接！

## 本地运行（可选）

```bash
pip install -r requirements.txt
python app.py
```

访问：http://127.0.0.1:10000
