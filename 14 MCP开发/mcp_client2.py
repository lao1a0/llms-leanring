import asyncio
import json
import os
from contextlib import AsyncExitStack
from typing import Optional

from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI

load_dotenv()


class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()

        # 1. 设置端点与密钥
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"), base_url=os.getenv("OPENAI_BASE_URL"),
            # https://api.moonshot.cn/v1
        )

    async def connect_to_server(self):
        server_params = StdioServerParameters(command="python", args=["web_search.py"], env=None, )
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        stdio, write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(stdio, write))
        await self.session.initialize()

    async def process_query(self, query: str) -> str:
        # 2. 设置系统提示词
        system_prompt = ("你是一个乐于助人的助手。"
                         "你具备在线搜索的功能。"
                         "在回答之前，请务必调用 web_search 工具来搜索互联网上的内容。"
                         "在进行搜索时，请不要遗漏用户问题中的信息，"
                         "并尽可能保持问题内容的完整性。"
                         "当用户的问题中涉及日期相关的内容时，"
                         "请直接使用搜索功能进行查询，并禁止插入具体的时间。")

        messages = [{"role": "system", "content": system_prompt}, {"role": "user", "content": query}, ]

        # 获取 MCP 工具列表
        response = await self.session.list_tools()
        available_tools = [{"type": "function",
            "function": {"name": tool.name, "description": tool.description, "input_schema": tool.inputSchema, }} for
            tool in response.tools]

        # 3. 请求 Kimi 模型（模型名从环境变量读取）
        response = self.client.chat.completions.create(model=os.getenv("OPENAI_MODEL"),  # moonshot-v1-8k / 32k / 128k
            messages=messages, tools=available_tools, )

        content = response.choices[0]
        if content.finish_reason == "tool_calls":
            tool_call = content.message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)

            result = await self.session.call_tool(tool_name, tool_args)
            print(f"\n\n[Calling tool {tool_name} with args {tool_args}]\n\n")

            messages.append(content.message.model_dump())
            messages.append({"role": "tool", "content": result.content[0].text, "tool_call_id": tool_call.id, })

            # 再次请求 Kimi 生成最终回答
            response = self.client.chat.completions.create(model=os.getenv("OPENAI_MODEL"), messages=messages, )
            return response.choices[0].message.content

        return content.message.content

    # 实现循环提问和最后退出后关闭session的操作
    async def chat_loop(self):
        while True:
            try:
                query = input("\nQuery: ").strip()
                if query.lower() == "quit":
                    break
                response = await self.process_query(query)
                print("\n" + response)
            except Exception:
                import traceback
                traceback.print_exc()

    async def cleanup(self):
        await self.exit_stack.aclose()


async def main():
    client = MCPClient()
    try:
        await client.connect_to_server()
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
