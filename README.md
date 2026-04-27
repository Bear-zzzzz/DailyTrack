# 📚 DailyTrack - Agent 开发学习计划

> **目标**：8 周掌握 Agent 开发核心知识，为高级面试做准备
> **开始日期**：2026-04-10
> **当前日期**：2026-04-27（第 5 周第 1 天）
> **整体进度**：77%（46/60 任务完成）

---

## 🎯 项目概览

这是一个**系统化的 Agent 开发学习项目**，包含理论学习、实战编码、面试准备三个维度。

### 📁 项目结构

```
DailyTrack/
├── 📋 README.md                    ← 你在这里
├── 📊 PROGRESS_TRACKER.md          ← 学习进度汇总
├── 📐 LEARNING_RULES.md            ← 工作流规范
│
├── 📚 Week1_Fundamentals/          ← 第 1 周（完整单元）
│   ├── Overview.md                 ← 周目标
│   ├── Concepts.md                 ← 核心概念
│   ├── Notes.md                    ← 学习笔记
│   ├── QnA.md                      ← 常见问题
│   └── Dailies/                    ← 每日打卡
│       ├── 2026-04-10_Day1.md
│       ├── 2026-04-11_Day2.md
│       └── ...
│
├── 📚 Week2_Frameworks/            ← 第 2 周（完整单元）
│   ├── Overview.md
│   ├── Concepts.md
│   ├── Notes.md
│   ├── QnA.md
│   ├── Dailies/
│   └── Project_LearningAgent/      ← 项目代码（可选）
│
├── 📚 Week3_Prompts/               ← 第 3 周（完整单元）
├── 📚 Week4_RAG/                   ← 第 4 周（完整单元）
├── 📚 Week5_Workflows/             ← 第 5 周（进行中）
├── 📚 Week6_MultiAgent/            ← 第 6 周（计划）
├── 📚 Week7_SystemDesign/          ← 第 7 周（计划）
├── 📚 Week8_Advanced/              ← 第 8 周（计划）
│
├── 🧠 INTERVIEWS/                  ← 全局：面试准备
│   ├── Interview_QnA.md
│   ├── System_Design_Cases.md
│   ├── Project_Portfolio.md
│   └── Mock_Interview.md
│
├── 📖 KNOWLEDGE_BASE/              ← 全局：参考资源
│   ├── Papers/
│   ├── Code_Examples/
│   ├── Best_Practices.md
│   └── Tools_and_Libraries.md
│
└── 🔧 ARCHIVE/                     ← 全局：废弃内容
    ├── Old_Structure/
    ├── Old_Reorganization_2026-04-27/
    └── Deprecated/
```

---

## 📊 学习进度一览

```
第1周 基础理论     [████████████████████░░░░░░░░░░░░] 95% ✅
第2周 框架实践     [██████████████████████████████████] 120%+ ✨
第3周 Prompt工程   [██████████████████████████████████] 100% ✅
第4周 RAG系统      [██████████████████████████████████] 100% ✅
第5周 工作流设计   [██████████░░░░░░░░░░░░░░░░░░░░░░░░] 40%
第6周 Agent系统    [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%
第7周 系统设计题   [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%
第8周+ 深化优化    [░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░] 0%

总体进度：46/60 任务完成 (77%)
累计用时：28.5 小时
```

---

## 🚀 快速开始

### 查看某一周的内容

**完成的周**：
- [Week 1：LLM 基础理论](./Week1_Fundamentals/) ✅
- [Week 2：Agent 框架](./Week2_Frameworks/) ✅
- [Week 3：Prompt 工程](./Week3_Prompts/) ✅
- [Week 4：RAG 系统](./Week4_RAG/) ✅

**进行中**：
- [Week 5：工作流设计](./Week5_Workflows/) 🟢

**计划中**：
- [Week 6：多 Agent 系统](./Week6_MultiAgent/) ⏳
- [Week 7：系统设计题](./Week7_SystemDesign/) ⏳
- [Week 8+：深化优化](./Week8_Advanced/) ⏳

### 每个周的内容包括

进入任意一个 Week 文件夹，你会看到：

```
Week5_Workflows/
├── Overview.md          ← 开始这里：周目标和学习内容
├── Concepts.md          ← 核心概念讲解
├── Notes.md             ← 个人学习笔记（可选）
├── QnA.md               ← 常见问题解答（可选）
└── Dailies/             ← 每日学习记录
    ├── 2026-04-27_Day1_TextToSQL.md
    ├── 2026-04-28_Day2_Implementation.md
    └── ...
```

