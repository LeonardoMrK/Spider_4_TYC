#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2019/12/16 19:00
# @Description:

#coding=utf-8

import xlwt
import xlrd
import os
from xlutils import copy

content_list = ['公司名：北京课通天下教育科技有限公司', '电话：010-56235410',
                'email：zhangshangling@kttx.cn', '网址：www.kttx.cn']


# str='https://www.tianyancha.com/search?key=%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8'
# # str='https://www.tianyancha.com/search/p2?key=%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8'
#
# url_list=str.split('?')
#
# new_url=url_list[0]+'/p2?'+url_list[1]
# print(new_url)



# def wirte_in_excel(content,line):
#     '''
#     用于将数据写入excel文件中
#     :param content: 要写入的数据，格式为list
#     :param line:写入的行数
#     :return:
#     '''
#
#     myWorkbook = xlwt.Workbook(encoding = 'utf-8')  # 添加工作薄
#     mySheet = myWorkbook.add_sheet('sheet1')  # 添加工作表
#     #style = xlwt.XFStyle()
#     col = 0
#     for each in content:
#         mySheet.write(line, col, each)
#         col += 1
#     myWorkbook.save('1.xls')#只能存为xls格式

# wirte_in_excel(content_list,1)



new_list=[['公司名：北京课通天下教育科技有限公司', '电话：010-56235410', 'email：zhangshangling@kttx.cn', '网址：www.kttx.cn', '地址：北京市海淀区东北旺西路8号中关村软件园8号楼3层327B室', '简介：简介：课通天下是一家专注于企业在线学习应用的研究开发机构， 致力于为培训行业提供云服务，中国唯一只服务培训机构e转型组织。 我们以“让好课通天下”为使命，通过为培训机构 提供OMO智能学习平台、内容服务、机构运营等三大支持 助推广大培训机构实现转型升级。', '经营范围：技术开发、技术推广、技术转让、技术咨询、技术服务；软件开发；销售计算机、软件及辅助设备；组织文化艺术交流活动（不含营业性演出）；经济贸易咨询；企业管理。（企业依法自主选择经营项目，开展经营活动；依法须经批准的项目，经相关部门批准后依批准的内容开展经营活动；不得从事本市产业政策禁止和限制类项目的经营活动。）'],['公司名：西安擎远时代教育科技有限公司', '电话：18792721217', 'email：xaqy029@sina.com','1', '网址：www.x-racetrack.com', '地址：陕西省西安市国家民用航天产业基地东长安街501号运维国际总部大厦B座903-003室',  '简介：简介：西安擎远时代教育科技有限公司是一家为教培市场搭建信息交互、资源整合、数据分析的共享平台，提供专业教培策划与咨询的服务型机构。', '经营范围：教学产品、教育软件、互联网软件的开发、销售与技术服务；玩具的开发、技术咨询；图书、报刊、电子出版物、工艺礼品、文体用品及器材、教学用具、玩具的销售；企业营销策划；会务服务；展览展示服务；文化交流活动的组织、策划（不含演出）。（依法须经批准的项目，经相关部门批准后方可开展经营活动）']]

def wirte_in_excel(content):

    book = xlrd.open_workbook('D:\\project\\pycharmworkspace\\clawer_TYC\\1.xlsx')
    new_book = copy.copy(book)  # 复制一个book
    sheet = new_book.get_sheet(0)  # 获取sheet1页

    # myWorkbook = xlwt.Workbook(encoding = 'utf-8')#添加工作薄
    # mySheet = myWorkbook.add_sheet('Sheet1')#添加工作表

    line = 0
    for each in content:
        if len(each)!=7:#剔除格式问题的信息
            print('有格式问题:',each)
        else:
            col = 0
            for each_ele in each:
                new_each = each_ele.split("：")[1]  # 切分只留下内容信息
                print(new_each)
                sheet.write(line, col, new_each)
                col += 1
            line += 1
    new_book.save('1.xls')



os.system('pause')
print(len(new_list[1]))
wirte_in_excel(new_list)