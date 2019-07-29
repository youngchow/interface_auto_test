# -*- coding: utf-8 -*-
import unittest
from scripts.handle_config import do_config
from cases import test_01_register
from datetime import datetime
from scripts.contants import REPORTS_DIR,CASES_DIR
from scripts.contants import CONFIGS_USER_ACCOUNTS
from scripts.handle_user import generate_users
from libs.HTMLTestRunnerNew import HTMLTestRunner
import os
if not os.path.exists(CONFIGS_USER_ACCOUNTS):# 如果用户账号坐在文件不存在，则创建账号
    generate_users()

#自动加载cases中的全部用例
suite = unittest.defaultTestLoader.discover(CASES_DIR,pattern='test_*.py')

# report_name = do_config.get_value('report', 'report_html_name') + datetime.strftime(datetime.now(), '%Y%m%d%H%M%S') + '.html'
report_name = do_config.get_value('report', 'report_html_name') + '.html'
html_full_path = os.path.join(REPORTS_DIR, report_name)
with open(html_full_path, mode='wb') as file:
    runner = HTMLTestRunner(stream=file, title='验证注册接口', tester='gordon', verbosity=2)
    runner.run(suite)
