
from models.user import User
from routes import *


main = Blueprint('user', __name__)

@main.route('/')
def index():
    print('login called')
    userid = session.get('user_id')
    if userid:
        return redirect(url_for('weibo.index'))
    else:
        return render_template('user_login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    '''
    user:userid:{}:username
    user:userid:{}:password
    :return:
    '''
    print('register called')
    form = request.form
    print('debug register form', form)

    # 每注册一个用户，用户的id自增
    r.incr('global:userid')
    userid = int(r.get('global:userid'))

    # 重新构建用户名和密码的key
    username = 'user:userid:{}:username'.format(userid)
    password = 'user:userid:{}:password'.format(userid)

    input_username = form.get('username')
    input_password = form.get('password')
    print('debug when register, userid, input_username, input_password', userid, input_username, input_password)

    # 有时还需要根据username来查userid，所以需要另外存一份
    # user:username:hhh:userid: 2
    # 这样一个键值对
    r.set('user:username:{}:userid'.format(input_username), userid)

    # 设置用户名和密码的value
    r.set(username, input_username)
    r.set(password, input_password)

    # 通过一个list维护一个50个最新的userid
    r.lpush('new_user_list', userid)
    # 剪切list，从0到最后一个（list是左闭右闭区间）
    r.ltrim(0, 49)

    print('debug username:', username)
    print('debug password:', password)
    return redirect(url_for('.index'))


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = request.form
    input_username = form.get('username')
    input_password = form.get('password')
    print('debug when login username_input:', input_username)
    print('debug when login password_input:', input_password)

    # 首先判断用户是否注册，即username是否存在
    # 方法是根据username去查userid是否存在，如果存在，说明已经注册过了；否则跳转到注册界面
    key_userid = 'user:username:{}:userid'.format(input_username)
    userid = r.get(key_userid)
    print('debug userid')
    if not userid:
        print('登陆失败，因为还未注册')
        return render_template('user_register.html')

    print('该用户已经注册过了')
    # 根据用户名去查找id，再根据id去查找password 看看这个password是否是用户输入对password
    # 如果是，则登陆成功，跳转到微博主页，否则，重定向到登陆界面重新登陆
    key_userid = int(r.get('user:username:{}:userid'.format(input_username)))
    key_password = 'user:userid:{}:password'.format(key_userid)
    print('debug key_userid:', key_userid)
    print('debug key_password:', key_password)
    password_db = r.get(key_password).decode('utf8')
    print('debug when login password_db:', password_db)
    if input_password == password_db:
        print('登录成功')
        session['user_id'] = key_userid
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.index'))



@main.route('/logout', methods=['GET', 'POST'])
def logout():
    print('退出登陆状态')
    session.pop('user_id')
    return render_template('user_login.html')