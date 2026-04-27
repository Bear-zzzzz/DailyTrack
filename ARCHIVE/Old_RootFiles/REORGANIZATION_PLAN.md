# 📐 DailyTrack 项目重组方案

> **目标**：建立清晰的、可扩展的、符合学习进度的项目结构

---

## 🏗️ 新的目录结构设计

```
DailyTrack/
│
├── 📋 README.md（项目总览）
├── 📊 PROGRESS_TRACKER.md（学习进度汇总，每周更新）
│
├── 🎯 LEARNING_RULES.md（学习规则和流程规范）
│
├── 📚 CURRICULUM/（课程内容按周组织）
│   ├── Week1_Fundamentals/
│   │   ├── 📄 Overview.md
│   │   ├── 📖 Concepts.md
│   │   ├── 📝 Notes.md
│   │   └── ❓ QnA.md
│   │
│   ├── Week2_Frameworks/
│   │   ├── 📄 Overview.md
│   │   ├── 📖 Concepts.md
│   │   ├── 📝 Notes.md
│   │   └── ❓ QnA.md
│   │
│   ├── Week3_Prompts/
│   ├── Week4_RAG/
│   ├── Week5_Workflows/
│   ├── Week6_MultiAgent/
│   ├── Week7_SystemDesign/
│   └── Week8_Advanced/
│
├── 🗓️ DAILIES/（按日期记录每日进度）
│   ├── Week1_Dailies/
│   │   ├── 2026-04-10_Day1.md
│   │   ├── 2026-04-11_Day2.md
│   │   └── ...
│   │
│   ├── Week2_Dailies/
│   ├── Week3_Dailies/
│   ├── Week4_Dailies/
│   ├── Week5_Dailies/
│   └── ...
│
├── 🧠 INTERVIEWS/（面试准备）
│   ├── Interview_QnA.md（高频问题库）
│   ├── System_Design_Cases.md（5 个系统设计题）
│   ├── Project_Portfolio.md（项目讲解稿）
│   └── Mock_Interview.md（模拟面试记录）
│
├── 🛠️ PROJECTS/（实战项目）
│   ├── Project1_LearningAgent/
│   │   ├── src/
│   │   ├── docs/
│   │   └── notes.md
│   │
│   ├── Project2_RAGSystem/
│   ├── Project3_TextToSQL/
│   └── Project4_MultiAgent/
│
├── 📚 KNOWLEDGE_BASE/（参考资料）
│   ├── Papers/
│   ├── Code_Examples/
│   ├── Best_Practices.md
│   └── Tools_and_Libraries.md
│
└── 🔧 ARCHIVE/（已完成或废弃内容）
    ├── Old_Structure/
    └── Deprecated/
```

---

## 📋 为什么这样组织？

### 原则 1️⃣：**按学习维度分类，不是随意混放**

**前：混乱的结构**
```
Week1_Day1_Log.md
Week1_Day1_Checkin.md
Week1_Day2_Checkin.md
Week1_Day3_Checkin.md
Agent_Learning_Progress_Tracker.md
...（30+ 个文件散落在根目录）
```

**后：清晰的结构**
```
CURRICULUM/Week1_Fundamentals/        ← 学习内容
  └── Concepts.md（理论）
  └── Notes.md（个人笔记）
  └── QnA.md（问题和答案）

DAILIES/Week1_Dailies/                ← 日常进度
  └── 2026-04-10_Day1.md（今天的打卡）
  └── 2026-04-11_Day2.md（昨天的打卡）

PROGRESS_TRACKER.md                   ← 汇总统计
```

### 原则 2️⃣：**Content 和 Tracking 分离**

- **Content 层**（CURRICULUM/）：学什么、怎么学
- **Tracking 层**（DAILIES/ + PROGRESS_TRACKER.md）：学到哪、进度如何
- **Interview 层**（INTERVIEWS/）：准备面试
- **Project 层**（PROJECTS/）：实战输出

### 原则 3️⃣：**时间维度可追踪**

每天一个文件：
```
DAILIES/Week5_Dailies/2026-04-27_Day1_TextToSQL.md
```

查看历史：
```
DAILIES/Week1_Dailies/2026-04-10_Day1.md   ← 第1周第1天
DAILIES/Week5_Dailies/2026-04-27_Day1.md   ← 第5周第1天
```

