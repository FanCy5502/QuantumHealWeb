from flask import Blueprint, request, jsonify, session
import sqlite3
import numpy as np
import json
from pyecharts.charts import Scatter3D
from pyecharts import options as opts
from sklearn.cluster import KMeans
from sklearn.linear_model import LinearRegression
from db import get_db  # 确保你有 `get_db` 连接数据库

bp = Blueprint('result', __name__, url_prefix='/result')

@@bp.route('/view_prediction/<int:patient_id>', methods=['GET'])
def view_prediction(patient_id):
    doctor_id = session.get('user_id')
    db = get_db()

    # 获取查询参数 pre（默认为 0，即放疗前）
    pre_treatment = int(request.args.get('pre', 0))  # 0: 放疗前, 1: 放疗后

    # 获取 tumor_set_id
    tumor_set = db.execute(
        "SELECT tumor_set_id FROM tumor_set WHERE patient_id = ?", (patient_id,)
    ).fetchone()
    if not tumor_set:
        return jsonify({'success': False, 'message': '未找到该患者的肿瘤数据'})
    tumor_set_id = tumor_set['tumor_set_id']

    # 处理放疗前数据请求
    if pre_treatment == 0:
        before_data = db.execute(
            "SELECT Xsparse, Ysparse, Zsparse, PETsparse FROM tumor_data WHERE tumor_set_id = ? AND is_post_treatment = 0",
            (tumor_set_id,)
        ).fetchall()
        if not before_data:
            return jsonify({'success': False, 'message': '未找到放疗前数据'})
        return jsonify({'success': True, 'data': format_3d_data(before_data, is_cluster=False)})

    # 处理放疗后数据请求（包括预测逻辑）
    elif pre_treatment == 1:
        after_data = db.execute(
            "SELECT Xsparse, Ysparse, Zsparse, PETsparse FROM tumor_data WHERE tumor_set_id = ? AND is_post_treatment = 1",
            (tumor_set_id,)
        ).fetchall()
        if after_data:
            return jsonify({'success': True, 'data': format_3d_data(after_data, is_cluster=False)})

        # 如果放疗后数据不存在，则进行预测
        input_data = db.execute(
            "SELECT Xsparse, Ysparse, Zsparse, DoseSparse FROM tumor_data WHERE tumor_set_id = ? AND is_post_treatment = 0",
            (tumor_set_id,)
        ).fetchall()
        if not input_data:
            return jsonify({'success': False, 'message': '无足够数据进行预测'})

        # 线性回归预测（示例）
        X = np.array([(row['DoseSparse'],) for row in input_data])
        y = np.random.normal(0, 0.1, len(X))  # 这里应替换为真实目标值
        model = LinearRegression()
        model.fit(X, y)
        predictions = model.predict(X)

        # 存入数据库
        for i, row in enumerate(input_data):
            db.execute(
                "INSERT INTO tumor_data (tumor_set_id, Xsparse, Ysparse, Zsparse, PETsparse, is_post_treatment) VALUES (?, ?, ?, ?, ?, 1)",
                (tumor_set_id, row['Xsparse'], row['Ysparse'], row['Zsparse'], predictions[i])
            )
        db.commit()

        return jsonify({'success': True, 'data': format_3d_data(input_data, values=predictions, is_cluster=False)})

    return jsonify({'success': False, 'message': '无效的参数'})

@bp.route('/view_clustering/<int:patient_id>', methods=['GET'])
def view_clustering(patient_id):
    doctor_id = session.get('user_id')
    db = get_db()
    
    # 获取该患者的肿瘤数据 ID
    tumor_set = db.execute(
        "SELECT tumor_set_id FROM tumor_set WHERE patient_id = ?", (patient_id,)
    ).fetchone()
    if not tumor_set:
        return jsonify({'success': False, 'message': '未找到该患者的肿瘤数据'})
    tumor_set_id = tumor_set['tumor_set_id']

    # 检查是否已有聚类数据
    existing_data = db.execute(
        "SELECT Xsparse, Ysparse, Zsparse, cluster_label FROM tumor_data WHERE tumor_set_id = ? AND is_post_treatment = 0 AND cluster_label IS NOT NULL",
        (tumor_set_id,)
    ).fetchall()
    
    if existing_data:
        return jsonify({'success': True, 'data': format_3d_data(existing_data, cluster=True)})
    
    # 获取原始数据进行聚类
    raw_data = db.execute(
        "SELECT Xsparse, Ysparse, Zsparse FROM tumor_data WHERE tumor_set_id = ? AND is_post_treatment = 0",
        (tumor_set_id,)
    ).fetchall()
    if not raw_data:
        return jsonify({'success': False, 'message': '无足够数据进行聚类'})
    
    # 进行KMeans聚类
    coords = np.array([(row['Xsparse'], row['Ysparse'], row['Zsparse']) for row in raw_data])
    kmeans = KMeans(n_clusters=3, random_state=42).fit(coords)
    labels = kmeans.labels_
    
    # 存入数据库
    for i, row in enumerate(raw_data):
        db.execute(
            "UPDATE tumor_data SET cluster_label = ? WHERE tumor_set_id = ? AND Xsparse = ? AND Ysparse = ? AND Zsparse = ?",
            (int(labels[i]), tumor_set_id, row['Xsparse'], row['Ysparse'], row['Zsparse'])
        )
    db.commit()
    
    # 返回 3D 画图数据
    return jsonify({'success': True, 'data': format_3d_data(raw_data, labels, cluster=True)})

def format_3d_data(data, values=None, cluster=False):
    points = []
    for i, row in enumerate(data):
        point = [row['Xsparse'], row['Ysparse'], row['Zsparse'], values[i] if values else row['PETsparse']]
        if cluster:
            point.append(row['cluster_label'] if 'cluster_label' in row else values[i])
        points.append(point)
    return points