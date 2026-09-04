from pathlib import Path


# 当前的工作目录
WORKDIR = Path.cwd()



# 设置技能目录是工作目录下面的skills的目录
SKILLS_DIR = WORKDIR / "skills"


# print(SKILLS_DIR)

for dir in sorted(SKILLS_DIR.iterdir()):
    print(dir)





# 使用乱码符号来防止这个程序崩溃
content = (WORKDIR / "text.md").read_text(encoding="utf-8", errors="replace")
print(content)


SKILL_REGISTRY = {}

if not SKILL_REGISTRY:
    print("30")