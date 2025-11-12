## 🔥 基于 EmbeddingGemma 的智能 RAG 应用

这个 Streamlit 应用展示了一个智能的检索增强生成（RAG）代理，使用 Google 的 EmbeddingGemma 进行嵌入，Llama 3.2 作为语言模型，全部通过 Ollama 本地运行。

> 如果只有 4 GB 内存，可以把 Llama 3.2 换成 1B 版（`ollama pull llama3.2:1b`），内存占用降到 1.3 GB 左右，仍能正常工作。

### 功能特点

- **本地 AI 模型**：使用 EmbeddingGemma 生成向量嵌入，Llama 3.2 进行文本生成
- **PDF 知识库**：动态添加 PDF 链接以构建知识库
- **向量搜索**：使用 LanceDB 进行高效的相似性搜索
- **交互式界面**：美观的 Streamlit 界面，用于添加源和查询
- **流式响应**：实时响应生成，可查看工具调用过程

### 如何开始？

1. 克隆 GitHub 仓库
```bash
git clone https://github.com/Shubhamsaboo/awesome-llm-apps.git 
cd awesome-llm-apps/rag_tutorials/agentic_rag_embedding_gemma
```

2. 安装所需依赖：
```bash
pip install -r requirements.txt
```

3. 确保 Ollama 已安装并运行，且包含所需模型：
   - 拉取模型：`ollama pull embeddinggemma:latest` 和 `ollama pull llama3.2:latest`
   - 如果 Ollama 服务器未运行，请启动它

4. 运行 Streamlit 应用：
```bash
streamlit run agentic_rag_embeddinggemma.py
```
   （注意：应用文件位于根目录）

5. 打开网络浏览器，访问提供的 URL（通常是 http://localhost:8501）与 RAG 代理进行交互。

### 工作原理？

1. **知识库设置**：在侧边栏中添加 PDF 链接以加载和索引文档。
2. **嵌入生成**：EmbeddingGemma 创建用于语义搜索的向量嵌入。
3. **查询处理**：用户查询被嵌入并与知识库进行搜索。
4. **响应生成**：Llama 3.2 根据检索到的上下文生成答案。
5. **工具集成**：代理使用搜索工具获取相关信息。

### 系统要求

- Python 3.8+
- 已安装并运行的 Ollama
- 所需模型：`embeddinggemma:latest`，`llama3.2:latest`

### 使用的技术

- **Agno**：构建 AI 代理的框架
- **Streamlit**：网络应用框架
- **LanceDB**：向量数据库
- **Ollama**：本地 LLM 服务器
- **EmbeddingGemma**：Google 的嵌入模型
- **Llama 3.2**：Meta 的语言模型