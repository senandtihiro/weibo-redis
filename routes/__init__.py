import redis

from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import session

from functools import wraps

r = redis.StrictRedis(host='localhost', port=6379, db=0)


def acquire_username():
    userid = session.get('user_id')
    print('debug userid:', userid)
    key_username = 'user:userid:{}:username'.format(userid)
    username = r.get(key_username)
    print('debug username:', username)
    if username:
        return username.decode('utf8')
    return username


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        userid = session.get('user_id')
        if not userid:
            print('没有登陆，不能看到微博界面')
            return render_template('user_login.html')
        print('{}登陆成功，现在可以查看微博界面'.format(userid))
        return func(*args, **kwargs)
    return wrapper
