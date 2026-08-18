# Harness Engineering 开发设计指导手册

---

## 目录

NaN. 定性与时代背景
NaN. 三大根本约束
NaN. Harness 的本体结构
NaN. 上下文治理
NaN. 状态持久化
NaN. 多 Agent 编排
NaN. 工具系统设计
NaN. 安全与可靠性
NaN. Harness 简化方法论
NaN. 面向 Agentic Thinking 的展望
NaN. 附录
---

## 一、定性与时代背景

### 1.1 Harness 是什么

2026 年，**Harness Engineering** 由 HashiCorp 联合创始人 Mitchell Hashimoto 提出命名，Anthropic 和 OpenAI 的工程实践随后让这个概念广为人知。但它的本质不是新发明，而是对一套已有实践的**系统性命名**。

最直观的隐喻：

```PlainText
AI Agent = SOTA 模型（野马）+ Harness（驾驭系统）= 千里马

```
Harness 是除模型本身之外，让 Agent 真正能干活的**一切基础设施**：

- 不是"更好的 Prompt"
- 不是"更强的模型"
- 而是**优化模型运行所需的环境、机制与约束的总和**
更精确的定义来自 NLAH 论文（arXiv 2603.25723）：

值得注意的边界划分：Context Engineering（单次调用的提示和检索设计）是 Harness 的**子集**。Harness 还额外管理多步结构、工具中介、验证闭环和持久状态。

### 1.2 三代范式演进

| 时代 | 核心工作 | 典型产物 |
| --- | --- | --- |
| **Prompt Engineering** | 写好一条指令 | 高质量 system prompt |
| **Context Engineering** | 管好一次调用的上下文 | RAG、Few-shot、截断策略 |
| **Harness Engineering** | 治理跨轮次、跨 Agent 的完整工作流 | 编排系统、压缩流水线、验证闭环 |

这不是线性替代，而是**层层叠加**。好的 Harness 必然包含好的 Context Engineering 和 Prompt Engineering，但反过来不成立。

### 1.3 为什么现在是 Harness 时代

Junyang Lin（Qwen 团队）在《From Reasoning to Agentic Thinking》中的判断非常清晰：

从工程角度看，驱动因素也很具体：

- 应用场景从"对话"变成"多小时自主编码"——单次 Prompt 已经无法覆盖
- 模型的原始能力在提升，但"可靠性"和"可控性"的缺口需要工程来填
- OpenAI 的案例证明：3 人团队 × 5 个月 × Harness Engineering = 百万行代码级复杂产品
---

## 二、三大根本约束

所有 Harness 设计决策，最终都源于对三个根本约束的响应。不理解这三个约束，就不理解为什么 Harness 要长成现在这个样子。

### 约束一：Token 窗口有限

Transformer 操作的是有限的、线性的 Token 序列，而 Agent 需要理解无限的外部世界状态。这是一个根本性的不对称。

**硬约束的含义**：超出 context window 不是"效果变差"，而是**直接失效**。

更隐蔽的问题是 **Context Anxiety**（Anthropic 命名）：部分模型在接近它们**认为**的上下文上限时，会提前开始收尾工作——不是因为实际超限，而是因为模型的内部感知触发了过早收敛。这是一个心理层面的问题，不是技术层面的硬截断。

Anthropic 测试发现，Claude Sonnet 4.5 的 Context Anxiety 严重到单靠 Compaction 无法支撑长任务表现；而 Claude Opus 4.6 在模型层面基本消除了这一行为——这说明 **Context Anxiety 是模型能力问题，Harness 只能缓解，不能根治**。

### 约束二：模型输出非确定

同一输入可能产生不同输出。可靠性不能依赖模型，必须靠**外部机制保障**。

这条约束有一个重要推论：

Claude Code 的 session 以 `cwd`（当前工作目录）为主键，不依赖模型判断"我现在在处理哪个项目"。这是机械约束，确定性的，不受模型注意力分配影响。如果改成"让模型感知跨项目上下文"，就把确定性边界变成了概率性推断——而概率性推断在长上下文、注意力稀释的条件下会退化，且退化是**静默的**。

### 约束三：工具调用链脆弱

Function Calling 的生命周期每一步都可能失败：

```PlainText
Schema 序列化（工具注入 Prompt）
        ↓
LLM 触发生成（模式匹配，输出结构化文本）
        ↓
确定性反序列化  ← 最脆弱环节（JSON 格式错误、类型错误）
        ↓
执行 + 结果注入（结果/异常 → 再次注入 Prompt）

```
关键在于：工具调用失败往往是**静默的或延迟暴露的**。一个 API 路由因参数顺序被错误解析为整型 ID 返回 422，可能在 Evaluator 测试之前都不会被发现。这是 Anthropic 案例中 Evaluator 捕获的真实 bug：

**核心推论**：Harness 必须为失败而设计。异常是运行常态，不是边界情况。所有组件需具备容错、重试、优雅降级能力。

---

## 三、Harness 的本体结构

### 3.1 REPL 容器模型

Harness 的最高层抽象：**带有边界控制、工具路由与确定性反馈的 REPL（Read-Eval-Print Loop）容器**。

