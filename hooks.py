





import json



from config import WORKDIR

# 字典，定义一个hook的字典，每一个事件对应回调函数的列表
HOOKS = {
    "UserPromptSubmit": [], # 输入query，执行llm之前
    "PreToolUse": [], # 收到这个tool_call 之后，但是执行之前
    "PostToolUse": [], # handler 之后执行之后，下一轮执行llm之前
    "Stop": [] # 最终输出前
}



# 定义禁止执行的命令的列表
DENY_LIST = [
    "rm -rf /",
    "sudo",
    "shutdown",
    "reboot", # 重启
    "mkfs", # 格式化硬盘
    "dd if=", # 硬盘对拷/清零
    "> /dev/sda", # 重定向覆盖硬盘
    "mv / /dev/null", # 移动根目录到黑洞
    "chmod 777 / -R", # 授予最高权限
    # "test", # 测试使用
]


# 定义需要用户确认的/审批的破坏性的命令
DESTRUCTIVE = [
    "rm ",
    "> /etc/",
    "chmod 777",
    "del",
    "erase",
    "taskkill /f", # 强制结束进程
]




# 注册钩子函数，将回调函数添加到对应事件的hook列表之中
def register_hook(event: str, callback):
    HOOKS[event].append(callback)


# 在工具调用前进行权限判断，如果不通过，返回不为none，如果通过了，返回none
def permission_hook(name: str, args: dict):
    if name == "bash" or name == "cmd":
        for pattern in DENY_LIST:
            if pattern in args.get("command", ""):
                print(f"\n\x1b[31m 🛑已经拦截：{pattern}\n\x1b[0m ")
                return f"禁止列表拒绝权限"

        # 破坏性的、毁灭性的
        for kw in DESTRUCTIVE:
            if kw in args.get("command", ""):
                print(f"\n\x1b[33m 可能存在破坏性的命令\n\x1b[0m ")
                print(f"工具:{name}({args})")
                # 提示用户是否允许执行 yes/y 才会继续执行
                choice = input("是否允许执行?[y/n]").strip().lower()
                if choice not in ("y", "yes"):
                    return f"用户拒绝执行"
    if name in("write_file", "edit_file"):
        # 获取要写入或者编辑的文件的路径 path
        path = args.get("path", "")
        if not (WORKDIR / path).resolve().is_relative_to(WORKDIR):
            # 检查到该文件不在这个当前的目录下面还是需要用户审批的
            print(f"\n\x1b[33m 在工作区域外面写入文件 \n\x1b[0m ")
            print(f"工具:{name}({args})")
            choice = input("是否允许执行?[y/n]").strip().lower()
            if choice not in ("y", "yes"):
                return f"用户拒绝执行"
    return None

# 这是打印调用信息的钩子
def log_hook(name: str, args: dict):

    # args_preview = str(list(args.values())[:2])[:60]
    print(f"\x1b[36m [hook][PreToolUse]{name}{json.dumps(args, ensure_ascii=False)} \x1b[0m")

    return None


def large_output_hook(name: str, args: dict, output):
    if len(str(output)) > 10000:
        print(f"\x1b[33m [hook][PostToolUse]: {name}输出的结果过大:{len(str(output))}字符 \x1b[0m")



def summary_hook(messages: list):
    # 统计本地会话之中工具调用的次数
    tool_count = sum(1 for m in messages if m.get("role") == "tool")
    print(f"\x1b[90m [hook][Stop]: 本次会话共计使用{tool_count}次工具调用 \x1b[0m")
    return None

# 触发通过hook函数
def trigger_hooks(event: str, *args):
    # 按照注册的顺序依次触发对应事件的hook
    for callback in HOOKS[event]:
        # 调用这个hook函数获取返回值
        result = callback(*args)
        # 不为none的话，就会终止执行，并且返回这个result
        if result is not None:
            return result
    # 如果所有的hook都返回none，就是通过了
    return None


# 触发用户相关的hook
def trigger_user_prompt_hooks(query: str):
    # 当前等待处理的查询
    current = query
    # 依次触发hook之中的回调函数
    for callback in HOOKS["UserPromptSubmit"]:
        # 调用每个回调函数等到结果
        result = callback(current)
        if isinstance(result, str):
            current = result
    return current

def workspace_inject_hook(query: str) -> str | None:
    print(f"\x1b[90m [hook][UserPromptSubmit]：注入工作目录：{WORKDIR} \x1b[0m")
    return f"<workspace>\n当前的工作目录是:{WORKDIR}\n</workspace>\n\n{query}"


register_hook("UserPromptSubmit", workspace_inject_hook)

# 注册这个权限钩子
register_hook("PreToolUse", permission_hook)

register_hook("PreToolUse", log_hook)

register_hook("PostToolUse", large_output_hook)


register_hook("Stop", summary_hook)