
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
    print('register called')
    form = request.form
    print('debug register form', form)
    r.set('user:name', form.get('username'))
    r.set('user:password', form.get('password'))
    r.incr('global:userid')
    userid = r.get('global:userid')
    r.set('user:id', userid)
    session['user_id'] = userid

    return redirect(url_for('.index'))





