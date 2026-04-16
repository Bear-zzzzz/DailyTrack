"""
Agent 状态定义
"""

from typing import TypedDict, List


class AgentState(TypedDict):
    """Agent 的状态"""
    question: str                    # 用户的问题
    thinking_history: List[str]      # 思考过程
    actions: List[dict]              # 执行的工具调用
    observations: List[str]          # 观察到的结果
    iteration_count: int             # 循环次数
    final_answer: str                # 最终答案
    status: str                      # 状态


def create_initial_state(question: str) -> AgentState:
    """初始化状态"""
    return {
        "question": question,
        "thinking_history": [],
        "actions": [],
        "observations": [],
        "iteration_count": 0,
        "final_answer": "",
        "status": "thinking"
    }
