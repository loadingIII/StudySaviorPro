from agent.agent import agent_stream
from schemas.agent_schemas import AgentQuestion
import asyncio


if __name__ == "__main__":

    async def main():
        question = "请介绍一下人工智能的历史发展？"
        data = AgentQuestion(question=question, session_id=1)

        async for chunk in agent_stream(data):
            print(chunk, end="")

    asyncio.run(main())