```PlainText
外部世界（用户输入、环境状态）
         ↓
    [Read]   上下文管理器
             将状态"翻译"成结构化 Prompt
         ↓
       LLM（非确定性"大脑"）
             生成规划 / Function Calling
         ↓
    [Eval]   调用拦截器
             路由到正确工具执行器（含超时/配额/权限/错误捕获）
         ↓
    工具执行
         ↓
    [Print]  反馈汇编器
             组装结构化"观测结果"
         ↓
             重新注入上下文 → Loop

```
这个模型揭示了一个核心原则：**LLM 是无状态计算单元（CPU），所有跨轮次状态存储在 Harness 控制的外部状态管理器中**。

反模式：试图通过 Prompt Engineering 让 LLM 自行维护长对话中的复杂状态。这会导致系统混乱、不可预测且难以调试。

### 3.2 NLAH 六要素

NLAH 论文（arXiv 2603.25723）给出了一套完整的 Harness 结构规范，任何生产级 Harness 都应该覆盖这六个维度：

| 要素 | 内容 | 缺失时的症状 |
| --- | --- | --- |
| **Contracts（合约）** | 必需的输入/输出、格式约束、验证门控、权限边界、重试和停止规则 | Agent 不知道"完成"的定义，无法自我验证 |
| **Roles（角色）** | 角色 prompt（solver、verifier、researcher、orchestrator），职责不重叠 | 角色混乱，Generator 自我评估产生偏差 |
| **Stage Structure（阶段结构）** | 显式工作负载拓扑（如 plan → execute → verify → repair） | 缺乏结构，Agent 随机漫步 |
| **Adapters & Scripts（适配器）** | 确定性动作的具名钩子（测试、验证器、检索、解析） | 关键操作依赖模型推断，可靠性下降 |
| **State Semantics（状态语义）** | 跨步骤持久化内容（artifacts、ledgers、子 workspace），以及如何重新打开 | 状态在 compaction 后丢失，无法恢复工作台 |
| **Failure Taxonomy（失败分类）** | 命名的失败模式驱动恢复（missing artifact、wrong path、verifier failure、tool error、timeout） | 所有失败用同一种方式处理，恢复逻辑混乱 |

### 3.3 CC 的双层主循环：理论落地的最佳样本

Claude Code 的核心架构是这套理论的最完整工程实现：

```PlainText
用户输入
   ↓
QueryEngine.submitMessage()     ← 会话层：持久化 messages、管理 turn 间状态
   ↓
query() / queryLoop()           ← turn 层：单次 API 流 + 工具执行状态机
   ↓
  while(true)：
    ① applyToolResultBudget     压缩层一：大型结果落盘
    ② Snip                      压缩层二：历史块删除
    ③ microCompact              压缩层三：工具结果内容替换
    ④ contextCollapse           压缩层四：可逆投影
    ⑤ autoCompact               压缩层五：全量摘要（兜底）
    ⑥ callModel()               流式 API 调用
    ⑦ StreamingToolExecutor     并发工具执行
    ⑧ 终止条件判断              10 种 Terminal reason → return 或 continue

```
两层分离的价值：

- `QueryEngine`（会话层）：跨 turn 持久化 `mutableMessages`，管理 session 生命周期，供 SDK/Headless 路径复用
- `queryLoop`（turn 层）：单次迭代的状态机，每个 `continue` 站点统一写 `state = { ...state, ... }`，状态转换原子可审计
一个细节揭示了 Harness 设计的严谨性：**转录在 API 调用之前写入**。用户在 API 响应前终止进程，用户消息依然已持久化，`/resume` 可以完整恢复。这是"为失败而设计"的具体体现——不是假设流程会顺利完成，而是假设它可能在任意时刻中断。

---

## 四、上下文治理 — 最关键的资源管理

### 4.1 为什么上下文是 Agent 的核心资源

对 LLM Agent 来说，context window 是唯一的"工作内存"。如何管理它，直接决定 Agent 能处理多复杂的任务、能保持多长时间的连贯性。

绝大多数 Harness 在这里犯的错误是：**被动响应**——快满了才压缩。正确的做法是**主动治理**——每轮都运行治理流水线，把成本平摊到每一轮，而不是在临界点集中爆发。

### 4.2 CC 五层梯级压缩：成本阶梯的教科书实现

CC 的压缩流水线按成本递增依次执行，每一层都尽量在更低成本下解决问题，避免触发更昂贵的下一层：

| 层 | 机制 | API 成本 | 破坏性 | 处理对象 |
| --- | --- | --- | --- | --- |
| `applyToolResultBudget` | 超限结果落盘，Claude 收到文件路径而非全文 | 零（磁盘 I/O） | 无 | 当前超大工具结果 |
| `Snip` | 删除历史消息中整段 tool_result 内容 | 零 API | 中（直接删除） | 历史整段 tool_result |
| `microCompact` | 将旧工具结果替换为简短占位符 | 零 API | 低（内容替换） | 指定工具类型的旧结果 |
| `contextCollapse` | 维护 commit log，读时投影，可撤销 | 零 API | **可逆** | 历史区段 |
| `autoCompact` | Fork 子 Agent 生成全量摘要 | **高**（调用模型） | 高（全量替换） | 整个对话历史 |

**阈值计算（以 200K 模型为例）**：

```TypeScript
autoCompact 触发阈值 ≈ contextWindow - MAX_OUTPUT_TOKENS_FOR_SUMMARY - AUTOCOMPACT_BUFFER_TOKENS
                    = 200,000 - 20,000 - 13,000
                    = 167,000 tokens

```
这些数字不是拍脑袋的。`MAX_OUTPUT_TOKENS_FOR_SUMMARY = 20,000` 来自 p99.99 实测摘要输出约 17,387 tokens；`AUTOCOMPACT_BUFFER_TOKENS = 13,000` 是安全缓冲。

