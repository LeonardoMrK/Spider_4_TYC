#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2020/1/3 12:19
# @Description:

#统计list中出现的元素个数
#参考：https://www.zybang.com/question/2fa278ce7f89fb437759d57ab4b20594.html
# numbers=["cc","cc","ct","ct","ac"]
# res = {}
# for i in numbers:
#     res[i] = res.get(i, 0) + 1
# print([k for k in res.keys()])
# print([v for v in res.values()])





#返回list中指定元素的所有索引
# a=["cc","cc","ct","ct","ac"]
# print([i for i,x in enumerate(a) if x=='cc'])



#统计list中出现的元素个数并获取其索引
#参考https://www.jianshu.com/p/c107f3d3c6ba
from collections import defaultdict
a=["cc","cc","ct","ct","ac"]
#a=[1,2,3,1,2,3]
d = defaultdict(list)
for i, v in enumerate(a):
    d[v].append(i)
print(d)
