






# 定义一个提示词片段的字典
PROMPT_SECTIONS = {
    # 一个多行的字符串
    "identity": (
        f"你是一个编程的Agent，直接行动，不要解释"
        f"你将在需要的情况下使用Windows CMD环境下执行任务，使用CMD完成任务"
        f""
    )
}


# 系统提示词

def get_system_prompt() -> str:
    return PROMPT_SECTIONS["identity"]
