# 项目1


```
flowchart LR
      classDef react fill:#e1d5e7,stroke:#9673a6,stroke-width:3px
      classDef shared fill:#e8f4f8,stroke:#4a90d9,stroke-width:2px,stroke-dasharray:3 3
      classDef guard fill:#ffe6cc,stroke:#d79b00,stroke-width:2px,stroke-dasharray:5 5
      classDef rag fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px
      classDef result fill:#d5e8d4,stroke:#82b366,stroke-width:3px
      User(("工单输入\nVIN + 时间窗 + 问题描述"))
      User --> Queue
      Queue[("SQLite\n任务队列")] --> Worker
      Worker["Worker × 4\nclaim / heartbeat"] --> Runtime
      S0["进程级共享\ncatalog / skill_registry\n构建一次，4线程复用"]
      S0 -. "闭包注入" .-> Runtime
      Runtime["LangGraph Runtime\nStateGraph（一次性）"] --> Loop
      subgraph Loop["Plan → Act → Observe 循环"]
          direction TB
          Plan["Plan\nLLM决策"]
          Act["Act\n权限校验+工具执行"]
          Obs["Observe\n护栏+防循环"]
          Plan -->|"tool_calls"| Act
          Act --> Obs
          Obs -->|"继续"| Plan
      end
      SB["State 纯数据\nevidence / history\ntool_results"]
      Loop -. "读写" .-> SB
      Plan -->|"reply"| Concl["结论输出\n根因+证据链+修复建议"]
      Obs -->|"max_turns/熔断"| Concl
      Guard["安全护栏\n权限+超时+防死循环+截断防护"]
      RAG["Hybrid RAG\n经验检索+代码检索"]
      Guard -. "约束" .-> Loop
      RAG -. "工具调用" .-> Act
      Concl --> M["诊断耗时↓15min\n自动化率75% 采纳率80%+"]
      class Plan,Act,Obs,Concl,Runtime react
      class S0,SB shared
      class Guard guard
      class RAG rag
      class M result
```
Situation（痛点）：传统排查靠人工，售后反应问题后，需要专家按经验逐个 排查，一个问题查几小时。工单量上来后专家瓶颈明显。

Task（目标）：把整个排查流程交给 LLM Agent 自动完成——用户提交工单，系统自动采集车云日志、检索代码仓库、给出根因和修复建议。核心要求：能跑长耗时任务不丢进度、业务线可配置化扩展、结果可审计可复用。

Action（架构）：请求进队列后，Worker 拉起 LangGraph 引擎，按 session（thread_id）隔离状态。首次调查创建空白 state；续调则由框架从原生 checkpoint 自动恢复 state，从上次断点继续。在 Plan→Act→Observe 循环中迭代调查，直到出结论。每个节点执行后 checkpoint 自动增量持久化。

Result（成果）：诊断耗时从数小时降到 15 分钟，自动化排查率 75%，人工采纳率 80%+，累计处理 200+ 工单



_详情：_


```
flowchart TB
      classDef react fill:#e1d5e7,stroke:#9673a6,stroke-width:3px
      classDef state fill:#e8f4f8,stroke:#4a90d9,stroke-width:2px
      classDef capability fill:#d5e8d4,stroke:#82b366,stroke-width:2px
      subgraph Loop["ReAct 推理循环"]
          direction TB
          Plan["Plan 节点\nLLM 决策: 选工具 or 回复"]
          Act["Act 节点\n权限校验 → 工具执行 → 收集证据"]
          Observe["Observe 节点\n轮次计数 + 护栏检查 + 防循环"]
          Plan -->|"tool_calls"| Act
          Act --> Observe
          Observe -->|"继续调查"| Plan
          Plan -->|"reply"| End["输出结论"]
          Observe -->|"max_turns/熔断"| End
      end
      State["State 会话数据\nevidence / history\ntool_results / turn_count"]
      subgraph Cap["Tool & Skill 能力层"]
          Tools["通用工具: exec / grep_log / read_file\nRAG 工具: search_experience / search_code"]
          Skills["Skill: log / taskmaster / code\nSKILL.md 指令手册，LLM 按需 read_skill"]
      end
      Plan -. "调用" .-> Tools
      Plan -. "加载指令" .-> Skills
      Act -. "执行" .-> Tools
      Act -. "读指令" .-> Skills
      Loop -. "读写 state" .-> State
      class Plan,Act,Observe,End react
      class State state
      class Tools,Skills,Cap capability
```
Plan 节点调 LLM 决策下一步——选工具执行还是直接回复。

