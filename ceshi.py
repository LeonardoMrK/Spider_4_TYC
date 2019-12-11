#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2019/12/2 10:14
# @Description: 天眼查爬虫。爬取目标：公司名称，电话，邮箱，网址，地址，简介，经营范围
#参考：
#https://www.cnblogs.com/chaihy/p/9540514.html
#https://www.cnblogs.com/jpapplication/p/10295803.html

import os
import json
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Iterable
from selenium.webdriver.common.keys import Keys






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
        self.url_dic={
                      'get_login': '/html/body/div[1]/div/div[1]/div[1]/div/div/div[2]/div/div[4]/a',
                      'login_user_pwd': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[1]/div[2]',
                      'login_user': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[2]/input',
                      'submit': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[5]',
                      'login_pwd': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[2]/div[3]/input',
                      'search':'/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/form/div/input',
                      'search_button':'/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div',
                      'company_list':'/html/body/div[2]/div/div[1]/div[4]/div[2]'
                    }


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
        time.sleep(6)#等待拼图拖拽验证


    def get_company_info(self,company_name):
        """
        输入关键词搜索，返回公司href列表,自带翻页功能
        :param company_name:
        :return:
        """
        href_list=[]
        input_company_name=self.browser.find_element_by_xpath(self.url_dic['search'])
        input_company_name.click()#选中搜索框
        input_company_name.send_keys(company_name)#输入想查询的公司名称
        time.sleep(1)
        # search_button=self.browser.find_element_by_xpath(self.url_dic['search_button'])
        # search_button.send_keys(Keys.ENTER)
        input_company_name.send_keys(Keys.ENTER)#再页面用按回车进入搜索，用click会出问题

########################################################
        currentPageUrl = self.browser.current_url
        print("当前页面的url是：", currentPageUrl)
        #从search后拆分，将url分成两部分，好进行翻页
########################################################

        company_list=self.browser.find_elements_by_xpath('.//div[contains(@class, "header")][1]/a[1]')#获取搜索页面的所有公司div,以list形式存，注意一定是elements
        #print(isinstance(company_list, Iterable))#可迭代

        for each in company_list:
            href=each.get_attribute('href')#获取超链
            href_list.append(href)

        # print(href_list)
        for each in href_list:
            time.sleep(0.5)
            self.browser.get(each)#进入公司详情页
            company=self.save_company_info()#保存信息
            print(company)
            break


    def save_company_info(self):
        """
        获取网页中的详细信息
        :return:
        """
        infomations = '' #通过字符串储存信息
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


#############################################
def information_filter():
    """
    根据经营范围内的关键字对数据进行筛选
    :return:
    """
    pass

def information_class():
    """
    根据公司地址对数据进行分类保存
    :return:
    """
    pass
#############################################

if __name__=="__main__":
    # url = "https://www.tianyancha.com/login"
    # url='https://www.tianyancha.com/vipintro/?jsid=SEM-BAIDU-PZ1907-SY-000100'
    url = 'https://www.tianyancha.com/'#要爬取的网站入口
    user='18811552008'
    password='shichanghuayuan2701'


    new=Get_company_info(url,user,password)#实例化类
    new.login()#采用账密形式登录，需要人工进行拼图拖拽验证
    new.get_company_info('字节跳动')







