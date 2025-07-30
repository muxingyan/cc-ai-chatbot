from flask import Flask, request, jsonify

app = Flask(__name__)

# 专家排序标准（示例，可替换成真实专家结论）
EXPERT_PRIORITY = [
    "一瓶水", "一把刀", "一块 20 英尺×20 英尺的帆布", 
    "一个磁罗盘", "一张地图"
]

# 不同角色（伙伴/助手）的回复模板
ROLE_RESPONSES = {
    "assistant": {
        "step1": "沙漠生存最迫切需求是补水、防晒、找方向！先选最救命的，你觉得哪件最关键？",
        "agree": "选得对！这确实能解决生存核心问题 —— 接下来怎么用它推进任务？",
        "guide": "下一步建议优先保障移动/导航，比如地图/罗盘，你想选哪个？"
    },
    "partner": {
        "canvas_agree": (
            "同意！帆布白天遮阳、晚上凝水、还能做求救信号，"
            "但它需要搭配刀裁剪，你打算咋用？"
        ),
        "canvas_disagree": (
            "有道理！帆布又大又占地方，没刀的话很难改造，"
            "或许该先选工具类物品？比如刀？"
        ),
        "knife_agree": (
            "对！刀能切割、建庇护所、自卫，"
            "但没水/方向的话，光有工具也难持久，你觉得呢？"
        ),
        "knife_disagree": (
            "是啊，刀解决不了「水源/迷路」核心问题，"
            "或许该先选水/罗盘？"
        ),
        # 更多物品逻辑可继续扩展...
    }
}

# 处理对话的核心逻辑
def process_dialogue(user_input, role):
    """
    user_input: 用户输入（如“我选水”）
    role: assistant/partner
    返回：智能回复
    """
    # 助手模式：引导式提问
    if role == "assistant":
        if "水" in user_input:
            return ROLE_RESPONSES["assistant"]["agree"] + "\n" + ROLE_RESPONSES["assistant"]["guide"]
        return ROLE_RESPONSES["assistant"]["step1"]
    
    # 伙伴模式：挑战/补充想法
    if role == "partner":
        if "帆布" in user_input:
            if "同意" in user_input.lower():
                return ROLE_RESPONSES["partner"]["canvas_agree"]
            else:
                return ROLE_RESPONSES["partner"]["canvas_disagree"]
        elif "刀" in user_input:
            if "同意" in user_input.lower():
                return ROLE_RESPONSES["partner"]["knife_agree"]
            else:
                return ROLE_RESPONSES["partner"]["knife_disagree"]
    return "你的选择很特别！能详细说说理由吗？"  # 兜底回复


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message', '')
    role = data.get('role', 'assistant')  # 默认 assistant

    response = process_dialogue(user_input, role)
    return jsonify({"response": response, "expert_tip": f"专家标准：{EXPERT_PRIORITY}"})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
