#!/usr/bin/env python
# coding: utf-8
# @Author  : Mr.K
# @Software: PyCharm Community Edition
# @Time    : 2020/1/3 8:38
# @Description:参数设置脚本，用来设置天眼查各个元素的入口url（需要不定时人为更新，以防止失效）以及保存路径


tyc_url_dic={
    'get_login': '/html/body/div[1]/div/div[1]/div[1]/div[1]/div/div[2]/div/div[4]/a',
    'login_user_pwd': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[1]/div[2]',
    'login_user': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/form/div[1]/div[1]/input',
    'submit': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/div[2]',
    'login_pwd': '/html/body/div[9]/div[2]/div/div[2]/div/div/div[3]/div[3]/div[2]/form/div[2]/input',
    'search': '/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/form/div/input',
    'search_button': '/html/body/div[1]/div/div[1]/div[2]/div/div/div[2]/div[2]/div[1]/div',
    'company_list': '/html/body/div[2]/div/div[1]/div[4]/div[2]'
}

save_path='D:\\project\\pycharmworkspace\\Spider_4_TYC\\1.xlsx'