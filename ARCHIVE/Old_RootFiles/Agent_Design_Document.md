# 🎨 第一个 Agent 系统设计文档

**设计日期**：2026-04-15
**设计者**：学习者
**难度等级**：初级（适合学习 LangGraph）
**预计实现时间**：2-4 小时

---

## 第一部分：需求分析

### 1.1 什么样的 Agent 适合初学者？

```
必须满足的条件：
  ✅ 功能清晰明确
  ✅ 数据来源容易获取
  ✅ 工具调用简单（2-4 个工具）
  ✅ 逻辑不过于复杂
  ✅ 能演示 Agent 的循环思考能力

避免的陷阱：
  ❌ 依赖复杂的外部 API
  ❌ 需要大量数据预处理
  ❌ 工具之间依赖复杂
  ❌ 难以调试和测试
```

### 1.2 Agent 的核心能力需求

```
一个好的学习项目应该体现：

1. 工具调用
   ✓ Agent 能理解何时使用哪个工具
   ✓ 能正确提取工具参数

2. 循环思考
   ✓ Agent 能反复思考和行动
   ✓ 能根据结果调整策略

3. 状态管理
   ✓ 记录思考过程
   ✓ 记录工具调用历史
   ✓ 根据历史做决策

4. 最终生成
   ✓ 整合所有信息
   ✓ 生成清晰的答案
```

---

## 第二部分：候选项目评估

### 候选项目 1：学习资源搜索 Agent

```
描述：
  用户提问学习话题 → Agent 搜索资源 → 推荐课程/书籍

优点：
  ✅ 需求清晰
  ✅ 用户容易理解
  ✅ 工具简单（搜索、排序）
  ✅ 有实用价值

缺点：
  ❌ 需要真实的搜索 API（成本）
  ❌ 难以完全本地化

评分：⭐⭐⭐⭐ 好
```

### 候选项目 2：数据分析 Agent

```
描述：
  用户上传数据 → Agent 分析 → 生成报告

优点：
  ✅ 能演示复杂逻辑
  ✅ 工具多样化
  ✅ 可以完全本地化

缺点：
  ❌ 需要数据预处理
  ❌ 需要 pandas、matplotlib
  ❌ 对初学者有点复杂

评分：⭐⭐⭐⭐⭐ 很好，但稍复杂
```

### 候选项目 3：智能问答 Agent（推荐）

```
描述：
  用户提问 → Agent 搜索本地知识库 → 整合回答

优点：
  ✅ 完全可本地化
  ✅ 工具简单清晰
  ✅ 能展示 Agent 思考过程
  ✅ 容易调试和测试
  ✅ 易于扩展

缺点：
  ❌ 需要准备知识库内容

评分：⭐⭐⭐⭐⭐ 最适合！
```

### 候选项目 4：代码调试 Agent

```
描述：
  用户粘贴代码错误 → Agent 分析 → 建议修复

优点：
  ✅ 技术人员能理解
  ✅ 工具很清晰
  ✅ 易于测试

缺点：
  ❌ 需要良好的错误理解
  ❌ LLM 理解能力要求高

评分：⭐⭐⭐ 可以，但中等难度
```

---

## 第三部分：推荐方案详解

### 🎯 最终选择：智能问答 Agent

**为什么选这个？**

```
原因 1：完全展示 LangGraph 的能力
  - 能演示多轮思考
  - 能演示工具调用
  - 能演示状态管理
  - 能演示循环和条件

原因 2：实用性强
  - 完全本地化
  - 无成本（不需要付费 API）
  - 可直接用于学习
  - 可轻松扩展

原因 3：学习价值高
  - 深刻理解 Agent 设计
  - 掌握 LangGraph 图形工作流
  - 为后续 RAG 打基础
  - 能快速看到效果

原因 4：调试友好
  - 容易测试各个组件
  - 容易追踪 Agent 思考
  - 容易添加日志
  - 容易验证结果
```

### 项目名称
```
🤖 LearningAssistant Agent
   "你的智能学习助手"
```

---

## 第四部分：系统架构设计

### 4.1 整体流程图

```
用户输入问题
    ↓
[接收与初始化]
    ↓
[Agent 决策循环]
  ├─ 思考节点
  │  └─ 分析问题，决定需要什么信息
  ├─ 工具调用节点
  │  ├─ 调用工具 1：搜索知识库
  │  ├─ 调用工具 2：查询相关概念
  │  └─ 调用工具 3：获取示例代码
  ├─ 观察节点
  │  └─ 整理工具返回的结果
  └─ 判断节点
     ├─ 信息是否充分？
     │  ├─ 是 → 生成答案
     │  └─ 否 → 回到思考（循环）
    ↓
[答案生成]
  └─ 整合所有信息，生成最终回答
    ↓
用户获得答案
```

### 4.2 工作流状态机

