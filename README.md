
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



## hook钩子函数
- 读取readme文件


## todowrite
- 可以在这个给他一个复杂任务，todowrite 先列一个计划清单，然后再这个
- 待办事项
- 进行之中
- 完成
- todowrite给模型一份可见的计划，
- 做着做着提示词的作用越来越小
- Nag Reminder 催促更新机制 
- todo_write本身不做任何这个机制
- 连续几轮没有调用这个todo_write就会添加这个提醒哈
- 拆分为这个todolist 每次完成一项就会打一个对勾哈
- 重构这个examples/hello.py这个文件，添加类型注解、文档字符串和这个main函数的保护,先列出3个步骤,然后每个步骤分别执行


## subagent
- 子agent哈
- agent已经有了这个计划，但是如果有一个任务太大了，假如说是重构整个这个认证的这个模块，光靠这个todo还是不太够
- 放到一个对话里面会被上下文淹没
- subagent就是把大任务拆分为小任务
- 大任务拆小，子进程有独立得上下文
- 给每个子任务干净得消息历史，同时保留主线程
- 父进程获得干净得summary，没有上下文膨胀
- eg: agent在修复bug
    - 会新开一个终端来追踪调用链，agent这个能力就是新开一个独立的子进程，给他一个消息列表，让他专心做一件事
- task-spawn subagent 全新的上下文 权限
    - 自己得while循环，最多30轮，不能递归创建这个spawn，工具会少很多
    - 最终只提取最后得结论，摘要文本，返回给parent
    - 子agent得工具比较受限，bash/read/write/edit/glob,但是没有task
    - 子agent得调用还是会经过permission
    - spawn 派生一个子进程
    - 同步得 只返回最终得结论
- agent teams 异步得
- 提示词：用户请求可以隔离得探索性工作，不要污染上下文
    - 父亲agent不会携带所有得细节
    - 使用子任务查找本项目安装了哪些第3方模块
- 核心：节约主agent这个上下文de长度，就是messages得数量
