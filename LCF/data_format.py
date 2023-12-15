import json
from sklearn.model_selection import train_test_split
import os
import re

def convert_to_dat(json_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as output:
        for group in json_data:
            content = group['content']
            annotations = group['annotations']

            # 使用正则表达式删除所有空白字符
            content_without_space = re.sub(r'\s', '', content)

            # 初始化标签序列，默认为"O" (negative)
            labels = ['O'] * len(content_without_space)

            # 将positive标签应用到标签序列
            for annotation in annotations:
                start = annotation['start']
                end = annotation['end']
                tag = annotation['tag']

                # 获取替换空格后的位置
                start_without_space = content_without_space.find(content[start:end])
                end_without_space = start_without_space + (end - start)

                labels[start_without_space:end_without_space] = ['B-' + tag] + ['I-' + tag] * (end_without_space - start_without_space - 1)

            # 写入.dat文件
            for char, label in zip(content_without_space, labels):
                output.write(f'{char} {label} {label_to_id(label)}\n')

            # 句子之间用空行隔开
            output.write('\n')


def label_to_id(label):
    if label == 'O':
        return '-1'  # neutral
    elif label.startswith('B'):
        return '2'  # positive
    elif label.startswith('I'):
        return '2'  # positive
    else:
        return '0'  # negative


def process_and_merge_data(folder_path):
    all_data = []

    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                all_data.extend(json_data)

    return all_data


# folder_path = './atepc_datasets/ours/'
folder_path = 'D:\test_proj\ATEPC\LCF\atepc_datasets\ours'
all_json_data = process_and_merge_data(folder_path)

train_data, test_data = train_test_split(all_json_data, test_size=0.2, random_state=42)

convert_to_dat(train_data, 'train.dat')
convert_to_dat(test_data, 'test.dat')
