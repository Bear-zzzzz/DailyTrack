# 🔧 Agent 实现指南 - Phase 2 节点实现

**开始时间**：2026-04-15
**目标**：实现四个核心节点
**最终产物**：agent/nodes.py 完整代码

---

# Phase 2：节点实现

## 2.1 思考节点（ThinkNode）

```python
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from typing import Any

def think_node(state: AgentState) -> dict:
    """
    思考节点：Agent 分析当前信息，决定下一步行动

    输入：state（当前状态）
    输出：更新的 state，包含新的思考记录和待执行的行动
    """

    # 1. 构建上下文信息
    current_question = state["question"]
    thinking_history = "\n".join(state["thinking_history"]) if state["thinking_history"] else "无"
    observations = "\n".join(state["observations"]) if state["observations"] else "无"

    # 2. 构建提示词
    think_prompt = PromptTemplate(
        input_variables=["question", "history", "observations", "iteration"],
        template="""
你是一个智能学习助手。基于用户的问题和已有的信息，决定下一步该做什么。

用户问题：{question}

之前的思考过程：
{history}

已有的观察/信息：
{observations}

迭代次数：{iteration}/3

请分析现有信息是否充分。如果不充分，决定下一步应该：
1. 搜索知识库（search_kb）
2. 获取相关概念（get_concepts）
3. 获取代码示例（get_code）

你的回复格式：
思考：[你的分析]
行动：[工具名称]
参数：[工具参数，JSON 格式]

例子：
思考：用户问的是 Transformer，我需要先搜索定义
行动：search_kb
参数：{{"query": "Transformer 定义"}}
"""
    )

    # 3. 调用 LLM 进行思考
    from config import llm_config
    llm = llm_config.get_llm()

    prompt_text = think_prompt.format(
        question=current_question,
        history=thinking_history,
        observations=observations,
        iteration=state["iteration_count"] + 1
    )

    response = llm(prompt_text)

    # 4. 解析 LLM 输出，提取思考和行动
    thinking = extract_thinking(response)
    action = extract_action(response)
    params = extract_params(response)

    # 5. 更新状态
    new_thinking_history = state["thinking_history"] + [thinking]
    new_action = {
        "tool": action,
        "args": params
    }
    new_actions = state["actions"] + [new_action]

    return {
        "thinking_history": new_thinking_history,
        "actions": new_actions,
        "status": "acting"
    }


def extract_thinking(response: str) -> str:
    """从 LLM 响应中提取思考部分"""
    if "思考：" in response:
        thinking = response.split("思考：")[1].split("行动：")[0].strip()
        return thinking
    return response[:100]  # 取前 100 个字符


def extract_action(response: str) -> str:
    """从 LLM 响应中提取行动（工具名称）"""
    if "行动：" in response:
        action = response.split("行动：")[1].split("参数：")[0].strip()
        return action.lower()
    return "search_kb"  # 默认搜索


def extract_params(response: str) -> dict:
    """从 LLM 响应中提取参数"""
    import json
    try:
        if "参数：" in response:
            params_str = response.split("参数：")[1].strip()
            # 尝试解析 JSON
            if "{" in params_str:
                json_start = params_str.find("{")
                json_end = params_str.rfind("}") + 1
                json_str = params_str[json_start:json_end]
                return json.loads(json_str)
    except:
        pass

    # 默认参数
    return {"query": "Transformer"}
```

## 2.2 工具调用节点（ActionNode）

```python
def action_node(state: AgentState) -> dict:
    """
    工具调用节点：执行思考节点决定的工具

    输入：state（包含待执行的 actions）
    输出：更新的 state，包含工具执行结果
    """

    from agent.tools import execute_tool

    # 1. 获取最后一个待执行的行动
    if not state["actions"]:
        return {
            "observations": state["observations"] + ["无法执行：没有待执行的行动"],
            "status": "judging"
        }

    latest_action = state["actions"][-1]
    tool_name = latest_action.get("tool", "search_kb")
    tool_args = latest_action.get("args", {})

    # 2. 执行工具
    try:
        result = execute_tool(tool_name, tool_args)
    except Exception as e:
        result = f"工具执行失败：{str(e)}"

    # 3. 处理结果（如果太长则截断）
    if len(result) > 500:
        result = result[:500] + "...[内容已截断]"

    # 4. 更新状态
    new_observations = state["observations"] + [result]
    new_iteration_count = state["iteration_count"] + 1

    return {
        "observations": new_observations,
        "iteration_count": new_iteration_count,
        "status": "judging"
    }
```

## 2.3 判断节点（JudgeNode）

```python
def judge_node(state: AgentState) -> str:
    """
    判断节点：判断是否获得足够信息，决定是继续思考还是生成答案

    输入：state（当前状态）
    输出：下一个节点的名称 ("thinking" 或 "generate")
    """

    # 1. 检查是否超过最大迭代次数
    if state["iteration_count"] >= 3:
        print(f"✓ 已达到最大迭代次数 ({state['iteration_count']})")
        return "generate"

    # 2. 检查是否有足够的观察
    num_observations = len(state["observations"])
    if num_observations >= 2:
        print(f"✓ 获得了充分的信息（{num_observations} 个观察）")
        return "generate"

    # 3. 检查最后的观察是否包含错误
    if state["observations"]:
        last_observation = state["observations"][-1]
        if "找不到" in last_observation or "错误" in last_observation:
            if num_observations >= 1:
                print(f"✓ 虽然有错误，但已有 1 个有效观察")
                return "generate"

    # 4. 默认继续思考
    print(f"→ 继续思考（已有 {num_observations} 个观察）")
    return "thinking"
```