```
State（状态机）定义：

{
  "question": str           # 用户的问题
  "thinking_history": list  # 思考过程记录
  "actions": list           # 执行的工具调用
  "observations": list      # 工具返回的结果
  "iteration_count": int    # 循环次数（防止无限循环）
  "final_answer": str       # 最终答案
  "status": str             # 状态："thinking", "acting", "judging", "done"
}

示例流：

iteration 1:
  thinking_history: ["需要查找 Transformer 的定义"]
  actions: [{"tool": "search_kb", "query": "Transformer 定义"}]
  observations: ["Transformer 是一种神经网络架构..."]
  status: "judging"

iteration 2（决策）:
  判断：信息不够
  status: "thinking"
  thinking_history: ["需要查找 Transformer 的应用"]

iteration 3:
  actions: [{"tool": "search_kb", "query": "Transformer 应用"}]
  observations: ["应用在 NLP、CV 等领域..."]
  status: "judging"

最后（决策）:
  判断：信息足够
  final_answer: "Transformer 是... 它的应用包括..."
  status: "done"
```

---

## 第五部分：详细设计

### 5.1 三个核心工具设计

#### **工具 1：知识库搜索（SearchKB）**

```
功能：在本地知识库中搜索相关信息

输入：
  query: str  # 搜索查询

输出：
  results: List[Dict]  # 搜索结果列表
  {
    "id": int,
    "title": str,
    "content": str,
    "relevance_score": float
  }

实现方式：
  简单版：关键词匹配（startswith）
  中等版：包含匹配（in）
  高级版：TF-IDF + 余弦相似度

知识库示例内容：
  1. Transformer 架构定义
  2. Self-Attention 原理
  3. Function Call 使用
  4. LoRA 微调方法
  5. 等等...
```

#### **工具 2：获取相关概念（GetRelatedConcepts）**

```
功能：获取与某个概念相关的其他概念

输入：
  concept: str  # 概念名称

输出：
  related: List[str]  # 相关概念列表

示例：
  输入："Transformer"
  输出：["Attention", "Self-Attention", "Position Encoding", "Feed-Forward"]

实现方式：
  用预定义的概念关系图
  或从知识库中提取
```

#### **工具 3：获取示例代码（GetCodeExample）**

```
功能：获取某个概念的代码示例

输入：
  concept: str  # 概念名称

输出：
  code: str     # 代码示例

示例：
  输入："Attention"
  输出：
    ```python
    def attention(Q, K, V):
        scores = Q @ K.T / sqrt(d_k)
        weights = softmax(scores)
        return weights @ V
    ```

实现方式：
  预定义代码示例字典
  按需返回相关代码
```

### 5.2 节点设计

#### **节点 1：思考节点（ThinkNode）**

```
功能：Agent 思考下一步该做什么

输入：
  state: State  # 当前状态

处理逻辑：
  1. 检查 state 中的 observations
  2. 分析信息是否充分
  3. 决定下一步行动（使用哪个工具）
  4. 记录思考过程

输出：
  state["thinking_history"].append("...")
  state["actions"].append({"tool": "...", "args": {...}})
```

#### **节点 2：工具调用节点（ActionNode）**

```
功能：执行工具调用

输入：
  state: State
  actions: list  # 待执行的行动

处理逻辑：
  1. 遍历 actions
  2. 对每个 action，调用相应的工具
  3. 收集结果
  4. 处理工具异常

输出：
  state["observations"].append(result)
  state["iteration_count"] += 1
```

#### **节点 3：判断节点（JudgeNode）**

```
功能：判断是否获得足够信息

输入：
  state: State

判断规则：
  1. 如果 iteration_count > 3，停止（防止无限循环）
  2. 如果 observations 中有足够信息，停止
  3. 否则继续思考

输出：
  返回下一个节点的名称：
    "thinking"  # 继续思考
    "generate"  # 生成答案
```

#### **节点 4：生成答案节点（GenerateNode）**

```
功能：根据所有信息生成最终答案

输入：
  state: State

处理逻辑：
  1. 整合 observations
  2. 调用 LLM 生成答案
  3. 确保答案完整清晰

输出：
  state["final_answer"] = "..."
  state["status"] = "done"
```

### 5.3 边的设计

```
转移规则：

think_node → action_node
  条件：总是执行

action_node → judge_node
  条件：总是执行

judge_node → think_node
  条件：判断为"继续思考"

judge_node → generate_node
  条件：判断为"生成答案"

generate_node → [END]
  条件：总是结束
```

---

## 第六部分：知识库设计

### 6.1 知识库内容结构

```
knowledge_base = {
  "Transformer": {
    "title": "Transformer 架构",
    "content": "Transformer 是由 Vaswani 等人在 2017 年提出的...",
    "related_concepts": ["Attention", "Self-Attention", "Position Encoding"],
    "difficulty": "中等"
  },
  "Attention": {
    "title": "Attention 机制",
    "content": "Attention 是一种...",
    "related_concepts": ["Transformer", "Self-Attention"],
    "difficulty": "高"
  },
  ...
}
```

### 6.2 示例知识库内容

```
包含以下概念的详细说明：
  1. Transformer 架构
  2. Self-Attention 机制
  3. Multi-Head Attention
  4. Position Encoding
  5. Feed-Forward Network
  6. 大模型训练流程
  7. Function Call
  8. LoRA 微调
  9. Embedding
  10. 分词算法

每个条目包含：
  - 定义和原理
  - 使用场景
  - 代码示例
  - 相关概念
```

