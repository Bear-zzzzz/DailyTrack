"""
Agent 功能测试脚本

这个脚本通过 5 个不同的测试场景来验证 Agent 系统的完整功能。
每个测试用例代表一个真实的用户问题场景。

测试目标：
1. 验证 Agent 能够处理多种类型的问题
2. 确认工具调用的正确性
3. 检查思考→行动→判断→生成的完整流程
4. 验证最终答案的质量和相关性
"""

from agent.graph import agent_graph
from agent.state import create_initial_state
from utils import format_thinking, format_observations, format_actions


def test_case(case_num: int, question: str, description: str):
    """
    运行一个测试用例

    参数：
        case_num: 测试用例编号
        question: 用户问题
        description: 测试用例描述
    """
    print(f"\n{'='*70}")
    print(f"测试用例 {case_num}：{description}")
    print(f"{'='*70}")
    print(f"问题：{question}\n")

    # 创建初始状态
    initial_state = create_initial_state(question)

    # 运行 Agent
    print("执行 Agent...\n")
    try:
        result = agent_graph.invoke(initial_state)
    except Exception as e:
        print(f"❌ 执行失败：{e}")
        return False

    # 分析结果
    print("-" * 70)
    print(f"思考过程 ({len(result['thinking_history'])} 步):")
    print(format_thinking(result["thinking_history"]))
    print()

    print(f"工具调用 ({len(result['actions'])} 次):")
    print(format_actions(result["actions"]))
    print()

    print(f"获取的信息 ({len(result['observations'])} 条):")
    print(format_observations(result["observations"]))
    print()

    # 检查是否有最终答案
    if result.get("final_answer"):
        print("✅ 最终答案已生成")
        print(f"答案长度：{len(result['final_answer'])} 字符")
    else:
        print("⚠️  未生成最终答案")

    print("-" * 70)
    return True


def main():
    """运行所有测试用例"""
    print("\n" + "="*70)
    print("Agent 系统功能验证测试")
    print("="*70)
    print("\n本测试包含 5 个场景，验证以下功能：")
    print("1. 概念定义查询（使用 search_kb 工具）")
    print("2. 相关概念探索（使用 get_concepts 工具）")
    print("3. 代码示例获取（使用 get_code 工具）")
    print("4. 复杂问题拆分（多个工具协同）")
    print("5. 深度问题理解（推理和总结）")

    # 定义 5 个测试用例
    test_cases = [
        (
            1,
            "什么是 Transformer？",
            "基础概念查询"
        ),
        (
            2,
            "Attention 机制的工作原理是什么？",
            "深度概念解释"
        ),
        (
            3,
            "LoRA 微调相关的概念有哪些？",
            "相关概念探索"
        ),
        (
            4,
            "Function Call 怎么实现？",
            "代码实现查询"
        ),
        (
            5,
            "Transformer 和 Self-Attention 有什么关系？",
            "概念关系理解"
        ),
    ]

    # 运行所有测试
    results = []
    for case_num, question, description in test_cases:
        success = test_case(case_num, question, description)
        results.append((case_num, description, success))

    # 总结结果
    print("\n" + "="*70)
    print("测试总结")
    print("="*70)

    passed = sum(1 for _, _, success in results if success)
    total = len(results)

    print(f"\n通过：{passed}/{total} 个测试用例\n")

    for case_num, description, success in results:
        status = "✅" if success else "❌"
        print(f"{status} 测试用例 {case_num}：{description}")

    print(f"\n总体通过率：{passed/total*100:.0f}%")

    if passed == total:
        print("\n🎉 所有测试通过！Agent 系统功能完整！")
    else:
        print(f"\n⚠️  有 {total-passed} 个测试未通过，请检查相关代码。")

    print("\n" + "="*70)


if __name__ == "__main__":
    main()
