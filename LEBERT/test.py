import torch
from models.ner_model import LEBertSoftmaxForNer
from os.path import join
from transformers import BertTokenizer, BertConfig
from torch.utils.data import DataLoader
from processors.processor import LEBertProcessor
import os
import json
from train import set_train_args, seed_everything

os.environ["CUDA_VISIBLE_DEVICES"] = "1"
device = "cpu"

pretrained_model_path = "./output/ours1/lebert-softmax/bert-base/load_word_embed/"
pretrained = '../pretrained/bert-base-chinese'


args = set_train_args()
seed_everything(args.seed)
args.device = torch.device("cuda:1" if torch.cuda.is_available() and args.device == 'gpu' else "cpu")

pretrain_model = 'bert-base'
args.output_path = join(args.output_path, args.dataset_name, args.model_class, pretrain_model, 'load_word_embed' if args.load_word_embed else 'not_load_word_embed')
args.train_file = join(args.data_path, 'train.json')
args.dev_file = join(args.data_path, 'dev.json')
args.test_file = join(args.data_path, 'test.json')
args.pred_file = join(args.data_path, 'pred.json')
args.label_path = join(args.data_path, 'labels.txt')


tokenizer = BertTokenizer.from_pretrained(pretrained, do_lower_case=True)
processor = LEBertProcessor(args, tokenizer)
args.id2label = processor.label_vocab.idx2token
args.ignore_index = processor.label_vocab.convert_token_to_id('[PAD]')

config = BertConfig.from_pretrained(args.pretrained_model_path)
config.num_labels = processor.label_vocab.size
config.loss_type = args.loss_type
config.add_layer = 1
config.word_vocab_size = processor.word_embedding.shape[0]
config.word_embed_dim = processor.word_embedding.shape[1]

model = LEBertSoftmaxForNer.from_pretrained(pretrained_model_path, config=config).to(device)
model.eval()

label_mapping = {
    1: "O",
    2: "B-positive",
    3: "B-negative",
    4: "B-neutral",
    5: "I-positive",
    6: "I-negative",
    7: "I-neutral",
}

def convert_to_labels(predictions, label_mapping):
    return [label_mapping[prediction] for prediction in predictions]


def convert_to_entities_and_emotions(label_sequence, tokens):
    current_entity = ""
    current_emotion = ""
    result = []

    for label, token in zip(label_sequence, tokens):
        label_type, label_emotion = label.split('-') if '-' in label else (label, None)

        # 处理B标签
        if label_type.startswith('B'):
            if current_entity:
                result.append((current_entity, current_emotion))
            current_entity = token
            current_emotion = label_emotion

        # 处理I标签
        elif label_type.startswith('I'):
            current_entity += token

    # 处理最后一个实体
    if current_entity:
        result.append((current_entity, current_emotion))

    return result


def modify(input_list):
    modified_list = input_list.copy()

    i_start = None
    for i in range(len(modified_list)):
        if modified_list[i].startswith('I-'):
            i_start = i
        elif modified_list[i] == 'O' and i_start is not None:
            if i + 1 < len(modified_list) and modified_list[i + 1].startswith('I-'):
                i_end = i
                for j in range(i_start, i_end + 1):
                    modified_list[j] = modified_list[i_start]

    return modified_list

while True:
    user_input = input("请输入一句话：")
    tokens = list(user_input)
    length = len(tokens)
    data = {"text": tokens, "label": ["O"] * len(tokens)}
    with open("./datasets/ner_data/ner_data/ours1/pred.json", "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, ensure_ascii=False)

    pred_dataset = processor.get_pred_data()
    pred_dataloader = DataLoader(pred_dataset, 1, shuffle=False, num_workers=0)
    with torch.no_grad():
        for data in pred_dataloader:
            input_ids = data['input_ids'].to(device)
            token_type_ids = data['token_type_ids'].to(device)
            attention_mask = data['attention_mask'].to(device)
            word_ids = data['word_ids'].to(device)
            word_mask = data['word_mask'].to(device)
            label_ids = data['label_ids'].to(device)
            loss, logits = model(input_ids, attention_mask, token_type_ids, word_ids, word_mask, processor.label_vocab.convert_token_to_id('[PAD]'), label_ids)
            preds = torch.argmax(logits, dim=2)[:, 1:].tolist()
            label_sequence = convert_to_labels(preds[0], label_mapping)[:length]
            label_sequence_1 = modify(label_sequence)
            result = convert_to_entities_and_emotions(label_sequence_1, tokens)

            for entity, emotion in result:
                print(f"{entity}:{emotion}")

