from agent.llms.llms import query_llm


def generate_queries(original_query, num_queries=3):
    prompt = (f"""
    你是一位精通信息检索和语义分析的专家助手。你的任务是将用户的单个复杂问题，拆解并重构为多个不同视角的独立查询语句。
    针对用户输入的问题，生成{num_queries}个不同版本的查询语句。这些查询语句应涵盖原问题的不同侧面、同义表达、具体化场景或潜在的隐含需求，以便检索系统能获取最全面的相关信息。
    # Constraints
    1. **多样性**：每个查询必须有明显的区别。
    2. **独立性**：每个查询都必须是完整的句子，不依赖上下文即可被搜索引擎理解。
    3. **准确性**：所有查询必须紧密围绕用户的核心意图，不能偏离主题。
    5. **格式**：仅输出查询列表，不要包含任何解释、前言或后缀。
    # Workflow
    1. 分析用户问题的核心意图和关键实体。
    2. 思考用户可能关心的不同维度（如：是什么、怎么做、优缺点、最新趋势、具体案例等）。
    3. 基于不同维度重写问题，形成{num_queries}个查询。
    4. 输出最终列表。
    # User Input
    {original_query}

# Output Format (Example)
    ####(在下一个"####"之前的内容为样例输出)
    
    "代码性能优化技巧"\n
    "提升程序运行速度的方法"\n
    "如何让代码跑得更快"\n
    "代码执行效率优化最佳实践"
    ####

# Execution
请针对上述用户输入生成多版本查询：
    """)

    response = query_llm.invoke(prompt)

    # 假设模型返回的格式是一个列表字符串，我们需要解析它
    generated_queries = response.content.strip().split('\n')
    # 将空元素过滤掉
    generated_queries = [query.strip('"') for query in generated_queries if query.strip()]
    return generated_queries


if __name__ == "__main__":
    original_query = "如何提高RAG执行效率？"
    # LLM生成多个查询
    multi_queries = generate_queries(original_query, num_queries=4)
