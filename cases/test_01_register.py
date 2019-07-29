# -*- coding: utf-8 -*-
from scripts.handle_log import do_logger
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_request import do_http_requests
from scripts.contants import TEST_DATA_FILES_PATH_CASES
from scripts.handle_context import HandleContext

import unittest
from libs.ddt import ddt,data
do_hanle_excel = HandleExcel(TEST_DATA_FILES_PATH_CASES,'register')
cases = do_hanle_excel.get_case()

@ddt
class TestRegister(unittest.TestCase):
    """
    测试注册接口
    """
    @classmethod
    def setUpClass(cls):
        do_logger.debug('{}'.format('开始执行用例。。。。'))

    @classmethod
    def tearDownClass(cls):
        do_logger.debug('{}'.format('测试用例执行完毕，停止执行。。。。'))
    @data(*cases)
    def test_register(self,one_case):
        case_id = one_case['case_id']
        title = one_case['title']
        data = one_case['data'] # 需要参数化， 将手机号替换
        new_data = HandleContext.register_paramaterization_not_exist(data) #参数已经被正常实际好替换
        do_logger.debug('获取到的data数据为：{}，在第【{}】'.format(new_data,case_id+1))
        url = one_case['url']
        total_url = do_config.get_value('requests','url_head') + url
        method = one_case['method']
        expected = one_case['expected']

        header = do_config.get_eval_data('requests','login_headers')
        register_res =do_http_requests.to_request(method=method,
                                                  url=total_url,
                                                  data=new_data,
                                                  headers=header)
        #real_result = login_res.json()['msg']
        real_result = register_res.text    #返回是字符串格式json
        #real_result = str(register_res.json()) #

        expected_result = expected
        msg = '测试' + title
        success_msg = do_config.get_value('msg', 'success_result')
        fail_msg = do_config.get_value('msg', 'fail_result')

        try:
            self.assertEqual(expected_result,real_result,msg=msg)
            do_hanle_excel.write_case(case_id+1,real_result,success_msg)
            do_logger.debug('{},用例执行成功,执行结果为:{}'.format(msg,success_msg))
        except AssertionError as e:
            do_hanle_excel.write_case(case_id+1,real_result,fail_msg)
            do_logger.debug('{},用例用例执行失败，结果为:{},失败原因：{}'.format(msg,fail_msg,e))
            raise e
if __name__ == '__main__':
    unittest.main()


