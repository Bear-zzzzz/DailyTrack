# 项目1

Situation（痛点）：传统排查靠人工，售后反应问题后，需要专家按经验逐个 排查，一个问题查几小时。工单量上来后专家瓶颈明显。

Task（目标）：把整个排查流程交给 LLM Agent 自动完成——用户提交工单，系统自动采集车云日志、检索代码仓库、给出根因和修复建议。核心要求：能跑长耗时任务不丢进度、业务线可配置化扩展、结果可审计可复用。

Action（架构）：请求进队列后，Worker 拉起 LangGraph 引擎，按 session（thread_id）隔离状态。首次调查创建空白 state；续调则由框架从原生 checkpoint 自动恢复 state，从上次断点继续。在 Plan→Act→Observe 循环中迭代调查，直到出结论。每个节点执行后 checkpoint 自动增量持久化。

Result（成果）：诊断耗时从数小时降到 15 分钟，自动化排查率 75%，人工采纳率 80%+，累计处理 200+ 工单_


agent流程本身是模型调用 - 工具调用，整个流程挂上了钩子系统。


循环每轮先过 before_model 链——预算计数、死循环检测、上下文蒸馏都在 LLM 调用之前完成，ContextBuilder来组装上下文。

模型调用外层套着wrap_model_call，这里进行对模型输出进行校验，处理模型故障 ，token消耗，耗时，finish reason信息，如果是length，那就进行续写

after model：更新state history字段

如果有tools call环节，

有tool calls：

```
走tools 节点：第一层 toolNode：遍历tool calls，根据name找 tool
             第二层 pathGuard：读白名单，写白名单；exec白名单 
             第三层 Cache：相同参数调用工具多次，拒绝并回灌（结果如下，请换思路）
             第四层 RuntimeCatalog执行层，：工具白名单 - 参数校验 - handler执行（超时/超长截断/记录留痕）
```

无tool calls：

after agent：goal评估，无结论继续跑（<=3次）



行为层：防模型失控，比如陷入死循环，假装完成任务。

```
1.防死循环：2次同工具同参数，拒绝执行并回灌
3.模型输出结果后，flash模型校验结果是否完成，未完成重跑<3次
```



边界层：防止越权

```
1.路径读写白名单:PathGuard，wraptoolcall，读写路径白名单，exec 脚本路径白名单
2.工具调用白名单
```

资源层：

1.工具调用超时 or 工具调用失败，注入提示。超过3次自动熔断，停止当前宫欧，用其他工具替代

2.工具调用输出截断；llm输出finish_reason=length截断，自动续写

3.上下文蒸馏：history>20k token时，保留最近3条完整tool result，触发flash模型压缩上下文，输出结构化摘要（已确认事实/已读资源/失败记录/关键推理/关键事实）





** > 本项目的 **RAG** 分为两个知识维度：问题排查经验库和代码仓库。**

**  >**

**  > 索引阶段：使用 tree-sitter 对 Kotlin/Java 源码进行 **AST** 级分块，按函数、类等语法节点精确切分；超大函数沿 statement 边界二次切分。每个 chunk 附带文件头（package + import）解决跨文件引用的上下文丢失。Metadata**

**  包含：file\_path、language、start\_line/end\_line（基础定位）；node\_name、node\_type、parent\_name、signature（结构语法）；keywords（node name驼峰拆分）、docstring（AST 提取 KDoc/JavaDoc）、summary（**LLM

**  离线生成的自然语言摘要）（语义检索）；commit\_sha（版本隔离）；file\_hash、sibling\_chunk\_ids（分块上下文）。向量写入 **Milvus**（**HNSW**），BM25 由 SQLite FTS5 承载，两库通过 chunk ID 关联。**

**  >**

**  > 检索阶段：BM25 和 Milvus 向量检索双路并行，各召回 Top50；RRF 融合为 Top20，经 kivy-qwen3-reranker-8b 精排取 **Top-K**。BM25 对 node\_name、signature、docstring 赋高权重，向量路以 summary 和 docstring**

**  匹配自然语言提问。BM25 零命中时触发 CamelCase 拆词前缀匹配 fallback。检索结果附带结构化 Metadata，Agent 无需阅读完整代码即可判断相关性。**

**  >**

**  > 工具化设计：封装为三个渐进式 Tool——search\_code\_symbols（**符号**导航，找方法名，类名列表）、search\_code\_snippet（代码片段检索）、read\_code\_file（完整文件读取），由 Agent plan 节点基于 LLM function calling 自主调用，结果回灌至**

**  prompt。**

## 项目二

背景 ：人工评测效率低、反馈滞后、质量无标尺、数据难沉淀

目标：搭建"评测-归因-调优-回归"闭环平台，替代人工，实现自动化、可量化、可拦截。

具体描述价值：每次改 prompt、换模型、调参数，都面临一个问题，改动是让解析更准了，还是把别的 case 改坏了

方案

- 6 维度评测 + 三层校验（规则→LLM→人工）
  _详情：_

  * Schema准确性：是否符合预定义的json格式；类型合法
  * 条件准确性：条件选择是否正确，参数是否符合用户语义
  * 动作准确性：动作选择是否正确，参数是否符合用户语义
  * 可执行性：任务生成后，实际上是否可以执行。（比如 触发条件 + 触发条件，实际上不可以执行；）
  * 文案合理性：长度合理，不多写用户提醒事项，文案口语化
  * 合规性：危险请求是否正常拦截；过权限任务不执行


