
from models.user import User
from routes import *


main = Blueprint('user', __name__)

@main.route('/')
def index():
    print('login called')
    weibo_list = []
    userid = session.get('user_id')
    print('debug user:', userid)
    if userid:
        return redirect(url_for('weibo.index', weibos=weibo_list))
    else:
        return render_template('user_register.html')


@main.route('/register', methods=['POST'])
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
    r.set('user:username:{}:userid'.format(input_username), userid)

    # 设置用户名和密码的value
    r.set(username, input_username)
    r.set(password, input_password)

    session['user_id'] = userid
    return redirect(url_for('.index'))





