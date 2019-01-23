
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

    input_username = form.get('username')
    input_password = form.get('password')
    print('debug when register, input_username, input_password', input_username, input_password)

    # 用户名唯一性检测
    key_id = 'user:username:{}:userid'.format(input_username)
    id_exist = r.get(key_id)
    print('debug id_exist:', id_exist)
    if id_exist:
        print('该用户名已经存在，请重新选择用户名')
        return render_template('user_register.html')

    # 每注册一个用户，用户的id自增
    r.incr('global:userid')
    userid = int(r.get('global:userid'))

    # 重新构建用户名和密码的key
    key_username = 'user:userid:{}:username'.format(userid)
    key_password = 'user:userid:{}:password'.format(userid)

    # 有时还需要根据username来查userid，所以需要另外存一份
    # user:username:hhh:userid: 2
    # 这样一个键值对
    r.set('user:username:{}:userid'.format(input_username), userid)

    # 设置用户名和密码的value
    r.set(key_username, input_username)
    r.set(key_password, input_password)

    username = r.get(key_username)
    password = r.get(key_password)
    print('成功注册用户，ID， 用户名，密码：', userid , username, password)

    # 通过一个list维护一个50个最新的userid
    r.lpush('new_user_list', userid)
    # 剪切list，从0到最后一个（list是左闭右闭区间）
    r.ltrim('new_user_list', 0, 49)

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
    password_db = r.get(key_password)

    print('login userid is:', userid)
    username = r.get('user:userid:{}:username'.format(int(userid)))
    print('debug when login password_db:', password_db)
    if input_password == password_db:
        print('登录成功')
        session['username'] = username
    else:
        print('登录失败')
    # 蓝图中的 url_for 需要加上蓝图的名字，这里是 user
    return redirect(url_for('.index'))


@main.route('/logout', methods=['GET', 'POST'])
def logout():
    print('退出登陆状态')
    session.pop('username')
    return render_template('user_login.html')


@main.route('/profile/<string:username>', methods=['GET', 'POST'])
def profile(username):
    print('{} 的个人主页'.format(username))
    # weibo_list = r.get('weibo')
    weibo_list = []
    # weibo_list = [item.decode('utf8') for item in user_name_list]
    return render_template('user_profile.html', weibo_list=weibo_list)