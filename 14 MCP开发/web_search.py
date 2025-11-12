import httpx
from mcp.server import FastMCP

# # 初始化 FastMCP 服务器
app = FastMCP('web-search')


@app.tool()
async def web_search(query: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/tools',
            headers={'Authorization': '11bf59d1fa39419fb94c5adfbfd295d6.YPJVVEnUxTGD3kfR'},
            json={
                'tool': 'web-search-pro',
                'messages': [
                    {'role': 'user', 'content': query}
                ],
                'stream': False
            }
        )

        res_data = []
        for choice in response.json()['choices']:
            for message in choice['message']['tool_calls']:
                search_results = message.get('search_result')
                if not search_results:
                    continue
                for result in search_results:
                    res_data.append(result['content'])

        return '\n\n\n'.join(res_data)


if __name__ == "__main__":
    app.run(transport='stdio')
