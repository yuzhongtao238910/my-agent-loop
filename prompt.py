

from config import WORKDIR

from skills import SKILL_REGISTRY


# 定义一个提示词片段的字典
PROMPT_SECTIONS = {
    # 一个多行的字符串
    "identity": (
        f"你是一个编程的Agent，直接行动，不要解释"
        f"你将在需要使用命令的情况下使用Windows CMD环境下执行任务，使用CMD完成任务"
        f"所有破坏性的操作都需要用户批准"
        f"开始多步骤任务之前,先使用todo_write规划步骤,执行过程之中及时更新状态"
        f"遇到复杂子问题的时候,使用spawn_subagent工具派生子agent"
    ),
    "workspace": f"工作目录是:{WORKDIR}",
    "skill": "需要完整的技术说明的时候,使用load_skill加载相关的文档"
}


def _assemble_system_prompt_(skills: str) -> str:
    sections = [PROMPT_SECTIONS["identity"], PROMPT_SECTIONS["workspace"]]
    if skills:
        sections.append(f"可用的技能：\n{skills}")
        sections.append(PROMPT_SECTIONS["skill"])
    return "\n\n".join(sections)

def _skills_text_():
    if not SKILL_REGISTRY:
        return ""

    # 便利技能注册表，为每一项技能生成md得列表条目，并且拼接返回
    return "\n".join(
        f"- **{skill['name']}**: {skill['description']}" for skill in SKILL_REGISTRY.values()
    )

# 系统提示词
def get_system_prompt() -> str:
    # return PROMPT_SECTIONS["identity"]
    return _assemble_system_prompt_(_skills_text_())


# 定义子agent的系统提示词
SUB_SYSTEM = {
    # 一个多行的字符串
    "identity": (
        f"你是一个位于{WORKDIR}目录之中的编程的Agent，直接行动，不要解释"
        f"你将在需要使用命令的情况下使用Windows CMD环境下执行任务，使用CMD完成任务"
        f"完成分配给你的任务，然后返回简洁摘要，不要继续委派"
    )
}
