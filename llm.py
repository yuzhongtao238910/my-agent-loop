

from config import client

# 定义调用大模型的函数

def call_llm(system: str, messages: list, max_tokens: int, model: str):
    """
        system: 系统的提示词
        messages: 消息列表
        max_tokens: 最大的token数量
        model: 模型
    """
    return client.chat.completions.create(
        model=model,
        # 系统提示词与原来的消息列表组成这个messages消息列表
        messages=[
            {"role": "system", "content": system},
            *messages
        ],
        max_tokens=max_tokens,
    )