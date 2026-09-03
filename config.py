




import os

from dotenv import load_dotenv


from openai import OpenAI
from pathlib import Path


# 加载.env文件，放入到环境变量之中
# override 表示如果环境里面之中有重名变量，那么就会覆盖哈
load_dotenv(override=True)

# 从环境变量之中获取模型名称
MODEL_ID = os.environ["MODEL_ID"]

client = OpenAI(
    api_key=os.environ["OPENAI_API_KEY"],
    base_url=os.environ["OPEN_BASE_URL"],
)

# 默认最大的token的数量哈就是8000
# 指的是模型输出得token得上限，也就是生成的内容 一般来说一个汉字等于1~2个token
# 
DEFAULT_MAX_TOKENS = 8000


# 当前的工作目录
WORKDIR = Path.cwd()

# change code page 设置命令行的编码是UTF-8
# UTF-8 对一个的是代码页面编65001 gbk是936
os.system("chcp 65001")


# 设置读写文件时候的编码是utf-8
TEXT_ENCODING="utf-8"


# 设置技能目录是工作目录下面的skills的目录
SKILLS_DIR = WORKDIR / "skills"