### 原则 4️⃣：**规则明确化**

新增 `LEARNING_RULES.md` 定义：
- 如何写每日笔记
- 文件命名规范
- Progress 更新频率
- 学习评估标准
- 内容检查清单

---

## 🎯 重组行动计划

### Phase 1️⃣：创建新结构（不删除旧文件）
```bash
# 创建新目录
mkdir -p CURRICULUM/Week{1..8}_*/
mkdir -p DAILIES/Week{1..8}_Dailies/
mkdir -p INTERVIEWS/
mkdir -p PROJECTS/
mkdir -p KNOWLEDGE_BASE/
mkdir -p ARCHIVE/
```

### Phase 2️⃣：迁移内容（按逻辑归类）
```
现有文件 → 新位置

Agent_Learning_Progress_Tracker.md
  → PROGRESS_TRACKER.md（重新整理）

Week1_Day1_Log.md, Week1_Day1_Checkin.md
  → DAILIES/Week1_Dailies/2026-04-10_Day1.md

Week1_Complete_Learning_Notes.md
  → CURRICULUM/Week1_Fundamentals/Notes.md

Agent_Development_Interview_Guide.md
  → INTERVIEWS/Interview_QnA.md

learning-agent/
  → PROJECTS/Project1_LearningAgent/
```

### Phase 3️⃣：创建规范文档
```
新增文件：
- LEARNING_RULES.md（学习规则）
- CURRICULUM/Week*/Overview.md（每周概览）
- CURRICULUM/Week*/Concepts.md（核心概念）
- INTERVIEWS/System_Design_Cases.md（5个系统设计题）
```

### Phase 4️⃣：清理和归档
```
ARCHIVE/
  ├── Old_Structure/（保留旧文件作为参考）
  ├── Deprecated/（过时的内容）
  └── README.md（说明什么在这里）
```

---

## 📝 核心规则（待详细定义）

### 规则 1️⃣：文件命名规范
```
✅ 按周按天组织：DAILIES/Week5_Dailies/2026-04-27_Day1_TextToSQL.md
✅ 课程内容按周：CURRICULUM/Week5_Workflows/Overview.md
❌ 避免：Week1_Day1_Log.md（散落在根目录）
❌ 避免：混乱的时间标记
```

### 规则 2️⃣：每个学习周的标准结构
```
CURRICULUM/Week5_Workflows/
├── Overview.md         ← 周目标、内容大纲
├── Concepts.md         ← 核心概念讲解
├── Notes.md            ← 个人学习笔记
└── QnA.md              ← 常见问题
```

### 规则 3️⃣：每日打卡的标准内容
```
DAILIES/Week5_Dailies/2026-04-27_Day1_TextToSQL.md

# 内容应包括：
- ✅ 今日目标（3 个）
- ✅ 完成情况（对应每个目标）
- ✅ 关键收获（3 点）
- ✅ 遇到的问题（可选）
- ✅ 明天计划
- ✅ 时间统计（花费了多少小时）
```

### 规则 4️⃣：PROGRESS_TRACKER 更新频率
```
- 每周更新一次
- 统计完成任务数、理解度、用时
- 更新总体进度百分比
- 记录下周计划
```

### 规则 5️⃣：面试准备的组织
```
INTERVIEWS/
├── Interview_QnA.md         ← 按难度分类
├── System_Design_Cases.md   ← 5 个案例的完整讲解稿
├── Project_Portfolio.md     ← 项目讲解准备
└── Mock_Interview.md        ← 模拟面试记录和反馈
```

---

## 🔍 你的确认事项

在我们开始重组之前，请确认：

1. **目录结构**：你同意上面的组织方式吗？有什么要调整的？

2. **规则明确化**：你想要我详细定义这些规则吗？
   - 文件命名规范
   - 每日笔记模板
   - Progress 更新模板
   - 等等

3. **内容迁移**：现有的内容我应该如何处理？
   - ✅ 保留有价值的内容，归到新结构中
   - ✅ 将旧结构保存到 ARCHIVE/
   - ❓ 是否需要合并相似的内容？

4. **从何时开始**：新结构从今天开始用？
   - 这样历史记录就分为"旧结构"和"新结构"

---

**等你的反馈后，我会立即执行整理工作。** ✅
