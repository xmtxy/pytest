import allure

from common.parameterize_util import read_testcase
from common.yaml_util import YamlUtil


class TestStep:
    def read_step(self, path_step):
        res = YamlUtil().read_all_yaml(path_step)
        for item in res:
            with allure.step(f'步骤{item[0]}：{item[1]}'):
                pass
    def read_step_yh(self,path_step):
        res = read_testcase(path_step)
        print(res)
        for item in res:
            with allure.step(f'{item["one"]}-{item["two"]}-{item["three"]}'):
                pass

