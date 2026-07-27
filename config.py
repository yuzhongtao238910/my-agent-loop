




import os

from dotenv import load_dotenv


from openai import OpenAI



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
DEFAULT_MAX_TOKENS = 8000