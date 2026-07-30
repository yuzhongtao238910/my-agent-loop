import os
import subprocess


"""
处理器
"""


def run_bash(command: str) -> str:
    # 定义一些危险的命令的列表
    dangerous = ["rm -rf", "sudo", "shutdown", "rebot", "> /dev/"]
    # 如果包含这个危险命令
    if any(d in command for d in dangerous):
        # 拒绝执行危险命令
        return f"错误，危险命令{command}已经被拦截"
    try:
        result = subprocess.run(
            command, # 要执行的命令
            shell=True, # 在shell之中执行
            cmd=os.getcwd(), # 把当前的工作目录设置为当前的路径
            capture_output=True, # 捕获标准的输出和标准错误输出
            timeout=120 # 超时时间设为120s
        )
        print(result.stdout)
        # stdout 以及这个 stderr 是 二进制的字节序列
        out = (result.stdout or b"") + (result.stderr or b"")
        

    except subprocess.TimeoutExpired:
        return f"错误:超时（120s）"
    except (FileNotFoundError, OSError) as e:
        return f"错误：{str(e)}"


# 定义字典，把工具的名称和真正的处理函数关联起来
TOOL_HANDLERS = {
    "bash": run_bash,
    "cmd": run_bash
}