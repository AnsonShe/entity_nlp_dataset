import json
import random

def combine_and_shuffle(files):
    combined_data = []

    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as file:
            original_data = json.load(file)
            combined_data.extend(original_data)

    random.shuffle(combined_data)
    return combined_data

def convert_to_new_format(data):
    new_format_data = []

    for item in data:
        content = item["content"]
        annotations = item["annotations"]

        text = list(content)
        label = ["O"] * len(text)

        for annotation in annotations:
            start = annotation["start"]
            end = annotation["end"]
            tag = annotation["tag"]

            label[start] = f"B-{tag}"
            if start != end:
                label[start + 1: end] = [f"I-{tag}"] * (end - start - 1)

        new_format_item = {"text": text, "label": label}
        new_format_data.append(new_format_item)

    return new_format_data

def split_and_write_files(data):
    total_samples = len(data)
    train_split = int(0.8 * total_samples)
    val_split = int(0.9 * total_samples)

    train_data = data[:train_split]
    val_data = data[train_split:val_split]
    test_data = data[val_split:]

    with open(f"train.json", "w", encoding="utf-8") as train_file:
        for item in train_data:
            json.dump(item, train_file, ensure_ascii=False)
            train_file.write('\n')

    with open(f"dev.json", "w", encoding="utf-8") as val_file:
        for item in val_data:
            json.dump(item, val_file, ensure_ascii=False)
            val_file.write('\n')

    with open(f"test.json", "w", encoding="utf-8") as test_file:
        for item in test_data:
            json.dump(item, test_file, ensure_ascii=False)
            test_file.write('\n')

# 合并多个 JSON 文件
file_paths = ["data/china.json", "data/daily.json", "data/TVB.json", "data/Xinhua.json"]
combined_data = combine_and_shuffle(file_paths)

# 转换格式并写入文件
with open("data/all_combined.json", "w", encoding="utf-8") as combined_file:
    for new_format_item in convert_to_new_format(combined_data):
        json.dump(new_format_item, combined_file, ensure_ascii=False)
        combined_file.write('\n')

# 读取合并后的数据
with open("data/all_combined.json", "r", encoding="utf-8") as combined_file:
    combined_data = [json.loads(line.strip()) for line in combined_file]

# 划分并写入训练集、验证集和测试集
split_and_write_files(combined_data)
