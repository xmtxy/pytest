
from time import sleep

import pytest #找到测试用例,执行
import requests #发送请求的包

from common.send_request import SendRequest  #导入公共的请求类
from common.yaml_util import write_yaml, read_yaml  #yaml文件的操作

# scope="function"-为函数级别  scope="class"-类级别 scope="session"-表示回话 autouse=False-不自动执行 params-数据驱动  ids-数据驱动的别名 name-别名
# @pytest.fixture(scope="class",autouse=False,params=["xM",'小黑子'],ids=['xM','IKUN'],name="db")
# def execute_db_connection(request):
#     print("连接数据库连接")
#     # yield 上面是用例之前的处理,下面是用例之后的处理 爷的
#     # request 返回值
#     yield request.param
#     print("关闭数据库连接")
class TestApi:
    # accessToken=""  #需要优化,其它的.py文件需要使用的话需要导入这个定义的类,然后.py文件执行也会执行下面的方法
    # 优化:将token保存在yaml文件中
    """
    def setup(self):
        print("用例之前")
    def teardown(self):
        print("用例之后")
    def setup_class(self):
        print("类之前")
    def teardown_class(self):
        print("类之后")
    这几个测试用例对所有的都生效,但是我想某个用例不执行,或者某个用例执行?
    比如:登录用例,不需要再执行类之前,其它不需要token的不需要用例之前或之后.....
    """
    # 优化 解决:用fixture 非斯扯  装饰器

    # 1.登录API
    # @pytest.mark.smoke
    # @pytest.mark.run(order=1)
    def test_login(self):
        url = "http://ceshi13.dishait.cn/admin/login"
        userinfo = {
            "username":"admin",
            "password":"admin"
        }
        # # res = requests.post(url=url,data=userinfo)
        res=SendRequest().all_send_request(method="post", url=url, data=userinfo)
        # # TestApi.accessToken=res.json()['data']['token']
        # write_yaml({"accessToken":[res.json()['data']['token']]}) #存储在yaml文件中
        write_yaml({"accessToken":res.json()['data']['token']}) #存储在yaml文件中


    # 2.获取管理员列表API
    # 标记
    # @pytest.mark.user_manager
    # 跳过
    # @pytest.mark.skip(reason="该版本不执行")
    # 执行顺序
    # @pytest.mark.run(order=2)
    def test_manager(self):
    # def test_manager(self,db): #执行多次,因为做了数据驱动
        page = 1
        url = f"http://ceshi13.dishait.cn/admin/manager/{page}"
        # headers = {
        #     # "token": TestApi.accessToken
        #     "token": read_yaml("accessToken")  #从yaml文件中读取token
        # }
        params = {
            "limit":10,
            "keyword":"admin"
        }
        # res=requests.get(url=url,headers=headers)
        # res = SendRequest().all_send_request(method="get", url=url, headers=headers, params=params)
        # print(res.json())
        # raise Exception("小黑子")  #自动抛出异常
        # print(db)

# 问题点:
# 1.token的关联:可以设置一个全局的token然后通过类名去调用这个token,但是引发了一个新的问题:2
# 2.参数token的问题,在其他的.py文件引入时,会同时执行这类里面所有的测试用例,解决:将token的数据存放在yaml文件中,然后再读取
# 3.但是引发了一个新的问题:接口再次执行时会再次生成多个相同的属性名,导致yaml文件出现红色下划线,如何解决?
# 解决思路:在整个项目之前去清空yaml文件,需要调用clear_yaml()方法

# 4.类和用例之前和之后执行的setup、teardown、setup_class、teardown_class,有一个问题是他们是对所有的用例都触发的,如何解决?
# 5.方法如下:
# scope="function"-为函数级别  scope="class"-类级别 autouse=False-不自动执行 params-数据驱动  ids-数据驱动的别名 name-别名
# @pytest.fixture(scope="class",autouse=False,params=["xM",'小黑子'],ids=['xM','IKUN'],name="db")
# def execute_db_connection(request):
#     print("连接数据库连接")
#     # yield 上面是用例之前的处理,下面是用例之后的处理 爷的
#     # request 返回值
#     yield request.param
#     print("关闭数据库连接")
# 如果设置,需要通过别名去调用,否则要通过定义的 execute_db_connection去调用(其中autouse=False),autouse=True则都不需要操作