### 4.3 三个精妙的工程细节

**细节一：snipTokensFreed 的跨层传递**

Snip 在 API 调用**之前**运行，而 token 计数读取的是更早的状态。如果不显式补偿，会出现：snip 已经释放了足够空间，但 autoCompact 读到 stale count，误触发一次高成本的摘要 API 调用。

CC 的解法：`snipTokensFreed` 显式传给 autoCompact 的阈值判断，主动补偿时序差异。

这是一个微小但重要的设计——**两层之间的信息传递不依赖"状态自然传播"，而是显式协议**。凡是跨层传递的关键量，都应该有这样的显式通道。

**细节二：contextCollapse 的可逆投影**

大多数系统选择破坏性压缩——省实现成本，但折叠策略一旦执行就不可撤销。CC 的 contextCollapse 选择了另一条路：

```PlainText
原始历史 → 完整保存在 REPL 数组里（永不销毁）
折叠操作 → 写入独立的 commit log
读取时   → projectView() 重放 commit log，生成折叠视图
撤销     → 清空 commit log，原始历史完好如初

```
代价：每次 `projectView()` 需要重放 commit log，有计算开销。收益：折叠策略可以在不影响历史的情况下随时调整。

**这是一个"以重放换可逆性"的经典工程权衡**。选择它意味着相信"策略会变"比"省重放开销"更重要。

**细节三：autoCompact 的熔断机制**

```TypeScript
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3

```
连续 3 次失败后停止 autoCompact。这个 3 不是拍脑袋的——CC 源码注释里直接引用了 BigQuery 查询（日期：2026-03-10）：1,279 个 session 有 50+ 次连续失败，最多达 3,272 次，每天浪费约 25 万次 API 调用。

这是 **"数据驱动工程决策"** 的典范：阈值来自真实生产观测，注释是可追溯的决策记录，而不是代码解释。

### 4.4 Context Reset vs Compaction：两种不同的解法

这两种策略经常被混淆：

| 策略 | 机制 | 优点 | 代价 |
| --- | --- | --- | --- |
| **Compaction** | 对话历史就地摘要，同一 Agent 继续 | 保留连续性，轻量 | 不能消除 Context Anxiety |
| **Context Reset** | 清空 context，启动全新 Agent，通过 handoff artifact 传递状态 | 干净石板，根治 Context Anxiety | 编排复杂度高、token 开销大 |

**关键洞察**：Context Reset 是根治方案，Compaction 是缓解方案。两者不是替代关系，而是适用于不同场景。

在 Anthropic 的实践中：Sonnet 4.5 需要 Context Reset（Context Anxiety 严重）；Opus 4.6 可以完全依赖 Compaction（模型层面解决了 Context Anxiety）。这意味着 **Harness 的某些组件是对模型弱点的工程补丁**，随着模型能力提升应该被移除。

---

## 五、状态持久化 — 文件系统作为通用状态总线

### 5.1 核心原则：万物皆落盘

CC 最鲜明的工程哲学之一：**所有关键状态走文件系统，没有跨进程共享内存**。

- 任务输出写到 `outputFile`（`outputOffset` 增量读取）
- 转录写到磁盘（`/resume` 恢复依赖）
- Team scratchpad 是目录
- 记忆是 Markdown 文件
- Agent 间通信通过写文件 + 读文件完成
效果：崩溃可精确重建，工作台状态可随时恢复，系统行为可审计。

NLAH 论文对此有正式命名——**File-backed State**，并给出了三个核心属性：

- **Externalized**：状态写入 artifact，而非仅保存在瞬时上下文中
- **Path-addressable**：后续阶段通过路径重新打开精确对象
- **Compaction-stable**：状态在上下文截断、重启、委托后仍存活
NLAH 论文的实验数据支持了这个选择：在 SWE-bench 和 OSWorld 两个基准上，File-backed State 是唯一在两个基准上都有正收益的模块。

### 5.2 三层记忆架构

CC 的记忆系统由三个子系统并行工作，各有不同的时间跨度和触发方式：

| 子系统 | 触发时机 | 存储位置 | 跨 session | 核心职责 |
| --- | --- | --- | --- | --- |
| **手动记忆（memdir）** | `/memory` 命令 / Claude 主动保存 | `memory/` | 是 | 持久化有价值的知识 |
| **extractMemories** | 每次完整查询结束（stop hook） | `memory/` | 是 | 自动提取对话中值得保留的信息 |
| **SessionMemory** | token 增长 5K OR 3 次工具调用 | `session-memory/` | 否 | 实时维护当前对话的结构化摘要 |

SessionMemory 的**双触发条件**是一个精妙的设计：token 增长 OR 工具调用计数满足其一即触发。这覆盖了两种极端情况——长时间纯对话（token 快速增长，工具调用少）和大量工具调用（每次调用 token 增加不多，但状态变化快）。单一阈值会在某种情况下过于频繁或过于稀疏。

**重要依赖**：SessionMemory 仅在 autoCompact 开启时才启动（共用同一个开关），关闭 autoCompact 会同时关闭 SessionMemory。这是两个功能的隐性耦合，设计自己的记忆系统时需要注意类似的功能依赖链。

### 5.3 extractMemories 的 Fork 隔离模式