选了工具就进 Act 节点，做权限校验、调工具（exec/grep_log/search_experience 等）、收集证据，结果写入 state。

然后 Observe 节点做轮次计数和护栏检查——检测重复调用、预算倒计时、熔断——没问题就回 Plan继续下一轮。证据充分或达到上限就输出结论。

Skill 是 Plan 节点按需通过 read_skill 加载的指令手册，教 LLM 怎么用工具；

Tool 是 Act 节点真正执行的能力。

State 是整个循环的数据总线，每轮 Plan→Act→Observe 都读写它。




```
  flowchart TB
      classDef guard fill:#ffe6cc,stroke:#d79b00,stroke-width:2px,stroke-dasharray:5 5
      subgraph G1["多重安全护栏"]
          direction LR
          GA["① 权限拦截\nact 节点校验 active_tools 白名单\n越权拒绝 + 纠正注入"]
          GB["② 超时熔断\n单工具 timeout kill\n连续失败 2 次自动中断"]
          GC["③ 防死循环\n重复检测 + 预算倒计时\nmax_turns=40 硬上限"]
          GD["④ 截断防护\nfinish_reason=length\n续写重试 / 空回复抛错"]
      end
      Plan["Plan 节点"] -->|"决策"| GA
      GA -->|"通过"| GB
      GB -->|"通过"| GC
      GC -->|"通过"| GD
      class GA,GB,GC,GD guard
```
四道防线逐层拦截。

① 权限拦截：act 节点校验工具是否在 active_tools 白名单，shell脚本采取正则，过滤rm，rf等黑名单内容，目录校验，越权直接拒绝并注入纠正提示。

② 超时熔断：每个工具有独立 timeout，超时 kill 进程，连续失败 2 次自动中断交回用户。

③ 防死循环：检测重复调用+同工具连续 N 次告警+预算倒计时（≤10

  轮强制收敛）+max_turns=40 硬上限。

④ 截断防护：LLM 输出被截断时自动续写，空回复抛错重试，杜绝假结论。




```
flowchart TB
      classDef rag fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px
      classDef step fill:#e8f4f8,stroke:#4a90d9,stroke-width:1px
      classDef llm fill:#e1d5e7,stroke:#9673a6,stroke-width:2px
      classDef offline fill:#f5f5f5,stroke:#666,stroke-width:2px,stroke-dasharray:5 5
      subgraph Plan["Plan 节点 — LLM 决策调 RAG Tool"]
          ECall["调 search_experience\nquery = 基于证据提取的关键词"]
          CCall["调 search_code\nquery = 关键词 | version = 版本号"]
      end
      subgraph Exp["经验 RAG 执行管线"]
          direction TB
          E1["① FTS5 + 向量 并行召回"]
          E2["② retrieval_state 过滤\nsuperseded/repelled 退出"]
          E3["③ Cross-Encoder Rerank\n+ quality_bonus 加权"]
          E4["④ 阈值过滤 → Top-K 截断\n取前 4 条"]
          E1 --> E2 --> E3 --> E4
      end
      subgraph Code["代码 RAG 执行管线"]
          direction TB
          C1["① FTS5 + 向量 并行检索\nversion → commit_sha 限定范围"]
          C2["② 融合排序\n0.35×FTS + 0.55×Vec"]
          C3["③ Top-K 截断\n取前 4 条"]
          C1 --> C2 --> C3
      end
      subgraph Offline["离线构建"]
          EM["历史工单\nLLM 提炼 → 经验库"]
          CK["Git仓库 clone\nAST 切分 → 代码索引"]
      end
      ECall --> E1
      CCall --> C1
      EM -. "供检索" .-> E1
      CK -. "供检索" .-> C1
      class ECall,CCall llm
      class E1,E2,E3,E4,C1,C2,C3 step
      class EM,CK offline
```
两个 RAG 都是 Tool，LLM 在 Plan 节点基于已收集证据决定调哪个、传什么参数。

经验走 4 步：Hybrid 召回→状态路由→Rerank+质量加权→阈值+Top-4。

代码走 3 步：Hybrid 召回（版本限定范围）→融合排序→Top-4。共同点是都有 FTS5+向量双路召回+Top-K 截断；差异点在经验多了



