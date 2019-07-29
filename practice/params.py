import requests
from scripts.handle_request import HttpRequests

do_request = HttpRequests()
url = 'http://tj.lemonban.com/futureloan/mvc/api/member/register'
data = '{"mobilephone":"18897310652","pwd":"123456","regname":"regname"}'

res = do_request.to_request(method='post',url=url,data=data)

print(res.text)


pass


dict1 = {'name':'zhangei',"age":30}
dict1['name'] = 900

print(dict1['name'])