# 🔌 Agent 实现指南 - Phase 3 图形组合

**开始时间**：2026-04-15
**目标**：将节点组合成 LangGraph 图形
**最终产物**：agent/graph.py 完整代码

---

# Phase 3：图形组合

## 3.1 使用 LangGraph 组合节点

LangGraph 的核心是将节点和边组织成一个有向无环图（DAG）。

### 基本概念

```python
from langgraph.graph import StateGraph

# 1. 定义状态（已在 Phase 1 完成）
class AgentState(TypedDict):
    question: str
    thinking_history: List[str]
    actions: List[dict]
    observations: List[str]
    iteration_count: int
    final_answer: str
    status: str

# 2. 定义节点（已在 Phase 2 完成）
def think_node(state): ...
def action_node(state): ...
def judge_node(state): ...
def generate_node(state): ...

# 3. 创建图
graph = StateGraph(AgentState)

# 4. 添加节点
graph.add_node("think", think_node)
graph.add_node("action", action_node)
graph.add_node("judge", judge_node)
graph.add_node("generate", generate_node)

# 5. 添加边（连接）
graph.add_edge("think", "action")
graph.add_edge("action", "judge")

# 6. 添加条件边（judge 根据条件选择下一个节点）
graph.add_conditional_edges(
    "judge",
    lambda state: "think" if state["status"] == "thinking" else "generate",
    {
        "think": "think",      # 继续思考
        "generate": "generate"  # 生成答案
    }
)

# 7. 设置入口和出口
graph.set_entry_point("think")
graph.set_finish_point("generate")

# 8. 编译图
runnable_graph = graph.compile()
```

### 流程图解释

```
        ┌─→ [思考节点]
        │        ↓
    开始 ┤   [工具调用节点]
        │        ↓
        │   [判断节点]
        │     /    \
        │    /      \
       否  /          \ 是
        │ /            \
        └→ [回到思考]   [生成答案]
                          ↓
                        结束
```

## 3.2 条件边的关键

```python
def router(state: AgentState) -> str:
    """
    路由函数：根据状态决定下一个节点

    返回：下一个节点的名称
    """
    # judge_node 会设置 status 为 "judging"
    # 这里根据其他状态变量决定

    if state["iteration_count"] >= 3:
        return "generate"  # 超过迭代限制，生成答案

    if len(state["observations"]) >= 2:
        return "generate"  # 有足够信息，生成答案

    return "think"  # 继续思考

graph.add_conditional_edges(
    "judge",
    router,  # 路由函数
    {
        "think": "think",
        "generate": "generate"
    }
)
```

---

# 完整 agent/graph.py 文件

```python
"""
LangGraph 图形定义

将四个节点组织成有向无环图（DAG）
"""

from langgraph.graph import StateGraph
from typing import List, TypedDict

# 导入状态定义
from agent.state import AgentState

# 导入节点实现
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

        # 如果已达到最大迭代次数
        if state["iteration_count"] >= 3:
            print(f"  → 已达最大迭代 ({state['iteration_count']}), 生成答案")
            return "generate"

        # 如果有足够的观察
        if len(state["observations"]) >= 2:
            print(f"  → 有足够信息 ({len(state['observations'])} 个), 生成答案")
            return "generate"

        # 继续思考
        print(f"  → 信息不足 ({len(state['observations'])} 个), 继续思考")
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


# ============ 可视化（可选） ============

def print_graph_structure():
    """打印图的结构"""
    print("Agent 工作流图结构：")
    print("""
    思考 (think)
      ↓
    行动 (action)
      ↓
    判断 (judge) ←─ 条件边
     / \\
    /   \\
继续思考  生成答案
 (think) (generate)
      ↓
    结束 (END)
    """)


# ============ 调试辅助 ============

def get_graph_info():
    """获取图的信息"""
    return {
        "nodes": ["think", "action", "judge", "generate"],
        "edges": [
            ("think", "action"),
            ("action", "judge"),
            ("judge", "think"),      # 条件边
            ("judge", "generate")     # 条件边
        ],
        "entry": "think",
        "exit": "generate"
    }
```

---

# 工作流执行示例

## 完整的执行流程

```python
from agent.graph import agent_graph
from agent.state import create_initial_state

# 创建初始状态
initial_state = create_initial_state("什么是 Transformer？")

# 执行 Agent
print("开始 Agent 执行...\n")

result = agent_graph.invoke(initial_state)

print("\n\n====== 最终结果 ======")
print(f"问题：{result['question']}")
print(f"\n思考过程：")
for i, thought in enumerate(result['thinking_history'], 1):
    print(f"  {i}. {thought}")

print(f"\n获取的信息：")
for i, obs in enumerate(result['observations'], 1):
    print(f"  {i}. {obs[:100]}...")

print(f"\n最终答案：")
print(result['final_answer'])
```

---

# 调试和监控

## 添加日志输出

```python
# 在 agent/graph.py 中添加

import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def create_agent_graph_with_logging():
    """添加日志的图创建函数"""

    def logged_think_node(state):
        logger.info(f"[THINK] 问题：{state['question']}")
        logger.info(f"[THINK] 已有观察：{len(state['observations'])}")
        result = think_node(state)
        logger.info(f"[THINK] 输出行动：{result['actions'][-1]['tool']}")
        return result

    def logged_action_node(state):
        logger.info(f"[ACTION] 执行工具：{state['actions'][-1]['tool']}")
        result = action_node(state)
        logger.info(f"[ACTION] 结果：{result['observations'][-1][:100]}")
        return result

    def logged_judge_node(state):
        logger.info(f"[JUDGE] 迭代次数：{state['iteration_count']}/3")
        logger.info(f"[JUDGE] 观察数量：{len(state['observations'])}")
        decision = judge_node(state)
        logger.info(f"[JUDGE] 决策：{'继续思考' if decision == 'think' else '生成答案'}")
        return decision

    def logged_generate_node(state):
        logger.info(f"[GENERATE] 开始生成答案")
        result = generate_node(state)
        logger.info(f"[GENERATE] 答案长度：{len(result['final_answer'])}")
        return result

    # 使用 logged 版本创建图
    graph = StateGraph(AgentState)
    graph.add_node("think", logged_think_node)
    graph.add_node("action", logged_action_node)
    graph.add_node("judge", logged_judge_node)
    graph.add_node("generate", logged_generate_node)
    # ... 其他配置相同
```

---

# Phase 3 完成状态

```
✅ StateGraph 创建完成
✅ 四个节点已注册
✅ 边和条件边已配置
✅ 入口和出口已设置
✅ 图已编译

现在可以进入 Phase 4（测试和优化）
```

---

## 下一步

现在你有了完整的图形。

接下来：Phase 4 创建 main.py 进行测试和优化
