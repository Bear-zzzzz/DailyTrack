# 📐 DailyTrack 学习规则 & 工作流规范

> **最后更新**：2026-04-27
> **适用范围**：所有学习内容、每日笔记、进度追踪、面试准备

---

## 🎯 第 1 部分：文件组织规范

### 1.1 目录结构说明

```
DailyTrack/
├── 📋 README.md                         ← 项目总览
├── 📊 PROGRESS_TRACKER.md               ← 学习进度汇总
├── 📐 LEARNING_RULES.md                 ← 本文件（规范）
│
├── 📚 CURRICULUM/                       ← 课程内容（按周）
│   ├── Week1_Fundamentals/
│   │   ├── Overview.md                  ← 周目标
│   │   ├── Concepts.md                  ← 核心概念
│   │   ├── Notes.md                     ← 个人笔记
│   │   └── QnA.md                       ← 问题解答
│   ├── Week2_Frameworks/
│   ├── Week3_Prompts/
│   ├── Week4_RAG/
│   ├── Week5_Workflows/
│   ├── Week6_MultiAgent/
│   ├── Week7_SystemDesign/
│   └── Week8_Advanced/
│
├── 🗓️ DAILIES/                          ← 日常进度（按周按日）
│   ├── Week1_Dailies/
│   │   ├── 2026-04-10_Day1.md           ← 每天一个文件
│   │   ├── 2026-04-11_Day2.md
│   │   └── ...
│   ├── Week2_Dailies/
│   ├── Week3_Dailies/
│   ├── Week4_Dailies/
│   └── Week5_Dailies/
│
├── 🧠 INTERVIEWS/                       ← 面试准备
│   ├── Interview_QnA.md                 ← 高频问题库
│   ├── System_Design_Cases.md           ← 5 个系统设计题
│   ├── Project_Portfolio.md             ← 项目讲解稿
│   └── Mock_Interview.md                ← 模拟面试记录
│
├── 🛠️ PROJECTS/                         ← 实战项目
│   ├── Project1_LearningAgent/
│   ├── Project2_RAGSystem/
│   ├── Project3_TextToSQL/
│   └── Project4_MultiAgent/
│
├── 📖 KNOWLEDGE_BASE/                   ← 参考资料
│   ├── Papers/
│   ├── Code_Examples/
│   ├── Best_Practices.md
│   └── Tools_and_Libraries.md
│
└── 🔧 ARCHIVE/                          ← 已完成或废弃内容
    ├── Old_Structure/                   ← 旧项目结构
    └── Deprecated/                      ← 过时的内容
```

### 1.2 文件命名规范

#### 课程内容文件

```
✅ 正确的格式
CURRICULUM/Week5_Workflows/Overview.md
CURRICULUM/Week5_Workflows/Concepts.md
CURRICULUM/Week5_Workflows/Notes.md
CURRICULUM/Week5_Workflows/QnA.md

❌ 错误的格式
Week5_Overview.md              （不在正确目录）
W5_Workflows_Overview.md        （缩写形式）
Overview_Week5_Workflows.md     （顺序错误）
```

#### 每日笔记文件

```
✅ 正确的格式
DAILIES/Week5_Dailies/2026-04-27_Day1_TextToSQL.md
DAILIES/Week1_Dailies/2026-04-10_Day1.md
DAILIES/Week2_Dailies/2026-04-16_Day1_Frameworks.md

格式说明：
- 日期：YYYY-MM-DD（ISO 8601 格式）
- Day标号：Day1, Day2, Day3...（不是 D1, d1）
- 可选主题：_TopicName（用下划线连接，大写首字母）

❌ 错误的格式
Week5_Day1.md                  （缺少日期）
2026-4-27_Day1.md              （月日缺少补零）
Week5_1_TextToSQL.md           （没有 Day 关键字）
W5D1.md                         （缩写形式）
```

#### 面试准备文件

