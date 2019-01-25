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
    weibo_list = acquire_weibo_list()
    username = acquire_username()
    print('debug username in weibo index page:', username)
    return render_template('weibo_index.html', weibos=weibo_list, username=username)


def acquire_weibo_list():
    weibo_list = r.lrange('weibo_list', 0, -1)
    if weibo_list:
        weibo_list = [json.loads(i) for i in weibo_list]
    else:
        weibo_list = []
    return weibo_list


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
    }

    # weibo这里不好直接用weibo作为key，将来查询特定id的微博的时候不好查
    # 这里应该跟user表设计那样，把主键值设置到key中，方便后面查询
    # 这样一来，value中也就没有必要保存一份weiboid了
    r.hmset('weibo:weiboid:{}'.format(weiboid), weibo_dict)

    # 发微博的时候还要将这条微博推送给自己的粉丝
    my_fans = r.smembers('follower:userid:{}'.format(current_userid()))

    weibo_obj = r.hgetall('weibo:weiboid:{}'.format(weiboid))

    weibo_obj = json.dumps(weibo_obj)
    print('debug weibo_obj:', weibo_obj)

    r.rpush('weibo_list', weibo_obj)
    print('debug weibo_list:', r.lrange('weibo_list', 0, -1))

    # 保存到数据库中了之后，我们需要传递一个微博对象的列表到html页面中去
    # 这里使用一个namedtuple来表示一个对象，没有必要定义一个类来表示（后面如果方法多了再考虑使用类）
    # Weibo = namedtuple('Weibo', 'content author create_time')
    # weibo = Weibo(content=content, author=author, create_time=create_time)

    print('用户成功创建了一条微博：', content)

    # 找到了我的粉丝之后，需要将我自己发送的微博发送给我的粉丝们
    # 下面就又需要为每个人建立一张表，用来保存这个用户接收到的微博的列表
    # 因为微博虽然很多，但是并不是每条微博都会被每个人看到，
    # 所以只需要维护一个只有1000条记录的微博，够看就可以了。
    # 如果微博实在是太多，那么就需要调数据库来存储了，不能全部放在内存中
    my_fans.add(current_userid())
    print('debug my_fans:', my_fans)
    print('debug type my_fans:', type(my_fans))

    for fans_id in my_fans:
        print('debug fans_id:', fans_id)
        print('debug weiboid:', weiboid)
        r.lpush('receive_weibo:{}'.format(fans_id), weiboid)

    return redirect(url_for('.index'))


@main.route('/timeline', methods=['GET', 'POST'])
@login_required
def timeline():
    weibo_list = acquire_weibo_list()
    user_name_list = r.sort('new_user_list', get='user:userid:*:username', by='global:userid')
    # user_name_list = [item.decode('utf8') for item in user_name_list]
    print('debug user_name_list:', user_name_list)
    return render_template('timeline.html', weibo_list=weibo_list, user_list=user_name_list)