### 今天的学习

**今天是**：2026-04-27（第 5 周第 1 天）

**你的进度**：
1. ✅ 学习了 Text-to-SQL 的核心概念
2. 📝 查看笔记：`Week5_Workflows/Dailies/2026-04-27_Day1_TextToSQL.md`
3. 📚 查看详细内容：`Week5_Workflows/Concepts.md`
4. ⏭️ 明天计划：实现 Text-to-SQL 系统

---

## 📋 核心学习内容总结

| 周 | 主题 | 状态 | 关键内容 |
|----|------|------|---------|
| 1 | LLM 基础理论 | ✅ | Transformer、Function Call、LoRA |
| 2 | Agent 框架 | ✅ | LangGraph、Chain vs Agent、工具定义 |
| 3 | Prompt 工程 | ✅ | CoT、参数调优、Prompt Caching |
| 4 | RAG 系统 | ✅ | 检索、向量化、混合检索、幻觉规避 |
| 5 | 工作流设计 | 🟢 | **Text-to-SQL（进行中）** |
| 6 | 多 Agent 系统 | ⏳ | 记忆管理、协作机制、反思循环 |
| 7 | 系统设计题 | ⏳ | 5 个完整的系统设计案例 |
| 8+ | 深化优化 | ⏳ | 性能优化、面试准备 |

---

## ✅ 使用指南

### 开始新的一天

1. **打开该周的 Overview.md**
   ```
   Week5_Workflows/Overview.md
   ```
   了解周目标和学习内容

2. **阅读课程内容**
   ```
   Week5_Workflows/Concepts.md
   ```

3. **创建或编辑每日笔记**
   ```
   Week5_Workflows/Dailies/2026-04-27_Day1_TextToSQL.md
   ```

4. **记录学习进度**
   - 今日目标
   - 完成情况
   - 关键收获
   - 时间统计

### 每周更新进度

1. 每周五更新 `PROGRESS_TRACKER.md`
2. 统计本周完成任务数、理解度、用时
3. 更新下周计划

### 遵循规范

详见 [`LEARNING_RULES.md`](./LEARNING_RULES.md)：
- 文件命名规范
- 每日笔记模板
- Progress 更新规范

---

## 🧠 准备面试

**面试资料**在 `INTERVIEWS/` 目录：

- [`Interview_QnA.md`](./INTERVIEWS/Interview_QnA.md) - 高频问题库
- [`System_Design_Cases.md`](./INTERVIEWS/System_Design_Cases.md) - 5 个系统设计题
- [`Project_Portfolio.md`](./INTERVIEWS/Project_Portfolio.md) - 项目讲解稿

---

## 📊 当前学习水平评估

| 维度 | 评分 | 评价 |
|------|------|------|
| 理论理解度 | 9/10 | ✅ 优秀 |
| 实践能力 | 7.5/10 | ✅ 良好 |
| 项目完成度 | 8/10 | ✅ 优秀 |
| 系统思维 | 8.5/10 | ✅ 优秀 |
| **综合评分** | **8.2/10** | ✅ 达标 |

**优势**：理论基础扎实、系统思维强、学习态度主动
**待加强**：实践编码、系统设计、工程化细节

---

## 🔗 重要文件

| 文件 | 说明 |
|------|------|
| [`LEARNING_RULES.md`](./LEARNING_RULES.md) | 工作流和规范说明 |
| [`PROGRESS_TRACKER.md`](./PROGRESS_TRACKER.md) | 详细的进度统计 |
| [`INTERVIEWS/Interview_QnA.md`](./INTERVIEWS/Interview_QnA.md) | 面试题库 |

---

## 📍 下一步

### 今天完成
- ✅ Text-to-SQL 核心概念学习（完成）
- ✅ 项目结构重组（刚完成）

### 明天计划（2026-04-28）
- [ ] 实现 Text-to-SQL 系统骨架
- [ ] 创建示例数据库
- [ ] 测试 Schema 验证

### 本周目标
- Day 1：核心概念 ✅
- Day 2：系统实现
- Day 3：复杂查询处理
- Day 4：优化和成本控制
- Day 5：知识整合和总结

---

**学习状态**：🟢 进行中，按计划进行
**下一检查点**：2026-04-28（明天）
**预计完成**：8 周后（2026-06-05）

---

*最后更新：2026-04-27*
*项目结构已重组，采用新的"每周完整单元"模式*
