# -*- coding: utf-8 -*-
from scripts.handle_log import do_logger
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_request import do_http_requests
from scripts.contants import TEST_DATA_FILES_PATH_CASES
from scripts.handle_context import HandleContext
import json
import unittest
from libs.ddt import ddt,data
do_hanle_excel = HandleExcel(TEST_DATA_FILES_PATH_CASES,'add')
cases = do_hanle_excel.get_case()

@ddt
class TestRegister(unittest.TestCase):
    """
    测试加标接口
    """
    @classmethod
    def setUpClass(cls):
        do_logger.debug('{}'.format('开始执行【加标接口】用例。。。。'))

    @classmethod
    def tearDownClass(cls):
        do_logger.debug('{}'.format('测试用例执行完毕，【加标接口用例】停止执行。。。。'))
    @data(*cases)
    def test_register(self,one_case):
        case_id = one_case['case_id']
        title = one_case['title']
        data = one_case['data']  # 需要参数化， 将手机号替换
        new_data = HandleContext.add_paramaterization(data)  # 参数已经被正常实际好替换

        do_logger.debug('new_data为：{}，类型【{}】在第【{}】'.format(new_data,type(new_data),case_id + 1))

        # if case_id > 1:
        #     new_data_update = json.loads(new_data, encoding='utf-8')
        #
        #     do_logger.debug(
        #         'new_data_update为：{}，类型【{}】在第【{}】'.format(new_data_update, type(new_data_update), case_id + 1))
        #     memberId = new_data_update['memberId']
        #     do_logger.debug('memberID为：{}，类型【{}】在第【{}】'.format(memberId, type(memberId), case_id + 1))

        url = one_case['url']
        total_url = do_config.get_value('requests', 'url_head') + url
        method = one_case['method']
        expected = one_case['expected']

        header = do_config.get_eval_data('requests', 'login_headers')
        register_res = do_http_requests.to_request(method=method,
                                                   url=total_url,
                                                   data=new_data,
                                                   headers=header)
        # real_result = login_res.json()['msg']
        real_result = register_res.json().get('code')  # 返回是字符串格式json

        expected_result = expected
        msg = '测试' + title
        success_msg = do_config.get_value('msg', 'success_result')
        fail_msg = do_config.get_value('msg', 'fail_result')
        try:
            self.assertEqual(str(expected_result), real_result, msg=msg)
            do_hanle_excel.write_case(case_id + 1, real_result, success_msg)
            do_logger.debug('{},用例执行成功,执行结果为:{}'.format(msg, success_msg))
        except AssertionError as e:
            do_hanle_excel.write_case(case_id + 1, real_result, fail_msg)
            do_logger.debug('{},用例用例执行失败，结果为:{},失败原因：{}'.format(msg, fail_msg, e))
            raise e


if __name__ == '__main__':
    unittest.main()


