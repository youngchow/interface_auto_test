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
do_hanle_excel = HandleExcel(TEST_DATA_FILES_PATH_CASES,'recharge')
cases = do_hanle_excel.get_case()

@ddt
class TestRecharge(unittest.TestCase):
    """
    测试充值接口
    """
    @classmethod
    def setUpClass(cls):
        cls.handle_mysql = HandleMysql()
        do_logger.debug('{}'.format('开始执行充值接口用例。。。。'))

    @classmethod
    def tearDownClass(cls):
        cls.handle_mysql.close()
        do_logger.debug('{}'.format('测试用例执行完毕，充值接口用例停止执行。。。。'))
    @data(*cases)
    def test_recharge(self,one_case):
        case_id = one_case['case_id']
        title = one_case['title']
        data = one_case['data'] # 需要参数化， 将手机号替换
        #换位recharge的参数化
        new_data = HandleContext.recharge_paramaterization(data) #参数已经被正常实际好替换
        do_logger.debug('获取到的data数据为：{}，在第【{}】'.format(new_data,case_id+1))
        url = one_case['url']
        total_url = do_config.get_value('requests','url_head') + url
        method = one_case['method']
        expected = one_case['expected']
        #充值之前查询金额
        check_sql = one_case['check_sql']
        if check_sql:
          check_sql= HandleContext.recharge_paramaterization(check_sql)
          mysql_data = self.handle_mysql.run_mysql(check_sql)
          amount_before_regarge = float(mysql_data['LeaveAmount']) # 返回decimal类型，需要用float转换
          amount_before_regarge = round(amount_before_regarge,2)

        header = do_config.get_eval_data('requests','login_headers')
        register_res =do_http_requests.to_request(method=method,
                                                  url=total_url,
                                                  data=new_data,
                                                  headers=header)
        #real_result = login_res.json()['msg']
        real_result = register_res.json().get('code')    #返回是字符串格式json

        expected_result = expected
        msg = '测试' + title
        success_msg = do_config.get_value('msg', 'success_result')
        fail_msg = do_config.get_value('msg', 'fail_result')

        try:
            self.assertEqual(str(expected_result),real_result,msg=msg)
            if check_sql:
                #check_sql = HandleContext.recharge_paramaterization(check_sql)
                #充值后的金额
                mysql_data = self.handle_mysql.run_mysql(check_sql)
                amount_after_regarge = float(mysql_data['LeaveAmount'])  # 返回decimal类型，需要用float转换
                amount_after_regarge = round(amount_after_regarge, 2)
                amount_expect_charge = json.loads(data,encoding='utf-8')['amount']
                do_logger.debug('{}....类型{},  在第【{}】行'.format(amount_expect_charge,type(amount_expect_charge),case_id+1))
                #将数据中计算出的充值前后的差值，再次转换为 取后2位小数
                amount_sql_recharge = round(amount_after_regarge-amount_before_regarge,2)
                self.assertEqual(amount_expect_charge,amount_sql_recharge,msg=msg)

            do_hanle_excel.write_case(case_id+1,real_result,success_msg)
            do_logger.debug('{},用例执行成功,执行结果为:{}'.format(msg,success_msg))
        except AssertionError as e:
            do_hanle_excel.write_case(case_id+1,real_result,fail_msg)
            do_logger.debug('{},用例用例执行失败，结果为:{},失败原因：{}'.format(msg,fail_msg,e))
            raise e
if __name__ == '__main__':
    unittest.main()


