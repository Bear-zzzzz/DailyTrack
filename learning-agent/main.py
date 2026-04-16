"""
Agent 主程序

使用方式：
  python3 main.py
"""

from agent.graph import agent_graph
from agent.state import create_initial_state
from utils import format_thinking, format_observations, format_actions


def run_agent(question: str):
    """
    运行 Agent

    Args:
        question: 用户问题
    """
    print("=" * 60)
    print(f"问题：{question}")
    print("=" * 60)
    print()

    # 创建初始状态
    initial_state = create_initial_state(question)

    # 执行 Agent
    print("Agent 开始思考...\n")
    try:
        result = agent_graph.invoke(initial_state)
    except Exception as e:
        print(f"执行失败：{e}")
        return

    # 输出结果
    print("=" * 60)
    print("AGENT 执行完成")
    print("=" * 60)
    print()

    print("📋 思考过程：")
    print(format_thinking(result["thinking_history"]))
    print()

    print("🔧 工具调用：")
    print(format_actions(result["actions"]))
    print()

    print("📝 获取的信息：")
    print(format_observations(result["observations"]))
    print()

    print("✅ 最终答案：")
    print(result["final_answer"])
    print()


def main():
    """主函数"""
    print("\n🤖 智能学习助手 Agent\n")

    # 测试用例
    test_questions = [
        "什么是 Transformer？",
        "Attention 机制的工作原理是什么？",
        "LoRA 微调如何减少参数？",
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n\n{'='*60}")
        print(f"测试用例 {i}/{len(test_questions)}")
        print(f"{'='*60}\n")

        run_agent(question)

        # 用户可以继续提问
        if i < len(test_questions):
            print("\n继续下一个问题...\n")


if __name__ == "__main__":
    # 可选：运行测试用例
    # main()

    # 或者：交互式问答
    while True:
        question = input("\n请提问（输入 'quit' 退出）: ").strip()
        if question.lower() == "quit":
            print("再见！")
            break
        if question:
            run_agent(question)
