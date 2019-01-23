# from models.weibo import Weibo
import json

from routes import *

from collections import namedtuple

main = Blueprint('weibo', __name__)



@main.route('/')
@login_required
def index():
    print('weibo index was called')
    # weibo_list = Weibo.query.order_by(Weibo.id.desc()).all()

    # 注意，这里需要取出来所有的微博，所以不能简单地用lpop，应为lpop只能取出来一个元素
    # weibo_list = r.lpop('weibo_list')
    weibo_list = r.lrange('weibo_list', 0, -1)
    if weibo_list:
        weibo_list = [json.loads(i) for i in weibo_list]
    else:
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
    print('debug input weibo content:', content)
    # 微博内容合法性检测
    if not content:
        print('微博内容不能为空')
        return

    r.incr('global:weiboid')
    weiboid = int(r.get('global:weiboid'))
    create_time = format_instant_time()
    author = acquire_username()

    # 由于weibo需要用到其很多属性，用key：value来保存取信息的时候不方便
    # 这里需要作为一个对象来存储，故需要用hash这个数据结构来保存微博
    weibo_dict = {
        'create_time': create_time,
        'author': author,
        'content': content,
        'weiboid': weiboid,
    }
    r.hmset('weibo', weibo_dict)
    weibo_obj = r.hgetall('weibo')
    weibo_obj = json.dumps(weibo_obj)
    r.rpush('weibo_list', weibo_obj)

    # 保存到数据库中了之后，我们需要传递一个微博对象的列表到html页面中去
    # 这里使用一个namedtuple来表示一个对象，没有必要定义一个类来表示（后面如果方法多了再考虑使用类）
    # Weibo = namedtuple('Weibo', 'content author create_time')
    # weibo = Weibo(content=content, author=author, create_time=create_time)

    print('用户成功创建了一条微博：', content)
    return redirect(url_for('.index'))


@main.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    weibo_list = []
    user_name_list = r.sort('new_user_list', get='user:userid:*:username', by='global:userid')
    # user_name_list = [item.decode('utf8') for item in user_name_list]
    print('debug user_name_list:', user_name_list)
    return render_template('timeline.html', weibo_list=weibo_list, user_list=user_name_list)

