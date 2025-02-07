from modelscope import snapshot_download
from swift.llm import (
    DatasetName,
    ModelType,
    SftArguments,
    Swift,
    get_model_tokenizer,
    get_template,
    register_model,
)
import torch

# 硬件配置
device_map = "auto"
load_in_4bit = True  # 必须开启4bit量化
use_flash_attn = True  # 开启Flash Attention

# 下载模型（Qwen1.5-7B-Chat 4bit量化版）
model_type = ModelType.qwen1half_7b_chat_awq
model_dir = snapshot_download(
    "qwen/Qwen1.5-7B-Chat-AWQ", revision="qwen1.5-7b-chat-awq"
)

# 注册自定义模型
register_model(
    model_type,
    "qwen/Qwen1.5-7B-Chat-AWQ",
    template_type="qwen",
    ignore_file_pattern=[r".+\.bin$"],  # 忽略原始bin文件
)

# 训练参数配置
sft_args = SftArguments(
    model_type=model_type,
    model_id_or_path=model_dir,
    # 数据配置
    dataset=["your-converted-data-dir", 0.1],  # 使用10%数据做验证
    dataset_test_ratio=0.1,
    # 训练参数
    output_dir="output",
    num_train_epochs=3,
    learning_rate=1e-4,
    max_length=2048,
    gradient_checkpointing=True,
    logging_steps=10,
    save_steps=500,
    # 硬件优化参数
    batch_size=1,  # 根据显存调整
    gradient_accumulation_steps=8,
    use_flash_attn=use_flash_attn,
    load_in_4bit=load_in_4bit,
    device_map=device_map,
    # LoRA配置
    lora_target_modules=["ALL"],
    lora_rank=64,
    lora_alpha=32,
)


def main():
    # 初始化模型
    model, tokenizer = get_model_tokenizer(
        sft_args.model_type,
        torch_dtype=torch.float16,
        device_map=device_map,
        model_id_or_path=sft_args.model_id_or_path,
    )

    # 配置模板
    template = get_template(
        sft_args.template_type,
        tokenizer,
        sft_args.max_length,
        sft_args.truncation_strategy,
    )

    # 开始训练
    trainer = Swift.train(
        model=model,
        args=sft_args,
        tokenizer=tokenizer,
        template=template,
    )

    # 保存最终模型
    trainer.save_model(sft_args.output_dir)
    tokenizer.save_pretrained(sft_args.output_dir)


if __name__ == "__main__":
    main()
