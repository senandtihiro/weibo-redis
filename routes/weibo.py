# from models.weibo import Weibo
from routes import *

from collections import namedtuple

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
@login_required
def add():
    '''
    微博保存在redis中的数据结构：
    主要需要保存三个要素：谁 什么时间 发了什么内容 的微博
    weibo:weiboid:2:create_time
    weibo:weiboid:2:author
    weibo:weiboid:2:content
    '''
    print('weibo add called')
    form = request.form
    print('debug weibo add form', form)
    content = form.get('content')

    # 微博内容合法性检测
    if not content:
        print('微博内容不能为空')
        return

    r.incr('global:weiboid')
    weiboid = r.get('global:postid')
    create_time = format_instant_time()
    author = acquire_username()
    r.set('weibo:weiboid:{}:create_time:'.format(weiboid), create_time)
    r.set('weibo:weiboid:{}:author:'.format(weiboid), author)
    r.set('weibo:weiboid:{}:content:'.format(weiboid), content)

    # 保存到数据库中了之后，我们需要传递一个微博对象的列表到html页面中去
    # 这里使用一个namedtuple来表示一个对象，没有必要定义一个类来表示（后面如果方法多了再考虑使用类）
    Weibo = namedtuple('Weibo', 'content author create_time')
    weibo = Weibo(content=content, author=author, create_time=create_time)
    print('debug weibo:', weibo.id)
    print('debug weibo:', weibo.content)
    print('debug weibo:', weibo.create_time)
    print('用户成功创建了一条微博：', content)
    return redirect(url_for('.index'))


@main.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    weibo_list = []
    user_name_list = r.sort('new_user_list', get='user:userid:*:username', by='global:userid')
    user_name_list = [item.decode('utf8') for item in user_name_list]
    print('debug user_name_list:', user_name_list)
    return render_template('timeline.html', weibo_list=weibo_list, user_list=user_name_list)

