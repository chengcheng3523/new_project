from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

# 创建一个全局的 db 实例
db = SQLAlchemy()

# Python SQLAlchemy 類定義：

class users(db.Model):
    # 定義 'users' 資料表的 ORM 類別，對應到 MySQL 資料庫中的 'users' 表。
    __tablename__ = 'users'                                     # 設定資料表名稱為 'users'

    # 必填欄位
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)# 'id' 欄位：整數類型，作為主鍵 (Primary Key)，自動遞增
    username = db.Column(db.String(255)) # 'username' 欄位：字串類型 (最多 255 個字元)，不可為空 (nullable=False)
    password = db.Column(db.String(255)) # 'password' 欄位：字串類型 (最多 255 個字元)，不可為空 (nullable=False)
    unit_name = db.Column(db.String(255))       # 'unit_name' 欄位：字串類型 (最多 255 個字元)，不可為空，代表所屬單位名稱
    plain_password = db.Column(db.String(255), comment='原始密碼')  # '這個之後可移除
    farmer_name = db.Column(db.String(50), comment='經營農戶姓名')
    phone = db.Column(db.String(50), comment='聯絡電話')
    fax = db.Column(db.String(50), comment='傳真')
    mobile = db.Column(db.String(50), comment='行動電話')
    address = db.Column(db.String(50), comment='住址')
    email = db.Column(db.String(50), comment='e-mail')
    total_area = db.Column(db.Numeric(10, 2) , comment='栽培總面積')
    notes = db.Column(db.String(50), comment='備註')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 關聯Users 关联到 Lands 和 Form002
    lands = db.relationship('Lands', backref='user', lazy=True)
    form002_records = db.relationship('Form002', backref='user', lazy=True)

# 定义 lands 数据模型
class Lands(db.Model):
    __tablename__ = 'lands'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # lands_id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    number = db.Column(db.String(50), unique=True, nullable=False)
    lands_number = db.Column(db.String(50), unique=True, nullable=False)  # lands_number 對應 area_code
    area = db.Column(db.Numeric(10, 2))
    crop = db.Column(db.String(100))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 反向關聯到 Form002
    form002_records = db.relationship('Form002', backref='land', lazy=True)

# 生產計畫模型
class Form002(db.Model):
    __tablename__ = 'form002'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    area_code = db.Column(db.String(20))
    area_size = db.Column(db.Numeric(10, 2) )
    month = db.Column(db.String(10) )
    crop_info = db.Column(db.String(255) )
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

@staticmethod
def validate_area_code(area_code):
    if not area_code:
        return False  # 避免 None 或空字串
    return db.session.query(db.exists().where(Lands.number == area_code)).scalar()

