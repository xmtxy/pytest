# 读取yaml的类
import os

import yaml


class YamlUtil:
    # 1.读取yaml文件
    def read_yaml(self,key):
        # os.getcwd() 获得目录的当前系统程序工作路劲
        print(os.getcwd()+"/extract.yaml") #D:\PythonPc_App\Dome_Api_test\common
        with open(os.getcwd()+"/extract.yaml",encoding="utf-8") as file:
            value = yaml.load(stream=file, Loader=yaml.FullLoader)  #懒加载
            return value[key]
    # 2.写入yaml文件
    def write_yaml(self,data):
        with open(os.getcwd() + "/extract.yaml", encoding="utf-8", mode="a") as file:
            yaml.dump(data, stream=file, allow_unicode=True)
    # 3.清空yaml文件
    def clear_yaml(self):
        with open(os.getcwd() + "/extract.yaml", encoding="utf-8", mode="w") as file:
            file.truncate() #扯 k特
    # read_yaml() #D:\PythonPc_App\Dome_Api_test\common

    # 注意点:
    # 在yaml_util中运行则,工作路径是 D:\PythonPc_App\Dome_Api_test\common
    # 如果实在ExecuteAll.py中运行则工作路径是 D:\PythonPc_App\Dome_Api_test

    # 4.读取所有的yaml数据
    def read_all_yaml(self,base_path):
        # os.getcwd() 获得目录的当前系统程序工作路径
        # print(os.getcwd()+"/extract.yaml") #D:\PythonPc_App\Dome_Api_test\common
        print(os.getcwd()+base_path)
        with open(os.getcwd()+base_path,encoding="utf-8") as file:
            value = yaml.load(stream=file, Loader=yaml.FullLoader)  #懒加载
            # print(value) # [['name', 'username', 'password', 'project', 'assert_str'], ['登录成功-获取token', 'admin', 'admin', 'DEFAULT', 'data'],...]
            return value
    # 5.读取测试用例
    # def read_testcase(self,yaml_name):
    #     with open(os.getcwd() + '\\test_case\\' + yaml_name, mode='r', encoding='utf-8') as f:
    #         value = yaml.load(f, yaml.FullLoader)
    #         return value

    # 读取config.yaml
    def read_config(self, one_node, two_node):
         with open(os.getcwd() + '/config.yaml', encoding='utf-8') as f:
            value = yaml.load(f, yaml.FullLoader)
            return value[one_node][two_node]