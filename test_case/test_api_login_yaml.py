# 登录的参数化
from time import sleep

import allure
import pytest  # 找到测试用例,执行
import requests  # 发送请求的包

from common.parameterize_util import read_testcase
from common.send_request import SendRequest  # 导入公共的请求类
# from common.yaml_util import write_yaml, read_yaml, read_all_yaml  # yaml文件的操作(未添加类之前的调用方式
from common.step_util import TestStep
from common.yaml_util import YamlUtil

@allure.feature("登录模块")
@allure.parent_suite("登录模块")
@allure.suite("登录模块测试用例")
@allure.sub_suite("登录模块测试用例执行情况")
@allure.description('登录模块测试用例 执行人：小明同学')
class TestApi:
    # 1.@pytest.mark.parametrize实现数据驱动:
    """
    @pytest.mark.parametrize("caseinfo",["admin","admin1"])
    def test_login_01(self,caseinfo):
        print(f"登录接口：{caseinfo}")

    @pytest.mark.parametrize("username,password", [["admin", "admin"], ["admin1", "admin1"]])
    def test_login_02(self, username, password):
        print(f"登录接口参数：{username,password}")

    @pytest.mark.parametrize("caseinfo", [{"username": "admin", "password": "admin"}, {"username": "admin1", "password": "admin1"}])
    def test_login_03(self, caseinfo):
        print(f"登录接口参数：{caseinfo['username'],caseinfo['password']}")
    """

    # 2.@pytest.mark.parametrize结合yaml实现数据驱动:
    @pytest.mark.parametrize("caseinfo", read_testcase("GetLogin.yaml"))  #第一个参数是参数名,第二个参数是参数值
    # @allure.title('{caseinfo}')
    # @pytest.mark.parametrize("caseinfo", YamlUtil().read_all_yaml("/test_case/get_login.yaml"))  #第一个参数是参数名,第二个参数是参数值
    @allure.link(name="接口地址:http://ceshi13.dishait.cn/admin/login", url="http://ceshi13.dishait.cn/admin/login")
    def test_login_yaml(self, caseinfo):
        allure.dynamic.title(f"{caseinfo['name']}，请求参数:{caseinfo['request']['data']}")
        # res = YamlUtil().read_all_yaml("/datas/Test_Step_Login.yaml")
        # for item in res:
        #     with allure.step(f'步骤{item[0]}：{item[1]}'):
        #         pass
        # TestStep().read_step("/datas/Test_Step_Login.yaml")

        # res = read_testcase("Test_GetLogin.yaml")
        # print(res)
        # TestStep().read_step_yh("Test_GetLogin.yaml")

        # print("\n", caseinfo['name'])
        # url = caseinfo['request']['url']
        # userinfo = caseinfo['request']['userinfo']
        # res = requests.post(url=url,data=userinfo)
        # res = SendRequest().send_request(method=caseinfo['request']['method'], url=url, data=userinfo, testName=caseinfo['name'], moduleName=caseinfo['moduleName'])
        res = SendRequest().standard_yaml(caseinfo) # 优化为一句
        # print(res.json())
        # TestApi.accessToken=res.json()['data']['token']
        # 需要作判断
        # print(res.json())
        # print(type(res.json())) #<class 'dict'> 字典
        # if "data" in res.json().keys():
        #     YamlUtil().write_yaml({"accessToken": res.json()['data']['token']})  # 存储在yaml文件中
        # write_yaml({"accessToken":res.json()['data']['token']}) #存储在yaml文件中

    # def test_manager(self):
    # # def test_manager(self,db): #执行多次,因为做了数据驱动
    #     page = 1
    #     url = f"http://ceshi13.dishait.cn/admin/manager/{page}"
    #     headers = {
    #         # "token": TestApi.accessToken
    #         "token": YamlUtil().read_yaml("accessToken")  #从yaml文件中读取token
    #     }
    #     params = {
    #         "limit": 10,
    #         "keyword": "admin"
    #     }
    #     # res=requests.get(url=url,headers=headers)
    #     res = SendRequest().all_send_request(method="get", url=url, headers=headers, params=params, testName="4.获取管理员列表")
    #     print("\n", res.json())


"""
    def test_upload(self):
        url = "http://ceshi13.dishait.cn/admin/image/upload"
        files = {
            "img": open("E:\\1.jpg", "rb")
            # "img": ('1.jpg', open("E:\\1.jpg", "rb"), "image/jpeg", {})
        }
        data = {
            "image_class_id": 174
        }
        headers = {
            "token": read_yaml("accessToken"),  # 从yaml文件中读取token
            # "Content-Type": "multipart/form-data"
        }
        SendRequest().all_send_request(method="post", url=url, headers=headers, files=files, data=data)
"""
