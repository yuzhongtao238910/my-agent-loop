
# sk-a64a7e20f95e4e10b92b9c15bd42472f



# harness project
## 驾驭大模型的工具 马具
### tool_call 
#### 循环 - 模型与真实世界的第一道连接


## 输出为什么不能无限输出
因为技术和成本的双重原因
1、算力的成本，因为每一个token都需要计算，无限的输出等于GPU的无限制消耗，成本失控
2、工程的稳定性，模型可能会陷入死循环，或者是胡说八道
3、另外在技术层面，llm内部使用的是这个transformer架构，生成是自回归的，一个字一个字的蹦出来，长度越长，计算量是平方级别的增加，效果就会越来越差，幻觉会增加


## harness engineering 驾驭工程
指的是ai智能体设计和构建约束得机制，以及反馈得回路，工程流程得控制，以及持续改进循环得系统工程实践
引导智能体正确的工作


## 一个循环+一个工具 = 一个agent



## 提示词
- 创建一个名为hello.py的文件，内容是打印这个helloworld
- 列出当前目录下面的所有的python文件
- 当前的这个git分支是什么哈
- uv run ../MY-AGENT-LOOP/main.py
- 查找所有的python文件


## tool_use
- 工具分发映射dispatch(name)
- bash
- read_file
- write_file
- edit_file
- glob


## 权限
- 权限：一种权限台，三种结果，harness将allow ask deny 决策放到了模型之外
- 工具执行之前，需要先做这个权限判断
- check_permission


## 注
- del /q tmp\\*
- /q 指的是这个静默的模式 quiet 不提示这个确认直接删除
- tmp\\* 删除tmp目录下面的所有的文件
- 2026-07-18-04哈

## hooks 挂到循环上，不写入循环内部
- UserPromptSubmit 输入大模型之前的调用 可以注入一些上下文
- PreToolUse 工具使用之前调用 权限检查 以及这个记录日志等等
- PostToolUse handler执行之后，下一轮之前 large_output_hook 
- stop 最终输出之前 例如这个summary_hook 摘要的钩子
- 扩展逻辑挂在外面，循环本身一字不改
- trigger_hooks()
- agent的核心循环本身保持不变
