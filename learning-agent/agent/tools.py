"""
Agent 工具定义

这个模块定义了 Agent 可以使用的三个核心工具。
每个工具都对应一个具体的功能，Agent 会根据问题的需求选择合适的工具。
"""

from knowledge.kb import search_kb, get_related_concepts, get_code_example


def tool_search_kb(query: str) -> str:
    """
    工具 1：语义搜索知识库（使用 Embedding）

    功能：
        在知识库中搜索与查询最相关的文档。
        使用 Sentence-Transformers 计算查询与文档的语义相似度，
        然后返回相似度最高的前 3 个结果。

    使用场景：
        - 用户问 "什么是 Transformer？"
        - 需要获取概念的具体定义和详细解释
        - 不仅依靠关键词匹配，而是理解语义

    参数：
        query (str): 用户的查询字符串

    返回值：
        str: 匹配的文档内容（包含相似度分数）

    例子：
        输入：tool_search_kb("注意力机制")
        输出：
            Attention 是一种机制... [相似度: 58.16%]
            ---
            Self-Attention 是 Attention 的特殊形式... [相似度: 48.23%]
    """
    from knowledge.kb import embedding_manager
    results = embedding_manager.search(query, top_k=3)
    if results:
        return "\n---\n".join(results)
    else:
        return f"没有找到关于 '{query}' 的信息"


def tool_get_concepts(query: str = None, concept: str = None) -> str:
    """
    工具 2：获取相关概念列表

    功能：
        当用户想了解某个概念的相关方向时，这个工具可以返回
        知识库中与该概念相关的其他概念列表。

    使用场景：
        - 用户问 "Transformer 相关还有什么？"
        - 用户想了解学习路径和概念间的关系
        - 需要探索相关的学习主题

    工作原理：
        1. 尝试从查询中识别已知概念
        2. 如果找到，返回该概念的相关概念列表
        3. 如果没找到，在知识库中搜索相关信息

    参数：
        query (str, 可选): 概念名称或包含概念的描述
        concept (str, 可选): 直接指定概念名称

    返回值：
        str: 相关概念列表

    例子：
        输入：tool_get_concepts("Transformer")
        输出：相关概念有：Attention, Self-Attention, Position Encoding
    """
    # 兼容 query 和 concept 两个参数名
    target = query or concept
    if not target:
        return "错误：未提供概念名称"

    # 从长字符串中提取知识库中存在的概念名称
    # 优先查找知识库中存在的概念
    from knowledge.kb import KNOWLEDGE_BASE

    known_concepts = list(KNOWLEDGE_BASE.keys())

    # 尝试直接匹配
    if target in known_concepts:
        concepts = get_related_concepts(target)
        if concepts:
            return f"相关概念有：{', '.join(concepts)}"
        else:
            return f"没有找到 '{target}' 的相关概念"

    # 尝试部分匹配（从目标字符串中找包含的概念）
    for concept_name in known_concepts:
        if concept_name.lower() in target.lower():
            concepts = get_related_concepts(concept_name)
            if concepts:
                return f"相关概念有：{', '.join(concepts)}"

    # 如果还是没找到，就搜索知识库
    from knowledge.kb import search_kb
    results = search_kb(target)
    if results:
        return f"找到的相关信息：{results[0][:200]}..."
    else:
        return f"没有找到关于 '{target}' 的相关概念或信息"


def tool_get_code(concept: str = None, query: str = None) -> str:
    """
    工具 3：获取代码示例

    功能：
        为某个概念提供实现代码示例，帮助用户理解具体实现方式。

    使用场景：
        - 用户问 "Transformer 怎么实现？"
        - 用户想看 Attention 的具体代码
        - 用户想了解 LoRA 的代码细节

    参数：
        concept (str): 概念名称
        query (str): 备选参数名（兼容 LLM 的不同调用方式）

    返回值：
        str: 代码示例（Python）

    例子：
        输入：tool_get_code("Attention")
        输出：
            代码示例：
            def attention(Q, K, V, mask=None):
                scores = Q @ K.transpose(-2, -1) / math.sqrt(d_k)
                ...
    """
    target = concept or query
    if not target:
        return "错误：未提供概念名称"

    code = get_code_example(target)
    return f"代码示例：\n{code}"


# 工具定义（供 Agent 使用）
TOOLS = [
    {
        "name": "search_kb",
        "description": "在知识库中搜索相关信息。输入：查询字符串，输出：相关文本和相似度分数",
        "func": tool_search_kb
    },
    {
        "name": "get_concepts",
        "description": "获取某个概念的相关概念列表。输入：概念名称，输出：相关概念名称",
        "func": tool_get_concepts
    },
    {
        "name": "get_code",
        "description": "获取某个概念的代码实现示例。输入：概念名称，输出：Python 代码",
        "func": tool_get_code
    }
]


def execute_tool(tool_name: str, args: dict) -> str:
    """
    执行工具

    这是工具的统一调用接口。Agent 通过指定工具名称和参数，
    这个函数负责找到对应的工具并执行。

    参数：
        tool_name (str): 工具名称（search_kb / get_concepts / get_code）
        args (dict): 工具的参数字典

    返回值：
        str: 工具执行的结果

    异常处理：
        如果工具执行过程中出现错误，会捕获异常并返回错误信息。
        如果找不到指定的工具，会返回提示信息。
    """
    for tool in TOOLS:
        if tool["name"] == tool_name:
            try:
                return tool["func"](**args)
            except Exception as e:
                return f"工具执行错误：{str(e)}"
    return f"找不到工具：{tool_name}"