```
✅ 正确的格式
INTERVIEWS/Interview_QnA.md
INTERVIEWS/System_Design_Cases.md
INTERVIEWS/Project_Portfolio.md
INTERVIEWS/Mock_Interview.md

❌ 错误的格式
Interview_Questions.md         （格式不统一）
interview_qa.md                （应该用下划线和大小写）
```

---

## 📝 第 2 部分：每日笔记模板

### 2.1 标准每日笔记结构

```markdown
# 📅 Week5 Day1 - 学习笔记

**日期**：2026-04-27 星期一
**学习阶段**：第 5 周第 1 天
**主题**：Text-to-SQL 深度学习

---

## ✅ 今日目标（3 个）

- [ ] 理解 Text-to-SQL 的 3 个关键难点
- [ ] 学习 Schema 设计的 5 个最佳实践
- [ ] 掌握 Few-shot 示例的构造方法

---

## 📊 完成情况

### 目标 1️⃣：理解 Text-to-SQL 的 3 个关键难点
- **状态**：✅ 完成
- **花费时间**：45 分钟
- **理解度**：8.5/10
- **关键收获**：
  - Schema 理解是主要瓶颈（30-40% 准确率损失）
  - 语义转换需要 Query 改写处理歧义
  - 复杂逻辑需要递进式 Few-shot 示例

### 目标 2️⃣：学习 Schema 设计的 5 个最佳实践
- **状态**：✅ 完成
- **花费时间**：50 分钟
- **理解度**：9/10
- **关键收获**：
  - 统一命名规范能提升 10-15% 准确率
  - 业务规则必须在 Schema 文档中明确写出
  - Few-shot 示例要涵盖常见查询模式

### 目标 3️⃣：掌握 Few-shot 示例的构造方法
- **状态**：✅ 完成
- **花费时间**：40 分钟
- **理解度**：8/10
- **关键收获**：
  - 示例需要多样性（简→中→难）
  - 每个示例要有清晰的注释
  - 心理学效应：前面简单例子帮助 LLM 学习

---

## 🎓 今日深层认知

### 最深的理解：
Text-to-SQL 的难点本质上是**信息不对称**：
- LLM 不清楚数据库结构 → Schema 文档要完整
- LLM 不理解业务规则 → Few-shot 要体现规则
- LLM 不会写复杂 SQL → 递进式示例教会它

### 挑战的认识：
- 准确率不可能达到 100%（自然语言本身有歧义）
- 需要多层次验证（语法→Schema→执行→业务规则）
- 成本优化很重要（缓存、模板、分层策略）

### 与前面内容的联系：
- Week 4 的 RAG 系统关于检索；这周是关于生成
- Week 2 的 Agent 工具调用与 Text-to-SQL 都需要精准理解意图
- Week 3 的 Prompt 工程直接应用到 Few-shot 示例设计

---

## ❓ 遇到的问题 & 解答

### Q1：为什么不能用 products.price 而要用 order_items.unit_price？
**A**：历史价格问题。订单生成时的价格可能与当前产品标价不同（折扣、历史变化）。
   - order_items.unit_price：订单时的实际价格 ✅
   - products.price：当前标价（不适合历史订单）❌

### Q2：为什么 Few-shot 要按"简→中→难"排序？
**A**：心理学效应和学习效率。
   - 简单例子让 LLM 快速理解规律
   - 中等例子建立信心
   - 复杂例子说明边界情况
   - 结果：准确率提升 15-25%

### Q3：SQL 验证的 4 个层级应该全都做吗？
**A**：看场景。
   - Level 1-2（语法+Schema）：必做，成本低
   - Level 3（执行）：重要场景做，有成本
   - Level 4（业务规则）：必做，成本低

---

## 🚀 明天计划

### 主要任务：
- [ ] 实践编码：创建示例数据库（SQLite）
- [ ] 实现 Text-to-SQL 系统的骨架
- [ ] 测试 Schema 验证和 SQL 执行

### 学习目标：
- 从理论转向实践
- 处理复杂查询（CTE、窗口函数）
- 建立 SQL 模板库

### 时间分配：
- 编码实现：1.5 小时
- 测试调试：30 分钟
- 总结反思：30 分钟

---

## ⏱️ 时间统计

| 项目 | 时间 | 笔记 |
|------|------|------|
| 理论学习 | 135 分钟 | 核心概念讲解 |
| 文档阅读 | 0 分钟 | （今日没有额外文档） |
| 实践编码 | 0 分钟 | 明天开始 |
| 反思总结 | 15 分钟 | 本笔记 |
| **总计** | **150 分钟** | **2.5 小时** |

---

## 📈 学习评估

| 维度 | 评分 | 目标 | 评价 |
|------|------|------|------|
| 理论理解度 | 8.4/10 | 8+ | ✅ 达标 |
| 核心概念掌握 | 9/10 | 9+ | ✅ 优秀 |
| 实践准备度 | 7/10 | 8+ | 🟡 待提升（明天实践） |
| 问题解决能力 | 8/10 | 8+ | ✅ 达标 |
| **总体评分** | **8.1/10** | **8+** | ✅ 达标 |

---

## 📝 备注

- 今天创建了完整的 Text-to-SQL 学习指南（Week5_Day1_Text_to_SQL_Guide.md）
- 已整理了学习进度和检查清单
- 明天准备动手实现，将理论转化为代码

---

**下次检查点**：2026-04-28（明天下午）
**预计进度更新**：Week 5 from 40% → 60%
```

