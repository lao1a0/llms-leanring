# 安装依赖库（如果尚未安装）
# pip install gguf

from gguf import GGUFReader

# 替换为你的模型文件路径
gguf_path = r"C:\Users\  \.ollama\models\blobs\sha256-8aacb627728edd476403129a889e01aa2b03bb1a7fc2f719105c84f920fe8a87"

# 加载模型
reader = GGUFReader(gguf_path)

# 打印元信息字段
print("🔍 GGUF 文件元信息：\n")
for key, field in reader.fields.items():
    try:
        # 尝试读取字段值（通常是 numpy 数组）
        value = field.parts[0].tolist() if hasattr(field.parts[0], 'tolist') else field.parts[0]
        print(f"{key}: {value}")
    except Exception as e:
        print(f"{key}: <无法解析> ({e})")

print("\n📦 模型张量信息：")
for tensor in reader.tensors:
    print(f"{tensor.name} | 类型: {tensor.tensor_type.name} | 形状: {tensor.shape.tolist()}")

