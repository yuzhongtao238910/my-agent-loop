


import json

from config import DEFAULT_MAX_TOKENS, MODEL_ID

from prompt import get_system_prompt

from llm import call_llm

from utils import assistant_message_dict

from tools.executor import execute_tool



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
        # 6、助手需要调用工具，那么就是循环所有的工具的调用
        for tool_call in assistant.tool_calls:
            # 获取工具的名称
            name = tool_call.function.name
            # 获取参数
            print(tool_call)
            args = json.loads(tool_call.function.arguments or '{}')
            print(f"\x1b[36m {name}{json.dumps(args, ensure_ascii=False)} \x1b[0m")
            # 执行工具，获取输出的结果
            output = execute_tool(name, args)
            # 需要把结果放入到这个消息列表之中
            messages.append({
                "role": "tool",
                "content": output,
                "tool_call_id": tool_call.id
            })