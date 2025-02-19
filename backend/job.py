from flask import (
    Blueprint, request, jsonify
)
import os
import sqlite3
from utils import generate_bar_chart_html, generate_pie_chart_html, generate_salary_bar_chart_html
import random
from collections import Counter

bp = Blueprint('job', __name__)  # 无urlprefix，因此用于根目录

# 获取数据库连接
def get_db_connection():
    conn = sqlite3.connect('boss.db')
    conn.row_factory = sqlite3.Row  # 为了能够按列名访问数据
    return conn

@bp.route('/job', methods=['GET'])
def get_jobs():
    selected_keywords = request.args.getlist('keywords[]')
    
    # 获取招聘信息
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM job_message_table")
    jobs = cursor.fetchall()
    conn.close()

    # 过滤招聘信息
    if selected_keywords:
        filtered_jobs = []
        for job in jobs:
            job_keywords = eval(job['key_words'])
            if all(keyword in job_keywords for keyword in selected_keywords):
                filtered_jobs.append(job)
        jobs = filtered_jobs

    if len(jobs) > 20:
        sampled_jobs = random.sample(jobs, 20)
    else:
        sampled_jobs = jobs

    updated_jobs = []
    for job in sampled_jobs:
        job_dict = dict(job)
        job_dict['key_words'] = eval(job_dict['key_words'])
        duration_seconds = job_dict['duration']
        hours = duration_seconds // 3600
        minutes = (duration_seconds % 3600) // 60
        if hours == 0:
            job_dict['duration_hours_minutes'] = f"{minutes}分钟"
        else:
            job_dict['duration_hours_minutes'] = f"{hours}小时{minutes}分钟"
        updated_jobs.append(job_dict)

    # 获取关键词和薪资数据
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT key_words, salary_avg FROM job_message_table")
    rows = cursor.fetchall()
    conn.close()

    keyword_salary = {}
    all_keywords = []
    for row in rows:
        key_words = eval(row['key_words'])
        salary_avg = row['salary_avg']
        for keyword in key_words:
            if keyword not in keyword_salary:
                keyword_salary[keyword] = {'total_salary': 0, 'count': 0}
            keyword_salary[keyword]['total_salary'] += salary_avg
            keyword_salary[keyword]['count'] += 1
            all_keywords.append(keyword)

    avg_salary_by_keyword = {
        keyword: int(keyword_salary[keyword]['total_salary'] / keyword_salary[keyword]['count'])
        for keyword in keyword_salary
    }

    sorted_keywords = sorted(avg_salary_by_keyword.items(), key=lambda x: x[1], reverse=True)[:20]
    top_keywords = [k for k, v in sorted_keywords]
    top_avg_salaries = [v for k, v in sorted_keywords]

    labels, counts = zip(*Counter(all_keywords).most_common(20))
    all_keywords = list(labels)

    return jsonify({
        'jobs': updated_jobs,
        'all_keywords': all_keywords,
        'selected_keywords': selected_keywords,
        'bar_html': generate_bar_chart_html(labels, counts),
        'pie_html': generate_pie_chart_html(labels, counts),
        'salary_bar_html': generate_salary_bar_chart_html(top_keywords, top_avg_salaries)
    })

    