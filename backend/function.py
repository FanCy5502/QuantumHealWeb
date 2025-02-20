import os
import pandas as pd
from flask import Blueprint, request, jsonify, session
from werkzeug.utils import secure_filename
from datetime import datetime
from db import get_db  # 确保你有 `get_db` 连接数据库

UPLOAD_FOLDER = 'uploads'  # 存放上传文件的文件夹
ALLOWED_EXTENSIONS = {'xlsx'}
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

bp = Blueprint('function', __name__, url_prefix='/function')

@bp.route('/upload', methods=['POST'])
def upload_tumor_data():
    # 获取当前登录医生的 ID
    doctor_id = session.get('user_id')
    if not doctor_id:
        return jsonify({'success': False, 'message': '未登录'}), 401

    # 检查文件是否上传
    if 'file' not in request.files:
        return jsonify({'success': False, 'message': '未选择文件'}), 400
    
    file = request.files['file']
    
    if file.filename == '' or not allowed_file(file.filename):
        return jsonify({'success': False, 'message': '文件格式不正确，仅支持 .xlsx'}), 400

    # 保存文件
    filename = secure_filename(file.filename)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    # 读取 Excel 文件
    try:
        df = pd.read_excel(filepath, usecols=['Xsparse', 'Ysparse', 'Zsparse', 'PrePETsparse', 'DoseSparse'])
    except Exception as e:
        return jsonify({'success': False, 'message': f'文件读取失败: {str(e)}'}), 500

    db = get_db()
    cursor = db.cursor()

    # 插入患者信息并获取 `patient_id`
    cursor.execute("INSERT INTO patient (doctor_id) VALUES (?)", (doctor_id,))
    patient_id = cursor.lastrowid

    # 插入 `tumor_set` 并获取 `tumor_set_id`
    upload_timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute(
        "INSERT INTO tumor_set (patient_id, doctor_id, upload_timestamp) VALUES (?, ?, ?)",
        (patient_id, doctor_id, upload_timestamp)
    )
    tumor_set_id = cursor.lastrowid

    # 批量插入 `tumor_data`
    tumor_data_records = [
        (row.Xsparse, row.Ysparse, row.Zsparse, row.PrePETsparse, row.DoseSparse, tumor_set_id, None)
        for _, row in df.iterrows()
    ]

    cursor.executemany(
        "INSERT INTO tumor_data (Xsparse, Ysparse, Zsparse, PETsparse, DoseSparse, tumor_set_id, is_post_treatment, cluster_label) VALUES (?, ?, ?, ?, ?, ?, 0, ?)",
        tumor_data_records
    )

    query = """
        SELECT p.patient_id, ts.upload_timestamp, COUNT(td.tumor_set_id) as tumor_size
        FROM patient p
        JOIN tumor_set ts ON p.patient_id = ts.patient_id
        JOIN tumor_data td ON ts.tumor_set_id = td.tumor_set_id
        WHERE p.doctor_id = ?
        GROUP BY p.patient_id, ts.upload_timestamp
        ORDER BY ts.upload_timestamp DESC
    """
    a_patient = db.execute(query, (doctor_id,)).fetchall()

    db.commit()

    return jsonify({'success': True, 'message': f"数据上传成功！共有{len(tumor_data_records)}条体素数据,第一个体素的信息为：{a_patient[0]['tumor_size']}，历史上传的病例数为：{len(a_patient)}", 'tumor_set_id': tumor_set_id})

# 显示历史上传列表
@bp.route('/get_patient_list', methods=['GET'])
def get_patient_list():
    doctor_id = session.get('user_id')
    if not doctor_id:
        return jsonify({'success': False, 'message': '请先登录'}), 401

    db = get_db()
    query = """
        SELECT p.patient_id, ts.upload_timestamp, COUNT(td.tumor_set_id) as tumor_size
        FROM patient p
        JOIN tumor_set ts ON p.patient_id = ts.patient_id
        JOIN tumor_data td ON ts.tumor_set_id = td.tumor_set_id
        WHERE p.doctor_id = ?
        GROUP BY p.patient_id, ts.upload_timestamp
        ORDER BY ts.upload_timestamp DESC
    """
    patients = db.execute(query, (doctor_id,)).fetchall()
    
    result = []
    for row in patients:
        result.append({
            'patient_id': row['patient_id'],
            'tumor_size': row['tumor_size'],
            'upload_timestamp': row['upload_timestamp']
        })
        
    return jsonify({'success': True, 'patients': result})

