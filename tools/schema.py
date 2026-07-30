

import platform




def _fn_tool(
    name: str,
    description: str,
    properties: dict,
    required: list[str]
) -> dict:
    """
        用于定义工具的函数,接收函数名称、函数描述、属性和必填的字段
        返回一个字典
    """
    return {
        "type": "function", # 类型是函数
        "function": { # 函数的具体内容
            "name": name, # 函数的名称
            "description": description, # 函数的描述
            "parameters": { # 参数的设置，是一个对象，包含属性和必须的字段
                "type": "object", 
                "properties": properties,
                "required": required
            }
        }
    }





def get_shell_tool():
    shell_name = "bash" if platform.system() != "Windows" else "cmd"
    return _fn_tool(shell_name, f"执行一条{shell_name}命令", {
        "command": {"type": "string"}
    }, ["command"])



TOOLS = [
    get_shell_tool(),    
]