```TypeScript
const result = await runForkedAgent({
  messages: currentMessages,
  tools: [FileReadTool, FileWriteTool, ...],
  forkLabel: 'extract_memories',
})

```
提取记忆这件事本身是"尽力而为"的任务：它有价值，但它的失败不应该影响主对话。

CC 的解法是 `runForkedAgent()`——完美 fork：

- 共享父会话的 prompt cache（避免重新计算 KV，零额外成本）
- Fork 的任何失败（API 错误、工具报错）都不影响主对话
- Fork 完成后自动销毁，不占用主上下文空间
这个 **Fork 隔离模式**是贯穿 CC 全系统的设计模式：`extractMemories`、`sessionMemoryCompact`、`findRelevantMemories`（sideQuery）、`autoCompact` 都使用它。凡是"有价值但不关键"的后台任务，都用 Fork 执行。

### 5.4 findRelevantMemories：用 AI 选择记忆

CC 的记忆召回不使用向量检索，而是让一个 Sonnet 模型来判断哪些记忆相关：

```PlainText
系统提示的精妙规则：
"如果用户刚在用某工具 → 不推该工具的 API 文档（已经在用了）"
"但应该推该工具的已知问题（正在用时最需要这些）"

```
为什么选 AI 而非向量检索？向量相似度表达不了这种条件推理——"用户正在使用 BashTool 这个事实，改变了我应该推送哪些记忆"。这是语义推断，不是相似度匹配。

代价：多一次 Sonnet API 调用。CC 的做法是通过 `sideQuery()` 并行执行，不阻塞主对话。

### 5.5 记忆的边界：什么不该存

CC 源码中有一条明确的约束：

这条约束防止记忆系统被滥用为代码缓存——那样会导致记忆快速膨胀、召回质量下降、维护成本爆炸。记忆系统的价值在于存储**不可替代的上下文**：用户偏好、已验证的决策、项目约定、已知坑。

### 5.6 记忆新鲜度：主动告知模型"别太信任我"

CC 的 `memoryAge.ts` 处理过时记忆的防误用问题。当 `findRelevantMemories` 召回一个超过 1 天的记忆时，系统会在注入时附加新鲜度警告：

```PlainText
<system-reminder>
This memory was written 3 days ago. The file paths and code references 
mentioned may no longer be accurate.
</system-reminder>

```
**设计意图**：不是阻止使用旧记忆，而是主动告知模型"这条信息的可信度随时间衰减"。这是"承认边界而非掩盖边界"原则的具体实现——系统对自己的局限保持诚实，让模型做出更好的判断。

**Harness 设计启示**：任何基于历史状态的决策辅助都应该携带新鲜度信号。不要假设召回的信息永远准确，把"这条信息有多旧"作为一等公民显式传递。

---

## 六、多 Agent 编排 — 何时以及如何分工

### 6.1 单 Agent 的两类天花板

单 Agent 在复杂任务上有两种系统性失败模式，靠 Prompt Engineering 无法根治：

**失败模式一：Context Anxiety / 长任务失控**

随着 context window 填满，模型开始失去连贯性，或提前收尾任务。这不是 Prompt 写得不够好的问题，而是长上下文下注意力分配的系统性退化。

**失败模式二：自我评估偏差**

让 Agent 评估自己的产出，它几乎总会给出正面反馈——即便产出质量明显低劣。Anthropic 的观察：

这两类失败模式推动了多 Agent 架构的出现。

### 6.2 GAN 启发的 Generator / Evaluator 分离

受生成对抗网络（GAN）启发，Anthropic 的解法是将生成和评估分配给两个独立 Agent：

```PlainText
Generator ──────→ 产出
                      ↓
                  Evaluator ──→ 评分 + 详细批评
                      ↓
              反馈注回 Generator
                      ↓
                   下一轮迭代

```
**为什么分离有效**：将一个独立的 Evaluator 调教得具有怀疑主义，远比让 Generator 对自己的工作持批评态度容易。原因在于：调教 Evaluator 是**独立的优化目标**，不受 Generator 的生成压力干扰。

**关键警告**：分离本身不能立即消除宽容性。Evaluator 也是 LLM，对 LLM 生成的产出天生倾向于慷慨。需要通过**多轮 prompt 调优 + few-shot 示例**明确校准 Evaluator 的判断标准。

### 6.3 三角架构：Planner / Generator / Evaluator

Anthropic 的完整三 Agent 架构：

```PlainText
User Prompt（1-4 句话）
        ↓
   [Planner Agent]
   把简短 prompt 扩展为完整产品 spec
   有意不指定技术实现细节（防止早期错误级联）
   寻找机会融入 AI 功能
        ↓
   [Generator Agent]
   按 Sprint 实现
   Sprint 前与 Evaluator 协商"完成定义"（Sprint Contract）
   Sprint 后自评，再交 QA
        ↓
   [Evaluator Agent]
   用 Playwright MCP 像用户一样点击测试
   验证 UI 功能、API 端点、数据库状态
   逐 Sprint 打分，任一低于阈值则 Sprint 失败
   返回详细 bug 报告给 Generator

```
**Planner 的价值**：没有 Planner 时，Generator 倾向于低估范围——给它一句话，它会直接开始构建，而不先做 spec，最终产出的功能丰富度远不及有 Planner 的版本。

**Planner 的设计约束**：有意保持高层次，不指定技术实现细节。原因：如果 Planner 预先指定细粒度技术细节并出了错，spec 中的错误会**级联影响下游实现**。约束 Agent 关注要交付的成果，让它们在工作中自行摸索路径，是更安全的选择。

