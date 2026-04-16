"""
工具函数
"""


def format_thinking(history: list) -> str:
    """格式化思考历史"""
    return "\n".join([f"- {t}" for t in history])


def format_actions(actions: list) -> str:
    """格式化行动"""
    result = []
    for action in actions:
        result.append(f"- 工具：{action.get('tool', 'N/A')}")
        if 'args' in action:
            result.append(f"  参数：{action['args']}")
    return "\n".join(result)


def format_observations(obs: list) -> str:
    """格式化观察"""
    return "\n".join([f"观察 {i+1}：{o}" for i, o in enumerate(obs)])


def should_continue(iteration_count: int, observations: list) -> bool:
    """判断是否应该继续循环"""
    if iteration_count >= 3:  # 最多 3 次循环
        return False
    if len(observations) >= 2:  # 有足够的观察
        return False
    return True
