# -*- coding: utf-8 -*-
import re
from scripts.handle_mysql import HandleMysql
from scripts.handle_config import HandleConfig
from scripts.contants import CONFIGS_USER_ACCOUNTS

class HandleContext:
    """
    使用正则 手机号等 数据进行参数化
    """
    not_existed_tel_pattern = r'\$\{not_existed_tel\}'
    invest_user_tel_pattern = r'\$\{invest_user_tel\}'
    invest_user_pwd_pattern = r'\$\{invest_user_pwd\}'
    admin_user_tel_pattern = r'\$\{admin_user_tel\}'
    admin_use_pwd_pattern = r'\$\{admin_user_pwd\}'
    borrow_user_id_pattern = r'\$\{borrow_user_id\}'
    invest_loan_id_pattern = r'\$\{loan_id\}'
    invest_user_id_pattern = r'\$\{invest_user_id\}'

    @classmethod
    def not_existed_tel_repalce(cls,data):
        """
        data 是待替换的原始字符串 用if先判断，可以节省资源
        """
        if re.search(cls.not_existed_tel_pattern,data):
            handle_mysql = HandleMysql()
            not_existed_tel = handle_mysql.create_not_existed_mobile()
            data = re.sub(cls.not_existed_tel_pattern,not_existed_tel,data)
        return data
        handle_mysql.close()

    @classmethod
    def existed_tel_replace(cls,data):
        pass
    @classmethod
    def invest_user_tel_replace(cls,data):
        do_conig = HandleConfig(CONFIGS_USER_ACCOUNTS)
        if re.search(cls.invest_user_tel_pattern,data):
            invest_tel = do_conig.get_value('invest_user','mobilephone')
            data = re.sub(cls.invest_user_tel_pattern,invest_tel,data)
        return data
    @classmethod
    def invest_user_pwd_replace(cls,data):
        pwd_config = HandleConfig(CONFIGS_USER_ACCOUNTS)
        if re.search(cls.invest_user_pwd_pattern,data):
            invest_pwd = pwd_config.get_value('invest_user','pwd')
            data = re.sub(cls.invest_user_pwd_pattern,invest_pwd,data)
        return data
    @classmethod
    def invest_user_id_repalce(cls,data):
        id_config = HandleConfig(CONFIGS_USER_ACCOUNTS)
        if re.search(cls.invest_user_id_pattern,data):
            invest_id = id_config.get_value('invest_user','id')
            data = re.sub(cls.invest_user_id_pattern,invest_id,data)
        return data
    @classmethod
    def admin_user_tel_replace(cls,data):
        admin_user_config = HandleConfig(CONFIGS_USER_ACCOUNTS)
        if re.search(cls.admin_user_tel_pattern,data):
            admin_user_tel = admin_user_config.get_value('admin_user','mobilephone')
            data = re.sub(cls.admin_user_tel_pattern,admin_user_tel,data)
        return data
    @classmethod
    def admin_user_pwd_replace(cls,data):
        admin_pwd_config = HandleConfig(CONFIGS_USER_ACCOUNTS)
        if re.search(cls.admin_use_pwd_pattern,data):
            admin_user_pwd = admin_pwd_config.get_value('admin_user','pwd')
            data = re.sub(cls.admin_use_pwd_pattern,admin_user_pwd,data)
        return data
    @classmethod
    def borrow_user_id_replace(cls,data):
        borrow_user_config = HandleConfig(CONFIGS_USER_ACCOUNTS)
        if re.search(cls.borrow_user_id_pattern,data):
            borrow_user_id = borrow_user_config.get_value('borrow_user','id')
            data = re.sub(cls.borrow_user_id_pattern,borrow_user_id,data)
        return data

    @classmethod
    def invest_loan_id_replace(cls, data):

        if re.search(cls.invest_loan_id_pattern, data):
            loan_id = getattr(cls, "loan_id")
            loan_id = str(loan_id)
            data = re.sub(cls.invest_loan_id_pattern, loan_id, data)

        return data

    @classmethod
    def register_paramaterization_not_exist(cls,data):
        data = cls.not_existed_tel_repalce(data)
        data = cls.invest_user_tel_replace(data)
        return data

    @classmethod
    def login_paramaterization(cls,data):
        data = cls.not_existed_tel_repalce(data)
        data = cls.invest_user_tel_replace(data)
        data = cls.invest_user_pwd_replace(data)
        return data
    @classmethod
    def recharge_paramaterization(cls,data):
        data = cls.invest_user_tel_replace(data)
        data = cls.invest_user_pwd_replace(data)
        data = cls.not_existed_tel_repalce(data)
        return data

    @classmethod
    def add_paramaterization(cls,data):
        data = cls.admin_user_tel_replace(data)
        data = cls.admin_user_pwd_replace(data)
        data = cls.borrow_user_id_replace(data)
        return data
    @classmethod
    def invest_paramaterization(cls,data):
        data = cls.admin_user_tel_replace(data)
        data = cls.admin_user_pwd_replace(data)
        data = cls.borrow_user_id_replace(data)
        data = cls.invest_loan_id_replace(data)
        data = cls.invest_user_tel_replace(data)
        data = cls.invest_user_pwd_replace(data)
        data = cls.invest_user_id_repalce(data)
        return data

if __name__ == '__main__':
    context = HandleContext()
    data1 = '{"mobilephone":"${not_existed_tel}","pwd":"123456","regname":"jason"}'
    data2 = '{"mobilephone":"18934567","pwd":"123456","regname":"jason"}'
    print(context.not_existed_tel_repalce(data1))
    print(context.not_existed_tel_repalce(data2))
    o_conig = HandleConfig(CONFIGS_USER_ACCOUNTS)
    invest_tel = o_conig.get_value('invest_user', 'mobilephone')
    print(invest_tel)