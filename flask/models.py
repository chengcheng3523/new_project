from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Python SQLAlchemy 類定義：

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

# 養液配製資材與代碼對照表
class Form05(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    nutrient_material_code = db.Column(db.String(50), nullable=False)
    nutrient_material_name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 肥料施用紀錄
class Form06(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 使用日期
    date_used = db.Column(db.Date, nullable=False)
    # 田區代號
    field_code  = db.Column(db.String(50), nullable=False)
    # 作物
    crop = db.Column(db.String(20), nullable=False)
    # 施肥別(基肥.追肥)
    fertilizer_type = db.Column(db.String(50), nullable=True)
    # 資材代碼或資材名稱
    material_code_or_name = db.Column(db.String(100), nullable=False)
    # 肥料使用量
    fertilizer_amount = db.Column(db.Numeric(10, 2), nullable=False)
    # 稀釋倍數
    dilution_factor = db.Column(db.Numeric(5, 2), nullable=True)
    # 操作人員
    operator = db.Column(db.String(100), nullable=False)
    # 製作流程
    process = db.Column(db.Text, nullable=True)
    # 備註
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 肥料資材與代碼對照表
class Form07(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    fertilizer_material_code = db.Column(db.String(50), nullable=False)# 肥料資材代碼
    fertilizer_material_name = db.Column(db.String(50), nullable=False)# 肥料資材名稱
    notes = db.Column(db.Text, nullable=True)    # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 肥料入出庫紀錄
class Form08(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    material_name = db.Column(db.String(100), nullable=False)             # 資材名稱
    manufacturer = db.Column(db.String(100), nullable=True)               # 廠商
    supplier = db.Column(db.String(100), nullable=True)                   # 供應商
    packaging_unit = db.Column(db.String(100), nullable=False)            # 包裝單位
    packaging_volume = db.Column(db.String(50), nullable=False)           # 包裝容量
    date = db.Column(db.Date, nullable=False)                             # 日期
    purchase_quantity = db.Column(db.Numeric(10, 2), nullable=False)      # 購入量
    usage_quantity = db.Column(db.Numeric(10, 2), nullable=False)        # 使用量
    remaining_quantity = db.Column(db.Numeric(10, 2), nullable=False)    # 剩餘量
    notes = db.Column(db.Text, nullable=True)                             # 備註 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# 有害生物防治或環境消毒資材施用紀錄
class Form09(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)            # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date_used = db.Column(db.Date, nullable=False)                              # 使用日期
    field_code = db.Column(db.String(50), nullable=False)                       # 田區代號
    crop = db.Column(db.String(100), nullable=False)                            # 作物名稱
    pest_target = db.Column(db.String(100), nullable=False)                     # 防治對象
    material_code_or_name = db.Column(db.String(100), nullable=False)          # 資材代碼或名稱
    water_volume = db.Column(db.Numeric(10, 2), nullable=False)                 # 用水量（公升）
    chemical_usage = db.Column(db.Numeric(10, 2), nullable=False)               # 藥劑使用量（公斤、公升）
    dilution_factor = db.Column(db.Numeric(10, 2), nullable=False)              # 稀釋倍數
    safety_harvest_period = db.Column(db.Integer, nullable=False)               # 安全採收期（天）
    operator_method = db.Column(db.String(100), nullable=False)                 # 操作方式
    operator = db.Column(db.String(100), nullable=False)                        # 操作人員
    notes = db.Column(db.Text, nullable=True)                                   # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)                # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 防治資材與代碼對照表
class Form10(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 唯一編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    pest_control_material_code = db.Column(db.String(100), nullable=False)  # 防治資材代碼
    pest_control_material_name = db.Column(db.String(100), nullable=False)  # 防治資材名稱
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 有害生物防治或環境消毒資材入出庫紀錄
class Form11(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    material_name = db.Column(db.String(255), nullable=False)  # 資材名稱
    dosage_form = db.Column(db.String(100), nullable=True)  # 劑型
    brand_name = db.Column(db.String(100), nullable=True)  # 商品名(廠牌)
    supplier = db.Column(db.String(100), nullable=True)  # 供應商
    packaging_unit = db.Column(db.String(100), nullable=False)  # 包裝單位
    packaging_volume = db.Column(db.Numeric(10, 2), nullable=True)  # 包裝容量
    date = db.Column(db.Date, nullable=False)  # 日期
    purchase_quantity = db.Column(db.Numeric(10, 2), nullable=True)  # 購入量
    usage_quantity = db.Column(db.Numeric(10, 2), nullable=True)  # 使用量
    remaining_quantity = db.Column(db.Numeric(10, 2), nullable=True)  # 剩餘量
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 其他資材使用紀錄
class Form12(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date_used = db.Column(db.Date, nullable=False)  # 使用日期
    field_code = db.Column(db.String(100), nullable=False)  # 田區代號
    crop = db.Column(db.String(100), nullable=False)  # 作物名稱
    material_code_or_name = db.Column(db.String(255), nullable=False)  # 資材代碼或資材名稱
    usage_amount = db.Column(db.Numeric(10, 2), nullable=False)  # 使用量
    operator = db.Column(db.String(100), nullable=False)  # 操作人員
    notes = db.Column(db.Text, nullable=True)  # 備註  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
    

# 其他資材與代碼對照表
class Form13(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 編號，自動遞增
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    other_material_code = db.Column(db.String(50), nullable=False)  # 其他資材代碼
    other_material_name = db.Column(db.String(255), nullable=False)  # 其他資材名稱
    notes = db.Column(db.Text, nullable=True)  # 備註
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
    
# 其他資材入出庫紀錄
class Form14(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    material_name = db.Column(db.String(255), nullable=False)  # 資材名稱
    manufacturer = db.Column(db.String(255), nullable=True)  # 廠商
    supplier = db.Column(db.String(255), nullable=True)  # 供應商
    packaging_unit = db.Column(db.String(100), nullable=False)  # 包裝單位
    packaging_volume = db.Column(db.String(50), nullable=True)  # 包裝容量
    date = db.Column(db.Date, nullable=False)  # 日期
    purchase_quantity = db.Column(db.Numeric(10, 2), nullable=False)  # 購入量
    usage_quantity = db.Column(db.Numeric(10, 2), nullable=False)  # 使用量
    remaining_quantity = db.Column(db.Numeric(10, 2), nullable=False)  # 剩餘量 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
 
# 場地設施之保養、維修及清潔管理紀錄
class Form15(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date = db.Column(db.Date, nullable=False)  # 日期
    item = db.Column(db.String(100), nullable=False)  # 項目
    operation = db.Column(db.String(100), nullable=False)  # 作業內容
    recorder = db.Column(db.String(255), nullable=False)  # 記錄人
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 器具/機械/設備之保養、維修、校正及清潔管理紀錄
class Form16(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date = db.Column(db.Date, nullable=False)  # 日期
    item = db.Column(db.String(100), nullable=False)  # 項目
    operation = db.Column(db.String(100), nullable=False)  # 作業內容
    recorder = db.Column(db.String(255), nullable=False)  # 記錄人
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 採收及採後處理紀錄
class Form17(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    harvest_date = db.Column(db.Date, nullable=False)  # 採收日期
    field_code = db.Column(db.String(50), nullable=False)  # 田區代號
    crop_name = db.Column(db.String(255), nullable=False)  # 作物名稱
    batch_or_trace_no = db.Column(db.String(50), nullable=True)  # 批次編號或履歷編號
    harvest_weight = db.Column(db.Numeric(10, 2), nullable=False)  # 採收重量 (處理前)
    process_date = db.Column(db.Date, nullable=False)  # 處理日期
    post_harvest_treatment = db.Column(db.String(100), nullable=False)  # 採後處理內容
    post_treatment_weight = db.Column(db.Numeric(10, 2), nullable=False)  # 處理後重量
    verification_status = db.Column(db.Enum('非驗證產品', '驗證產品'), nullable=False)  # 驗證狀態
    verification_organization = db.Column(db.String(255), nullable=True)  # 驗證機構
    notes = db.Column(db.Text, nullable=True)  # 備註
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 乾燥作業紀錄
class Form18(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    arena = db.Column(db.String(255), nullable=False)  # 處理場所
    process_date = db.Column(db.Date, nullable=False)  # 處理日期
    item = db.Column(db.String(255), nullable=False)  # 品項
    batch_number = db.Column(db.String(50), nullable=False)  # 批次編號
    fresh_weight = db.Column(db.Numeric(10, 2), nullable=False)  # 鮮重 (公斤)
    operation = db.Column(db.Text, nullable=True)  # 作業內容
    dry_weight = db.Column(db.Numeric(10, 2), nullable=False)  # 乾重 (公斤)
    remarks = db.Column(db.Text, nullable=True)  # 備註
    
# 包裝及出貨紀錄
class Form19(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    package = db.Column(db.String(255), nullable=False)  # 包裝場所
    sale_date = db.Column(db.Date, nullable=False)  # 販售日期
    product_name = db.Column(db.String(255), nullable=False)  # 產品名稱
    sales_target = db.Column(db.Text, nullable=False)  # 銷售對象
    batch_number = db.Column(db.String(50), nullable=False)  # 批次編號
    shipment_quantity = db.Column(db.Numeric(10, 2), nullable=False)  # 出貨量 (公斤)
    packaging_spec = db.Column(db.Text, nullable=False)  # 包裝規格
    label_usage_quantity = db.Column(db.Integer, nullable=False)  # 標章使用數量
    label_void_quantity = db.Column(db.Integer, nullable=False)  # 標章作廢數量
    verification_status = db.Column(db.String(255), nullable=False)  # 驗證狀態
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 作業人員衛生及健康狀態檢查紀錄
class Form20(db.Model):
    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    checkitem = db.Column(db.Text, nullable=False)  # 檢查項目
    jobdate = db.Column(db.Date, nullable=False)  # 作業日期
    operator_name = db.Column(db.String(255), nullable=False)  # 作業人員姓名
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間

# 客戶抱怨/回饋紀錄
class Form22(db.Model):

    id = db.Column(db.String(50), primary_key=True)  # 編號
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # 關聯 `users` 表
    date = db.Column(db.Date, nullable=False)  # 日期
    customer_name = db.Column(db.String(255), nullable=False)  # 客戶名稱
    customer_phone = db.Column(db.String(50), nullable=False)  # 客戶電話
    complaint = db.Column(db.Text, nullable=False)  # 客訴內容
    resolution = db.Column(db.Text, nullable=False)  # 處理結果
    processor = db.Column(db.String(255), nullable=False)  # 處理人簽名/日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # 建立時間
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 更新時間
