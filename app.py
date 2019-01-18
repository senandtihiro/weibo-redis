from flask import Flask
from flask_script import Manager

from routes.weibo import main as routes_weibo
from routes.user import main as routes_user


app = Flask(__name__)
manager = Manager(app)

def register_routes(app):
    app.register_blueprint(routes_weibo)
    app.register_blueprint(routes_user, url_prefix='/login')


def configure_app():
    app.secret_key = 'secret key'
    register_routes(app)


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    print('server run')
    # app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=5001,
    )
    app.run(**config)


if __name__ == '__main__':
    configure_app()
    manager.run()


