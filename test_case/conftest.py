# 用例执行前需要清除的yaml文件(如:token
import pytest
# from common.yaml_util import clear_yaml #(未添加类之前的调用方式

# scope="function"-为函数级别  scope="class"-类级别 scope="session"-表示回话 autouse=False-不自动执行 params-数据驱动  ids-数据驱动的别名 name-别名
# @pytest.fixture(scope="class",autouse=False,params=["xM",'小黑子'],ids=['xM','IKUN'],name="db")
# def execute_db_connection(request):
#     print("连接数据库连接")
#     # yield 上面是用例之前的处理,下面是用例之后的处理 爷的
#     # request 返回值
#     yield request.param
#     print("关闭数据库连接")
from common.yaml_util import YamlUtil  # (添加类之后的调用方式)


@pytest.fixture(scope="session", autouse=True)
def clear_yaml_data(request):
    YamlUtil().clear_yaml()