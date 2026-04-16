"""
Agent 工具定义
"""

from knowledge.kb import search_kb, get_related_concepts, get_code_example


def tool_search_kb(query: str) -> str:
    """工具 1：搜索知识库"""
    results = search_kb(query)
    if results:
        return "\n---\n".join(results)
    else:
        return f"没有找到关于 '{query}' 的信息"


def tool_get_concepts(query: str = None, concept: str = None) -> str:
    """工具 2：获取相关概念"""
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


def tool_get_code(concept: str) -> str:
    """工具 3：获取代码示例"""
    code = get_code_example(concept)
    return f"代码示例：\n{code}"


# 工具定义（供 Agent 使用）
TOOLS = [
    {
        "name": "search_kb",
        "description": "在知识库中搜索相关信息。输入：查询字符串，输出：相关文本",
        "func": tool_search_kb
    },
    {
        "name": "get_concepts",
        "description": "获取某个概念的相关概念列表。输入：概念名称，输出：相关概念",
        "func": tool_get_concepts
    },
    {
        "name": "get_code",
        "description": "获取某个概念的代码实现示例。输入：概念名称，输出：代码",
        "func": tool_get_code
    }
]


def execute_tool(tool_name: str, args: dict) -> str:
    """执行工具"""
    for tool in TOOLS:
        if tool["name"] == tool_name:
            try:
                return tool["func"](**args)
            except Exception as e:
                return f"工具执行错误：{str(e)}"
    return f"找不到工具：{tool_name}"