### 2.2 使用方式

每完成一天的学习，复制上面的模板，填充你的信息。文件保存到：
```
DAILIES/Week5_Dailies/2026-04-27_Day1_TextToSQL.md
```

---

## 📊 第 3 部分：Progress Tracker 更新规范

### 3.1 更新频率

| 时间 | 内容 | 谁做 |
|------|------|------|
| 每天晚上 | 更新当天的日常笔记 | 你 |
| 每周五晚上 | 更新 PROGRESS_TRACKER.md | 你 |
| 每月 | 整体评估和调整计划 | 你 |

### 3.2 每周更新的内容

```markdown
## 📊 第 5 周统计（进行中）

- 完成任务：4 / 12（模块 1-2 完成）
- 投入时间：2.5 小时
- 理解度：8.4% → ___%（本周更新）
- 状态：🟢 进行中（40% → ___%）

### 关键数据
- 本周学习时间：__ 小时
- 本周平均理解度：__ %
- 累计投入：__ 小时
- 下周计划：__
```

---

## 🎓 第 4 部分：课程内容模板

### 4.1 Overview.md（周目标概览）

```markdown
# Week 5：工作流设计

**周目标**：任务拆分、Text-to-SQL、工作流管理

**学习时间**：15-20 小时
**完成标准**：
- [ ] 理解 3 个核心难点
- [ ] 掌握 5 个最佳实践
- [ ] 能实现基础系统

**学习路径**：
Day 1（周一）：核心概念 - Text-to-SQL 难点分析
Day 2（周二）：实战编码 - 搭建系统骨架
Day 3（周三）：复杂查询 - CTE 和窗口函数
Day 4（周四）：优化完善 - 性能和成本优化
Day 5（周五）：系统总结 - 知识整合

**核心内容**：
1. Text-to-SQL 的 3 个关键难点
2. Schema 设计的 5 个最佳实践
3. Few-shot 示例的构造方法
4. SQL 验证和纠错策略
5. 成本优化方案
```

### 4.2 Concepts.md（核心概念）

```markdown
# 核心概念讲解

## 概念 1：Text-to-SQL 难点

### 难点 1.1：Schema 理解障碍
- 原因：...
- 影响：...
- 解决方案：...

### 难点 1.2：语义转换困难
...

## 概念 2：Few-shot 构造
...

## 关键要点总结
- 重点 1
- 重点 2
- 重点 3
```

