# 🛠️ Agent 实现指南 - Phase 1 到完成

**开始时间**：2026-04-15
**目标**：完整实现 LearningAssistant Agent
**最终产物**：一个可工作的 Agent 系统

---

# 第一部分：环境准备

## 1.1 系统要求检查

```bash
# 检查 Python 版本
python --version
# 需要 >= 3.8

# 检查 pip 版本
pip --version
```

## 1.2 安装必需库

```bash
# 安装核心库
pip install langchain langchain-openai langgraph python-dotenv

# 如果使用 Claude（推荐）
pip install anthropic

# 如果使用 OpenAI
pip install openai

# 其他可能需要的
pip install typing-extensions
```

## 1.3 设置 API Key

### 方法 A：使用 OpenAI（如果有账户）

```bash
# 创建 .env 文件
touch .env

# 添加内容
OPENAI_API_KEY=your_api_key_here
```

### 方法 B：使用 Claude（推荐，如果有 Anthropic API）

```bash
# 创建 .env 文件
ANTHROPIC_API_KEY=your_api_key_here
```

### 方法 C：本地测试（无需 API）

我会为你提供一个模拟 LLM 的版本，可以离线测试流程。

---

# 第二部分：项目结构创建

## 2.1 创建项目目录

```bash
mkdir learning-agent
cd learning-agent

# 创建子目录
mkdir agent knowledge tests

# 创建文件
touch agent/__init__.py
touch agent/state.py
touch agent/tools.py
touch agent/nodes.py
touch agent/graph.py
touch knowledge/__init__.py
touch knowledge/kb.py
touch config.py
touch utils.py
touch main.py
touch test.py
touch .env
```

## 2.2 最终结构

```
learning-agent/
├── agent/
│   ├── __init__.py
│   ├── state.py          # 状态定义
│   ├── tools.py          # 工具定义
│   ├── nodes.py          # 节点定义
│   └── graph.py          # 图形定义
├── knowledge/
│   ├── __init__.py
│   └── kb.py             # 知识库
├── tests/
│   └── test_agent.py     # 测试
├── config.py             # 配置
├── utils.py              # 工具函数
├── main.py               # 主程序
├── .env                  # API Key
└── .gitignore            # Git 忽略
```

---

# 第三部分：Phase 1 - 基础搭建

## 3.1 定义状态（state.py）

```python
from typing import TypedDict, List

class AgentState(TypedDict):
    """Agent 的状态定义"""
    question: str                    # 用户的问题
    thinking_history: List[str]      # 思考过程
    actions: List[dict]              # 执行的工具调用
    observations: List[str]          # 观察到的结果
    iteration_count: int             # 循环次数
    final_answer: str                # 最终答案
    status: str                      # 状态："thinking", "acting", "judging", "done"

# 初始化状态
def create_initial_state(question: str) -> AgentState:
    return {
        "question": question,
        "thinking_history": [],
        "actions": [],
        "observations": [],
        "iteration_count": 0,
        "final_answer": "",
        "status": "thinking"
    }
```

## 3.2 创建知识库（knowledge/kb.py）