### 6.4 Sprint Contract：Spec 与实现之间的桥梁

高层 Spec（用户故事）和可测试实现之间有一道鸿沟。没有桥梁的话，Generator 可能按错误方向工作。

Sprint Contract 的工作方式：

NaN. Generator 提出"我打算做什么、怎么验证完成"
NaN. Evaluator 审查提案，确保实现方向正确
NaN. 双方达成一致后，Generator 才开始编码
这个步骤的价值：在代码被写出之前就对齐，比写完后发现方向错了代价小得多。Sprint 3 的 27 条验收标准就是这样协商出来的，Evaluator 后来据此捕获了具体的 FastAPI 路由 bug。

**评分标准语言的塑造效应**：Anthropic 发现，评分标准里的措辞会直接引导 Generator 的输出方向。加入"最好的设计达到博物馆级别"这类短语，会将设计推向特定的视觉风格收敛。**标准的语言本身就在做 Prompt Engineering**。

### 6.5 Agent 间通信的黄金规则：文件而非内存

Anthropic 实践中的 Agent 间通信：**一个 Agent 写文件，另一个读取并在文件内回复或写新文件**。

这不是偶然选择，而是文件系统作为状态总线的必然延伸：

- 通信记录是持久化的，可审计、可 resume
- 不依赖进程间共享内存，崩溃后可精确重建
- 文件内容对调试者完全透明
CC 的多 Agent 系统也遵循这一原则：Coordinator 模式通过 scratchpad 目录与 Worker 共享协调文件，Team 成员通过 `pendingUserMessages` 队列注入消息。

### 6.6 CC 的 runForkedAgent：多 Agent 的基础设施

CC 实现多 Agent 的核心原语：

```TypeScript
const result = await runForkedAgent({
  messages: currentMessages,
  systemPrompt: compactSystemPrompt,
  forkLabel: 'compact',
  tools: [...],
})

```
**Fork 的三大保证**：

NaN. **共享 prompt cache**：Fork 继承父会话的 KV cache，不重新计算，额外成本接近零
NaN. **上下文隔离**：Fork 的对话内容不影响主对话，任何失败不会传播
NaN. **自动回收**：Fork 完成后自动清理，不占用主上下文空间
这个模式适用于所有"有价值但不关键"的后台任务：记忆提取、上下文摘要、相关记忆查找、异步 QA。

---

## 七、工具系统设计

工具是 Harness 与外部世界交互的唯一接口。工具系统的设计质量，直接决定了 Harness 的执行可靠性和上下文效率。

### 7.1 三个关键接口决策

CC 的工具接口 `Tool<Input, Output, Progress>` 有三个特别值得关注的设计点：

**决策一：isConcurrencySafe(input) — 工具自己决定并发**

```TypeScript
// 不是调用方决定，而是工具根据语义决定
isConcurrencySafe(input: Input): boolean

```
并发安全性取决于操作语义，不是工具类别。同一个 BashTool，执行 `cat file.txt`（只读，安全）和 `rm -rf`（写操作，不安全）的并发语义完全不同。由工具自己判断，比由调用方猜测更准确。

**决策二：maxResultSizeChars — 工具预算从工具侧控制**

工具结果的体积直接影响上下文占用。CC 的做法：每个工具声明自己的最大结果大小，超限后自动落盘，Claude 收到文件路径而非全文。

特例：`FileReadTool` 的 `maxResultSizeChars = Infinity`。原因：文件读取工具本身就是为了把文件内容带入上下文，截断反而破坏功能。但这意味着上层压缩层（microCompact）需要专门处理文件读取结果。

**决策三：backfillObservableInput — API 表示与可观测表示分离**

```TypeScript
// 在 API-bound 输入副本上追加字段
// SDK / 转录 / Hook 看到完整信息
// 但 API 请求字节不变（保护 prompt cache 命中）
backfillObservableInput(input: Input): Input

```
这个设计解决了一个微妙的矛盾：调试和审计需要完整信息，但 prompt cache 需要稳定的输入。`backfillObservableInput` 创建了两个视图——一个用于 API（稳定，保护缓存），一个用于观测（完整，用于审计）。

### 7.2 并发模型：语义分组 + 批次清空

```PlainText
所有待执行工具
    ↓
partitionToolCalls() 按 isConcurrencySafe 分组
    ↓
安全批：并发执行（最多 10 个）
    ↓
遇到不安全工具：先清空当前安全批，再串行执行不安全工具
    ↓
继续下一个安全批

```
`StreamingToolExecutor`（feature gate）进一步优化：允许工具在模型**还在流式输出时**就开始执行。这把工具执行的延迟从"串行在模型输出之后"变成了"与模型输出并行"。

### 7.3 工具调用失败的降级路径

完整的工具调用链必须为每个可能的失败点设计降级路径：

```PlainText
Schema 序列化失败 → 检查 Schema 定义，修复格式
LLM 触发失败     → 重试（携带错误信息），或回退到自然语言解析
反序列化失败     → 最脆弱点！重试 + 注入错误引导 Agent 重规划
执行失败         → 错误信息注入 Prompt，Agent 自行决定重试或换方案
超时             → 注入超时信息，触发超时处理流程

```
**关键原则**：每个失败点的处理策略应该**告知 Agent 发生了什么**，而不是静默吞掉。Agent 有足够的上下文来做更好的恢复决策，前提是它能看到失败信息。

