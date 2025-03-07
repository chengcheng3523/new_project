from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class users(db.Model):
    # 定義 'users' 資料表的 ORM 類別，對應到 MySQL 資料庫中的 'users' 表。
    __tablename__ = 'users'                                     # 設定資料表名稱為 'users'

    # 必填欄位
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)# 'id' 欄位：整數類型，作為主鍵 (Primary Key)，自動遞增
    username = db.Column(db.String(255), nullable=False) # 'username' 欄位：字串類型 (最多 255 個字元)，不可為空 (nullable=False)
    password = db.Column(db.String(255), nullable=False) # 'password' 欄位：字串類型 (最多 255 個字元)，不可為空 (nullable=False)
    unit_name = db.Column(db.String(255))       # 'unit_name' 欄位：字串類型 (最多 255 個字元)，不可為空，代表所屬單位名稱
    land_parcel_id = db.Column(db.String(20))   # 'land_parcel_id' 欄位：字串類型 (最多 20 個字元)，不可為空，代表土地地段編號

    plain_password = db.Column(db.String(255), comment='原始密碼')  # '這個之後可移除
    farmer_name = db.Column(db.String(50), comment='經營農戶姓名')
    phone = db.Column(db.String(50), comment='聯絡電話')
    fax = db.Column(db.String(50), comment='傳真')
    mobile = db.Column(db.String(50), comment='行動電話')
    address = db.Column(db.String(50), comment='住址')
    email = db.Column(db.String(50), comment='e-mail')
    total_area = db.Column(db.Numeric(10, 2), nullable=True, comment='栽培總面積')
    notes = db.Column(db.String(50), comment='備註')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 定义 land_parcels 数据模型
class LandParcel(db.Model):
    __tablename__ = 'land_parcels'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    number = db.Column(db.String(50), nullable=False)
    land_parcel_number = db.Column(db.String(50), nullable=False)
    area = db.Column(db.Numeric(10, 2), nullable=False)
    crop = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 生產計畫模型
class Form002(db.Model):
    __tablename__ = 'form002'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    area_code = db.Column(db.String(20), nullable=False)
    area_size = db.Column(db.Numeric(10, 2), nullable=False)
    month = db.Column(db.String(10), nullable=False)
    crop_info = db.Column(db.String(255), nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)



# 種苗登記表
class Form02(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    cultivated_crop = db.Column(db.String(100), nullable=False)
    crop_variety = db.Column(db.String(100), nullable=False)
    seed_source = db.Column(db.String(255), nullable=False)
    seedling_purchase_date = db.Column(db.Date, nullable=False)
    seedling_purchase_type = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 栽培工作模型
class Form03(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    operation_date = db.Column(db.Date, nullable=False)
    field_code = db.Column(db.String(50), nullable=False)
    crop = db.Column(db.String(100), nullable=False)
    crop_content = db.Column(db.Text, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 養液配製紀錄
class Form04(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    preparation_date = db.Column(db.Date, nullable=False)
    material_code_or_name = db.Column(db.String(50), nullable=False)
    usage_amount = db.Column(db.Numeric(10, 2), nullable=False)
    preparation_process = db.Column(db.Text, nullable=False)
    final_ph_value = db.Column(db.Numeric(10, 2), nullable=False)
    final_ec_value = db.Column(db.Numeric(10, 2), nullable=False)
    preparer_name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 液配製資材與代碼对照
class Form05(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nutrient_material_code = db.Column(db.String(50), nullable=False)
    nutrient_material_name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