- 异步并发调度 + 结果自动落库
  _详情：

  提交评测任务后，系统将评测集拆解为 N 个独立 Job 入队，Worker 池并发消费。每个 Job 执行链路分三步：

  先调用 Agent 服务获取输出，

  再经过规则层做 Schema 硬校验，

  最后交由评测 LLM做多维度判分。

  三者结果汇总后写入数据库并更新完成计数，全部 Job 完成后生成聚合报告，直连数据看板可视化展示。


  展示6个维度的指标雷达图，Prompt/模型/流程三类根因占比分布，以及跨版本评测结果趋势图


  * 历史可追溯：同一条用例的历次评分可比，一眼看出是变好还是回退
  * 评测集复用：积累的 query+GT 直接作为下次回归的输入
  * 数据驱动分析，生成趋势图


- **  > 评测结束后生成聚合报告，对每类评测**指标**进行 Bad Case 归因分析：

  **Schema** 参数问题 → 对比模型原始输出和 Agent 最终输出，原始输出无问题则是后处理改写错误；

  条件准确度问题（如 repeatType 选错）→ 从 **prompt** **  定位相关规则，检查是否为写法缺陷；

  将当前模型与外部 **SOTA** 模型横向对比，效果差距大则归因模型能力。

  ** **  > 建立质量发布 Gate：**

  dev** 版本部署后自动触发全量评测流水线，评测、聚合指标、生成版本报告，与上一版本对比——出现效果回退（修复 N 条但回归 M** **  条且净负向）则告警并拦截上线正式环境；

  线上版本每日凌晨自动跑流水线，监控线上效果退化，提前预警。Bad Case 结构化归因至 Prompt/流程/模型
-
- 评测集 1000+ 条，全量回归 天级→分钟级，助力达标率 59%→87%


**挑战： 用 LLM 评 LLM，判分可信度存疑** ** **  难在哪：评测 LLM 自己是概率模型，会误判——该过的判死（误杀），该死的放过（漏检）。更隐蔽的是系统性偏差：对某类输出（长 **JSON**、含农历字段）稳定判低，达标率整体失真。** ** **  解决：** **  - 规则层先行：Schema 合规、白名单、参数合法性等能写成硬规则的绝不交给 LLM 判，缩小 LLM judge 管辖范围** **  - GT 对比模式：不给 LLM 开放判断"对不对"，而是给 **query** + agent 输出 + GT，让它做"两者语义是否等价"的结构化比较——从开放判断降级为有**锚点**比对，稳定性大幅提升** **  - 判分可审计：LLM judge 必须输出判分理由 + 触犯规则编号，不是只给一个分** **  - 人工抽查校准：错误集中的 case 和 LLM 判分不确定的 case 进人工复核，人直接拿 agent 输出 vs GT 逐字段比对，纠错结果反哺 GT 和评测 prompt，判分可信度持续校准**


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

_详情：非主驾拒绝（仅驾驶员可发起指令）、任意车门未关（防止车辆移动时人员未就位）



能力授权层：检验功能开关与车型能力是否支持该指令

_详情：_（车型，相关设置开关）

_VLA 指挥开关（ad_vla_agent_driver）、VLA 泊车开关（ad_vla_parking）、VLA_

_  召唤开关（ad_vla_call）、语音指令开关（isVoiceCommandOpen）、ADAS Max 车型校验_

_

状态层：检验当前车辆运行状态是否与指令语义匹配

**泊车指令 legalStates=[APA\_STANDBY, PARK\_IN\_SEARCHING]**

行车指令 legalStates=[NOA\_ACTIVE, AVP\_ACTIVE, ROAM\_ACTIVE]**


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



**挑战：复杂车辆状态空间下的指令安全性保证**

**一条"开始泊车"的指令，在不同状态下应有完全不同的行为，由档位，车辆行驶状态，功能开关，座位状态等决定。**


**指令优先级分流策略：● 指令优先级分流策略：策略驱动的分层路由**

**  指令到达**

**    │**

**    ├─ 安全层 ─── 所有指令强制执行，策略中配置（如：主驾校验=true、车门校验=true）**

**    │   不通过 → 终止 + **TTS** 反馈**

**    │**

**    ├─ 能力层 ─── 策略中声明该指令依赖的能力开关与车型授权**

**    │   例：行车指令 requires=[VLA\_COMMAND\_SWITCH, AD\_MAX\_CAPABILITY]**

**    │        保存车位 requires=[VLA\_PARK\_SWITCH]**

**    │        泊车指令 requires=[]（无额外授权，基础功能）**

**    │   不满足 → 终止 + TTS 反馈**

**    │**

**    ├─ 状态层 ─── 策略中声明该指令合法的车辆运行状态集合**

**    │   例：泊车指令 legalStates=[APA\_STANDBY, PARK\_IN\_SEARCHING]**

**    │        行车指令 legalStates=[NOA\_ACTIVE, AVP\_ACTIVE, ROAM\_ACTIVE]**

**    │   不匹配 → 终止 + TTS 反馈**

**    │**

**    └─ 路由 ─── 策略中声明的下发目标**

**        例：泊车/选车位 → routeTarget=LOCAL\_PARK\_MODULE（本地触发）**

**            行车指令   → routeTarget=DDS\_TO\_AD（包装 **DCC** 发送）**

**这样每新增一条指令，只需声明策略四元组，框架自动串联安全→能力→状态→路由，不修改已有逻辑。**

**消除全局校验的误伤，每层的功能相互独立，防止复杂逻辑耦合**
