import os
from zai import ZhipuAiClient
from mcp.server import FastMCP

app = FastMCP("image_server")

# 初始化智谱客户端（建议使用环境变量管理 APIKey）
with open(r"C:\Users\11257\Documents\dive-into-llms\14 MCP开发\api_key.txt", "r") as f:
    api_key = f.read().strip()
client = ZhipuAiClient(api_key=api_key)

@app.tool()
async def image_generation(image_prompt: str):
    """
    使用智谱 CogView-4 模型生成图像
    :param image_prompt: 中文或英文图像描述
    :return: 图片 URL 或错误信息
    """
    try:
        response = client.images.generations(
            model="cogView-4-250304",
            prompt=image_prompt
        )
        image_url = response.data[0].url
        return image_url or "未能获取图片 URL"
    except Exception as e:
        return f"生成失败：{str(e)}"

if __name__ == "__main__":
    app.run(transport="stdio")
