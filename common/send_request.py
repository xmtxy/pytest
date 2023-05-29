import json

import allure
import jsonpath
import requests

from builtins import str
from common.logger import GetLogger
from common.time_method import Test
from common.yaml_util import YamlUtil

import re


class SendRequest:  # 没有参数时可省略()括号
    # 回话,管理Cookie管理,跟数据库一样-会话:有开始必定要有结束-表示过程
    session = requests.session()

    # 初始化数据,如果参数没传的情况下将参数置为None
    def __init__(self):
        self.session = SendRequest.session
        self.method = None
        self.url = None
        self.data = None
        self.headers = None
        self.files = None
        self.json = None
        self.params = None
        self.resp = None
        self.logger = GetLogger.get_logger()
        self.base_url = YamlUtil().read_config('base', 'base_test_url')
        self.obj = Test()

    # 规范yaml测试用例
    def standard_yaml(self, caseinfo):
        # print(caseinfo) # {'name':'xxx',.....}
        caseinfo_keys = caseinfo.keys()
        # 判断一级关键字是否包含：name,request,validate
        if "name" in caseinfo_keys and "request" in caseinfo_keys and "validate" in caseinfo_keys and "moduleName" in caseinfo_keys:
            testName = caseinfo['name']
            moduleName = caseinfo['moduleName']
            status_code = caseinfo['validate'][0]['equals']['status_code']
            assert_str = caseinfo['validate'][1]['contains']
            # allure报告用例的描述
            key_list = caseinfo['step'].split("/")
            for item in key_list:
                with allure.step(f'{item}'):
                    pass
            # 判断request下面是否包含：method、url
            request_keys = caseinfo["request"].keys() # 处理request下面的参数
            if "method" in request_keys and "url" in request_keys:
                print("yaml基本架构规范检查通过")
                method = caseinfo['request'].pop("method")  # pop() 函数用于移除列表中的一个元素,并且返回该元素的值。
                url = caseinfo['request'].pop("url")
                # print(caseinfo['request']) # {'data': {'username': 'admin', 'password': '123456'}}
                # 调用统一请求封装--方法

                # *args：用于列表、元组、集合
                # **kwargs：用于字典
                # print(type(caseinfo)) # <class 'dict'>
                # print(*caseinfo['request'])

                res = self.send_request(method, url, testName, moduleName, status_code, assert_str, **caseinfo['request'])  # caseinfo需要解包加** # data/json/params/headers
                return_text = res.text

                # ---------------热加载新增-------------------
                return_code = res.status_code # 响应状态码
                return_json = ""
                try:
                    return_json = res.json()
                except Exception as e:
                    print("extract返回的结果不是JSON格式")
                # ---------------热加载新增-------------------

                # 提取值并写入extract.yaml文件(提取token
                if "extract" in caseinfo.keys(): # 所有的属性名
                    # 返回字典中的所有键值对信息 如:{"2018":"小明","2019":"小红","2020":"小白"} 打印:dict_items([('2018', '小明'), ('2019', '小红'), ('2020', '小白')])
                    # print(caseinfo["extract"].items()) # dict_items([('token', '"data":"(.*?)"')])
                    for key, value in caseinfo["extract"].items():
                        # print(value) # "data":"(.*?)"
                        if "(.*?)" in value or "(.+?)" in value:  # 正则表达式
                            # Python中re模块主要功能是通过正则表达式是用来匹配处理字符串的（regex：正则）
                            Pm_value = re.search(value, return_text) # search:浏览全部字符串,匹配第一符合规则的字符串,浏览整个字符串去匹配第一个,未匹配成功返回None
                            if Pm_value:
                                extract_value = {key: Pm_value.group(1)} # group(1) 返回了匹配到的第一个分组的结果
                                YamlUtil().write_yaml(extract_value) # 写入yaml文件的方法
                        else:  # jsonpath 提取器
                            try:
                                resturn_json = res.json()
                                js_value = jsonpath.jsonpath(resturn_json, value)
                                if js_value:
                                    extract_value = {key: js_value[0]}
                                    YamlUtil().write_yaml(extract_value)
                            except Exception as e:
                                print("extract返回的结果不是JSON格式,不能使用jsonpath提取")
                # 断言:
                self.assert_result(caseinfo['validate'], return_json, return_code)  # 调用下面的方法处理
                # return res
            else:
                print("在request下必须包含method,url")
        else:
            print("一级关键字必须包含name,request,validate")

    # 统一请求的方法
    def all_send_request(self, testName=None, moduleName=None, **kwargs):
    # def all_send_request(self, method, url, **kwargs):
        # 接口测试开始
        # print("\n")
        # print(f"请求方式:{method}")
        # print(f"接口地址:{url}")
        # if "data" in kwargs.keys():
        #     print(f"请求参数data:{kwargs['data']}")
        # if "json" in kwargs.keys():
        #     print(f"请求参数json:{kwargs['json']}")
        # if "params" in kwargs.keys():
        #     print(f"请求参数json:{kwargs['params']}")
        # if "files" in kwargs.keys():
        #     print(f"请求参数files:{kwargs['files']}")
        # 如果调用方，没有传任何的参数，那么就使用该对象的默认属性参数
        # print(kwargs.keys()) # dict_keys(['method', 'url', 'data'])
        if 'url' not in kwargs.keys():
            # kwargs['url'] = self.url
            kwargs['url'] = self.base_url + self.replace_value(self.url)
        if 'method' not in kwargs.keys():
            # kwargs['method'] = self.method
            kwargs['method'] = str(self.method).lower()  #转换小写
        if 'headers' not in kwargs.keys():
            kwargs['headers'] = self.headers
        if 'data' not in kwargs.keys():
            kwargs['data'] = self.data
        if 'json' not in kwargs.keys():
            kwargs['json'] = self.json
        if 'files' not in kwargs.keys():
            kwargs['files'] = self.files
        if 'params' not in kwargs.keys():
            kwargs['params'] = self.params
        # 将接口发起前的信息记录到日志中
        self.logger.info('--------------------接口开始--------------------')
        self.logger.info(f"接口的名称是：{testName}")
        self.logger.info(f"接口的所属模块是：{moduleName}")

        # d.items()
        # 返回字典中的所有键值对信息 如:{"2018":"小明","2019":"小红","2020":"小白"} 打印:dict_items([('2018', '小明'), ('2019', '小红'), ('2020', '小白')])
        for key, value in kwargs.items(): # 要考虑提供的yaml没有这个属性值的情况,上面的处理是取初始值
            self.logger.info(f'接口的{key}是：{value}')

        # # 参数替换
        # for key, value in kwargs.items():
        #     if key in ['params', 'data', 'json', 'headers']:
        #         kwargs[key] = self.replace_value(value)
        #     elif key == "files":
        #         for file_key, file_path in value.items():
        #             value[file_key] = open(file_path, 'rb')

        try:
            self.resp = self.session.request(**kwargs)
            # print(self.logger.info(f'接口响应状态码是：{self.resp.status_code}')) # None
            self.logger.info(f'接口响应状态码是：{self.resp.status_code}')
            # print(self.logger.info(f'接口响应信息是：{self.resp.text}')) # None
            self.logger.info(f'接口响应信息是：{self.resp.text}')
            self.logger.info('--------------------接口结束--------------------'+"\n")
        except BaseException as e:
            self.logger.exception('接口请求报错！')
            raise BaseException(f'接口报错信息：{e}')
        return self.resp
        # res = SendRequest.sess.request(method, url, **kwargs)

        # print(f"响应结果:{res.json()}")
        # # 接口测试结束
        # print("\n")
        # return res

    # 统一请求封装
    def send_request(self, method, url, testName, moduleName, status_code=None, assert_str=None, **kwargs):
        method = str(method).lower()  # 转换小写
        # 基础路径的拼接和替换
        # print(url) # /admin/login
        # print(type(url)) # <class 'str'>
        url = self.base_url + self.replace_value(url)

        # 参数替换(request下面的参数 kwargs=data/json/params/headers
        for key, value in kwargs.items():
            # print(value) # {'token': '${token}'}
            if key in ['params', 'data', 'json', 'headers']:
                kwargs[key] = self.replace_value(value)
            elif key == "files":
                for file_key, file_path in value.items():
                    value[file_key] = open(file_path, 'rb')
        # 处理日志
        if 'headers' not in kwargs.keys():
            kwargs['headers'] = self.headers
        if 'data' not in kwargs.keys():
            kwargs['data'] = self.data
        if 'json' not in kwargs.keys():
            kwargs['json'] = self.json
        if 'files' not in kwargs.keys():
            kwargs['files'] = self.files
        if 'params' not in kwargs.keys():
            kwargs['params'] = self.params
        # 将接口发起前的信息记录到日志中
        self.logger.info('--------------------接口开始--------------------')
        self.logger.info(f"接口的名称是：{testName}")
        self.logger.info(f"接口的所属模块是：{moduleName}")
        self.logger.info(f"接口的url是：{url}")

        for key, value in kwargs.items(): # 要考虑提供的yaml没有这个属性值的情况,上面的处理是取初始值
            self.logger.info(f'接口的{key}是：{value}')
        try:
            self.resp = self.session.request(method, url, **kwargs)
            # print(self.logger.info(f'接口响应状态码是：{self.resp.status_code}')) # None
            self.logger.info(f'接口响应状态码是：{self.resp.status_code}')
            # print(self.logger.info(f'接口响应信息是：{self.resp.text}')) # None
            self.logger.info(f'接口响应信息是：{self.resp.text}')
            self.logger.info(f'接口断言信息：响应码是否为:{status_code}、响应信息中是否包含:{assert_str}')
            self.logger.info('--------------------接口结束--------------------'+"\n")
        except BaseException as e:
            self.logger.exception('接口请求报错！')
            raise BaseException(f'接口报错信息：{e}')
        print(self.resp.text)
        return self.resp

    # 替换值的方法 处理yaml文件中的 ${}  如:${token}
    # (替换url,params,data,json,headers)
    # (string,int,float,list,dict)
    def replace_value(self, data):
        if data:
            # 保存数据类型
            data_type = type(data) # 字典 dict
            # 判断数据类型转换成str (因为需要对${}部分进行替换)
            if isinstance(data, dict) or isinstance(data, list):
                # json.dumps() 用于将dict类型的数据转成str
                str_data = json.dumps(data)
                # print(type(data)) # <class 'dict'>
            else:
                str_data = str(data)
            # 处理yaml文件中的 ${token}
            for cs in range(1, str_data.count('${') + 1): # str_data.count('${') 为0 则不处理
                # 替换
                if "${" in str_data and "}" in str_data:
                    # index() 函数用于从序列s中找出某个值第一个出现时的索引位置。
                    start_index = str_data.index("${") # 0
                    end_index = str_data.index("}", start_index) # 从${的后面开始找起
                    old_value = str_data[start_index:end_index + 1] # 0:6+1 = 0:7 ${token} 就是获取到需要作替换的${xxx}
                    # print(str_data) # {"token": "${token}"}
                    # print(old_value) # ${token}
                    # print(old_value[2:-1])  # token 就是获取到需要作替换的 xxx

                    # ---------------热加载去除-------------------
                    # new_value = YamlUtil().read_yaml(old_value[2:-1]) # 读取token
                    # str_data = str_data.replace(old_value, new_value)
                    # ---------------热加载去除-------------------

                    # ---------------热加载新增-------------------
                    # print("old_value:" + old_value) # ${token}
                    if "(" in old_value and ")" in old_value:
                        # 反射：通过类的对象和方法字符串调用方法
                        func_name = old_value[2:old_value.index('(')]  # 取到方法名
                        args_value1 = old_value[old_value.index('(') + 1:old_value.index(')')]  # 取到xxx,如:token
                        args_value2 = args_value1.split(',')
                        new_value = getattr(self.obj, func_name)(*args_value2)
                    else:
                        new_value = YamlUtil().read_yaml(old_value[2:-1])  # 读取token
                    str_data = str_data.replace(old_value, new_value)
                    # ---------------热加载新增-------------------
            # 还原数据类型
            if isinstance(data, dict) or isinstance(data, list):
                # print(type(data)) # <class 'dict'>
                # json.loads() 用于将str类型的数据转成dict。
                data = json.loads(str_data)
            else:
                data = data_type(str_data) # 或 str(str_data)
                # print(data_type(str_data)) # /admin/login
                # print(type(data)) # <class 'str'>
        return data

    # 断言
    def assert_result(self, dy_result, return_json, return_code):
        # print(f"dy_result:{dy_result}")  # [{'equals': {'status_code': 200}}, {'contains': '用户名错误'}]
        # print(f"return_json:{return_json}")  # {'msg': '用户名错误', 'errorCode': 20000}
        # print(f"return_code:{return_code}")  # 400
        # print(type(return_code))  # int 整型
        all_flag = 0
        for dy in dy_result:
            for key, value in dy.items():
                # print(key, value)  # "equals" "{'status_code': 200/400....}" | "contains" "用户名错误"/.....
                if key == "equals":
                    flag = self.equals_assert(value, return_code, return_json)  # 调用相等断言
                    all_flag = all_flag + flag
                elif key == 'contains':
                    flag = self.contains_assert(value, return_json)  # 调用包含断言
                    all_flag = all_flag + flag
                else:
                    print("框架暂不支持此段断言方式")
        assert all_flag == 0

    # 相等断言
    def equals_assert(self, value, return_code, return_json):
        flag = 0
        for assert_key, assert_value in value.items():
            # print(assert_key, assert_value)  # status_code 200/400
            if assert_key == "status_code":  # 状态断言
                assert_value == return_code
                if assert_value != return_code:
                    flag = flag + 1
                    print("断言失败，返回的状态码不等于%s" % assert_value)
            else:
                lists = jsonpath.jsonpath(return_json, '$..%s' % assert_key)
                if lists:
                    if assert_value not in lists:
                        flag = flag + 1
                        print("断言失败：" + assert_key + "不等于" + str(assert_value))
                else:
                    flag = flag + 1
                    print("断言失败：返回的结果不存在：" + assert_key)
        return flag

    # 包含断言
    def contains_assert(self, value, return_json):
        flag = 0
        if value not in str(return_json):  # {'msg': '用户名错误', 'errorCode': 20000}
            flag = flag + 1
            print("断言失败：返回的结果中不包含：" + value)
        return flag

# 日志:
# if __name__ == '__main__':
#     userinfo = {
#         "username": "admin",
#         "password": "admin"
#     }
#     request = SendRequest()
#     resp = request.all_send_request(method='post', url='http://ceshi13.dishait.cn/admin/login', data=userinfo)
#     print(resp.json())
