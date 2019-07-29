import re
from scripts.handle_config import HandleConfig
from scripts.contants import CONFIGS_FILE_TESTCASE2
from scripts.handle_mysql import HandleMysql
from scripts.handle_request import do_http_requests


class RegisterAccount:

    sql = "SELECT Id,Pwd,MobilePhone FROM member WHERE MobilePhone = %s"
    data = '{"mobilephone":"${not_existed_tel}","pwd":"123456","regname":"jason_loan"}'
    url = 'http://tj.lemonban.com/futureloan/mvc/api/member/register'

    def __init__(self):
        self.handle_mysql = HandleMysql()
        self.do_config = HandleConfig(CONFIGS_FILE_TESTCASE2)

    def register(self):
        not_existed_mobile = self.handle_mysql.create_not_existed_mobile()
        new_data = re.sub(r'\$\{not_existed_tel\}',not_existed_mobile,self.data)

        do_http_requests.to_request('post',url =self.url,data = new_data)
        sql_result = self.handle_mysql.run_mysql(self.sql,args=(not_existed_mobile,))

        return sql_result

    def close(self):
        self.handle_mysql.close()

    def write_data(self):
        content = self.register()
        datas = {"account":content}
        self.do_config.write_config(datas,CONFIGS_FILE_TESTCASE2)


if __name__ == '__main__':

    reg = RegisterAccount()
    reg.write_data()
    reg.close()