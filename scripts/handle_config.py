# -*- coding: utf-8 -*-
from configparser import ConfigParser
from scripts.contants import CONFIGS_FILE_TESTCASE1

class HandleConfig:

    def __init__(self,filename):
        self.filename = filename
        self.config = ConfigParser()
        self.config.read(self.filename,encoding='utf-8')

    def get_value(self,section,option):

        return self.config.get(section,option)

    def get_int(self,section,option):

        return self.config.getint(section,option)

    def get_float(self,section,option):

        return self.get_float(section,option)

    def get_boolean(self,section,option):

        return self.get_boolean(section,option)

    def get_eval_data(self,section,option):

        return eval(self.get_value(section,option))

    def write_config(self,datas,filename):
        #datas = {
        #     'file_path': {'case_path': 'cases.xlsx', 'log_path': 'record_run_result.txt'},
        #     'msg': {'success_result': 'pass', 'fail_result': 'fail', 'expected_result': 'none'}
        # }
        write_config = ConfigParser()

        for key in datas:
            write_config[key] = datas[key]
        with open(filename,mode='w') as file:
            write_config.write(file)


do_config = HandleConfig(CONFIGS_FILE_TESTCASE1)