## 项目二

背景 ：人工评测效率低、反馈滞后、质量无标尺、数据难沉淀

目标：搭建"评测-归因-调优-回归"闭环平台，替代人工，实现自动化、可量化、可拦截。

具体描述价值：每次改 prompt、换模型、调参数，都面临一个问题，改动是让解析更准了，还是把别的 case 改坏了

方案

- 6 维度评测 + 三层校验（规则→LLM→人工）
_详情：_

  * Schema准确性：是否符合预定义的json格式；类型合法
  * 完整性：是否遗漏输入中的意图要素；多 action、条件不丢
  * 流畅性：提醒文案是否自然；llmMessage
  * 准确性：输出语义和用户原始意图一致；conditions/actions/code参数准确
  * 可执行性：输出结果，下游是否能无错执行
  * safety：危险请求是否正常拦截；过权限任务不执行
- 异步并发调度 + 结果自动落库
_详情：_

  * 历史可追溯：同一条用例的历次评分可比，一眼看出是变好还是回退
  * 评测集复用：积累的 query+GT 直接作为下次回归的输入
  * 数据驱动分析，生成趋势图
- Bad Case 结构化归因至 Prompt/流程/模型
_详情：_

  * （多个模型均发生同类问题）归因到 Prompt 缺陷 → 在 prompt.md 对应规则处补边界 case 或改措辞，加示例
  * post_process阶段处理有误，非llm问题，时间处理错误
  * 模型问题：单个模型生成效果不佳，其余模型正常
- CI/CD 嵌入 质量 Gate，不达标自动拦截
_详情：_

  * 监测部署到test环节后，跑全量测试集，通过后才允许推送至生产环境
  * 每天凌晨自动跑全量，退化则触发告警
成果

  评测集 1000+ 条，全量回归 天级→分钟级，助力达标率 59%→87%



项目3:

**背景：**语音助手"理想同学"与自动驾驶系统之间缺少承接层，自然语言意图无法直接转化为车辆控制指令，行车和泊车场景均存在链路断裂

**任务：**构建语言模块到自动驾驶系统的核心承接层，实现意图解析，安全门控，指令下发

**行动项：**

1.高可用指令承接层：
VoiceRepo：集成语音sdk，负责和语音模块交互，接受语音识别结果

_详情：语音识别结果，（domain，content，command，dialog id，source location），补齐 VAD 时间戳、来源_

_同时负责AD指令回复的透传_



DDSRepo（经过DDS总线和自动驾驶域交互）

VoiceCopilotBehavior，Filter + 路由决策

2.动态安全门控

3层filter：

安全层：与车辆物理安全直接相关的硬约束，不满足则无条件拦截

_详情：非主驾拒绝（仅驾驶员可发起指令）、任意车门未关（防止车辆移动时人员未就位）_



状态层：检验当前车辆运行状态是否与指令语义匹配

_详情：_（APA泊车拦截质量，行车/avp未激活，拦截）

_APA运行中拦截（泊车执行期间不接受新指挥指令）、行车/AVP/漫游未激活拦截（无可用的智能驾驶功能承载指令）、APO方向可用性校验（向左/向右指令仅在对应方向可用时放行）_

能力层：检验功能开关与车型能力是否支持该指令 

_详情：_（车型，相关设置开关）

_VLA 指挥开关（ad_vla_agent_driver）、VLA 泊车开关（ad_vla_parking）、VLA_

_  召唤开关（ad_vla_call）、语音指令开关（isVoiceCommandOpen）、ADAS Max 车型校验_



高风险任务二次确认机制：idle - need_confirm - CONFIRM - executable



_详情：_

_ IDLE（初始态）_

_    ↓ AD返回executable=1，判定为长时任务_

_  NEED_CONFIRM（等待用户确认，注册confirm/cancel场景）_

_    ↓ 用户说"确认"_

_  CONFIRM（已确认，发送至AD等待执行）_

_    ↓ AD返回tts并标记executable_

_  EXECUTABLE（任务进入执行态）_

3.全链路审计：每条发送给AD的DCC，携带dialog id，多段耗时，来源位置，实现端到端追踪

**成果：累计服务 1100w+ 次，月活 90W+，月活渗透率达 20%+，成为行业 L3 级智能驾驶交互标杆**

