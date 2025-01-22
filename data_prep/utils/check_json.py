import json


def print_structure(data, indent=0):
    """
    递归打印 JSON 数据的结构。
    :param data: JSON 数据（字典、列表或其他类型）
    :param indent: 缩进级别，用于格式化输出
    """
    if isinstance(data, dict):
        print(" " * indent + "字典 (dict):")
        for key, value in data.items():
            print(" " * (indent + 2) + f"键: {key}")
            print_structure(value, indent + 4)
    elif isinstance(data, list):
        print(" " * indent + f"列表 (list), 长度: {len(data)}")
        if len(data) > 0:
            print_structure(data[0], indent + 4)
    else:
        print(" " * indent + f"值: {data} (类型: {type(data).__name__})")


with open("atri_raw/b101.ks.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("JSON 文件结构:")
print_structure(data)
