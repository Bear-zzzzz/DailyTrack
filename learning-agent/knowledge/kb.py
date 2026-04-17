"""
知识库
"""

from typing import List


KNOWLEDGE_BASE = {
    "Transformer": {
        "title": "Transformer 架构",
        "content": """Transformer 是由 Vaswani 等人在 2017 年论文《Attention is All You Need》中提出的神经网络架构。
核心特点：
1. 使用 Self-Attention 替代递推机制，支持完全并行化
2. 包含 Encoder 和 Decoder 两部分
3. 能够捕捉长距离依赖关系
4. 是 BERT、GPT 等大模型的基础

结构：
- Encoder：多层 Transformer Block
- Decoder：多层 Transformer Block
- 每层包含：Self-Attention + Feed-Forward Network""",
        "related_concepts": ["Attention", "Self-Attention", "Position Encoding"],
        "difficulty": "中等",
        "keywords": ["架构", "并行", "注意力"]
    },

    "Attention": {
        "title": "Attention 机制",
        "content": """Attention 是一种机制，允许模型在处理信息时选择性地关注输入的不同部分。

核心公式：
Attention(Q, K, V) = softmax(Q·K^T / √d_k) · V

其中：
- Q（Query）：查询
- K（Key）：键
- V（Value）：值
- d_k：键的维度

优点：
1. 能够建模长距离依赖
2. 计算效率高
3. 易于并行化
4. 提供可解释性（注意力权重）""",
        "related_concepts": ["Transformer", "Self-Attention"],
        "difficulty": "高",
        "keywords": ["机制", "相似度", "加权"]
    },

    "Self-Attention": {
        "title": "Self-Attention 原理",
        "content": """Self-Attention 是 Attention 的特殊形式，其中查询、键和值都来自同一来源。

三个步骤：
1. 计算 Q、K、V（通过线性变换）
   Q = x·W_Q
   K = x·W_K
   V = x·W_V

2. 计算相似度：Q·K^T

3. 生成加权和：softmax·V

应用：让每个词能关注所有其他词（包括自己）

特点：
- 无需预定义的上下文窗口
- 能直接建模任意词对的关系
- 是 Transformer 的核心""",
        "related_concepts": ["Attention", "Multi-Head Attention"],
        "difficulty": "中等",
        "keywords": ["三步骤", "Q", "K", "V"]
    },

    "LoRA": {
        "title": "LoRA 微调",
        "content": """LoRA（Low-Rank Adaptation）是一种参数高效的微调方法。

核心思想：
- 冻结预训练权重 W
- 添加小的秩-r 分解矩阵 ΔW = B·A
- 只训练 A 和 B（参数减少 50-100 倍）

公式：
y = W·x + ΔW·x = W·x + B·A·x

其中 A ∈ R^(r × d_in)，B ∈ R^(d_out × r)，r << min(d_in, d_out)

优势：
1. 参数少（1.6% 的参数）
2. 速度快（1000倍快）
3. 效果好（95% 的效果）
4. 易于切换任务""",
        "related_concepts": ["微调", "参数效率", "矩阵分解"],
        "difficulty": "中等",
        "keywords": ["低秩", "参数", "微调"]
    },

    "Function Call": {
        "title": "Function Call 原理",
        "content": """Function Call 使模型能够调用外部工具和函数。

工作流程：
1. 定义工具（JSON Schema）
   描述函数名、参数、作用

2. 模型理解何时调用工具
   根据用户输入判断需要什么工具

3. 模型提取工具参数
   从推理结果中解析参数值

4. 系统执行工具
   调用对应的函数

5. 返回结果给模型
   模型继续推理或返回最终答案

意义：
从 Chatbot（生成文本）升级到 Agent（执行任务）
使模型能够主动采取行动，而不仅仅生成文本""",
        "related_concepts": ["Agent", "工具调用", "JSON Schema"],
        "difficulty": "中等",
        "keywords": ["工具", "执行", "参数"]
    },
}


def search_kb(query: str, top_k: int = 3) -> List[str]:
    """搜索知识库"""
    results = []
    query_lower = query.lower()

    for key, item in KNOWLEDGE_BASE.items():
        # 简单的关键词匹配
        score = 0
        if query_lower in key.lower():
            score += 10
        if query_lower in item["title"].lower():
            score += 5

        for keyword in item.get("keywords", []):
            if query_lower in keyword.lower():
                score += 2

        if score > 0:
            results.append({
                "title": item["title"],
                "content": item["content"],
                "score": score
            })

    # 按分数排序，返回前 top_k
    results.sort(key=lambda x: x["score"], reverse=True)
    return [r["content"] for r in results[:top_k]]


def get_related_concepts(concept: str) -> List[str]:
    """获取相关概念"""
    if concept in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[concept].get("related_concepts", [])
    return []


def get_code_example(concept: str) -> str:
    """获取代码示例"""
    code_examples = {
        "Attention": """
# Attention 实现示例
import math
from torch.nn import functional as F

def attention(Q, K, V, mask=None):
    d_k = Q.shape[-1]
    scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
    if mask is not None:
        scores = scores + mask
    weights = F.softmax(scores, dim=-1)
    return weights @ V
""",
        "Transformer": """
# Transformer Block 实现示例
import torch.nn as nn

class TransformerBlock(nn.Module):
    def __init__(self, d_model, num_heads, d_ff):
        super().__init__()
        self.attention = nn.MultiheadAttention(d_model, num_heads)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Linear(d_ff, d_model)
        )
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)

    def forward(self, x):
        x = x + self.attention(x, x, x)[0]
        x = self.norm1(x)
        x = x + self.ffn(x)
        x = self.norm2(x)
        return x
""",
        "LoRA": """
# LoRA 实现示例
import torch.nn as nn

class LoRA(nn.Module):
    def __init__(self, in_features, out_features, rank=8):
        super().__init__()
        self.A = nn.Linear(in_features, rank, bias=False)
        self.B = nn.Linear(rank, out_features, bias=False)
        nn.init.normal_(self.A.weight, 0, 0.01)
        nn.init.zeros_(self.B.weight)

    def forward(self, x):
        return self.B(self.A(x))
""",
    }
    return code_examples.get(concept, "没有该概念的代码示例")


# 初始化 Embedding Manager
from knowledge.embeddings import EmbeddingManager
embedding_manager = EmbeddingManager()
embedding_manager.index_documents(KNOWLEDGE_BASE)
