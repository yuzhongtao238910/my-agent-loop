





# 工具函数，可以把pydantic类型的大模型的回复的消息对象转换为字典
def assistant_message_dict(message) -> dict:
    # model_dump 可以把这个对象转换为字典，排除为none
    data = message.model_dump(exclude_none=True)
    # 角色的类型设置为助手
    data["role"] = "assistant"
    return data