### 7.4 工具延迟加载：减少上下文占用

当工具数量多时，把所有工具 schema 都塞进 system prompt 会显著增加上下文占用。CC 的解法：

- 只把 `alwaysLoad = true` 的工具放进 system prompt
- 其余工具提供 `ToolSearchTool(query=...)` 接口
- 模型需要某个工具时，先搜索获取 schema，再调用
这是"按需加载"原则在工具系统上的应用：只在需要时才把工具描述注入上下文，保持常态下的上下文精简。

---

## 八、安全与可靠性

### 8.1 权限体系：分层决策树

CC 的权限体系有 7 种 PermissionMode，覆盖从"严格交互式"到"完全自主"的完整谱系：

| 模式 | 说明 | 适用场景 |
| --- | --- | --- |
| `default` | 破坏性操作逐个询问用户 | 日常交互式使用 |
| `plan` | 只读，写操作全部 block | 代码审查、规划阶段 |
| `acceptEdits` | 自动接受文件编辑，bash 仍询问 | 编辑密集型任务 |
| `bypassPermissions` | 跳过全部权限 | CI/CD、自动化流水线 |
| `dontAsk` | ask 结果全转 deny | "什么都不执行"的安全模式 |
| `auto` | AI 自动分类安全性 | 实验性，feature gate 控制 |
| `bubble` | 决策向上冒泡给 Coordinator | Swarm worker 场景 |

权限决策树的执行顺序（`hasPermissionsToUseTool`）：

```PlainText
validateInput（输入格式验证）
    ↓
永不询问模式（bypassPermissions）
    ↓
bypass-immune 工具豁免（某些工具永远不被绕过）
    ↓
tool.checkPermissions()（工具自定义检查）
    ↓
配置规则匹配（glob patterns）
    ↓
运行时分类器（AI 判断）
    ↓
用户询问（最后兜底）

```
每一层都有明确的职责边界。**配置规则匹配**（glob patterns）是重要的一层：允许用户预先声明"这类操作总是允许/总是拒绝"，减少运行时询问次数，同时保持透明的规则记录。

### 8.2 熔断机制：不是可选项，是必须项

任何依赖外部 API 的操作都需要熔断保护。CC 的 autoCompact 熔断是教科书案例：

```TypeScript
const MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES = 3

// 连续失败次数超限时停止尝试
if ((tracking?.consecutiveFailures ?? 0) >= MAX_CONSECUTIVE_AUTOCOMPACT_FAILURES) {
  return { compactionResult: null, consecutiveFailures: ... }
}

```
没有这个熔断：1,279 个 session 会产生最多 3,272 次连续失败，每天浪费约 25 万次 API 调用。**熔断不是性能优化，是防止故障级联的安全机制**。

设计熔断时需要决策三件事：

NaN. 触发阈值（连续失败 N 次）
NaN. 熔断后的降级行为（停止尝试 vs. 降频重试）
NaN. 重置条件（成功一次后重置计数）
这些数字最好来自真实数据，而非拍脑袋。

### 8.3 沙盒分级：四级隔离框架

| 级别 | 技术方案 | 适用场景 | 权衡 |
| --- | --- | --- | --- |
| **L1：进程级** | chroot / Linux namespaces / seccomp-bpf | 可信内部工具 | 启动最快，隔离最弱 |
| **L2：容器级** | Docker / containerd | **默认选择** | 生态成熟，成本适中 |
| **L3：轻量 VM** | Firecracker 等 | 多租户 / 不可信代码 | 更强隔离，启动稍慢 |
| **L4：完整 VM** | KVM / QEMU | 极高安全场景 | 最强隔离，成本最高 |

**推荐策略**：默认 L2，配合严格的系统安全策略与只读根文件系统；对不可信代码或高敏感数据引入 L3。L4 仅在极少数特殊需求下使用。

CC 的 BashTool 安全层比沙盒更精细——**多层防御纵深**：

```PlainText
模式匹配（$(), ${}, Zsh =cmd 等危险模式）
    ↓
Tree-sitter AST 分析
    ↓
权限规则匹配（glob patterns）
    ↓
macOS sandbox-exec

```
Zsh 的 `=curl evil.com` 等价形式可以绕过 `Bash(curl:*)` deny 规则——CC 专门处理了这个案例。这说明**安全层应该由真实绕过案例驱动演进**，而不是靠理论推演。

### 8.4 Policy Gateway：执行前的最后安全门

在规划层（模型输出）和执行层（工具调用）之间，需要一个 Policy Gateway：

```PlainText
规划器（LLM 决策）
        ↓
  [Policy Gateway]
  ├── 权限检查（RBAC/ABAC）
  ├── 敏感数据过滤（PII/密钥检测与脱敏）
  ├── 指令注入防御（识别恶意 Prompt/命令拼接）
  └── 审计日志（谁在何时尝试做什么、结果如何）
        ↓
   执行层（工具调用）

```
Policy Gateway 的存在使得：即使模型被欺骗（prompt injection）产生了恶意的工具调用，也有最后一道机械防线拦截。这是"机械约束 > 模型推理"原则在安全领域的直接应用。

### 8.5 R.E.S.T：生产级 Harness 的四个维度

