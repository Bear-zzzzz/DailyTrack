"""
Agent 的四个核心节点实现

节点流程：
  思考 → 行动 → 判断 → [继续思考 或 生成答案]
"""

import json
from typing import Dict, Any
from agent.state import AgentState
from agent.tools import execute_tool
from config import llm_config


# ============ 节点 1：思考节点 ============

def think_node(state: AgentState) -> Dict[str, Any]:
    """
    思考节点：Agent 分析当前信息，决定下一步行动
    """
    # 构建上下文1
    question = state["question"]
    history = "\n".join(state["thinking_history"]) if state["thinking_history"] else "无"
    observations = "\n".join(state["observations"]) if state["observations"] else "无"
    iteration = state["iteration_count"] + 1

    # 构建提示词
    prompt = f"""你是一个智能学习助手。基于用户的问题和已有的信息，决定下一步该做什么。

用户问题：{question}

之前的思考过程：
{history}

已有的观察/信息：
{observations}

迭代次数：{iteration}/3

请分析现有信息是否充分。如果不充分，决定下一步应该：
1. search_kb - 搜索知识库
2. get_concepts - 获取相关概念
3. get_code - 获取代码示例

回复格式必须是：
思考：[你的分析]
行动：[工具名称]
参数：{{"query": "..."}}"""

    # 调用 LLM
    response = llm_config.call_llm(prompt)

    # 解析响应
    thinking = _extract_thinking(response)
    action = _extract_action(response)
    params = _extract_params(response)

    print(f"[思考] {thinking}")
    print(f"[行动] {action}, 参数: {params}\n")

    # 更新状态
    return {
        "thinking_history": state["thinking_history"] + [thinking],
        "actions": state["actions"] + [{"tool": action, "args": params}],
        "status": "acting"
    }


def _extract_thinking(response: str) -> str:
    """提取思考部分"""
    try:
        if "思考：" in response:
            return response.split("思考：")[1].split("行动：")[0].strip()
    except:
        pass
    return response[:100]


def _extract_action(response: str) -> str:
    """提取行动（工具名称）"""
    try:
        if "行动：" in response:
            action = response.split("行动：")[1].split("参数：")[0].strip()
            return action.lower()
    except:
        pass
    return "search_kb"


def _extract_params(response: str) -> dict:
    """提取参数"""
    try:
        if "参数：" in response:
            params_str = response.split("参数：")[1].strip()
            if "{" in params_str:
                json_start = params_str.find("{")
                json_end = params_str.rfind("}") + 1
                return json.loads(params_str[json_start:json_end])
    except:
        pass
    return {"query": "AI"}


# ============ 节点 2：工具调用节点 ============

def action_node(state: AgentState) -> Dict[str, Any]:
    """
    工具调用节点：执行待执行的工具
    """
    if not state["actions"]:
        return {
            "observations": state["observations"] + ["错误：无待执行行动"],
            "iteration_count": state["iteration_count"] + 1,
            "status": "judging"
        }

    # 获取最后一个行动
    action = state["actions"][-1]
    tool_name = action.get("tool", "search_kb")
    tool_args = action.get("args", {})

    # 执行工具
    try:
        result = execute_tool(tool_name, tool_args)
    except Exception as e:
        result = f"工具执行错误：{str(e)}"

    # 截断长结果
    if len(result) > 300:
        result = result[:300] + "\n...[内容已截断]"

    print(f"[工具结果] {result[:100]}...\n")

    return {
        "observations": state["observations"] + [result],
        "iteration_count": state["iteration_count"] + 1,
        "status": "judging"
    }


# ============ 节点 3：判断节点 ============

def judge_node(state: AgentState) -> Dict[str, Any]:
    """
    判断节点：这个节点不直接改变状态，只返回空字典
    实际的路由决策在 graph.py 的 judge_router 中进行
    """
    # 这个节点只是为了在图中占一个位置
    # 实际的决策在 judge_router 中进行
    return {}


# ============ 节点 4：生成答案节点 ============

def generate_node(state: AgentState) -> Dict[str, Any]:
    """
    生成答案节点：整合信息生成最终答案
    """
    # 整合信息
    question = state["question"]
    observations = "\n---\n".join(state["observations"])

    # 生成提示词
    prompt = f"""根据以下信息，为用户生成一个清晰、完整的答案。

用户问题：{question}

获取的信息：
{observations}

请生成最终答案，包含：
1. 直接回答问题
2. 关键概念说明
3. 代码示例（如果有）
4. 总结

最终答案："""

    # 调用 LLM
    final_answer = llm_config.call_llm(prompt)

    print(f"[生成答案]\n{final_answer}\n")

    return {
        "final_answer": final_answer,
        "status": "done"
    }
