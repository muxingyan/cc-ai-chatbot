
def generate_response(user_input, role, task, prompts):
    task_prompts = prompts.get(task, {})
    role_prompt = task_prompts.get(role, {})
    intro = role_prompt.get("intro", "")
    pattern = role_prompt.get("response_pattern", "这是一个模拟回答：{input}")
    response_text = pattern.replace("{input}", user_input)
    return {"response": response_text, "role": role}