## 2.4 生成答案节点（GenerateNode）

```python
def generate_node(state: AgentState) -> dict:
    """
    生成答案节点：整合所有信息，生成最终答案

    输入：state（包含所有观察和思考过程）
    输出：更新的 state，包含最终答案
    """

    from config import llm_config

    # 1. 整合所有信息
    question = state["question"]
    observations = "\n---\n".join(state["observations"])
    thinking_summary = "\n".join(state["thinking_history"])

    # 2. 构建生成提示词
    generate_prompt = f"""
根据以下信息，为用户生成一个清晰、完整的答案。

用户问题：{question}

思考过程：
{thinking_summary}

获取的信息：
{observations}

请生成一个结构清晰的最终答案，包含：
1. 直接回答问题
2. 相关概念说明（如果有）
3. 代码示例（如果有）
4. 总结

最终答案：
"""

    # 3. 调用 LLM 生成答案
    llm = llm_config.get_llm()
    final_answer = llm(generate_prompt)

    # 4. 更新状态
    return {
        "final_answer": final_answer,
        "status": "done"
    }
```

---

# 节点实现要点

## 关键设计决策

1. **思考节点**：
   - 使用 LLM 分析现有信息
   - 输出格式标准化（思考、行动、参数）
   - 提取逻辑鲁棒（能处理各种 LLM 格式）

2. **工具调用节点**：
   - 执行最后一个待执行的行动
   - 异常处理：工具失败时返回错误信息
   - 结果截断：防止状态过大

3. **判断节点**：
   - 三重检查：迭代次数、观察数量、错误检查
   - 返回下一个节点名称，不修改状态

4. **生成答案节点**：
   - 整合整个思考过程
   - 结构化输出（直接回答 + 概念 + 代码 + 总结）
   - 最后一步，无需判断

## 错误处理

```python
# 在各节点中添加
try:
    # 操作代码
except Exception as e:
    return {
        "observations": state["observations"] + [f"错误：{str(e)}"],
        "status": "error"
    }
```

## 日志输出

```python
# 添加调试日志
def think_node_with_logging(state):
    print(f"[思考节点] 问题：{state['question']}")
    print(f"[思考节点] 已有 {len(state['observations'])} 个观察")
    result = think_node(state)
    print(f"[思考节点] 输出行动：{result['actions'][-1]}")
    return result
```

---

# 完整 agent/nodes.py 文件

```python
"""
Agent 的四个核心节点实现

节点流程：
  思考 → 行动 → 判断 → [继续思考 或 生成答案]
"""

from typing import Dict, Any
import json
from agent.state import AgentState
from agent.tools import execute_tool


# ============ 节点 1：思考节点 ============

def think_node(state: AgentState) -> Dict[str, Any]:
    """
    思考节点：Agent 分析当前信息，决定下一步行动
    """
    from config import llm_config

    # 构建上下文
    question = state["question"]
    history = "\n".join(state["thinking_history"]) if state["thinking_history"] else "无"
    observations = "\n".join(state["observations"]) if state["observations"] else "无"
    iteration = state["iteration_count"] + 1

    # 构建提示词
    prompt = f"""
你是一个智能学习助手。基于用户的问题和已有的信息，决定下一步该做什么。

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

回复格式：
思考：[你的分析]
行动：[工具名称]
参数：{{"query": "..."}}
"""

    # 调用 LLM
    llm = llm_config.get_llm()
    response = llm(prompt)

    # 解析响应
    thinking = _extract_thinking(response)
    action = _extract_action(response)
    params = _extract_params(response)

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
    if len(result) > 500:
        result = result[:500] + "\n...[内容已截断]"

    return {
        "observations": state["observations"] + [result],
        "iteration_count": state["iteration_count"] + 1,
        "status": "judging"
    }


# ============ 节点 3：判断节点 ============

def judge_node(state: AgentState) -> str:
    """
    判断节点：决定是继续思考还是生成答案

    返回值：
      "thinking" - 继续思考
      "generate" - 生成答案
    """

    # 检查迭代次数
    if state["iteration_count"] >= 3:
        return "generate"

    # 检查观察数量
    if len(state["observations"]) >= 2:
        return "generate"

    # 继续思考
    return "thinking"


# ============ 节点 4：生成答案节点 ============

def generate_node(state: AgentState) -> Dict[str, Any]:
    """
    生成答案节点：整合信息生成最终答案
    """
    from config import llm_config

    # 整合信息
    question = state["question"]
    observations = "\n---\n".join(state["observations"])

    # 生成提示词
    prompt = f"""
根据以下信息，为用户生成一个清晰、完整的答案。

用户问题：{question}

获取的信息：
{observations}

请生成最终答案，包含：
1. 直接回答问题
2. 关键概念说明
3. 代码示例（如果有）
4. 总结

最终答案：
"""

    # 调用 LLM
    llm = llm_config.get_llm()
    final_answer = llm(prompt)

    return {
        "final_answer": final_answer,
        "status": "done"
    }


# ============ 节点导出 ============

# 用于 LangGraph 的节点字典
NODES = {
    "think": think_node,
    "action": action_node,
    "judge": judge_node,
    "generate": generate_node
}
```

---

# 完成状态

Phase 2 完成的标志：

```
✅ think_node - 思考节点完成
✅ action_node - 工具调用节点完成
✅ judge_node - 判断节点完成
✅ generate_node - 生成答案节点完成
✅ 节点间通信定义清晰
✅ 错误处理完整

现在可以进入 Phase 3（图形组合）
```

---

## 下一步

现在你有了完整的四个节点。

接下来：Phase 3 将这些节点组合成一个 LangGraph 图形
