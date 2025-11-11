import gradio as gr
import requests
import torch
from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
)

# 指定模型目录路径
model_dir = "bert-base-uncased"

# 从预训练模型目录加载配置、分词器和模型
# AutoConfig: 自动加载模型配置，设置分类任务的标签数量为3
# 加载文件：config.json
# 作用：加载模型配置信息，包括模型架构、标签数量等参数
config = AutoConfig.from_pretrained(model_dir, num_labels=3, finetuning_task="text-classification")
# AutoTokenizer: 自动加载与模型匹配的分词器
# vocab.txt（词汇表文件）
# tokenizer_config.json（分词器配置）
# special_tokens_map.json（特殊标记映射）
tokenizer = AutoTokenizer.from_pretrained(model_dir)
# AutoModelForSequenceClassification: 自动加载用于序列分类的预训练模型
# 加载文件：pytorch_model.bin 或 model.safetensors
# 作用：加载预训练模型的权重参数，用于实际的推理任务
model = AutoModelForSequenceClassification.from_pretrained(model_dir, config=config)


def inference(input_text):
    """
    推理函数：对输入文本进行分类预测

    Args:
        input_text (str): 待分类的输入文本

    Returns:
        str: 预测的类别标签
    """
    # 使用分词器对输入文本进行编码
    # batch_encode_plus: 批量编码文本
    inputs = tokenizer.batch_encode_plus(
        [input_text],
        max_length=512,  # 最大序列长度为512
        truncation=True,  # 超长部分截断
        padding="max_length",  # 使用最大长度填充（替换pad_to_max_length）
        return_tensors="pt",  # 返回PyTorch张量格式
    )

    # 禁用梯度计算（推理阶段不需要计算梯度）
    with torch.no_grad():
        # 将编码后的输入传入模型，获取预测logits
        logits = model(**inputs).logits

    # 获取预测概率最高的类别ID
    predicted_class_id = logits.argmax().item()
    # 将类别ID转换为对应的标签名称
    output = model.config.id2label[predicted_class_id]
    return output



# 创建Gradio界面
demo = gr.Interface(
    # 指定处理函数
    fn=inference,
    # 输入组件：文本框
    inputs=gr.Textbox(label="Input Text", scale=2, container=False),
    # 输出组件：文本框
    outputs=gr.Textbox(label="Output Label"),
    # 示例输入数据
    examples=[
        ["My last two weather pics from the storm on August 2nd. People packed up real fast after the temp dropped and winds picked up.",
         1],
        ["Lying Clinton sinking! Donald Trump singing: Let's Make America Great Again!", 0],
    ],
    # 界面标题
    title="Tutorial: BERT-based Text Classificatioin",
)

# 启动Gradio应用，debug=True启用调试模式
demo.launch(debug=True)
