# -*- coding: utf-8 -*-
from scripts.handle_config import do_config
import logging

class HandleLogging:
    def __init__(self):
        self.caselogger = logging.getLogger(do_config.get_value('log','logger_name'))

        self.caselogger.setLevel(do_config.get_value('log','logger_level'))

        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(do_config.get_value('log','log_filename'))

        console_handler.setLevel(do_config.get_value('log','console_level'))
        file_handler.setLevel(do_config.get_value('log','file_level'))

        simple_formattor = logging.Formatter(do_config.get_value('log','simple_formatter'))
        complicated_formattor = logging.Formatter(do_config.get_value('log','verbose_formatter'))

        console_handler.setFormatter(simple_formattor)
        file_handler.setFormatter(complicated_formattor)

        self.caselogger.addHandler(console_handler)
        self.caselogger.addHandler(file_handler)

    def get_logging(self):

        return self.caselogger
do_logger = HandleLogging().get_logging()

# if __name__ == '__main__':
#     case_logger = HandleLogging().get_logging()
#     case_logger.debug('这是一个debug级别的日志信息')
#     case_logger.info('这是一个info级别的日志信息')
#     case_logger.warning('这是一个warning级别的日志信息')
#     case_logger.error('这是一个error级别的日志信息')
#     case_logger.critical('这是一个critical级别的日志信息')


