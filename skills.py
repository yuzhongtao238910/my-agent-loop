

"""
启动的时候扫描目录
"""

from config import SKILLS_DIR, TEXT_ENCODING

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



_scan_skills()