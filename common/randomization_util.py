# 随机数的处理方法

"""
我们需要yaml文件中实现动态参数变化?
热加载:就是在代码执行过程当中动态的调用Python中的方法达到或得动态参数的目的
"""

import random
import time
from common.yaml_util import YamlUtil


class DebugTalk:

    # 获得随机数
    def get_randon_number(self, min, max):
        return random.randint(int(min), int(max))

    # 读取extract.yaml文件中的值
    def read_extract_data(self, key):
        return YamlUtil().read_yaml(key)