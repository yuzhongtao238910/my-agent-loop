from pathlib import Path

"""
msg1 = (
    "hello",
    "world"
)
msg2 = (
    "hello"
    "world"
)
print(msg1)
print(msg2)
print("rm -rf" in "rm -rf")
"""
import sys
import os



# bytes bytes[]
# bytes 是一个单个的字节序列，有点像字符串 使用的是连续的内存 可以存图片文件 是不能编辑的
# bytes[] 多个独立的bytes的对象哈

img_data: bytes= b"\xff\xd8"

# print(img_data, type(img_data), img_data.decode(encoding="gbk"))

# chunks = list[bytes] = []

sys.stdout.write("stdout")
sys.stderr.write("stderr")
sys.stdout.write("stdout")
sys.stderr.write("stderr")



WORKDIR = Path.cwd()


# 不安全：绝对路径
p3 = "/tmp/upload.exe"
p4 = "C:\\Users\\EDY\\Desktop"
path3 = (WORKDIR / p3).resolve()  # /tmp/upload.exe ❌

print(path3, "46")


path4 = (WORKDIR / p4).resolve()  # /tmp/upload.exe ❌

print(path4, "51")