### 4.3 Notes.md（个人学习笔记）

```markdown
# 学习笔记

## 我的理解

...（自己的话总结）

## 常见陷阱

...

## 与其他内容的关联

Week 4 的... 与本周的... 有关联：...

## 我的疑问

- Q1：...
- Q2：...
```

### 4.4 QnA.md（问题解答）

```markdown
# 常见问题解答

## Q1：为什么...？
A：...

## Q2：如何...？
A：...

## Q3：什么时候...？
A：...
```

---

## 🧠 第 5 部分：面试准备规范

### 5.1 Interview_QnA.md

按难度分类高频问题：

```markdown
# 高频面试题库

## 🟢 基础题（一定要会）

### Q1：解释 Transformer 架构和 Self-Attention
A：...

### Q2：Function Call 怎么训练？
A：...

## 🟡 进阶题（优先掌握）

### Q1：RAG 和微调怎么选择？
A：...

## 🔴 难题（加分项）

### Q1：设计一个游戏社区客服系统
A：...
```

### 5.2 System_Design_Cases.md

5 个完整的系统设计案例：

```markdown
# 系统设计案例

## 案例 1：游戏社区客服助手

**需求分析**：...
**架构设计**：...
**关键技术**：...
**讲解稿**（5分钟）：...

## 案例 2：Text-to-SQL 系统
...

## 案例 3：代码生成系统
...

## 案例 4：论文翻译系统
...

## 案例 5：数据分析系统
...
```

---

## ✅ 第 6 部分：检查清单

### 每日检查（Day Start）
```
- [ ] 打开 DAILIES/Week_/Date_Day_.md
- [ ] 填写今日目标（3 个）
- [ ] 开始学习
```

### 每日检查（Day End）
```
- [ ] 填写完成情况
- [ ] 记录关键收获（3 点）
- [ ] 记录遇到的问题
- [ ] 制定明天计划
- [ ] 统计时间
- [ ] 保存文件
```

### 每周检查（Friday）
```
- [ ] 审阅本周 5 天的笔记
- [ ] 统计本周总时间和理解度
- [ ] 更新 PROGRESS_TRACKER.md
- [ ] 评估本周目标完成情况
- [ ] 制定下周计划
- [ ] 整理本周知识（可选）
```

### 每月检查（Month End）
```
- [ ] 回顾本月进度
- [ ] 评估是否按计划进行
- [ ] 调整后续计划（如需要）
- [ ] 整理和归档过期内容
```

---

## 🎯 快速参考

### 我应该把文件放在哪里？

| 文件类型 | 存储位置 | 命名格式 |
|---------|---------|---------|
| 周度课程内容 | CURRICULUM/Week_/Concepts.md | 固定 |
| 每日笔记 | DAILIES/Week_/YYYY-MM-DD_DayN.md | 按日期 |
| 面试题库 | INTERVIEWS/Interview_QnA.md | 固定 |
| 项目代码 | PROJECTS/ProjectN_/ | 项目名 |
| 参考资料 | KNOWLEDGE_BASE/ | 按类型 |
| 废弃内容 | ARCHIVE/ | 原名称 |

### 文件何时创建？

| 文件 | 创建时间 | 创建者 |
|------|---------|--------|
| CURRICULUM/Week_/Overview.md | 每周开始（周一） | 你或 Claude |
| DAILIES/Week_/Date_Day_.md | 每天（天开始） | 你 |
| PROGRESS_TRACKER.md | 每周五更新 | 你 |
| INTERVIEWS/... | 第 6 周开始 | 你或 Claude |

---

## 🔄 反馈机制

- **每周反思**：检查是否按规则执行
- **每月调整**：如果规则不适用，提出修改
- **持续改进**：根据实际情况优化

---

**制定日期**：2026-04-27
**最后更新**：2026-04-27
**版本**：v1.0
