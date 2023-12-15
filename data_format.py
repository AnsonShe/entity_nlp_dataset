import json

with open('TVBnews_annotations.json', 'r', encoding='utf-8') as file:
    json_data = json.load(file)

extracted_data = []
for example in json_data.get("examples", []):
    annotations = example.get("annotations", [])

    # 检查是否包含"pass"标签，如果没有则保留该组数据
    if all(annotation.get("tag", "").lower() != "pass" for annotation in annotations):
        extracted_example = {
            "content": example.get("content", ""),
            "annotations": []
        }

        for annotation in annotations:
            extracted_annotation = {
                "end": annotation.get("end", 0),
                "tag": annotation.get("tag", ""),
                "start": annotation.get("start", 0),
                "value": annotation.get("value", "")
            }
            extracted_example["annotations"].append(extracted_annotation)

        extracted_data.append(extracted_example)

with open('data/TVB.json', 'w', encoding='utf-8') as output_file:
    json.dump(extracted_data, output_file, ensure_ascii=False, indent=2)
