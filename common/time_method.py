# 获取随机时间和本地时间的一个方法

import random
import time

from common.yaml_util import YamlUtil


class Test:
    # 获取随机时间
    def get_random_time(self):
        # return str(int(time.time()))[1:6]     #获取随机时间，得到的是时间戳
        return time.strftime('%H:%M:%S', time.localtime(time.time()))  # 获取本地时间，并将格式转换成时分秒

    # 读取extract.yaml文件中的值
    def read_extract_data(self, key):
        return YamlUtil().read_yaml(key)