# Form02 種苗登記表
class Form02(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    crop = db.Column(db.String(100) )
    crop_variety = db.Column(db.String(100) )
    seed_source = db.Column(db.String(255))
    seedling_purchase_date = db.Column(db.Date)
    seedling_purchase_type = db.Column(db.String(50))
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @staticmethod
    def validate_crop(crop):
        if not crop:
            return False  # 避免 None 或空字串
        return db.session.query(db.exists().where(Lands.crop == crop)).scalar()
    
# 栽培工作模型
class Form03(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    operation_date = db.Column(db.Date)
    field_code = db.Column(db.String(50))
    crop = db.Column(db.String(100))
    crop_content = db.Column(db.Text)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 肥料施用紀錄
class Form06(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    date_used = db.Column(db.Date)              # 使用日期
    field_code  = db.Column(db.String(50))      # 田區代號
    crop = db.Column(db.String(20))             # 作物
    fertilizer_type = db.Column(db.String(50), nullable=True)   # 施肥別(基肥.追肥)
    fertilizer_material_name = db.Column(db.String(100))        # 資材代碼或資材名稱
    fertilizer_amount = db.Column(db.Numeric(10, 2))            # 肥料使用量
    dilution_factor = db.Column(db.Numeric(5, 2), nullable=True)# 稀釋倍數
    operator = db.Column(db.String(100))                        # 操作人員
    process = db.Column(db.Text, nullable=True)                 # 製作流程
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 肥料資材與代碼對照表
class Form07(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fertilizer_material_code = db.Column(db.String(50))# 肥料資材代碼
    fertilizer_material_name = db.Column(db.String(50))# 肥料資材名稱
    manufacturer = db.Column(db.String(50), nullable=True)# 廠商
    supplier = db.Column(db.String(50), nullable=True)# 供應商
    packaging_unit = db.Column(db.String(50))# 包裝單位
    packaging_volume = db.Column(db.String(50), nullable=True)# 包裝容量
    notes = db.Column(db.Text, nullable=True)    # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 肥料入出庫紀錄
class Form08(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    fertilizer_material_name = db.Column(db.String(100))             # 資材名稱
    manufacturer = db.Column(db.String(100), nullable=True)               # 廠商
    supplier = db.Column(db.String(100), nullable=True)                   # 供應商
    packaging_unit = db.Column(db.String(100))            # 包裝單位
    packaging_volume = db.Column(db.String(50))           # 包裝容量
    date = db.Column(db.Date)                             # 日期
    purchase_quantity = db.Column(db.Numeric(10, 2))      # 購入量
    usage_quantity = db.Column(db.Numeric(10, 2))        # 使用量
    remaining_quantity = db.Column(db.Numeric(10, 2))    # 剩餘量
    notes = db.Column(db.Text, nullable=True)                             # 備註 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 有害生物防治或環境消毒資材施用紀錄
class Form09(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    date_used = db.Column(db.Date)                              # 使用日期
    field_code = db.Column(db.String(50))                       # 田區代號
    crop = db.Column(db.String(100))                            # 作物名稱
    pest_target = db.Column(db.String(100))                     # 防治對象
    pest_control_material_name = db.Column(db.String(100))          # 資材代碼或名稱
    water_volume = db.Column(db.Numeric(10, 2))                 # 用水量（公升）
    chemical_usage = db.Column(db.Numeric(10, 2))               # 藥劑使用量（公斤、公升）
    dilution_factor = db.Column(db.Numeric(10, 2))              # 稀釋倍數
    safety_harvest_period = db.Column(db.Integer)               # 安全採收期（天）
    operator_method = db.Column(db.String(100))                 # 操作方式
    operator = db.Column(db.String(100))                        # 操作人員
    notes = db.Column(db.Text, nullable=True)                                   # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)                # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 防治資材與代碼對照表
class Form10(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 唯一編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    pest_control_material_code = db.Column(db.String(100))  # 防治資材代碼
    pest_control_material_name = db.Column(db.String(100))  # 防治資材名稱
    dosage_form = db.Column(db.String(100), nullable=True)  # 劑型
    brand_name = db.Column(db.String(100), nullable=True)  # 商品名(廠牌)
    supplier = db.Column(db.String(100), nullable=True)  # 供應商
    packaging_unit = db.Column(db.String(100))  # 包裝單位
    packaging_volume = db.Column(db.Numeric(10, 2), nullable=True)  # 包裝容量
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 有害生物防治或環境消毒資材入出庫紀錄
class Form11(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    pest_control_material_name = db.Column(db.String(255))  # 資材名稱
    dosage_form = db.Column(db.String(100), nullable=True)  # 劑型
    brand_name = db.Column(db.String(100), nullable=True)  # 商品名(廠牌)
    supplier = db.Column(db.String(100), nullable=True)  # 供應商
    packaging_unit = db.Column(db.String(100))  # 包裝單位
    packaging_volume = db.Column(db.Numeric(10, 2), nullable=True)  # 包裝容量
    date = db.Column(db.Date)  # 日期
    purchase_quantity = db.Column(db.Numeric(10, 2), nullable=True)  # 購入量
    usage_quantity = db.Column(db.Numeric(10, 2), nullable=True)  # 使用量
    remaining_quantity = db.Column(db.Numeric(10, 2), nullable=True)  # 剩餘量
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 其他資材使用紀錄
class Form12(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    
    date_used = db.Column(db.Date)  # 使用日期
    field_code = db.Column(db.String(100))  # 田區代號
    crop = db.Column(db.String(100))  # 作物名稱
    other_material_name = db.Column(db.String(255))  # 資材代碼或資材名稱
    usage_amount = db.Column(db.Numeric(10, 2))  # 使用量
    operator = db.Column(db.String(100))  # 操作人員
    notes = db.Column(db.Text, nullable=True)  # 備註  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
    

# 其他資材與代碼對照表
class Form13(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    other_material_code = db.Column(db.String(50))  # 其他資材代碼
    other_material_name = db.Column(db.String(255))  # 其他資材名稱
    manufacturer = db.Column(db.String(255), nullable=True)  # 廠商
    supplier = db.Column(db.String(255), nullable=True)  # 供應商
    packaging_unit = db.Column(db.String(100))  # 包裝單位
    packaging_volume = db.Column(db.String(50), nullable=True)  # 包裝容量
    notes = db.Column(db.Text, nullable=True)  # 備註
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
    
# 其他資材入出庫紀錄
class Form14(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    other_material_name = db.Column(db.String(255))  # 資材名稱
    manufacturer = db.Column(db.String(255), nullable=True)  # 廠商
    supplier = db.Column(db.String(255), nullable=True)  # 供應商
    packaging_unit = db.Column(db.String(100))  # 包裝單位
    packaging_volume = db.Column(db.String(50), nullable=True)  # 包裝容量
    date = db.Column(db.Date)  # 日期
    purchase_quantity = db.Column(db.Numeric(10, 2))  # 購入量
    usage_quantity = db.Column(db.Numeric(10, 2))  # 使用量
    remaining_quantity = db.Column(db.Numeric(10, 2))  # 剩餘量 
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
 
# 場地設施之保養、維修及清潔管理紀錄
class Form15(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date = db.Column(db.Date)  # 日期
    item = db.Column(db.String(100))  # 項目
    operation = db.Column(db.String(100))  # 作業內容
    recorder = db.Column(db.String(255))  # 記錄人
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 器具/機械/設備之保養、維修、校正及清潔管理紀錄
class Form16(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date = db.Column(db.Date)  # 日期
    item = db.Column(db.String(100))  # 項目
    operation = db.Column(db.String(100))  # 作業內容
    recorder = db.Column(db.String(255))  # 記錄人
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 採收及採後處理紀錄
class Form17(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    harvest_date = db.Column(db.Date)  # 採收日期
    field_code = db.Column(db.String(50))  # 田區代號
    lands_id = db.Column(db.Integer, db.ForeignKey('lands.id'), nullable=False)
    crop_name = db.Column(db.String(255))  # 作物名稱
    batch_or_trace_no = db.Column(db.String(50), nullable=True)  # 批次編號或履歷編號
    harvest_weight = db.Column(db.Numeric(10, 2))  # 採收重量 (處理前)
    process_date = db.Column(db.Date)  # 處理日期
    post_harvest_treatment = db.Column(db.String(100))  # 採後處理內容
    post_treatment_weight = db.Column(db.Numeric(10, 2))  # 處理後重量
    verification_status = db.Column(db.String(255))  # 驗證狀態 
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 乾燥作業紀錄
class Form18(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    arena = db.Column(db.String(255))  # 處理場所
    process_date = db.Column(db.Date)  # 處理日期
    item = db.Column(db.String(255))  # 品項
    batch_number = db.Column(db.String(50))  # 批次編號
    fresh_weight = db.Column(db.Numeric(10, 2))  # 鮮重 (公斤)
    operation = db.Column(db.Text, nullable=True)  # 作業內容
    dry_weight = db.Column(db.Numeric(10, 2))  # 乾重 (公斤)
    remarks = db.Column(db.Text, nullable=True)  # 備註
    
# 包裝及出貨紀錄
class Form19(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    package = db.Column(db.String(255))  # 包裝場所
    sale_date = db.Column(db.Date)  # 販售日期
    product_name = db.Column(db.String(255))  # 產品名稱
    sales_target = db.Column(db.Text)  # 銷售對象
    batch_number = db.Column(db.String(50))  # 批次編號
    shipment_quantity = db.Column(db.Numeric(10, 2))  # 出貨量 (公斤)
    packaging_spec = db.Column(db.Text)  # 包裝規格
    label_usage_quantity = db.Column(db.Integer)  # 標章使用數量
    label_void_quantity = db.Column(db.Integer)  # 標章作廢數量
    verification_status = db.Column(db.String(255))  # 驗證狀態
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 作業人員衛生及健康狀態檢查紀錄
class Form20(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    checkitem = db.Column(db.Text)  # 檢查項目
    jobdate = db.Column(db.Date)  # 作業日期
    operator_name = db.Column(db.String(255))  # 作業人員姓名
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 客戶抱怨/回饋紀錄
class Form22(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date = db.Column(db.Date)  # 日期
    customer_name = db.Column(db.String(255))  # 客戶名稱
    customer_phone = db.Column(db.String(50))  # 客戶電話
    complaint = db.Column(db.Text)  # 客訴內容
    resolution = db.Column(db.Text)  # 處理結果
    processor_name  = db.Column(db.String(50))  # 處理人員
    processor_date = db.Column(db.Date)            # 處理日期

    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
