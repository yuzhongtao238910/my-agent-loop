


import inspect
from tools.handlers import TOOL_HANDLERS


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


    