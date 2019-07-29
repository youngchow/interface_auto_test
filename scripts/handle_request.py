# -*- coding: utf-8 -*-
from scripts.handle_log import do_logger
from scripts.handle_config import do_config
import requests
import json

class HttpRequests:
    def __init__(self):
        self.one_session = requests.Session()

    def para_to_str(self,para):
        if isinstance(para,str):
            try:
                para = json.loads(para)
            except Exception as e:
                para = eval(para)
                do_logger.error('将json转为python中的数据类型时，出现异常：{}'.format(e))
        return para

    def to_request(self, method, url, data=None,is_json=False, **kwargs):
        method = method.upper()

        data = self.para_to_str(data)
        # if isinstance(data, str):
        #     try:
        #         data = json.loads(data)
        #     except Exception as e:
        #         data = eval(data)
        #         do_logger.error('将json转为python中的数据类型时，出现异常：{}'.format(e))

        if method == 'GET':
            res = self.one_session.request(method=method, url=url, params=data, **kwargs)
        elif method == 'POST':

            if is_json:
                res = self.one_session.request(method=method, url=url, json=data, **kwargs)
            else:
                res = self.one_session.request(method=method, url=url, data=data, **kwargs)
        else:
            res = None

            do_logger.error('不支持【{}】方法名'.format(method))

        return res


do_http_requests =HttpRequests()
if __name__ == '__main__':
    # 从配置文件中 读取数据

    do_request = HttpRequests()
    url = 'http://tj.lemonban.com/futureloan/mvc/api/member/register'
    data = '{"mobilephone": "18897310653", "pwd": "123456", "regname": "regname"}'
    new_data = {"mobilephone": "18897310651", "pwd": "123456", "regname": "regname"}

    res = do_request.to_request(method='post', url=url, data=new_data)

    print(res.text)

