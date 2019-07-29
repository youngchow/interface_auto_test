# -*- coding: utf-8 -*-
from scripts.handle_log import HandleLogging
from scripts.handle_config import HandleConfig
from scripts.handle_excel import HandleExcel
from scripts.handle_request import do_http_requests
from scripts.contants import TEST_DATA_FILES_PATH_CASES
from scripts.contants import CONFIGS_FILE_TESTCASE1
from scripts.handle_context import HandleContext
import unittest

from libs.ddt import ddt,data

handexcel = HandleExcel(TEST_DATA_FILES_PATH_CASES,'login')
cases =handexcel.get_case()
do_logger = HandleLogging().get_logging()
do_config = HandleConfig(CONFIGS_FILE_TESTCASE1)


@ddt
class TestLogin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        do_logger.debug('{}'.format('开始执行登录接口用例。。。。'))

    @classmethod
    def tearDownClass(cls):
        do_logger.debug('{}'.format('测试用例执行完毕，登录接口用例停止执行。。。。'))


    @data(*cases)
    def test_login(self,one_case):
        case_id = one_case['case_id']
        title = one_case['title']
        data = one_case['data']
        new_data = HandleContext.login_paramaterization(data)
        url = one_case['url']
        total_url = do_config.get_value('requests','url_head')+url
        method = one_case['method']
        expected = one_case['expected']

        header = do_config.get_eval_data('requests','login_headers')

        login_res = do_http_requests.to_request(method=method,
                                                url=total_url,
                                                data=new_data,
                                                headers=header)
        real_result = login_res.text
        expected_result = expected
        msg = '测试' + title
        success_msg = do_config.get_value('msg', 'success_result')
        fail_msg = do_config.get_value('msg', 'fail_result')
        try:
            self.assertEqual(expected_result,real_result,msg=msg)
            handexcel.write_case(case_id+1,real_result,success_msg)
            do_logger.debug('{},用例执行成功,执行结果为:{}'.format(msg,success_msg))
        except AssertionError as e:

            handexcel.write_case(case_id+1,real_result,fail_msg)
            do_logger.debug('{},用例用例执行失败，结果为:{},失败原因：{}'.format(msg, fail_msg, e))
            raise e
if __name__ == '__main__':
    unittest.main()