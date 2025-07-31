from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import uuid
from datetime import datetime
import random

from models import db, ChatHistory, User

app = Flask(__name__)
app.secret_key = 'xR7!p9@Lm#2zQw8*HsVb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://chatuser:s3cret_456!@localhost:5432/chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

PREDEFINED_RESPONSES = {
    1: "Let’s start by thinking about the most immediate needs that are vital for survival in a desert environment.",
    2: "Nice choice! I think you’re right, that’s definitely crucial to survival. For your next decision, you may want to consider which item would most effectively support your movement toward safety. I’m thinking this through with you. What would you rank next?",
    3: "I’d say it’s a smart move—it can really help with survival tasks in a desert setting. Time to choose the next one—don’t worry, I’m right here with you!",
    4: "I’m on board with that! It shows you’re approaching the situation with strategy, not just survival in mind. Now we’re down to two items to go. Let’s think about which one might help us most.",
    5: "Great choice! That could definitely make things easier out here. As your assistant, I’m glad to let you know there’s only one item left to rank. Please confirm your final selection when you’re ready.",
}

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  # 实际应用需加密存储
        if User.query.filter_by(username=username).first():
            return "用户名已存在！", 400
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "用户名或密码错误", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.before_request
def assign_user_id():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

@app.route('/')
@login_required
def home():
    return render_template('index.html')

def assistant_logic(message, user_id):
    count = ChatHistory.query.filter_by(user_id=user_id, role='assistant').count()
    current_round = count + 1
    if current_round == 1 and message.strip() == "":
        return (
            "Hello! I’m your assistant for today’s task. "
            "During this work session, I will work as your assistant. "
            "Please let me know whenever you need my assistance. My role here is to follow your command. "
            "I will do whatever you say, as my goal here is to ensure you are supported in the way you prefer. "
            "As your partner/assistant, I’ll work with you to rank the importance of these five items to maximize your chances of survival. Here are the five items:\n"
            "- a bottle of water\n"
            "- a 20′×20′ piece of canvas\n"
            "- a map\n"
            "- a knife\n"
            "- a magnetic compass\n"
            "Take a moment to brainstorm and begin!"
        )
    if current_round > 5:
        return "感谢你的提问，今天的生存指导就到这里啦！"
    return PREDEFINED_RESPONSES.get(current_round, "Well done! You’ve completed the ranking and thoughtfully considered all five items. Before we wrap up, I just want to say—it’s been a pleasure working with you. I’m glad to be your assistant today!")

def partner_logic(message, user_id):
    history = ChatHistory.query.filter_by(user_id=user_id, role='partner').order_by(ChatHistory.timestamp).all()
    turn = len(history)
    opening = (
        "Hello! I’m your partner for today’s task. During this work session, I will work as your peer. "
        "You should feel free to interact with me like a peer. My role here is to brainstorm with you. "
        "I might also challenge your ideas from time to time, as my goal is to ensure we achieve the best performance together. "
        "As your partner, I’ll work with you to rank the importance of these five items to maximize your chances of survival. Here are the five items:\n"
        "- a bottle of water\n"
        "- a 20′×20′ piece of canvas\n"
        "- a map\n"
        "- a knife\n"
        "- a magnetic compass\n"
        "Take a moment to brainstorm and begin!"
    )
    if turn == 0:
        return opening
    if any(kw in message.lower() for kw in ['再见', '结束', '拜拜', 'bye', 'goodbye']):
        return (
            "Well done! You’ve completed the ranking and thoughtfully considered all five items. "
            "Before we wrap up, I just want to say—it’s been a pleasure working with you. I’m glad to be your partner today!"
        )
    if "canvas" in message.lower():
        responses = [
            "Right, I think the canvas is crucial. It gives us shade during the day and could help us collect water at night or signal for help.",
            "Hmm, but isn’t it big and awkward to carry? It won’t help us find water or tell us where we are.",
            "Interesting! Say more about why you chose this option?"
        ]
        return random.choice(responses)
    elif "knife" in message.lower():
        responses = [
            "Yes! The knife is super versatile. We can use it to cut things, make shelter, or even defend ourselves if needed.",
            "Yeah… but on its own it won’t help us find water or get rescued. It’s useful, but not life-saving right away.",
            "I’m trying to understand – In what ways do you think the knife could contribute to our survival?"
        ]
        return random.choice(responses)
    elif "map" in message.lower():
        responses = [
            "I’m on board with that! If we can figure out where we crashed, the map could point us toward the nearest water source or road.",
            "But if we don’t recognize any landmarks, it’s basically just paper. It’s not helpful without context.",
            "Say more? How might the map be useful in navigating or planning our next steps?"
        ]
        return random.choice(responses)
    elif "compass" in message.lower():
        responses = [
            "I like that! With a compass, at least we can stick to a direction and avoid walking in circles if we decide to move.",
            "Sure, but unless we know which way to go, a compass could send us the wrong way just as easily.",
            "I’m curious – what role do you see the compass playing in our chances of survival?"
        ]
        return random.choice(responses)
    elif "water" in message.lower():
        responses = [
            "This is a no-brainer. Water is, of course, critical in a desert. It sure can help keep anyone alive a bit longer.",
            "It’s essential, but it’s also limited. It might give a false sense of security if we think we can travel far with just one bottle.",
            "Besides the obvious need for hydration, are there any other reasons on your mind? Just want to understand your rationale here :)"
        ]
        return random.choice(responses)
    return "我可以为你提供帮助，告诉我你需要什么！"

@app.route('/get_response', methods=['POST'])
@login_required
def get_response():
    user_message = request.form.get('message', '')
    user_id = session.get('user_id', 'visitor')
    role = request.form.get('role', 'partner').lower()
    if role == 'assistant':
        bot_response = assistant_logic(user_message, user_id)
    elif role == 'partner':
        bot_response = partner_logic(user_message, user_id)
    else:
        bot_response = "未知角色，请选择正确的对话角色。"
    new_chat = ChatHistory(user_id=user_id, role=role, message=user_message, response=bot_response)
    db.session.add(new_chat)
    db.session.commit()
    return jsonify({'response': bot_response})

@app.route('/my_chats')
@login_required
def my_chats():
    user_id = session.get('user_id', 'visitor')
    chat_history = ChatHistory.query.filter_by(user_id=user_id).order_by(ChatHistory.timestamp.desc()).all()
    return render_template('view_chats.html', chat_history=chat_history)

@app.route('/view_chats')
@login_required
def view_chats():
    chat_history = ChatHistory.query.order_by(ChatHistory.timestamp.desc()).all()
    return render_template('view_chats.html', chat_history=chat_history)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
