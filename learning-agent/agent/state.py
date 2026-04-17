"""
Agent 状态定义

这个模块定义了 Agent 在执行过程中的状态结构。
使用 TypedDict 确保类型安全。
"""

from typing import TypedDict, List


class AgentState(TypedDict):
    """
    Agent 的执行状态

    这个 TypedDict 定义了 Agent 在 LangGraph 中的所有状态字段。
    每个字段的含义和用途：
    """
    question: str                    # 用户输入的问题
    thinking_history: List[str]      # Agent 的思考过程记录（链式思维）
    actions: List[dict]              # 已执行的工具调用记录 [{"tool": "...", "args": {...}}, ...]
    observations: List[str]          # 工具执行结果的观察 (Observation in ReAct)
    iteration_count: int             # 当前循环次数（用于控制最大迭代）
    final_answer: str                # Agent 生成的最终答案
    status: str                      # 当前状态（thinking/acting/judging/done）


def create_initial_state(question: str) -> AgentState:
    """
    创建初始化状态

    Args:
        question: 用户的问题

    Returns:
        AgentState: 初始化后的状态字典

    说明：
        - thinking_history 为空（尚未开始思考）
        - actions 为空（尚未执行任何工具）
        - observations 为空（尚未获得任何观察）
        - iteration_count 为 0（开始第一次循环）
        - 初始状态为 "thinking"（等待思考节点处理）
    """
    return {
        "question": question,
        "thinking_history": [],
        "actions": [],
        "observations": [],
        "iteration_count": 0,
        "final_answer": "",
        "status": "thinking"
    }
