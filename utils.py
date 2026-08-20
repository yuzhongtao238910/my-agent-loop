

from pathlib import Path
from config import WORKDIR



# 工具函数，可以把pydantic类型的大模型的回复的消息对象转换为字典
def assistant_message_dict(message) -> dict:
    # model_dump 可以把这个对象转换为字典，排除为none
    data = message.model_dump(exclude_none=True)
    # 角色的类型设置为助手
    data["role"] = "assistant"
    return data



# data 是一个字节的类型，返回这个字符串
def decode_subprocess_output(data: bytes | None)-> str:
    if not data:
        return ""
    for encoding in ("utf-8", "gbk", "cp936"):
        try:
            return data.decode(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return data.decode("utf-8", errors="replace")



# 安全路径
def safe_path(p: str) -> Path:
    """
    此函数接受路径，返回一个path
    """

    # 得到p的绝对路径
    # 
    path = (WORKDIR / p).resolve()


    # 判断path是不是在WORKDIR工作区域内部的子路径，如果不是就会抛出异常
    # "../config/secret.txt"
    # "/tmp/upload.exe"
    if not path.is_relative_to(WORKDIR):
        raise ValueError(f"超出工作区域:{p}")
    # 返回最终安全生成的路径的对象哈
    return path


def extract_text(content: str) -> str:
    if content is None:
        return ""
    if isinstance(content, str):
        return content
    return str(content)