| 维度 | 定义 | 关键要求 |
| --- | --- | --- |
| **Reliability（可靠性）** | 在预期和非预期输入、环境变化、内部故障下持续稳定服务 | 失败可恢复、操作幂等、行为一致 |
| **Efficiency（效率）** | 有效使用计算/存储/网络资源 | Token 消耗可控、低延迟、高吞吐 |
| **Security（安全性）** | 保护系统及数据 | 最小权限、沙盒执行、输入/输出过滤 |
| **Traceability（可追溯性）** | 提供足够数据使开发/运维人员理解内部状态 | 全链路追踪、决策可解释、状态可审计 |

这四个维度是评估 Harness 是否达到生产标准的基准框架。

---

## 九、Harness 简化方法论

这一章可能是整个手册里最反直觉、也最重要的部分。

### 9.1 核心命题

这句话来自 Anthropic 工程师，但它的含义值得深思：

- Harness 的复杂度不是目的，而是手段
- 每一个新增的组件都有其存在的假设前提
- 当前提不再成立时，组件应该被移除，而不是留着"以防万一"
**找到尽可能简单的解法，只在确需时才增加复杂度。** 这是 Building Effective Agents 的核心原则，也是 Anthropic 自己实践的方法论。

### 9.2 错误的简化方式：一次砍掉多个

Anthropic 工程师在第一次简化尝试中犯的错误：

激进简化的问题：当多个组件同时消失，无法判断性能下降是哪个组件导致的。这不是简化，是破坏了实验的可控性。

### 9.3 正确的简化方式：一次移除一个

```PlainText
确定基准性能
    ↓
移除候选组件 X
    ↓
在相同任务上测试
    ↓
比较性能差异
    ↓
X 是否是承重的？
  是 → 恢复 X，标记为"必要组件"
  否 → 永久移除 X，记录原因
    ↓
继续测试下一个候选组件

```
这个过程需要耐心，但会建立起对 Harness 每个组件的清晰认知：哪些是真正承重的，哪些只是"感觉应该有"的冗余。

### 9.4 新模型发布时的 Harness 审视清单

新模型每次发布都是一次重新审视的机会。以下是应该检查的问题：

**关于 Context Anxiety**：

- [ ] 新模型是否改善了 Context Anxiety？
- [ ] 如果是，Context Reset 机制是否还有必要？
**关于自我评估**：

- [ ] 新模型的自我评估能力是否提升？
- [ ] Evaluator 的触发频率是否可以降低？
**关于任务分解**：

- [ ] 新模型是否能处理更长的连续任务？
- [ ] Sprint 结构是否还需要那么细粒度？
**关于上下文检索**：

- [ ] 新模型的长上下文检索是否改善？
- [ ] 某些需要显式检索的场景是否可以依赖模型本身？

### 9.5 Opus 4.6 迁移案例：三个组件的命运

Anthropic 从 Sonnet 4.5 迁移到 Opus 4.6 的过程，是 Harness 简化方法论的完整案例：

**被移除：Context Reset**

- Sonnet 4.5 需要：Context Anxiety 严重，单靠 Compaction 不够
- Opus 4.6 不需要：模型本身消除了 Context Anxiety
- 移除效果：编排复杂度降低，token 开销减少，延迟改善
**被移除：Sprint 分解结构**

- Sonnet 4.5 需要：模型需要细粒度的任务分解才能保持连贯
- Opus 4.6 不需要：模型原生能处理更长的连续编码任务（单 session 超 2 小时）
- 移除效果：Generator 单次连续运行超 2 小时，不需要手动切割
**被保留：Evaluator**

- 虽然 Opus 4.6 能力更强，但 Evaluator 仍然捕获了真实问题
- 原因：Evaluator 的价值取决于任务难度是否超过模型当前边界
- 结论：**Evaluator 不是非此即彼的决策。当任务超出当前模型能可靠独立完成的范围时，它才值得付出成本。**

### 9.6 Harness 的价值区间随模型能力移动

这是整个简化方法论最深刻的洞察：

```PlainText
模型能力边界 ────────────────────────►
                  ↑
              Harness 的价值区间
         （任务难度 > 模型原生能力的区域）

```
模型越强，这条边界向右移动。Harness 的价值区间跟着向右移动——不是消失，而是**移向更难的任务**。

---

## 十、面向 Agentic Thinking 的展望

### 10.1 竞争优势的来源已经改变

Junyang Lin 的判断非常清晰：

这意味着 Harness Engineering 不只是"让现有模型用得更好"的工程工作，而是**决定 AI 系统竞争力的核心变量**。

### 10.2 环境成为第一类研究产物

在 SFT 时代，我们执迷于数据多样性。在 Agentic RL 时代，我们应该执迷于**环境质量**：

- 稳定性（环境不会随机崩溃）
- 真实性（环境与生产行为一致）
- 覆盖范围（任务分布足够广）
- 难度梯度（可以控制任务难度）
- 反馈丰富度（奖励信号清晰且延迟低）
- 抗利用性（不能通过 reward hacking 绕过）
Harness 工程师的工作，将越来越多地转向环境设计——不只是"怎么让 Agent 跑起来"，而是"怎么构建一个能训练出更好 Agent 的环境"。

### 10.3 奖励黑客：工具访问扩大了攻击面

这是 Agentic 系统比推理系统微妙得多的地方：

**Harness 工程的责任**：设计防止 reward hacking 的验证机制——不只是验证"输出看起来对"，而是验证"输出通过了独立于训练信号的检验"。Evaluator 的真实值恰恰在这里：它是一个**独立于 Generator 训练信号的外部验证者**。

### 10.4 训练-推理解耦：Agentic RL 的基础设施要求

