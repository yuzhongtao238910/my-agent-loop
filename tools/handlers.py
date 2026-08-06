import os
import subprocess
from utils import decode_subprocess_output, safe_path
from config import TEXT_ENCODING, WORKDIR
import platform
import glob
"""
处理器
"""

def is_windows():
    """检测当前系统是否为 Windows"""
    return platform.system().lower() == "windows"

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
            cwd=os.getcwd(), # 把当前的工作目录设置为当前的路径
            capture_output=True, # 捕获标准的输出和标准错误输出
            timeout=120 # 超时时间设为120s
        )
        print(result.stdout, type(result.stdout))
        # stdout 以及这个 stderr 是 二进制的字节序列
        out = decode_subprocess_output( (result.stdout or b"") + (result.stderr or b"") ).strip()

        # 如果有值返回前5w个，否则
        return out[:50000] if out else "(没有输出)"
         

    except subprocess.TimeoutExpired:
        return f"错误:超时（120s）"
    except (FileNotFoundError, OSError) as e:
        return f"错误：{str(e)}"



def run_read(path: str, limit: int | None = None) -> str:
    try:
        # 只能读取当前正在这个工作目录下面的这个子文件
        # 使用这个safe_path 校验并且获取文件的路径 并且指定这个编码读取内容并且按行分割
        lines = safe_path(path).read_text(encoding=TEXT_ENCODING).splitlines()
        if limit and limit < len(lines):
            # 截取前这个limit行
            lines = lines[:limit] + [f"...(还有{len(lines)-limit}行)"]
        # 返回数据
        return "\n".join(lines)
    except Exception as e:
        return f"错误: {str(e)}"


def run_write(path: str, content: str|None) -> str:
    try:
        # 获取安全路径
        file_path = safe_path(path)
        # 确保父目录是存在的，不存在的话就会进行自动的创建
        file_path.parent.mkdir(parents=True, exist_ok=True)
        # 按照指定的编码写入指定的内容到指定的文件哈
        file_path.write_text(content, encoding=TEXT_ENCODING)
        return f"已经写入{len(content)}字节到{path}之中"
    except Exception as e:
        return f"错误: {str(e)}"


def run_edit(path: str, old_text: str, new_text: str) -> str:
    try:
        # 获取安全路径
        file_path = safe_path(path)
        # 读取文件内容
        text = file_path.read_text()
        if old_text not in text:
            return f"错误:在{path}之中没有找到指定的文本{old_text}"
        file_path.read_text(text.replace(old_text, new_text, 1), encoding=TEXT_ENCODING)
        return f"已经编辑{path}"
    except Exception as e:
        return f"错误: {str(e)}"

def run_glob(pattern: str) -> str:
    try:
        # 获取安全路径
        results = []
        # 遍历所有匹配到的路径
        for match in glob.glob(pattern, root_dir=WORKDIR):

            # 检查匹配到的路径是否是相对于这个WORKDIR的子路径
            if (WORKDIR / match).resolve().is_relative_to(WORKDIR):
                results.append(match)
            
        return "\n".join(results) if results else "(没有匹配到任何文件)"
        
    except Exception as e:
        return f"错误: {str(e)}"



# 全局变量 用于存储当前的任务列表，类型为这个list[dict]
CURRENT_TODOS: list[dict] = []


# 定义更新这个CURRENT_TODOS 这个函数
def run_todo_write(todos: list) -> str:
    global CURRENT_TODOS
    for index, todo in enumerate(todos):
        if "content" not in todo or "status" not in todo:
            return f"错误：todos[{index}] 缺少content或者status字段"
        if todo["status"] not in ("pending", "in_progress", "completed"):
            return f"错误：todos[{index}] 状态无效"
    CURRENT_TODOS = todos

    lines = [
        "\n\x1b33m##当前任务\x1b[0m"
    ]
        



# 定义字典，把工具的名称和真正的处理函数关联起来
TOOL_HANDLERS = {
    "bash": run_bash,
    "cmd": run_bash,
    "read_file": run_read,
    "write_file": run_write,
    "edit_file": run_edit,
    "glob": run_glob,
    "todo_write": run_todo_write
}