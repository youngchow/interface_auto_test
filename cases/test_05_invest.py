# -*- coding: utf-8 -*-
from scripts.handle_log import do_logger
from scripts.handle_config import do_config
from scripts.handle_excel import HandleExcel
from scripts.handle_request import do_http_requests
from scripts.contants import TEST_DATA_FILES_PATH_CASES
from scripts.handle_context import HandleContext
from scripts.handle_mysql import HandleMysql
import unittest
from libs.ddt import ddt,data
import json
do_hanle_excel = HandleExcel(TEST_DATA_FILES_PATH_CASES,'invest')
cases = do_hanle_excel.get_case()

@ddt
class TestRecharge(unittest.TestCase):
    """
    测试投资接口
    """
    @classmethod
    def setUpClass(cls):
        cls.handle_mysql = HandleMysql()
        do_logger.debug('{}'.format('开始执行投资接口用例。。。。'))

    @classmethod
    def tearDownClass(cls):
        cls.handle_mysql.close()
        do_logger.debug('{}'.format('测试用例执行完毕，投资接口用例停止执行。。。。'))
    @data(*cases)
    def test_invest(self,one_case):
        case_id = one_case['case_id']
        title = one_case['title']
        data = one_case['data'] # 需要参数化， 将手机号替换
        #换位recharge的参数化
        new_data = HandleContext.invest_paramaterization(data) #参数已经被正常实际好替换
        do_logger.debug('获取到的new_data数据为：{}，在第【{}】'.format(new_data,case_id+1))
        url = one_case['url']
        total_url = do_config.get_value('requests','url_head') + url
        method = one_case['method']
        expected = one_case['expected']
        check_sql = one_case['check_sql']
        header = do_config.get_eval_data('requests','login_headers')
        invest_res =do_http_requests.to_request(method=method,
                                                  url=total_url,
                                                  data=new_data,
                                                  headers=header)
        invest_res_content = invest_res.text
        if '加标成功' in invest_res_content:  # 确定一定是加标成功
            if check_sql:
                check_sql = HandleContext.invest_paramaterization(check_sql)
                mysql_data = self.handle_mysql.run_mysql(check_sql)
                loan_id = mysql_data['Id']
                do_logger.debug('load_id的值为【{}】,在第  {}  行,返回值类型 {}'.format(loan_id,case_id+1,type(loan_id)))
                # 使用全局变量来解决接口依赖，极有可能出现循环导入，会抛出异常
                #接口依赖是动态获取变量的过程
                #HandleContext.loan_id = loan_id
                setattr(HandleContext,"loan_id",loan_id) # 给一个对象动态的创建属性
        real_result = invest_res.json().get('code')    #返回是字符串格式json
        expected_result = expected
        msg = '测试' + title
        success_msg = do_config.get_value('msg', 'success_result')
        fail_msg = do_config.get_value('msg', 'fail_result')

        try:
            self.assertEqual(str(expected_result),real_result,msg=msg)
            do_hanle_excel.write_case(case_id+1,real_result,success_msg)
            do_logger.debug('{},用例执行成功,执行结果为:{}'.format(msg,success_msg))
        except AssertionError as e:
            do_hanle_excel.write_case(case_id+1,real_result,fail_msg)
            do_logger.debug('{},用例用例执行失败，结果为:{},失败原因：{}'.format(msg,fail_msg,e))
            raise e
if __name__ == '__main__':
    unittest.main()


