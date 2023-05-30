# 执行全部的测试用例并生成测试报告
import os
from time import sleep

import pytest

# from common.yaml_util import read_yaml, write_yaml, read_all_yaml #(未添加类之前的调用方式
# from common.yaml_util import YamlUtil  # (添加类之后的调用方式)

if __name__ == '__main__':
    pytest.main()  # 执行时需要把文件名作修改  allure是处理的临时文件
    sleep(3)  # 让它先生成临时文件
    # split = 'allure ' + 'generate ' + './report/temporary ' + '-o ' + './report/html ' + '--clean'
    # os.system(split)  # 调用dos命令
    # YamlUtil().write_yaml({"age":"18","student":[{"name":"admin"},{"username":"IKUN"}]})
    # print(YamlUtil().read_yaml("age"))
    # print(YamlUtil().read_all_yaml("/test_case/get_login.yaml"))
