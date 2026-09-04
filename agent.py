


import json

from config import DEFAULT_MAX_TOKENS, MODEL_ID

from prompt import get_system_prompt

from llm import call_llm

from utils import assistant_message_dict

from tools.executor import execute_tool

from permission import check_permission


from hooks import trigger_hooks



# 定义变量，用于记录上次todo_write调用以来的
# while true 走的次数
rounds_since_todo = 0

def agent_loop(messages: list):
    # 声明这个是全局变量
    global rounds_since_todo
    # 将最大的tokens数量设置为默认的值8000，未来这个值可能会变化
    max_tokens = DEFAULT_MAX_TOKENS
    # 把模型先设置为这个默认模型，未来如果这个默认模型不能使用的话，就可以切换为备用的模型
    model = MODEL_ID
    while True:
        # 1、获取系统的提示词
        system = get_system_prompt()
        # print("system", system)
        # every这个3lun 提示一次，更新下列表哈
        if rounds_since_todo >= 3 and messages:
            # 初始有一个计划，然后这个没事这个提示一下进度
            messages.append({
                "role": "user",
                "content": "<reminder>请及时更新你的todo列表</reminder>"
            })
            print(f"\x1b[33m 请更新你的todo列表 \x1b[0m ")
            rounds_since_todo = 0
        # 2、调用大模型
        response = call_llm(system, messages, max_tokens, model)
        choice = response.choices[0]
        # 3、获取输出的信息
        assistant = choice.message
        # 4、放入这个messages里面
        messages.append(assistant_message_dict(assistant))

        # 每一轮调用加1
        rounds_since_todo += 1

        # 5、如果助手没有工具的调用，那么就会终止循环
        if not assistant.tool_calls:
            # 调用这个trigger_hooks 触发名字是stop的钩子 传入当前的消息列表
            force = trigger_hooks("Stop", messages)
            if force:
                # 说明活没干完，说明hook返回这个需要进一步处理的信息
                # 有值得话就作为这个user的消息，来进一步这个处理
                messages.append({
                    "role": "user",
                    "content": force
                })
                # 重新进入这个agent loop的流程
                continue
            return
        # 6、助手需要调用工具，那么就是循环所有的工具的调用
        for tool_call in assistant.tool_calls:
            # 获取工具的名称
            name = tool_call.function.name
            # 获取参数
            print(tool_call)
            args = json.loads(tool_call.function.arguments or '{}')
            # print(f"\x1b[36m {name}{json.dumps(args, ensure_ascii=False)} \x1b[0m")
            # 进行权限的检查操作，对工具调用进行权限检查
            # reason = check_permission(name, args)

            # if reason is not None:
            #     # 如果没有通过权限检查，将权限被拒绝的原因信息添加到消息列表之中
            #     messages.append({
            #         "role": "tool", # 角色是工具
            #         "content": reason + ".", # 拒绝的原因
            #         "tool_call_id": tool_call.id # 关联的工具id
            #     })
            #     # 如果本次工具调用失败了，那么就会继续调用下一个工具
            #     continue

            # 工具调用前 触发这个PreToolUse 这个hook 返回是否允许工具执行
            blocked = trigger_hooks("PreToolUse", name, args)
            # 只要有一个hook函数返回了这个不是none的值，后面的hook不走了
            if blocked:
                messages.append({
                    "role": "tool", # 角色是工具
                    "content": str(blocked) + ".", # 拒绝的原因
                    "tool_call_id": tool_call.id # 关联的工具id
                })
                continue
            # 执行工具，获取输出的结果
            output = execute_tool(name, args)

            # 触发这个PostToolUse 这个hook进行后置处理
            trigger_hooks("PostToolUse", name, args, output)
            # 如果本地调用的工具就是这个todo_wtite  那么就会重置为0 哈
            if name == "todo_write":
                rounds_since_todo = 0;
            # 需要把结果放入到这个消息列表之中
            messages.append({
                "role": "tool",
                "content": output,
                "tool_call_id": tool_call.id
            })