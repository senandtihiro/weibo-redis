
from models.user import User
from routes import *


main = Blueprint('user', __name__)
user = None

@main.route('/')
def index():
    global user
    print('login called')
    weibo_list = []
    if user:
        return redirect(url_for('weibo.index'))
    else:
        return render_template('user_register.html')


@main.route('/register', methods=['POST'])
def register():
    global user
    print('register called')
    form = request.form
    print('debug register form', form)
    user = User(form)
    user.userid += 1
    print('debug user:', user.userid)
    print('debug user:', user.name)
    print('debug user:', user.password)

    return redirect(url_for('.index'))