```python
# 知识库数据
KNOWLEDGE_BASE = {
    "Transformer": {
        "title": "Transformer 架构",
        "content": """
        Transformer 是由 Vaswani 等人在 2017 年论文 "Attention is All You Need" 中提出的神经网络架构。
        核心特点：
        1. 使用 Self-Attention 替代递推机制，支持完全并行化
        2. 包含 Encoder 和 Decoder 两部分
        3. 能够捕捉长距离依赖关系
        """,
        "related_concepts": ["Attention", "Self-Attention", "Position Encoding"],
        "difficulty": "中等",
        "keywords": ["架构", "并行", "注意力"]
    },

    "Attention": {
        "title": "Attention 机制",
        "content": """
        Attention 是一种机制，允许模型在处理信息时选择性地关注输入的不同部分。
        核心公式：Attention(Q, K, V) = softmax(Q·K^T/√d_k)·V
        优点：
        1. 能够建模长距离依赖
        2. 计算高效
        3. 易于并行化
        """,
        "related_concepts": ["Transformer", "Self-Attention"],
        "difficulty": "高",
        "keywords": ["机制", "相似度", "加权"]
    },

    "Self-Attention": {
        "title": "Self-Attention 原理",
        "content": """
        Self-Attention 是 Attention 的特殊形式，其中查询、键和值都来自同一来源。
        三个步骤：
        1. 计算 Q、K、V（通过线性变换）
        2. 计算相似度：Q·K^T
        3. 生成加权和：softmax·V
        应用：让每个词能关注所有其他词
        """,
        "related_concepts": ["Attention", "Multi-Head Attention"],
        "difficulty": "中等",
        "keywords": ["三步骤", "Q", "K", "V"]
    },

    "LoRA": {
        "title": "LoRA 微调",
        "content": """
        LoRA（Low-Rank Adaptation）是一种参数高效的微调方法。
        核心思想：
        - 冻结预训练权重 W
        - 添加小的秩-r 分解矩阵 ΔW = B·A
        - 只训练 A 和 B（参数减少 50-100 倍）
        优势：
        1. 参数少（1.6% 的参数）
        2. 速度快（1000倍快）
        3. 效果好（95% 的效果）
        """,
        "related_concepts": ["微调", "参数效率", "矩阵分解"],
        "difficulty": "中等",
        "keywords": ["低秩", "参数", "微调"]
    },

    "Function Call": {
        "title": "Function Call 原理",
        "content": """
        Function Call 使模型能够调用外部工具和函数。
        工作流程：
        1. 定义工具（JSON Schema）
        2. 模型理解何时调用工具
        3. 模型提取工具参数
        4. 系统执行工具
        5. 返回结果给模型
        意义：从 Chatbot（生成文本）升级到 Agent（执行任务）
        """,
        "related_concepts": ["Agent", "工具调用", "JSON Schema"],
        "difficulty": "中等",
        "keywords": ["工具", "执行", "参数"]
    },
}

def search_kb(query: str, top_k: int = 3) -> List[str]:
    """搜索知识库"""
    results = []
    query_lower = query.lower()

    for key, item in KNOWLEDGE_BASE.items():
        # 简单的关键词匹配
        score = 0
        if query_lower in key.lower():
            score += 10
        if query_lower in item["title"].lower():
            score += 5

        for keyword in item.get("keywords", []):
            if query_lower in keyword.lower():
                score += 2

        if score > 0:
            results.append({
                "title": item["title"],
                "content": item["content"],
                "score": score
            })

    # 按分数排序，返回前 top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return [r["content"] for r in results[:top_k]]

def get_related_concepts(concept: str) -> List[str]:
    """获取相关概念"""
    if concept in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[concept].get("related_concepts", [])
    return []

def get_code_example(concept: str) -> str:
    """获取代码示例"""
    code_examples = {
        "Attention": """
def attention(Q, K, V, mask=None):
    scores = Q @ K.T / math.sqrt(Q.shape[-1])
    if mask is not None:
        scores = scores + mask
    weights = softmax(scores, dim=-1)
    return weights @ V
        """,
        "Transformer": """
class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff):
        self.attention = MultiHeadAttention(d_model, num_heads)
        self.ffn = FeedForward(d_model, d_ff)

    def forward(self, x):
        x = x + self.attention(x)
        x = x + self.ffn(x)
        return x
        """,
        "LoRA": """
class LoRA(nn.Module):
    def __init__(self, input_dim, output_dim, r=8):
        self.A = nn.Linear(input_dim, r)
        self.B = nn.Linear(r, output_dim)

    def forward(self, x):
        return self.B(self.A(x))
        """,
    }
    return code_examples.get(concept, "没有该概念的代码示例")
```

## 3.3 定义工具（agent/tools.py）

```python
from knowledge.kb import search_kb, get_related_concepts, get_code_example

def tool_search_kb(query: str) -> str:
    """工具 1：搜索知识库"""
    results = search_kb(query)
    if results:
        return "\n---\n".join(results)
    else:
        return f"没有找到关于 '{query}' 的信息"

def tool_get_concepts(concept: str) -> str:
    """工具 2：获取相关概念"""
    concepts = get_related_concepts(concept)
    if concepts:
        return f"相关概念有：{', '.join(concepts)}"
    else:
        return f"没有找到 '{concept}' 的相关概念"

def tool_get_code(concept: str) -> str:
    """工具 3：获取代码示例"""
    code = get_code_example(concept)
    return f"代码示例：\n{code}"

# 工具定义（供 Agent 使用）
TOOLS = [
    {
        "name": "search_kb",
        "description": "在知识库中搜索相关信息。输入：查询字符串，输出：相关文本",
        "func": tool_search_kb
    },
    {
        "name": "get_concepts",
        "description": "获取某个概念的相关概念列表。输入：概念名称，输出：相关概念",
        "func": tool_get_concepts
    },
    {
        "name": "get_code",
        "description": "获取某个概念的代码实现示例。输入：概念名称，输出：代码",
        "func": tool_get_code
    }
]

def execute_tool(tool_name: str, args: dict) -> str:
    """执行工具"""
    for tool in TOOLS:
        if tool["name"] == tool_name:
            try:
                return tool["func"](**args)
            except Exception as e:
                return f"工具执行错误：{str(e)}"
    return f"找不到工具：{tool_name}"
```

## 3.4 简单的 LLM 包装（config.py）

```python
import os
from dotenv import load_dotenv

load_dotenv()

# 配置 LLM
class LLMConfig:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.provider = "openai" if "OPENAI" in os.environ else "anthropic"

    def get_llm(self):
        """获取 LLM 实例"""
        if self.provider == "openai":
            from langchain.llms import OpenAI
            return OpenAI(
                api_key=self.api_key,
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
        else:
            from langchain.llms import Anthropic
            return Anthropic(
                api_key=self.api_key,
                model="claude-opus-4-5-20251101",
                temperature=0.7
            )

llm_config = LLMConfig()
```

## 3.5 工具函数（utils.py）

```python
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
```

---

## 完成状态

Phase 1 完成的标志：

```
✅ agent/state.py - 状态定义完成
✅ knowledge/kb.py - 知识库创建完成
✅ agent/tools.py - 工具定义完成
✅ config.py - 配置完成
✅ utils.py - 工具函数完成

现在可以进入 Phase 2（节点实现）
```

---

## 下一步

现在你有了 Phase 1 的完整代码。

选择：
  A) 我将代码粘贴下来
  B) 我直接在我的电脑上创建这些文件
  C) 先看 Phase 2 的代码（节点实现）

准备好继续吗？🚀