---

## 第七部分：测试场景

### 7.1 测试用例

```
测试 1：简单查询
  输入："什么是 Attention？"
  期望：Agent 搜索 Attention 定义，返回清晰解释

测试 2：复杂查询（需要多工具）
  输入："Transformer 和 LSTM 有什么区别？"
  期望：
    - 搜索 Transformer
    - 搜索 LSTM
    - 获取相关概念
    - 生成对比答案

测试 3：循环思考
  输入："解释 Function Call 如何在 Agent 中使用"
  期望：
    - 第 1 轮思考：搜索 Function Call 定义
    - 第 2 轮思考：搜索 Agent 定义
    - 第 3 轮思考：搜索应用示例
    - 最后：生成整合答案

测试 4：边界情况
  输入："什么是 XYZABC？"（不存在的概念）
  期望：Agent 正确处理，返回"找不到相关信息"
```

### 7.2 成功标准

```
Agent 可以成功：
  ✅ 理解用户问题
  ✅ 自动选择合适的工具
  ✅ 正确调用工具
  ✅ 处理工具返回结果
  ✅ 根据结果决定是否继续
  ✅ 生成清晰的最终答案
  ✅ 记录完整的思考过程
```

---

## 第八部分：技术栈

### 8.1 必需库

```
LangChain：
  - 用于 LLM 连接
  - 用于 Prompt 管理
  - 用于工具定义

LangGraph：
  - 用于构建图形工作流
  - 用于管理状态
  - 用于节点和边

其他：
  - openai（如果使用 OpenAI 的 LLM）
  - python-dotenv（管理 API Key）
```

### 8.2 代码结构

```
project/
├── main.py                 # 主程序入口
├── agent/
│  ├── __init__.py
│  ├── graph.py            # LangGraph 定义
│  ├── nodes.py            # 节点定义
│  ├── tools.py            # 工具定义
│  └── state.py            # 状态定义
├── knowledge/
│  ├── __init__.py
│  └── kb.py               # 知识库
├── config.py              # 配置文件
├── utils.py               # 工具函数
└── test.py                # 测试文件
```

---

## 第九部分：实现计划

### 9.1 分阶段实现

```
Phase 1：基础搭建（1-2 小时）
  ✓ 定义 State
  ✓ 定义工具
  ✓ 实现知识库

Phase 2：节点实现（1 小时）
  ✓ 实现思考节点
  ✓ 实现工具调用节点
  ✓ 实现判断节点
  ✓ 实现生成节点

Phase 3：图形组合（30 分钟）
  ✓ 定义节点
  ✓ 定义边
  ✓ 编译图

Phase 4：测试和优化（1-2 小时）
  ✓ 测试基础功能
  ✓ 测试循环逻辑
  ✓ 测试异常处理
  ✓ 优化提示词
```

### 9.2 难度等级

```
Phase 1：⭐ 简单
  - 就是定义数据结构和字典

Phase 2：⭐⭐ 中等
  - 需要理解节点逻辑
  - 需要和 LLM 交互

Phase 3：⭐ 简单
  - 就是组合已有的部分

Phase 4：⭐⭐⭐ 复杂
  - 需要调试 Agent 行为
  - 需要优化提示词
```

---

## 第十部分：扩展方向

### 10.1 可选的增强功能

```
短期（完成基础后）：
  1. 添加更多工具
  2. 改进知识库搜索
  3. 添加对话历史
  4. 改进答案格式

中期（1-2 周后）：
  1. 集成真实的知识库（从 PDF）
  2. 添加向量化搜索（LlamaIndex）
  3. 添加缓存机制
  4. 改进错误处理

长期（后续）：
  1. 多轮对话
  2. 用户反馈学习
  3. 性能优化
  4. 部署到线上
```

---

## 第十一部分：风险评估和应对

### 11.1 可能的风险

```
风险 1：Agent 陷入无限循环
  原因：判断逻辑不清
  应对：设置最大循环次数限制

风险 2：工具调用失败
  原因：参数错误或异常
  应对：添加异常处理和重试机制

风险 3：LLM 理解不清
  原因：提示词设计不好
  应对：反复迭代优化提示词

风险 4：性能问题
  原因：工具调用过多
  应对：优化工具调用策略
```

---

## 最终建议

### 这个设计为什么最优？

```
✅ 学习价值最高
   - 完整展示 LangGraph 所有特性
   - 深刻理解 Agent 工作原理

✅ 实现难度适中
   - 不会过于复杂
   - 能快速看到成果

✅ 扩展性强
   - 可轻松添加工具
   - 可轻松扩展知识库
   - 可作为后续项目基础

✅ 实用意义高
   - 可以真正用来学习
   - 代码可复用
   - 概念可迁移
```

### 下一步行动

```
现在你有了完整的设计。

选择：
  A) 确认这个设计，准备实现
  B) 修改某些需求
  C) 选择另一个项目

建议：A - 现在就可以开始实现了！
```

---

**设计完成！** 🎨

现在你有一个清晰的蓝图。下一步就是把它变成代码！

要开始实现吗？ 🚀

