
from agent import agent_loop

def main():
    print("输入问题，回车发送，输入q退出提问。\n")

    # 初始化历史消息列表
    history = []
    # 进入无限循环，不断接收用户的输入
    while True:
        try:
            # 获取用户的输入，带有提示符号
            query = input("\x1b[36m >> \x1b[0m")
        except (EOFError, KeyboardInterrupt):
            # 异常的时候退出循环
            break;
        # 如果输入的内容是空的，或者是 q quit exit 就会推出哈
        if query.strip().lower() in ("q", "quit", "exit", ""):
            break;
        history.append({
            "role": "user",
            "content": query
        })
        # 调用代理循环处理历史消息
        agent_loop(history)
        # 获取历史记录之中最后一条消息
        final = history[-1]
        # 如果最后一条消息是助手的回复，并且有内容输出
        if final.get("role") == "assistant" and final.get("content"):
            print(final["content"])
        


if __name__ == "__main__":
    main()