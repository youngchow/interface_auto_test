# -*- coding: UTF-8 -*-
import unittest
from libs.HTMLTestRunnerNew import HTMLTestRunner
from scripts.handle_config import do_config
from cases import test_01_register
from datetime import datetime
from scripts.contants import REPORTS_DIR
import os


suite = unittest.TestSuite()
loader = unittest.TestLoader()
case = loader.loadTestsFromModule(test_01_register)
suite.addTests(case)

report_name = do_config.get_value('report','report_html_name') + datetime.strftime(datetime.now(),'%Y%m%d%H%M%S') + '.html'
html_full_path = os.path.join(REPORTS_DIR,report_name)
with open(html_full_path,mode='wb') as file:
    runner = HTMLTestRunner(stream=file,title='验证注册接口',tester='gordon',verbosity=2)
    runner.run(suite)