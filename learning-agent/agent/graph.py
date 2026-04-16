"""
LangGraph 图形定义

将四个节点组织成有向无环图（DAG）
"""

from langgraph.graph import StateGraph
from agent.state import AgentState
from agent.nodes import think_node, action_node, judge_node, generate_node


def create_agent_graph():
    """
    创建 Agent 的工作流图

    返回：编译后的 runnable graph
    """

    # ============ 创建图 ============
    graph = StateGraph(AgentState)

    # ============ 添加节点 ============
    graph.add_node("think", think_node)
    graph.add_node("action", action_node)
    graph.add_node("judge", judge_node)
    graph.add_node("generate", generate_node)

    # ============ 添加边（连接） ============
    # 思考 → 行动
    graph.add_edge("think", "action")

    # 行动 → 判断
    graph.add_edge("action", "judge")

    # 判断 → 思考 或 生成（条件边）
    def judge_router(state: AgentState) -> str:
        """判断逻辑：决定是继续思考还是生成答案"""
        # 检查迭代次数
        if state["iteration_count"] >= 3:
            print(f"[判断] 已达最大迭代次数 ({state['iteration_count']}/3)，准备生成答案\n")
            return "generate"

        # 检查观察数量
        if len(state["observations"]) >= 2:
            print(f"[判断] 获得充分信息 ({len(state['observations'])} 个观察)，准备生成答案\n")
            return "generate"

        # 继续思考
        print(f"[判断] 信息不足 ({len(state['observations'])} 个观察)，继续思考\n")
        return "think"

    graph.add_conditional_edges(
        "judge",
        judge_router,
        {
            "think": "think",
            "generate": "generate"
        }
    )

    # ============ 设置入口和出口 ============
    graph.set_entry_point("think")  # 从思考开始
    graph.set_finish_point("generate")  # 生成答案后结束

    # ============ 编译图 ============
    compiled_graph = graph.compile()

    return compiled_graph


# 创建全局 graph 实例
agent_graph = create_agent_graph()
