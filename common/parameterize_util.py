# @pytest.mark.parametrize 和 yaml 结合的处理方法:

import json
from common.yaml_util import YamlUtil
import os
import yaml


# 读取测试用例(因为需要对数据进行进一步的处理....
def read_testcase(yaml_name):
    base_path = os.getcwd() + '\\test_case\\' + yaml_name
    # print(base_path)
    with open(base_path, mode='r', encoding='utf-8') as f:
        caseinfo = yaml.load(f, yaml.FullLoader)
        # print(caseinfo,len(caseinfo)) # [{"name":"$ddt{name},...."}] 1
        # print(dict(*caseinfo).keys()) # ['name', 'parameterize', 'request', 'extract', 'validate']
        # print(*caseinfo) # {"name":"$ddt{name},...."}
        if len(caseinfo) >= 2:  # 判断yaml用例文件中有几条用例,当用例大于等于2时,直接返回caseinfo === 不做数据驱动
            return caseinfo
        else:  # 当等于1时,因为数据驱动后的caseinfo是字典列表我们就需要对caseinfo解包
            if "parameterize" in dict(*caseinfo).keys():  # 转化成字典
                new_caseinfo = ddt(*caseinfo)  # 调用下面的方法
                # print(new_caseinfo)
                return new_caseinfo
            elif "datas" in dict(*caseinfo).keys():
                new_caseinfo = step(*caseinfo)  # 调用下面的方法
                return new_caseinfo
            else:
                return caseinfo


def ddt(caseinfo):  # 传入的值是集合{"name":"$ddt{name}",......}
    if "parameterize" in caseinfo.keys(): # {'name', 'parameterize', 'request', 'extract', 'validate'}
        caseinfo_str = json.dumps(caseinfo)  # 判断parameterize是否在caseinfo中,返回原数据
        # print(caseinfo_str)  # {"name":"$ddt{name}",......}
        # for 循环遍历 得到每一对的()
        for param_key, param_value in caseinfo["parameterize"].items(): # d.items()返回字典中的所有键值对信息 [(),(),...]
            # print(caseinfo["parameterize"].items()) # dict_items([('name-username-password-project-assert_str', '/datas/Pm_Login_List.yaml')])
            key_list = param_key.split("-")  # 将param_key转成列表 # 就是将 name-username-password-project-assert_str 转化成列表
            data_list = YamlUtil().read_all_yaml(param_value)  # 读取param_value
            # print(data_list) # [['name', 'username', 'password', 'project', 'assert_str'], ['登录成功-获取token', 'admin', 'admin', 'DEFAULT', 'data'],...]
             # 规范yaml数据文件的写法(不一致就退出执行
            length_flag = True
            # for 循环遍历
            for data in data_list:
                if len(data) != len(key_list):
                    length_flag = False
                    break
            # 替换值( length_flag = True 后执行的逻辑....
            new_caseinfo = []
            if length_flag:
                for x in range(1, len(data_list)):  # 循环数据的行数 1,2,3,4  === 测试数据的条数
                    # print(x)
                    temp_caseinfo = caseinfo_str
                    for y in range(0, len(data_list[x])):  # 循环数据列-读取值 0,1,2,3,4  === 每一条测试数据的元素个数
                        # print(y)
                        if data_list[0][y] in key_list:  #[['name', 'username', 'password', 'project', 'assert_str'],[],..] 每一个值循环一次,所以需要内外层都循环
                            # 替换原始的yaml里面的 $ddt{xxx}
                            # a = 2 isinstance(a,int) # 结果返回 True
                            if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                                temp_caseinfo = temp_caseinfo.replace('"$ddt{' + data_list[0][y] + '}"',
                                                                      str(data_list[x][y]))
                            else:
                                temp_caseinfo = temp_caseinfo.replace("$ddt{" + data_list[0][y] + "}",
                                                                      str(data_list[x][y]))  # 从1开始,也就是第二条测试数据去取数据
                    new_caseinfo.append(json.loads(temp_caseinfo))

        # print(new_caseinfo) # [{'name':'xxx',......}]
        # print(type(new_caseinfo)) # list
        return new_caseinfo
    else:
        return caseinfo

def step(caseinfo):
    if "datas" in caseinfo.keys():
        caseinfo_str = json.dumps(caseinfo)  # 判断datas是否在caseinfo中,返回原数据
        # print(caseinfo_str)
        # for 循环遍历 得到每一对的()
        for param_key, param_value in caseinfo["datas"].items():  # d.items()返回字典中的所有键值对信息 [(),(),...]
            key_list = param_key.split("-")  # 将param_key转成列表 # 就是将 one-two-three-four-five-six-seven-eight-nine-ten 转化成列表
            data_list = YamlUtil().read_all_yaml(param_value)  # 读取param_value
            # print(key_list)
            # print(data_list)  # [[....], ['输入正确账号', '输入正确密码', '点击登录'],...]
            # 规范yaml数据文件的写法(不一致就退出执行
            length_flag = True
            # for 循环遍历
            """
            for data in data_list:
                if len(data) != len(key_list):
                    print(len(data))
                    data.append(' ')
                    print(len(data))
                    print(len(key_list))
                    length_flag = False
                    break
                print(data)  # ['one',...][][][]...
            """
            for data in data_list:
                for i in range(len(key_list)-len(data)):
                    data.append('None')
            # 替换值( length_flag = True 后执行的逻辑....
            new_caseinfo = []
            if length_flag:
                for x in range(1, len(data_list)):  # 循环数据的行数 1,2,3,4  === 测试数据的条数
                    temp_caseinfo = caseinfo_str
                    for y in range(0, len(data_list[x])):  # 循环数据列-读取值 0,1,2,3,4  === 每一条测试数据的元素个数
                        # print(key_list)['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten']
                        if data_list[0][y] in key_list:  # 每一个值循环一次,所以需要内外层都循环
                            # 替换原始的yaml里面的 $ddt{xxx}
                            # a = 2 isinstance(a,int) # 结果返回 True
                            if isinstance(data_list[x][y], int) or isinstance(data_list[x][y], float):
                                temp_caseinfo = temp_caseinfo.replace('"$step{' + data_list[0][y] + '}"',
                                                                      str(data_list[x][y]))
                            else:
                                print(data_list[x][y])
                                temp_caseinfo = temp_caseinfo.replace("$step{" + data_list[0][y] + "}",
                                                                      str(data_list[x][y]))  # 从1开始,也就是第二条测试数据去取数据

                    new_caseinfo.append(json.loads(temp_caseinfo))

            # print(new_caseinfo) # [{'name':'xxx',......}]
            # print(type(new_caseinfo)) # list
        return new_caseinfo
    else:
        return caseinfo
