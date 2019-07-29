# -*- coding: utf-8 -*-
from scripts.handle_config import do_config
import pymysql
import random
import string

class HandleMysql:
    def __init__(self):
        self.conn = pymysql.connect(
               host = do_config.get_value('mysql','host'),
               user = do_config.get_value('mysql','user'),
               password=do_config.get_value('mysql','password'),
               db=do_config.get_value('mysql','db'),
               port=do_config.get_int('mysql','port'),
               charset=do_config.get_value('mysql','charset'),
               cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor =self.conn.cursor()

    def run_mysql(self,sql,args = None,is_more = False):
        self.cursor.execute(sql,args)
        self.conn.commit()

        if is_more:
            return self.cursor.fetchall()
        else:
            return self.cursor.fetchone()

    def close(self):
        self.cursor.close()
        self.conn.close()

    @staticmethod
    #完全不需要任何参数，不需要调用其他方法
    def create_mobile():
        start_mobile = ['138','158','188','178']
        #random.choice()
        mobile_head = random.sample(start_mobile,1)
        mobile_body = random.sample(string.digits,8)
        mobile = ''.join(mobile_head+mobile_body)

        return mobile
    def is_exist_mobile(self,mobile):
        sql = "select MobilePhone from member where MobilePhone = %s"

        if self.run_mysql(sql,args=(mobile,)): # 返回不为空(true)，表示号码已经存在 返回true
            return True
        else:
            return False

    def create_not_existed_mobile(self):
        while True: # 可以写为： while false?
            one_mobile = self.create_mobile()
            if not self.is_exist_mobile(one_mobile):
                break
        return one_mobile

    def create_existed_mobile(self):
        sql = "select MobilePhone from member limit 1"
        two_mobile = self.run_mysql(sql)
        existed_mobile = two_mobile['MobilePhone']
        return existed_mobile

if __name__ == '__main__':
    sql = 'SELECT RegName,LeaveAmount FROM member where MobilePhone = %s'

    #sql = 'SELECT * FROM member LIMIT 10'
    handle_mysql = HandleMysql()
    handle1 = handle_mysql.run_mysql(sql,args=('15828641020',))
    #handle_mysql.close()
    print(handle1)
    hh = handle_mysql.create_mobile()
    print(hh)
    print('创建未注册的手机号:{}'.format(handle_mysql.create_not_existed_mobile()))
    print('创建已经注册的手机号:{}'.format(handle_mysql.create_existed_mobile()))



