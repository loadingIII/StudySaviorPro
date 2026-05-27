# sub_agents 包导出
# 使用懒加载避免循环导入和 async 连接池在非异步上下文中初始化


def __getattr__(name):
    if name == "create_supervisor" or name == "get_sub_agent_tools":
        from agent.sub_agents.supervisor import create_supervisor, get_sub_agent_tools
        return {"create_supervisor": create_supervisor, "get_sub_agent_tools": get_sub_agent_tools}[name]
    if name == "question_agent":
        from agent.sub_agents.question_agent import question_agent
        return question_agent
    if name == "context_agent":
        from agent.sub_agents.context_agent import context_agent
        return context_agent
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
