# Week 2：Agent 框架和工具实践

**周目标**：选择框架、理解 Chain vs Agent、完成一个简单项目

**学习时间**：12 小时（已完成）
**完成度**：120% ✅✨（超额完成，集成了 Embedding 搜索）
**平均理解度**：96%

---

## 📚 学习内容

### 框架对比与选择
- [x] 对比 LangChain、AutoGen、LlamaIndex、LangGraph
- [x] 选择 LangGraph 作为框架
- [x] 理解 Chain vs Agent 的区别

### 环境搭建
- [x] 创建虚拟环境
- [x] 安装所有依赖
- [x] 运行官方示例

### Agent 设计和实现
- [x] 定义 3 个自定义工具（search_kb、get_concepts、get_code）
- [x] 实现 4 节点的完整 Agent（think→action→judge→generate）
- [x] 集成 Embedding 语义搜索
- [x] 测试 5 个不同的任务

### 代码质量
- [x] 详细的代码注释和文档
- [x] 清晰的状态管理（state.py）
- [x] 功能完整的工具定义（tools.py）

---

## 🎓 核心概念

### Chain vs Agent
- **Chain**：固定的工作流，按顺序执行
- **Agent**：决策循环，根据情况选择下一步
- **LangGraph**：基于图的 Agent 框架，支持条件边和循环

### ReAct 框架
```
Thought → Action → Observation → Thought → ...
```

### 工具定义
```python
def tool(question: str, params: dict) -> str:
    """
    自定义工具必须有：
    - 清晰的输入输出
    - 错误处理
    - 文档字符串
    """
```

### Embedding 搜索
从关键字搜索升级到语义搜索，提升准确率

---

## 📁 相关文件

- 框架对比详情：`CURRICULUM/Week2_Frameworks/Concepts.md`
- 项目代码：`PROJECTS/Project1_LearningAgent/`
- 每日笔记：`DAILIES/Week2_Dailies/`

---

## 🛠️ 项目成果

**项目**：LearningAssistant Agent
- **状态**：✅ 完成（120%）
- **代码行数**：~1500 行
- **功能**：
  - ✅ 4 节点 Agent（think→action→judge→generate）
  - ✅ 3 个工具（search_kb、get_concepts、get_code）
  - ✅ Embedding 语义搜索
  - ✅ 完整文档和注释

**性能指标**
- 成功完成任务数：5 / 5（100%）
- 代码可读性：高
- 文档完整性：高

---

## ✅ 完成标准检查

- [x] 能快速用框架搭建基础 Agent
- [x] 理解工具定义和调用流程
- [x] 能诊断 Agent 失败的原因

---

**最后更新**：2026-04-17
**状态**：✅ 完成
