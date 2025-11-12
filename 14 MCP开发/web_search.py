with open("api_key.txt", "r") as f:
    api_key = f.read().strip()

# 测试key
# def run_v4_sync():
#     msg = [
#         {
#             "role": "user",
#             "content":"中国队奥运会拿了多少奖牌"
#         }
#     ]
#     tool = "web-search-pro"
#     url = "https://open.bigmodel.cn/api/paas/v4/tools"
#     request_id = str(uuid.uuid4())
#     data = {
#         "request_id": request_id,
#         "tool": tool,
#         "stream": False,
#         "messages": msg
#     }
#
#     resp = requests.post(
#         url,
#         json=data,
#         headers={'Authorization': api_key},
#         timeout=300
#     )
#     print(resp.content.decode())
#
#
#
# if __name__ == '__main__':
#     run_v4_sync()

import httpx
from mcp.server import FastMCP

# # 初始化 FastMCP 服务器
app = FastMCP('web-search')


@app.tool()
async def web_search(query: str) -> str:
    """
    搜索互联网内容

    Args:
        query: 要搜索内容

    Returns:
        搜索结果的总结
    """
    print(api_key)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'https://open.bigmodel.cn/api/paas/v4/tools',
            headers={'Authorization': "92fdeac0062a4c43a4f628f468221bdd.Jgv0olWyZxNast1y"},
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


if __name__ == '__main__':
    app.run(transport='stdio')
