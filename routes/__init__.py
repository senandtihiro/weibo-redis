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
    username = session.get('username')
    print('current username is:', username)
    return username


def current_userid():
    username = acquire_username()
    key_userid = 'user:username:{}:userid'.format(username)
    userid = r.get(key_userid)
    print('current user id:', userid)
    return userid


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