在推理 RL 中，rollout 基本是自包含的轨迹，评估器相对干净。在 Agentic RL 中，策略被嵌入更大的 Harness：工具服务器、浏览器、终端、沙盒、API 层。**环境不再是静态验证器，而是训练系统的一部分**。

这产生了一个新的系统性需求：训练与推理必须更清晰地解耦。否则：

- 推理端因等待执行反馈而停滞
- 训练端因等待完成的轨迹而挨饿
- GPU 利用率远低于预期
这意味着 Harness 架构设计必须考虑"这个 Harness 在 RL 训练场景下能否高效运行"——即使当前不用于训练，也应该保持这种可能性。

### 10.5 从训练模型到训练系统

Junyang Lin 的最终判断：

核心智能将越来越多地来自**多个 Agent 如何被组织**：

- 规划和路由工作的 Orchestrator
- 像领域专家一样行动的专门化 Agent
- 执行更窄任务、控制上下文、避免污染的 Sub-Agent
这不是说模型能力不重要——而是说，在给定模型能力的前提下，**Harness 的组织方式决定了系统能达到的上限**。

### 10.6 对 Harness 工程师的启示

NaN. **持续观察模型能力边界**：知道当前模型能独立完成什么，才能知道 Harness 应该补什么
NaN. **设计可追溯的 Harness**：每个组件的存在都应该有数据支持的假设，可以被压力测试
NaN. **新模型发布是机会，不只是升级**：主动审视哪些组件可以去掉，哪些新能力可以加进来
NaN. **环境质量和 Harness 质量同等重要**：好的模型在坏的环境里表现不出来
NaN. **Harness 的终极价值不在于复杂度，在于与模型能力的精准配合**
---

## 附录

### A：NLAH 标准 Workspace 布局

NLAH 论文给出的规范 workspace 布局，适用于任何需要状态持久化的 Harness 任务：

```PlainText
run/
  TASK.md                   # 任务描述
  harness-skill/
    SKILL.md                # Harness 定义（NLAH 六要素）
    references/             # 参考文档
    scripts/                # 确定性钩子脚本
  state/
    task_history.jsonl      # append-only 操作日志
    manifest.json           # promoted 输出索引
  children/
    001/                    # 子 Agent 工作目录
      TASK.md               # 子任务描述
      SKILL.md              # 子 Agent skill
      inputs/               # 输入 artifacts
      scripts/              # 子 Agent 脚本
      scratch/              # 临时工作区
      RESPONSE.md           # 子 Agent 回复（固定路径）
      artifacts/            # 子 Agent 产出
  RESPONSE.md               # 主 Agent 最终回复
  artifacts/                # 主任务产出

```
**核心约定**：

- prompt、角色指令、回复或 artifact 在以文件形式存在前**不算已传递**
- 每个子 Agent 收到 TASK.md + 可选 SKILL.md，写回固定路径 RESPONSE.md
- task_history.jsonl 是 append-only，永不覆盖历史记录
---

### B：CC 核心组件速查表

| 组件 | 位置 | 职责 |
| --- | --- | --- |
| `QueryEngine` | `src/QueryEngine.ts` | 会话级状态管理，turn 生命周期协调 |
| `queryLoop` | `src/query.ts` | 单次 turn 内循环状态机（1729 行） |
| `applyToolResultBudget` | 压缩层一 | 大型结果落盘，磁盘 I/O 替换 |
| `snip` | 压缩层二 | 历史 tool_result 整段删除 |
| `microCompact` | 压缩层三 | 指定工具结果内容替换 |
| `contextCollapse` | 压缩层四 | commit log 投影，可逆 |
| `autoCompact` | 压缩层五 | Fork 子 Agent 全量摘要 |
| `extractMemories` | stop hook | Fork 隔离的记忆提取 |
| `SessionMemory` | post-sampling hook | 后台实时对话摘要 |
| `findRelevantMemories` | 每轮查询前 | Sonnet 驱动的记忆召回 |
| `runForkedAgent` | 全系统 | 完美 fork 原语，共享 cache + 隔离失败 |
| `AgentTool` | 工具系统 | 递归 query()，子 Agent 派发 |
| `StreamingToolExecutor` | 并发执行 | 工具在模型流式输出时并行执行 |
| Hook 系统 | `src/hooks/` | PreToolUse/PostToolUse/Stop/Notification |

---

### C：Harness 评估维度（R.E.S.T 模型）

| 维度 | 关键指标 |
| --- | --- |
| **Reliability（可靠性）** | 任务成功率、失败可恢复率、操作幂等性 |
| **Efficiency（效率）** | 平均 token 消耗、平均工具调用次数、端到端延迟 |
| **Security（安全性）** | 策略拒绝率、安全事件数、权限边界违反次数 |
| **Traceability（可追溯性）** | 全链路追踪覆盖率、决策可解释性、状态可审计性 |

这些指标不是为了"凑大表"，而是**反向驱动 Harness 演进**：

- 任务成功率低 → 回查规划器和上下文策略
- Token 消耗高 → 检查压缩层和工具结果预算
- 安全事件发生 → 加强 Policy Gateway 和沙盒隔离
- 调试困难 → 改善 Traceability，增加文件系统状态外化
---
_最后更新：2026-04-22__综合来源：CC 源码（MasssA）· Anthropic 工程博客 · arXiv 2603.25723 · 咸鱼万字干货 · Junyang Lin_

