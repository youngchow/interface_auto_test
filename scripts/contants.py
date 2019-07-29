# -*- coding: utf-8 -*-
import os

# 获取项目根路径

# roots_path = os.path.abspath(__file__) #获取 此py文件的的目录
# print(roots_path)
# roots = os.path.dirname(roots_path)#获取py文件所在的文件夹目录
# print(roots)
# root_path = os.path.dirname(roots)#获取文件夹的目录，即为跟目录
# print(root_path)
#
# root = os.path.dirname(root_path)
# print(root)
# 综合写法， 一层 一层 找项目根目录

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIGS_DIR = os.path.join(BASE_DIR,'configs')
CONFIGS_FILE_TESTCASE1 = os.path.join(CONFIGS_DIR,'testcase1.ini')
CONFIGS_USER_ACCOUNTS = os.path.join(CONFIGS_DIR,'user_accounts.ini')

#只是将datas的目录拼接，并不是 程序自己获取的
DATA_DIR = os.path.join(BASE_DIR,'datas')
TEST_DATA_FILES_PATH_CASES = os.path.join(DATA_DIR,'cases.xlsx')

CASES_DIR = os.path.join(BASE_DIR,'cases')


LOG_DIR = os.path.join(BASE_DIR,'logs')

REPORTS_DIR = os.path.join(BASE_DIR,'reports')


