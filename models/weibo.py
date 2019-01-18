import time
from models import *


class Weibo:
    # 下面是字段定义
    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.id = 0
        self.weibo = form.get('weibo', '')
        self.created_time = dt

