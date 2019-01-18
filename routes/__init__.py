from flask import Blueprint
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for

import redis
r = redis.StrictRedis(host='localhost', port=6379, db=0)

