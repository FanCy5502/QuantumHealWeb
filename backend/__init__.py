import os
from flask import Flask, redirect, url_for
from flask_cors import CORS

# 应用工厂函数
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    CORS(app, supports_credentials=True)  # 允许跨域
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    CORS(app, resources={r"/*": {"origins": "http://localhost:2025", "supports_credentials": True}})
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    # try:
    #     os.makedirs(app.instance_path)
    # except OSError:
    #     pass

    # 初始化数据库
    import db
    db.init_app(app)
    with app.app_context():
        db.init_db()

    # 认证蓝图：注册新用户、登录和注销视图
    import auth
    app.register_blueprint(auth.bp)

    # 功能蓝图：上传数据，预测、聚类结果生成和查询视图
    import function
    app.register_blueprint(function.bp)


    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))  # 重定向到 job 蓝图中的路由

    # # 招聘信息蓝图
    # import job
    # app.register_blueprint(job.bp)

    return app