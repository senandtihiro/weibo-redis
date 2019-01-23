import redis
import time

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from functools import wraps

r = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)


def acquire_username():
    userid = session.get('user_id')
    print('debug userid:', userid)
    key_username = 'user:userid:{}:username'.format(userid)
    username = r.get(key_username)
    print('debug username:', username)
    if username:
        return username
    return username


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        username = session.get('username')
        # username = r.get('user:userid:{}:username:'.format(userid))
        print('when login, username:', username)
        if not username:
            print('in call func:', func.__name__)
            print('没有登陆，不能看到微博界面')
            return render_template('user_login.html')
        print('{}登陆成功，现在可以查看微博界面'.format(username))
        return func(*args, **kwargs)
    return wrapper


def format_instant_time():
    format = '%Y/%m/%d %H:%M:%S'
    v = int(time.time()) + 3600 * 8
    valuegmt = time.gmtime(v)
    dt = time.strftime(format, valuegmt)
    return dt
