import json

with open("atri_raw/b101.ks.json", "r", encoding="utf-8") as f:
    data = json.load(f)
extracted_data = []
for scene in data["scenes"]:
    if "texts" in scene:
        for item in scene["texts"]:
            if isinstance(item, list) and len(item) >= 6:
                character_name = item[0]
                dialogue_entries = item[2] if isinstance(item[2], list) else []
                for entry in dialogue_entries:
                    if isinstance(entry, list) and len(entry) >= 3:
                        simplified_chinese_dialogue = entry[2]
                        if simplified_chinese_dialogue:
                            extracted_data.append(
                                {
                                    "character": (
                                        character_name if character_name else "未知角色"
                                    ),
                                    "dialogue": simplified_chinese_dialogue,
                                }
                            )

with open("extracted_dialogue.json", "w", encoding="utf-8") as f:
    json.dump(extracted_data, f, ensure_ascii=False, indent=4)
