# 调用sty的一个函数
import string

# from LEBERT.sty import function
#
# result = function("国务院台办发言人朱凤莲12月8日表示，新一批台东县番荔枝包装厂和果园已通过海关总署注册登记，随着台湾地区番荔枝产季来临，将为台湾地区番荔枝输入大陆创造有利条件。")
# print(result)


from LCF.sty1 import functionLCF
result = functionLCF("国务院台办发言人朱凤莲12月8日表示，新一批台东县番荔枝包装厂和果园已通过海关总署注册登记，随着台湾地区番荔枝产季来临，将为台湾地区番荔枝输入大陆创造有利条件。")
print(result)


# result = result.split('\n')
# # print(result)
# output=[]
# list = []
# for i in result:
#     # result = result.split(': ')
#     words = str(i)
#     words = words.split('：')
#     # print(words)
#     words = tuple(words)
#     list.append(words)
# list.pop()
# print(list)

