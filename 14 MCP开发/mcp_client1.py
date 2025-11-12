import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 为 stdio 连接创建服务器参数
server_params = StdioServerParameters(# 服务器执行的命令，这里我们使用 uv 来运行 web_search.py
    command='python', # 运行的参数
    args=['web_search.py'], )


async def main():
    # 创建 stdio 客户端
    async with stdio_client(server_params) as (stdio, write):
        # 创建 ClientSession 对象
        async with ClientSession(stdio, write) as session:
            # 初始化 ClientSession
            await session.initialize()

            # 列出可用的工具
            response = await session.list_tools()
            print(response)

            # 调用工具
            response = await session.call_tool('web_search', {'query': '今天杭州天气'})
            print(response)


if __name__ == '__main__':
    asyncio.run(main())
