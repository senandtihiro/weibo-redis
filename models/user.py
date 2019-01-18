import time

class User:
    # 下面是字段定义
    def __init__(self, form):
        format = '%Y/%m/%d %H:%M:%S'
        v = int(time.time()) + 3600 * 8
        valuegmt = time.gmtime(v)
        dt = time.strftime(format, valuegmt)
        self.userid = 0
        self.name = form.get('username', '')
        self.password = form.get('password', '')
        self.created_time = dt
