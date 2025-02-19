import sqlite3
import click
from flask import current_app,g
from flask.cli import with_appcontext

# 连接数据库git
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

# 断开数据库连接
def close_db(e=None):
    db = g.pop('db',None)
    if db is not None: # 检查连接是否建立
        db.close()

# 初始化数据库
def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db) # 告诉 Flask 在返回响应后进行清理的时候调用close_db
    app.cli.add_command(init_db_command) # 添加命令init_db_command与 flask 一起工作
