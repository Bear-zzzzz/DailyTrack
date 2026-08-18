# 📅 Week6 Day3 - 多Agent系统实现 + Reflexion反思循环

**日期**：2026-04-29
**主题**：多Agent实现实践 + 反思改进循环

---

## ✅ 学习成果

### 多Agent系统实现

**LangGraph Supervisor + Worker 完整架构**：
- ✅ State 设计：task、next_worker、worker_instructions、worker_results、final_answer、error_log、retry_count
- ✅ Worker 节点：验证输入 → 执行任务 → 返回结构化结果（带置信度、来源、时间戳）
- ✅ Supervisor 节点：任务分配 → 评估质量 → 决定下一步（重试/换人/整合）
- ✅ 路由逻辑：conditional_edges → worker_a / worker_b / FINISH / RETRY
- ✅ Worker 完成后回 Supervisor，集中控制便于调试

**关键设计原则**：
- 每个 Worker 有明确的输入 schema（结构化指令）
- Supervisor 是唯一的路由决策点
- 失败时路由到 supervisor 而不是直接重试

### Reflexion 反思循环实现

**3步骤**：执行 → 观察 → 生成反思 → 存入程序记忆
```
执行 → Error "column not found"
反思："以为 user_name 存在，实际是 username，下次先检查 Schema"
存储到程序记忆 → 下次检索到这条教训，自动应用
```

**实现要点**：
- 反思 prompt 用具体 checklist，不用通用"评估好不好"
- 迭代上限 2-3 次，避免无限循环
- 只在复杂/高风险任务上应用，控制成本
- 结合外部验证（工具执行）弥补LLM自我反思的局限

---

**状态**：✅ Day 3 完成
