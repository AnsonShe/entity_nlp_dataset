import os
import argparse

from ATEPC.LEBERT.sty import function
from ATEPC.LCF.sty1 import functionLCF
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import History,Result
from .serializers import HistorySerializer,ResultSerializer



# 获取历史记录
class historyListView(APIView):
    def get(self,request):
        histories_list = History.objects.all()
        histories = HistorySerializer(instance=histories_list,many=True)

        return Response(histories.data)

# 输入
class lcfCreateView(APIView):
    def get(self,request):
        result_list = Result.objects.all()
        result = ResultSerializer(instance=result_list,many=True)
        original_data = result.data
        # 创建一个用于存储转换结果的字典
        return Response(original_data)

    def post(self,request):
        # 添加至历史
        # input = HistorySerializer(data=request.data)
        input_text = request.data
        # history = History.objects.create(text=input_text['text'])
        result = functionLCF(input_text['text'])
        # print(result)
        words_list = [res[0] for res in result]
        labels_list = [res[1] for res in result]
        # print(f'wl:${words_list}')
        # print(f'll:${labels_list}')
        words = ','.join(words_list)
        # print(words)
        labels = ','.join(labels_list)
        # print(labels)
        # result = Result.objects.create(word=words, label_group=labels)
        res_serializer = ResultSerializer(data={'word':words,'label_group':labels})
        if res_serializer.is_valid():
            res_serializer.save()
            return Response(res_serializer.data)
        else:
            return Response(res_serializer.errors)
        # return Response('ok')
# 输入
class lebertCreateView(APIView):
    def get(self,request):
        result_list = Result.objects.all()
        result = ResultSerializer(instance=result_list,many=True)
        original_data = result.data
        # 创建一个用于存储转换结果的字典
        return Response(original_data)

    def post(self,request):
        # 添加至历史
        # input = HistorySerializer(data=request.data)
        input_text = request.data
        history = History.objects.create(text=input_text['text'])
        # 调用AI模型
        result = function(input_text['text'])
        # print(result)
        words_list = [res[0] for res in result]
        labels_list = [res[1] for res in result]
        words = ','.join(words_list)
        labels = ','.join(labels_list)
        # result = Result.objects.create(word=words, label_group=labels)
        res_serializer = ResultSerializer(data={'word':words,'label_group':labels})
        # 测试
        # word_data = "国务院台办,朱凤莲,台东县,海关总署,台湾,台湾,大陆"
        # label_data = "ORG,PER,LOC,ORG,LOC,LOC,LOC"
        if res_serializer.is_valid():
            res_serializer.save()
            return Response(res_serializer.data)
        else:
            return Response(res_serializer.errors)

"""
    {
        "id": 1,
        "word": "国务院台办,朱凤莲,台东县,海关总署,台湾,台湾,大陆",
        "label_group": "ORG,PER,LOC,ORG,LOC,LOC,LOC"
    }
    =>
    {
      "id":1,
      "word":[{"国务院台办":"ORG"},{"朱凤莲":"PER"},{"台东县":"LOC"},{"海关总署":"ORG"},{"台湾":"LOC"},{"台湾":"LOC"},{"大陆":"LOC"}]
    }
"""

#
# def predict(user_input):
#
#     cmd = r'python D:\lebert\ATEPC\LEBERT-NER-Chinese-master\test.py --text'+user_input
#     print(cmd)
#     output = os.popen(cmd).readlines() # 执行test.py
#     model.interface(string)


