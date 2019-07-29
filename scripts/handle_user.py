# -*- coding: utf-8 -*-
from scripts.handle_mysql import HandleMysql
from scripts.handle_request import HttpRequests
from scripts.handle_config import HandleConfig
from scripts.contants import CONFIGS_FILE_TESTCASE1
from scripts.contants import CONFIGS_USER_ACCOUNTS
import json


def create_new_user(regname,pwd = '123456'):
    handle_mysql = HandleMysql()
    send_request = HttpRequests()
    do_config = HandleConfig(CONFIGS_FILE_TESTCASE1)
    url =do_config.get_value('requests','url_head') + '/member/register'
    print(url)
    sql = "select Id from member where MobilePhone = %s;"

    while True:
        mobilephone = handle_mysql.create_not_existed_mobile()
        print(mobilephone)
        print(pwd)
        print(regname)
        data = {"mobilephone":mobilephone,"pwd":pwd,"regname":regname}
        #new_data = json.dumps(data)
        res = send_request.to_request(method="post",url=url,data=data)
        print(res.text)
        result = handle_mysql.run_mysql(sql,(mobilephone,))
        print('ddddddd{}'.format(result))
        #result为空，说明注册没成功，则执行for循环下一次，直到成功
        if result:
            user_id = result['Id']
            break
    user_dict = {
        regname:{
            "Id":user_id,
            "regname":regname,
            "mobilephone":mobilephone,
            "pwd":pwd
        }
    }
    return  user_dict

    handle_mysql.close()


def generate_users():
    user_datas_dicts = {}
    user_datas_dicts.update(create_new_user("admin_user"))
    user_datas_dicts.update(create_new_user("invest_user"))
    user_datas_dicts.update(create_new_user("borrow_user"))
    other_do_config = HandleConfig(CONFIGS_USER_ACCOUNTS)
    other_do_config.write_config(user_datas_dicts,CONFIGS_USER_ACCOUNTS)

if __name__ == '__main__':
    generate_users()

    pass