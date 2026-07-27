


import json

from config import DEFAULT_MAX_TOKENS, MODEL_ID

from prompt import get_system_prompt

from llm import call_llm

from utils import assistant_message_dict



def agent_loop(messages: list):
    # 将最大的tokens数量设置为默认的值8000，未来这个值可能会变化
    max_tokens = DEFAULT_MAX_TOKENS
    # 把模型先设置为这个默认模型，未来如果这个默认模型不能使用的话，就可以切换为备用的模型
    model = MODEL_ID
    while True:
        # 1、获取系统的提示词
        system = get_system_prompt()
        # 2、调用大模型
        response = call_llm(system, messages, max_tokens, model)
        choice = response.choices[0]
        # 3、获取输出的信息
        assistant = choice.message
        # 4、放入这个messages里面
        messages.append(assistant_message_dict(assistant))
        # 5、如果助手没有工具的调用，那么就会终止循环
        if not assistant.tool_calls:
            return
        