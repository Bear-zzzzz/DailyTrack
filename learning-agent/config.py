"""
LLM 配置

支持：
1. 本地 OpenAI 兼容服务（推荐）
2. 远程 OpenAI
3. Anthropic Claude
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMConfig:
    """LLM 配置类"""

    def __init__(self):
        # 检查是否使用本地 LLM
        self.use_local = os.getenv("USE_LOCAL_LLM", "true").lower() == "true"

        if self.use_local:
            self.base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://127.0.0.1:15731/v1")
            self.api_key = os.getenv("LOCAL_LLM_API_KEY", "sk-synapse-proxy")
            self.model = os.getenv("LOCAL_LLM_MODEL", "gpt-5.4")
            self.provider = "local"
        else:
            # 远程 API
            self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
            self.provider = "openai" if "OPENAI" in os.environ else "anthropic"
            self.model = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
            self.base_url = None

    def get_llm(self):
        """获取 LLM 客户端"""
        if self.use_local:
            return OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        elif self.provider == "openai":
            return OpenAI(api_key=self.api_key)
        else:
            # Anthropic
            from anthropic import Anthropic
            return Anthropic(api_key=self.api_key)

    def call_llm(self, prompt: str) -> str:
        """
        调用 LLM 的便捷方法

        Args:
            prompt: 输入提示

        Returns:
            LLM 的响应
        """
        client = self.get_llm()

        if self.use_local or self.provider == "openai":
            # 使用 OpenAI 兼容 API
            response = client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000,
            )
            return response.choices[0].message.content
        else:
            # Anthropic
            message = client.messages.create(
                model=self.model,
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text


# 创建全局配置实例
llm_config = LLMConfig()

print(f"✓ LLM 已配置")
print(f"  提供商: {llm_config.provider}")
print(f"  模型: {llm_config.model}")
if llm_config.use_local:
    print(f"  地址: {llm_config.base_url}")
