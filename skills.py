

"""
启动的时候扫描目录
"""

from config import SKILLS_DIR, TEXT_ENCODING

from utils import parse_frontmatter

# 定义一个全局字典，用于存放技能信息，key是自字符串，value是字典
SKILL_REGISTRY = {}


# 扫描技能目录下面所有的技能
def _scan_skills():
    # 如果技能目录不存在，那么就会直接返回
    if not SKILLS_DIR.exists():
        return 

    # 循环技能目录下面的所有子目录，按照名称来排序
    for dir in sorted(SKILLS_DIR.iterdir()):
        # 如果不是目录，那么就会跳过哈
        if not dir.is_dir():
            continue
        # 构建描述文件的路径
        manifest = dir / "SKILL.md"
        # 如果描述文件不存在，就会继续跳过
        if not manifest.exists():
            continue

        # 读取文件内容
        # errors
        raw = manifest.read_text(encoding=TEXT_ENCODING, errors="replace")

        # 解析meta数据，获取元信息和正文内容
        meta, _body = parse_frontmatter(raw)

        name = meta.get("name", dir.name)
        description = meta.get("description", _body.split("\n")[0].lstrip("#").strip())

        # 将技能信息存入全局
        SKILL_REGISTRY[name] = {
            "name": name, # 技能得名字
            "description": description, # 技能得描述
            "when_to_use": "", # 先空着
            "content": _body # 技能得正文
        }




_scan_skills()


def run_load_skill(name: str):
    skill = SKILL_REGISTRY.get(name)
    if not skill:
        return f"没有找到技能{name}"

    print(f"\x1b[90m [技能{name}已经加载] {name} \x1b[0m ")
    return skill["content"]