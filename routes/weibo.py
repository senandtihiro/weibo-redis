from models.weibo import Weibo
from routes import *


main = Blueprint('weibo', __name__)



@main.route('/')
@login_required
def index():
    print('weibo index was called')
    # weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()
    weibo_list = []
    username = acquire_username()
    return render_template('weibo_index.html', weibos=weibo_list, username=username)


@main.route('/add', methods=['POST'])
def add():
    print('add called')
    form = request.form
    print('debug add form', form)
    weibo = Weibo(form)
    weibo.id += 1
    print('debug weibo:', weibo.id)
    print('debug weibo:', weibo.weibo)
    print('debug weibo:', weibo.created_time)

    return redirect(url_for('.index'))


@main.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    weibo_list = []
    user_name_list = r.sort('new_user_list', get='user:userid:*:username', by='global:userid')
    user_name_list = [item.decode('utf8') for item in user_name_list]
    print('debug user_name_list:', user_name_list)
    return render_template('timeline.html', weibo_list=weibo_list, user_list=user_name_list)

