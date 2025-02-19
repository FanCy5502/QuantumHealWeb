# 认证蓝图：注册新用户、登录和注销视图
import os
import random
from pathlib import Path
import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 注册视图
@bp.route('/register', methods=['GET', 'POST'])
def register():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    if not username or not password :
        return jsonify({
            'success': False,
            'message': 'aaa注册失败，用户名或密码为空'
        })
    db = get_db()
    try:
        db.execute(
            "INSERT INTO doctor (username,password) VALUES (?,?)",
            (username, generate_password_hash(password)),
        )
        db.commit()
    except db.IntegrityError:
        return jsonify({
            'success': False,
            'message': '注册失败，该用户名已经注册过'
        })
    return jsonify({
        'success': True,
        'message': '注册成功'
    })

# 登录视图
@bp.route('/login', methods=['GET', 'POST'])
def login():
    username = request.get_json().get('username')
    password = request.get_json().get('password')
    db = get_db()
    user = db.execute(
        'SELECT * FROM doctor WHERE username = ? ', (username,)
    ).fetchone()
    if user is None:
        return jsonify({
            'success': False,
            'message': '登录失败，不存在的用户名'
        })
    elif not check_password_hash(user['password'], password):  # 匹配密码
        print(generate_password_hash(password))
        print('user[password]: ', user['password'])
        print('password: ', password)
        return jsonify({
            'success': False,
            'message': '登录失败，密码错误'
        })
    # 验证成功后，用户id存储在以新会话（session:用于存储横跨请求的值的dict）中;session数据会存储到一个向浏览器发送的cookie中。
    session.clear()
    session['user_id'] = user['doctor_id']
    return jsonify({
        'success': True,
        'message': '登录成功'
    })

@bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({
        'success': True,
        'message': '登出成功'
    })