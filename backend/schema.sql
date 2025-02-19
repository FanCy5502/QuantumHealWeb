-- 删除表（如果存在），以便重新初始化数据库
DROP TABLE IF EXISTS doctor;
DROP TABLE IF EXISTS patient;
DROP TABLE IF EXISTS tumor_set;
DROP TABLE IF EXISTS tumor_data;

-- 创建医生信息表
CREATE TABLE doctor (
    doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 医生ID，自增主键
    username TEXT NOT NULL,  -- 医生用户名
    password TEXT NOT NULL  -- 医生密码
);

-- 创建患者信息表
CREATE TABLE patient (
    patient_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 患者ID，自增主键
    doctor_id INTEGER NOT NULL,  -- 该患者所属医生的ID
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE
);

-- 创建肿瘤数据集表（唯一标识一个患者的肿瘤）
CREATE TABLE tumor_set (
    tumor_set_id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 肿瘤数据集ID
    patient_id INTEGER NOT NULL,  -- 该肿瘤数据所属的患者
    doctor_id INTEGER NOT NULL,  -- 该患者所属医生的ID（冗余存储，方便查询）
    upload_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- 统一的上传时间
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE
);

-- 创建肿瘤体素数据表（体素级数据）
CREATE TABLE tumor_data (
    Xsparse INTEGER NOT NULL,  -- 体素坐标X
    Ysparse INTEGER NOT NULL,  -- 体素坐标Y
    Zsparse INTEGER NOT NULL,  -- 体素坐标Z
    PETsparse REAL NOT NULL,  -- 记录SUV值（无论是放疗前还是放疗后）
    DoseSparse REAL NOT NULL,  -- 放疗剂量
    tumor_set_id INTEGER NOT NULL,  -- 该体素所属肿瘤数据集ID
    is_post_treatment BOOLEAN NOT NULL,  -- 放疗前(0)或放疗后(1)（预测数据）
    cluster_label INTEGER,  -- 体素的聚类结果（0,1,2,3），仅放疗前数据有值
    FOREIGN KEY (tumor_set_id) REFERENCES tumor_set(tumor_set_id) ON DELETE CASCADE
);
