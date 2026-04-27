# Week 1：LLM 基础理论

**周目标**：理解 Transformer 架构、Function Call 原理、微调方案

**学习时间**：6.5 小时（已完成）
**完成度**：95% ✅
**平均理解度**：96%

---

## 📚 学习内容

### Day 1-5 核心任务

- [x] Transformer 架构（Q/K/V、Attention）
- [x] Self-Attention 三步骤
- [x] Multi-head Attention 原理
- [x] 位置编码和相对位置编码
- [x] Feed-Forward Network
- [x] 大模型训练流程（预训练→指令→RLHF）
- [x] Function Call 训练机制
- [x] LoRA、QLoRA 微调方案
- [x] Embedding 和分词原理
- [x] 第 1 周小结和面试题生成

---

## 🎓 核心概念

### Transformer 架构
- Encoder-Decoder 结构
- 自注意力机制（Self-Attention）
- 多头注意力（Multi-head Attention）
- 位置编码（Positional Encoding）

### 大模型训练
- **预训练**：Next Token Prediction
- **指令微调**：Supervised Fine-tuning (SFT)
- **对齐训练**：RLHF（Reinforcement Learning from Human Feedback）

### Function Call 原理
- 在指令微调中训练的工具调用能力
- JSON 格式的函数定义
- 条件触发和参数识别

### 微调方案对比
- **Full Finetune**：所有参数更新，成本高，效果最好
- **LoRA**：只训练小的低秩矩阵，参数少 99%，效果好
- **QLoRA**：LoRA + 量化，成本最低

---

## 📁 相关文件

- 详细概念：`CURRICULUM/Week1_Fundamentals/Concepts.md`
- 常见问题：`CURRICULUM/Week1_Fundamentals/QnA.md`
- 每日笔记：`DAILIES/Week1_Dailies/2026-04-10_Day1.md` 等

---

## ✅ 完成标准检查

- [x] 能用 5 分钟讲清楚 Attention 机制
- [x] 理解为什么 Function Call 需要在指令微调中训练
- [x] 掌握 LoRA vs Full Finetune 的权衡

---

**最后更新**：2026-04-15
**状态**：✅ 完成
