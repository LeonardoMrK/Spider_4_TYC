#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2019/12/2 10:14
# @Description: 天眼查爬虫。爬取目标：公司名称，电话，邮箱，网址，地址，简介，经营范围，最后写入至excel
#参考：
#https://www.cnblogs.com/chaihy/p/9540514.html
#https://www.cnblogs.com/jpapplication/p/10295803.html
#coding=utf-8

import os
import re
import sys
import json
import time
import xlrd
import xlwt
import requests
from xlutils import copy
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Iterable
from selenium.webdriver.common.keys import Keys
from config import tyc_url_dic,save_path






class Get_company_info(object):

    def __init__(self,url,user,password):
        """
        初始化driver
        :param url:目标url
        :return:
        """
        self.url=url#入口网址
        self.user=user#用户名
        self.password=password#密码
        self.chrome_diver_path = 'D:\Anaconda2\envs\python3\Lib\site-packages\selenium\webdriver\chrome\chromedriver.exe'  # 驱动地址
        self.browser = webdriver.Chrome(executable_path=self.chrome_diver_path)  # 声明浏览器驱动
        self.browser.get(url)#打开登录页面
        time.sleep(1)#必须延时，否则元素找不完全
        #print(self.browser.page_source)#打印源码
        self.url_dic=tyc_url_dic#从config.py中获取各个元素的url


    def login(self):
        """
        采用账户密码形式登录
        :return:
        """
        #self.browser.find_elements_by_class_name('link-white')[2].click()  # 打开登录框
        self.browser.find_element_by_xpath(self.url_dic['get_login']).click()  # 打开登录框
        time.sleep(1)
        while True:#点击密码登录
            try:
                self.browser.find_element_by_xpath(self.url_dic['login_user_pwd']).click()
                break
            except Exception:
               time.sleep(1)

        self.browser.find_element_by_xpath(self.url_dic['login_user']).send_keys(self.user)#输入手机号码
        self.browser.find_element_by_xpath(self.url_dic['login_pwd']).send_keys(self.password)#输入密码
        self.browser.find_element_by_xpath(self.url_dic['submit']).click()
        print('等待人工操作，完成后按任意键')
        os.system('pause')#程序暂停，等待人工处理
        #time.sleep(6)#等待拼图拖拽验证



    def get_company_info(self,company_name):
        """
        输入关键词搜索，返回公司href列表,自带翻页功能
        :param company_name:
        :return:
        """
        all_information=[]#用来保存所有信息的列表
        input_company_name=self.browser.find_element_by_xpath(self.url_dic['search'])
        input_company_name.click()#选中搜索框
        input_company_name.send_keys(company_name)#输入想查询的公司名称
        time.sleep(1)
        # search_button=self.browser.find_element_by_xpath(self.url_dic['search_button'])
        # search_button.send_keys(Keys.ENTER)
        input_company_name.send_keys(Keys.ENTER)#再页面用按回车进入搜索，用click会出问题


        #获取起始页url
        originPageUrl = self.browser.current_url#起始页url
        print("起始页url为：", originPageUrl)
        #从'search'后拆分，由于搜索采用的是get请求，因此以'?'为分隔将url分成两部分（注意汉字被加密成了16进制）
        #例如网页url格式如下：
        #第1页：https://www.tianyancha.com/search?key=%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8
        #第n页：https://www.tianyancha.com/search/p2?key=%E5%AD%97%E8%8A%82%E8%B7%B3%E5%8A%A8
        url_list = originPageUrl.split('?')#切分第一页url
        # new_url = url_list[0] + '/p2?' + url_list[1]#翻页
        # print('第2页的url为',new_url)


     # 当出现多次人工验证页面时，等待验证
        while(1):
            try:
                flag_str = self.browser.find_element_by_class_name('captcha-title').text#通过找title的方式作为标志
                if flag_str=='天眼查校验':
                    print('等待验证111，完成后按任意键')
                    os.system('pause')  # 程序暂停，等待人工处理
            except:#当不出现二次人工验证时，break，继续向下执行
                break



        #获取上限页码
        try:
            end_page = self.browser.find_element_by_class_name(
                'num.-end').text  # 原classname为num end,空格需要用"."代替，一定要注意用的方法是element，不是elements！
            # print(end_page)#取得带有总页码的str文本
            end_page_num = re.findall('\d{1,}', end_page)[0]  # 取得当前搜索结果的总页码数
            #print(end_page_num)
        except:#有些搜索页码比较小的没有num -end关键词
            print('找不到总共页码')

        end_page_num=7#【测试时为了方便就遍历5页】，实际使用时注释掉这行
        all_page_url=[]#用于储存所有页的容器
        all_page_url.append(originPageUrl)

        # 检测是否出现了人工验证页面,如果出现，则先验证
        try:#当出现验证页面时，try里会无法执行，此时会跳到except中执行【这里有bug，因为跳出可能不是因为页面没出现所致，不如用ifelse实现】
            for page in range(2,int(end_page_num)+1):
                new_url=url_list[0] + '/p'+str(page)+'?' + url_list[1]#翻页
                all_page_url.append(new_url) #当前搜索关键词下的所有页面的url，添加入一个list中
        except:#出现验证页面时（try中代码会出错），此时执行except中的内容
            print('等待验证，完成后按任意键')
            os.system('pause')  # 程序暂停，等待人工处理
            for page in range(2, int(end_page_num) + 1):
                new_url = url_list[0] + '/p' + str(page) + '?' + url_list[1]  # 翻页
                all_page_url.append(new_url)

        #【如果想从第n页开始爬取，则把range中的起始值改为n-1】
        for i in range(5,len(all_page_url)):#依次遍历list中的每页
            href_list = []#每次都要将href_list即存放每页中所有连接的容器清空（要保证这个容器的作用域仅限于这个for循环中）
            time.sleep(0.5)
            print("当前处理页面为第%d页" % (i + 1))
            self.browser.get(all_page_url[i])  # 页面跳转
            time.sleep(0.5)

            # 检测是否出现了人工验证页面,如果出现，则先验证
            flag_str = self.browser.title
            #print(flag_str)
            if flag_str=='天眼查校验':#通过if的方式判断标志物来判断有没有出现验证页面
                print('等待验证112，完成后按任意键')
                os.system('pause')  # 程序暂停，等待人工处理

            else:#没出现验证则按照正常流程继续执行，抓取信息
                company_list=self.browser.find_elements_by_xpath('.//div[contains(@class, "header")][1]/a[1]')#获取搜索页面的所有公司div,以list形式存，注意一定是elements，不是element
                #print(isinstance(company_list, Iterable))#可迭代

                for each in company_list:
                    href=each.get_attribute('href')#获取超链
                    href_list.append(href)
                #print(href_list)#打印当前页面收集的href列表

                for i in range(0,len(href_list)):
                    # 同理判断有无出现人工验证，每一个循环都要判断一次，因为人工验证时随机跳出的
                    flag_str = self.browser.title
                    if flag_str == '天眼查校验':
                        print('等待验证113，完成后按任意键')
                        os.system('pause')  # 程序暂停，等待人工处理
                    else:
                        time.sleep(0.5)
                        self.browser.get(href_list[i])#进入公司详情页
                        company=self.save_company_info()#保存信息
                        # print(company)  # 此时格式为str
                        company=company.split("\n")#按照行分离，此时变为list格式
                        company.pop()#弹出最后一个没用的空白元素
                        print(company)#此时格式为list
                        #print(len(company))#一共7个有效元素，依次为公司名、电话、email、网址、地址、简介、经营范围
                        #break#【如果用于测试，每页只想爬取一个网页，直接在此break即可】

                        all_information.append(company)

        return all_information



    def wirte_in_excel(self,content):
        '''
        用于将数据写入excel文件中
        :param content: 要写入的数据，格式为list
        :return:
        '''
        book = xlrd.open_workbook(save_path)#输入保存路径
        new_book = copy.copy(book)  # 复制一个book
        sheet = new_book.get_sheet(0)  # 获取sheet1页

        # myWorkbook = xlwt.Workbook(encoding = 'utf-8')#添加工作薄
        # mySheet = myWorkbook.add_sheet('Sheet1')#添加工作表
        error_list=[]
        line=0
        for each in content:
            if len(each) != 7:  # 剔除格式问题的信息
                print('注意！有一条信息录入失败')
                error_list.append(each)
            else:
                col = 0
                for each_ele in each:
                    new_each = each_ele.split("：")[1]  # 切分只留下内容信息
                    sheet.write(line, col, new_each)
                    col += 1
                line+=1
        new_book.save('1.xls')
        return error_list#返回录入失败信息



    def save_company_info(self):
        """
        获取网页中的详细信息
        :return:
        """
        infomations = '' #通过字符串储存信息
        flag_str = self.browser.title
        if flag_str == '天眼查校验':
            print('等待验证115，完成后按任意键')
            os.system('pause')  # 程序暂停，等待人工处理
        else:
            company_name = self.browser.find_element_by_xpath('.//div[contains(@class, "header")][1]/h1')
            infomations += '公司名：' + company_name.text + '\n'# 电话
            phone = self.browser.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[1]/div[1]/span[2]')
            infomations += '电话：' + phone.text + '\n'
            email = self.browser.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[1]/div[2]/span[2]')    # 邮箱
            infomations += 'email：' + email.text + '\n'

            #获取网址
            try:
                link = self.browser.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[1]/a[1]')
            except:
                link = self.browser.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[1]/span[2]')
            infomations += '网址：' + link.text + '\n'
            #print(link.text)

            #获取地址
            try:
                ad = self.browser.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[2]/span[2]')
                address = ad.get_attribute('title')
            except:
                ad = self.browser.find_element_by_xpath('.//div[contains(@class, "detail ")][1]/div[2]/div[2]/div[1]')
                address = ad.text
            infomations += '地址：' + address + '\n'

            # 获取简介
            try:
                s = self.browser.find_element_by_xpath('.//div[contains(@class, "summary")][1]/span[1]')
                summary = self.get_summary(s)
            except:
                try:
                    summary = self.browser.find_element_by_xpath('.//div[contains(@class, "summary")][1]/div[1]/div[1]')
                except:
                    summary= self.browser.find_element_by_xpath('.//div[contains(@class, "summary")][1]/span[2]')
            infomations += '简介：' + summary.text + '\n'
            #infomations += summary.text + '\n'

            #获取经营范围
            try:
                j=self.browser.find_element_by_xpath('/html/body/div[2]/div/div/div[5]/div[1]/div/div[2]/div[1]/div[2]/div[2]/table[2]/tbody/tr[11]/td[2]/span')
                infomations += '经营范围：' + j.text + '\n'
            except:
                infomations += '经营范围：'+"暂无信息"+ '\n'

        return infomations

    def get_summary(self,e):
        """
        获取公司简介
        :param e:
        :return:
        """
        e.click()
        summary = self.browser.find_element_by_xpath('.//div[@class="body -detail modal-scroll"][1]')
        return summary




if __name__=="__main__":
    # url = "https://www.tianyancha.com/login"
    # url='https://www.tianyancha.com/vipintro/?jsid=SEM-BAIDU-PZ1907-SY-000100'
    url = 'https://www.tianyancha.com/'#要爬取的网站入口
    user='188 0128 5831'#用户名
    password='Sarmusliu136883'#密码

    new=Get_company_info(url,user,password)#实例化类
    new.login()#采用账密形式登录，需要人工进行拼图拖拽验证
    result=new.get_company_info('教育科技')#获取该关键词下所有的信息

    print(new.wirte_in_excel(result))#写入数据至excel并返回写入失败的数据)

##########################################
#问题：
#1.在爬取信息时会遇到验证码，导致程序终止，因此需要使用方法在遇到问题时暂停
#然后等待人工验码，点击提交后继续
#2.采用获取title的方法会进入bug页面：https://antirobot.tianyancha.com/captcha/verify/p6?return_url=https%3A%2F%2Fwww.tianyancha.com%2Fsearch%3Fkey%3D%25E6%2595%2599%25E8%2582%25B2%25E7%25A7%2591%25E6%258A%2580&rnd=





