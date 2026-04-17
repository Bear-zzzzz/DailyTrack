"""
Embedding 管理模块
"""

import os
import json
import numpy as np
from typing import List, Dict
from sentence_transformers import SentenceTransformer, util

class EmbeddingManager:
    """使用 embedding 进行智能搜索"""

    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """初始化 embedding 模型"""
        print(f"加载 Embedding 模型: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.embeddings = {}
        self.documents = {}

    def index_documents(self, documents: Dict) -> None:
        """为文档构建索引"""
        print(f"对 {len(documents)} 个文档进行 embedding...")

        for key, doc in documents.items():
            # 合并标题和内容进行 embedding
            text = f"{doc['title']} {doc['content']}"
            embedding = self.model.encode(text)

            self.embeddings[key] = embedding
            self.documents[key] = doc

        print(f"✓ 完成。已索引 {len(self.embeddings)} 个文档\n")

    def search(self, query: str, top_k: int = 3) -> List[str]:
        """使用 embedding 搜索"""
        if not self.embeddings:
            return ["错误：没有索引文档"]

        # 对查询进行 embedding
        query_embedding = self.model.encode(query)

        # 计算相似度
        similarities = {}
        for key, doc_embedding in self.embeddings.items():
            similarity = util.pytorch_cos_sim(query_embedding, doc_embedding)[0][0].item()
            similarities[key] = similarity

        # 排序并返回前 top_k
        top_results = sorted(similarities.items(), key=lambda x: x[1], reverse=True)[:top_k]

        results = []
        for key, score in top_results:
            doc = self.documents[key]
            results.append(f"{doc['content']}\n[相似度: {score:.2%}]")

        return results
