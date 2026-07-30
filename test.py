

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



# bytes bytes[]
# bytes 是一个单个的字节序列，有点像字符串 使用的是连续的内存 可以存图片文件 是不能编辑的
# bytes[] 多个独立的bytes的对象哈

img_data: bytes= b"\xff\xd8"

print(img_data, type(img_data), img_data.decode(encoding="gbk"))