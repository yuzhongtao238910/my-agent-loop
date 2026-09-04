

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



BASE_TOOLS = [
    get_shell_tool(),    
    _fn_tool("read_file", f"读取文件的内容", {"path": {"type": "string"}, "limit": {"type": "integer"}}, ["path"]),
    _fn_tool("write_file", f"将内容写入文件", {"path": {"type": "string"}, "content": {"type": "string"}}, ["path", "content"]),
    _fn_tool("edit_file", f"在文件之中精确替换文本（仅仅会替换一次）", {"path": {"type": "string"}, "old_text": {"type": "string"}, "new_text": {"type": "string"}}, ["path", "old_text", "new_text"]),
    _fn_tool("glob", f"按照glob模式查询文件", {"pattern": {"type": "string"}}, ["pattern"]),
    

]


TOOLS = [
    *BASE_TOOLS,
    _fn_tool(
        "todo_write", 
        f"创建并且管理当前编码会话的任务列表", 
        {
            "todos": {
                "type": "array", 
                "items": {
                    "type": "object",
                    "properties": {
                        "content": {
                            "type": "string" 
                        },
                        "status": { 
                            "type": "string",
                            "enum": ["pending", "in_progress", "completed"]
                        }
                    },
                    "required": ["content", "status"]
                }
            }
        }, 
        ["todos"]
    ),
    _fn_tool(
        "spawn_subagent", # 派生子代理 
        f"启动子agent处理复杂的子任务,仅返回最终的结论", 
        {
            "description": {
                "type": "string", 
            }
        }, 
        ["description"]
    ),
    _fn_tool(
        "load_skill", # 加载技能
        f"按照名称来加载技能的完整内容", 
        {
            "name": {
                "type": "string", 
            }
        }, 
        ["name"]
    ),
]