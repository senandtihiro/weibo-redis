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



