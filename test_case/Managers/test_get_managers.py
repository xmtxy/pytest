import allure
import pytest

from common.parameterize_util import read_testcase
from common.send_request import SendRequest
from common.step_util import TestStep
from common.yaml_util import YamlUtil


@allure.feature("管理员模块")
@allure.parent_suite("管理员模块")
@allure.suite("管理员模块测试用例")
@allure.sub_suite("管理员模块测试用例执行情况")
@allure.description('管理员模块测试用例 执行人：小明同学')
class Test_Manage_Api:
    # 1.管理员列表接口
    """
    story 1 case 1的用例描述：test story 1 的test case 1
    :return: 成功1
    """
    @pytest.mark.parametrize("manages", read_testcase("\\Managers\\Managers.yaml"))  # 第一个参数是参数名,第二个参数是参数值
    @allure.link(name="接口地址:http://ceshi13.dishait.cn/admin/manager/1", url="http://ceshi13.dishait.cn/admin/manager/1")
    def test_get_manages(self, manages):
        # url = manages['request']['url']
        # userinfo = manages['request']['data']
        # headers = {
        #     "token": YamlUtil().read_yaml("token")  # 从yaml文件中读取token 需要进一步的处理token,可以从一个yaml文件中读取,目前两个了.....
        # }
        # print(headers['token'])
        # res = SendRequest().all_send_request(method=manages['request']['method'], headers=headers, url=url, data=userinfo,
        #                                      testName=manages['name'], moduleName=manages['moduleName'])
        allure.dynamic.title(f"{manages['name']}，请求参数:{manages['request']['data']}")
        # TestStep().read_step("/datas/Test_Step_Managers.yaml")

        # key_list = manages['step'].split("/")
        # for item in key_list:
        #     with allure.step(f'{item}'):
        #         pass
        res = SendRequest().standard_yaml(manages)
        # print("\n", res.json())
