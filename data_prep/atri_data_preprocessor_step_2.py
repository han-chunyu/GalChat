import json
import os
from glob import glob
from collections import defaultdict

# ======================
# 标记为未完成, 有待修改
# ======================


def merge_consecutive_messages(messages):
    """合并连续的同角色消息"""
    merged = []
    current_role = None
    current_content = []

    for msg in messages:
        if msg["role"] == current_role:
            current_content.append(msg["content"])
        else:
            if current_role is not None:
                merged.append(
                    {"role": current_role, "content": "\n".join(current_content)}
                )
            current_role = msg["role"]
            current_content = [msg["content"]]

    if current_role is not None:
        merged.append({"role": current_role, "content": "\n".join(current_content)})

    return merged


def convert_dialogue(chunk_path, output_dir):
    with open(chunk_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    converted = []
    context_stack = []  # 保存历史上下文
    current_system = ""
    current_dialogue = defaultdict(list)

    # 合并连续消息
    merged_messages = merge_consecutive_messages(data["dialogues"])

    for msg in merged_messages:
        if msg["role"] == "system":
            # 系统消息作为长期上下文
            current_system = msg["content"]
            context_stack.append(current_system)
        elif msg["role"] == "user":
            # 用户消息开始新对话
            if current_dialogue:
                # 保存未完成的对话（如只有assistant的情况）
                converted.append(current_dialogue)
                current_dialogue = defaultdict(list)
            current_dialogue["messages"].append(
                {
                    "role": "system",
                    "content": "\n".join(context_stack[-5:]),  # 保留最近5个系统上下文
                }
            )
            current_dialogue["messages"].append(
                {"role": "user", "content": msg["content"]}
            )
        elif msg["role"] == "assistant":
            # 处理多轮assistant回复
            if "assistant" in current_dialogue:
                new_dialogue = {"messages": current_dialogue["messages"][:-1].copy()}
                converted.append(new_dialogue)

            action = msg.get("action", "")
            traits = f"[特质{msg.get('traits','')}]" if "traits" in msg else ""
            processed_content = f"{traits}{action} {msg['content']}".strip()

            current_dialogue["messages"].append(
                {"role": "assistant", "content": processed_content}
            )
            converted.append(current_dialogue.copy())

    if converted:
        base_name = os.path.basename(chunk_path)
        output_path = os.path.join(output_dir, f"converted_{base_name}")
        final_data = []
        for dialogue in converted:
            if len(dialogue["messages"]) >= 3:  # 至少包含system+user+assistant
                final_entry = {
                    "messages": [
                        dialogue["messages"][0],  # system
                        dialogue["messages"][1],  # user
                        dialogue["messages"][2],  # assistant
                    ]
                }
                final_data.append(final_entry)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(final_data, f, ensure_ascii=False, indent=2)
        print(f"Processed {chunk_path} => {output_path} ({len(final_data)} dialogues)")
    else:
        print(f"Skipped {chunk_path} (no valid dialogues)")


input_dir = "data_prep/processed_data/atri_raw_data"
output_dir = "data_prep/converted_data"

os.makedirs(output_dir, exist_ok=True)
for chunk_file in glob(os.path.join(input_dir, "chunk_*.json")):
    convert_dialogue(chunk_file, output_dir)
