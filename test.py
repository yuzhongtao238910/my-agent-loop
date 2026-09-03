from pathlib import Path


# 当前的工作目录
WORKDIR = Path.cwd()



# 设置技能目录是工作目录下面的skills的目录
SKILLS_DIR = WORKDIR / "skills"


# print(SKILLS_DIR)

for dir in sorted(SKILLS_DIR.iterdir()):
    print(dir)
