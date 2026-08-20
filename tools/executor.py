




import json

import inspect
from tools.handlers import TOOL_HANDLERS
from config import client, MODEL_ID, DEFAULT_MAX_TOKENS
from prompt import SUB_SYSTEM
from hooks import trigger_hooks
# 引入基础工具
from tools.schema import BASE_TOOLS
from utils import assistant_message_dict, extract_text


# 接收工具的名称和参数的字典哈，返回对应的结果哈
# args = {"name": "yuzhongtao", "age": 18, "command": "xxx"}
def execute_tool(name: str, args: dict) -> str:
    # 根据工具的名称从这个TOOL_HANDLERS获取对应的处理函数
    handler = TOOL_HANDLERS.get(name)
    # 如果没有找到对应的处理函数，那么就会返回错误提示
    if not handler:
        return f"未知工具:{name}"
    # 获取处理函数的参数的签名
    sig = inspect.signature(handler)
    # 从输入参数之中筛选出来处理函数所需要的有效的参数哈
    valid = {
        k:v for k, v in args.items() if k in sig.parameters
    }
    return handler(**valid)





# 定义运行子agent的函数 参数为这个描述字符串，返回字符串
def run_spawn_subagent(description: str):
    print(f"\x1b[35m [子agent已经启动] 任务是:{description} \x1b[0m ")
    # 创建一个新的上下文列表 用户的描述是第一条的用户消息
    messages = [
        {
            "role": "user",
            "content": description
        }
    ]

    # subagent就是一轮对话，用户的输入就是：description
    # 最多进行30轮的交互
    for _ in range(30):
        response = client.chat.completions.create(
            model=MODEL_ID,
            # 系统提示词与原来的消息列表组成这个messages消息列表
            messages=[
                {"role": "system", "content": SUB_SYSTEM["identity"]},
                *messages
            ],
            max_tokens=DEFAULT_MAX_TOKENS,
            tools=BASE_TOOLS,
        )
        # 获取message
        assistant = response.choices[0].message

        messages.append(assistant_message_dict(assistant))

        if not assistant.tool_calls:
            break;
        # 获取tool call的列表
        for tool_call in assistant.tool_calls:
            # 获取工具的名称
            name = tool_call.function.name

            args = json.loads(tool_call.function.arguments or '{}')

            # 工具调用前 触发这个PreToolUse 这个hook 返回是否允许工具执行
            blocked = trigger_hooks("PreToolUse", name, args)
            if blocked:
                messages.append({
                    "role": "tool", # 角色是工具
                    "content": str(blocked) + ".", # 拒绝的原因
                    "tool_call_id": tool_call.id # 关联的工具id
                })
                continue
            # 执行工具，获取输出的结果
            output = execute_tool(name, args) if name in TOOL_HANDLERS else f"未知工具"

            # 触发这个PostToolUse 这个hook进行后置处理
            trigger_hooks("PostToolUse", name, args, output)

            print(f"\x1b[90m [SubAgent] {name} {str(output)[:100]} \x1b[0m ")

            # 需要把结果放入到这个消息列表之中
            messages.append({
                "role": "tool",
                "content": output,
                "tool_call_id": tool_call.id
            })
    # 从所有的消息之中最后一条内容之中提取这个文本为最终结果
    result = extract_text(messages[-1].get("content"))

    # 如果没有提取到，反向查找assistant角色消息并且提取结果
    # 核心就是找到最后一条助手的回复
    if not result:
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                result = extract_text(msg.get("content"))
                if result:
                    break;
    # 
    print(f"\x1b[35m [SubAgent] 完成任务 {result} \x1b[0m ")
    return result

TOOL_HANDLERS["spawn_subagent"] = run_spawn_subagent