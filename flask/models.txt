from flask_restx import fields

# 定義使用者資料模型，供 Swagger 文件與驗證使用
def create_user_model(api):
    return api.model('User', {
        'username': fields.String(required=True, description='帳號'),
        'plain_password': fields.String(required=True, description='原始密碼'),
        'unit_name': fields.String(description='單位名稱'),
        'farmer_name': fields.String(description='經營農戶姓名'),
        'phone': fields.String(description='聯絡電話'),
        'fax': fields.String(description='傳真'),
        'mobile': fields.String(description='行動電話'),
        'address': fields.String(description='住址'),
        'email': fields.String(description='e-mail'),
        'total_area': fields.Float(description='栽培總面積'),
        'notes': fields.String(description='備註')
    })

# 定義農地資料模型
def create_land_parcel_model(api):
    return api.model('LandParcel', {
        'username': fields.String(required=True, description='帳號'),
        'number': fields.String(required=True, description='農地編號'),
        'land_parcel_number': fields.String(required=True, description='農地地籍號碼'),
        'area': fields.Float(required=True, description='面積（單位：公頃）'),
        'crop': fields.String(description='種植作物'),
        'notes': fields.String(description='備註')
    })

# 定義生產計畫資料模型
def create_form002_model(api):
    return  api.model('Form002', {
      'username': fields.String(required=True, description='使用者名稱'),
      'land_parcel_id': fields.Integer(required=True, description='農地 ID'),
      'area_code': fields.String(required=True, description='場區代號'),
      'area_size': fields.Float(required=True, description='場區面積（公頃）'),
      'month': fields.String(required=True, description='月份'),
      'crop_info': fields.String(required=True, description='種植作物種類、產期、預估產量'),
      'notes': fields.String(description='備註')
})

# 定義 Form02 資料模型
def create_form02_model(api):
    return api.model('Form02', {
        'username': fields.String(required=True, description='使用者名稱'),
        'land_parcel_id': fields.Integer(required=True, description='農地 ID'),
        'cultivated_crop': fields.String(required=True, description='栽培作物'),
        'crop_variety': fields.String(required=True, description='栽培品種'),
        'seed_source': fields.String(required=True, description='種子(苗)來源'),
        'seedling_purchase_date': fields.Date(required=True, description='育苗(購入)日期'),
        'seedling_purchase_type': fields.String(required=True, description='育苗(購入)種類'),
        'notes': fields.String(description='備註')
    })

# 定義 Form03 資料模型
def create_form03_model(api):
    return api.model('Form03', {
        'username': fields.String(required=True, description='使用者名稱'),
        'land_parcel_id': fields.Integer(required=True, description='農地 ID'),
        'operation_date': fields.Date(required=True, description='作業日期'),
        'field_code': fields.String(required=True, description='田區代號'),
        'crop': fields.String(required=True, description='作物'),
        'crop_content': fields.String(required=True, description='作物內容（工作代碼及描述）'),
        'notes': fields.String(description='備註')
    })

# 定義 Form04 資料模型
def create_form04_model(api):
    return api.model('Form04', {
        'username': fields.String(required=True, description='使用者名稱'),
        'preparation_date': fields.Date(required=True, description='配製日期'),
        'material_code_or_name': fields.String(required=True, description='資材代碼或資材名稱'),
        'usage_amount': fields.Float(required=True, description='使用量(公斤/公升)'),
        'preparation_process': fields.String(description='配製流程簡述'),
        'final_ph_value': fields.Float(description='最終 pH 值'),
        'final_ec_value': fields.Float(description='最終 EC 值(mS/cm)'),
        'preparer_name': fields.String(description='配製人員名稱'),
        'notes': fields.String(description='備註')
    })

# 定義 Form05 資料模型
def create_form05_model(api):
    return api.model('Form05', {
        'nutrient_material_code': fields.String(required=True, description='養液配製資材代碼'),
        'nutrient_material_name': fields.String(required=True, description='養液配製資材名稱'),
        'notes': fields.String(description='備註')
    })

# 定義 Form06 資料模型
def create_form06_model(api):
    return api.model('Form06', {
        'date_used': fields.Date(required=True, description='使用日期'),
        'field_code': fields.String(required=True, description='田區代號'),
        'crop': fields.String(required=True, description='作物'),
        'fertilizer_type': fields.String(required=True, description='施肥別 (基肥, 追肥)'),
        'material_code_or_name': fields.String(required=True, description='資材代碼或資材名稱'),
        'fertilizer_amount': fields.Float(required=True, description='肥料使用量 (公斤/公升)'),
        'dilution_factor': fields.Float(description='稀釋倍數 (液肥適用)'),
        'operator': fields.String(required=True, description='操作人員'),
        'process': fields.String(description='製作流程'),
        'notes': fields.String(description='備註')
    })

# 定義 Form07 資料模型
def create_form07_model(api):
    return api.model('Form07', {
        'fertilizer_material_code': fields.String(required=True, description='肥料資材代碼'),
        'fertilizer_material_name': fields.String(required=True, description='肥料資材名稱'),
        'notes': fields.String(description='備註')
    })

# 定義 Form08 資料模型
def create_form08_model(api):
    return api.model('Form08', {
        'material_name': fields.String(required=True, description='資材名稱'),
        'manufacturer': fields.String(description='廠商'),
        'supplier': fields.String(description='供應商'),
        'packaging_unit': fields.String(required=True, description='包裝單位'),
        'packaging_volume': fields.String(required=True, description='包裝容量（如：公克、公斤、毫升、公升等）'),
        'date': fields.Date(required=True, description='日期'),
        'purchase_quantity': fields.Float(required=True, description='購入量'),
        'usage_quantity': fields.Float(required=True, description='使用量'),
        'remaining_quantity': fields.Float(required=True, description='剩餘量'),
        'notes': fields.String(description='備註')
    })

# 定義 Form09 資料模型
def create_form09_model(api):
    return api.model('Form09', {
        'date_used': fields.Date(required=True, description='使用日期'),
        'field_code': fields.String(required=True, description='田區代號'),
        'crop': fields.String(required=True, description='作物名稱'),
        'pest_target': fields.String(required=True, description='防治對象（如：蟲）'),
        'material_code_or_name': fields.String(required=True, description='資材代碼或名稱'),
        'water_volume': fields.Float(required=True, description='用水量（公升）'),
        'chemical_usage': fields.Float(required=True, description='藥劑使用量（公斤、公升）'),
        'dilution_factor': fields.Float(required=True, description='稀釋倍數'),
        'safety_harvest_period': fields.Integer(required=True, description='安全採收期（天）'),
        'operator_method': fields.String(required=True, description='操作方式'),
        'operator': fields.String(required=True, description='操作人員'),
        'notes': fields.String(description='備註')
    })

# 定義 Form10 資料模型
def create_form10_model(api):
    return api.model('Form10', {
        'pest_control_material_code': fields.String(required=True, description='防治資材代碼'),
        'pest_control_material_name': fields.String(required=True, description='防治資材名稱'),
        'notes': fields.String(description='備註')
    })

# 定義 Form11 資料模型
def create_form11_model(api):
    return api.model('Form11', {
        'material_name': fields.String(required=True, description='資材名稱'),
        'dosage_form': fields.String(description='劑型'),
        'brand_name': fields.String(description='商品名(廠牌)'),
        'supplier': fields.String(description='供應商'),
        'packaging_unit': fields.String(required=True, description='包裝單位'),
        'packaging_volume': fields.Float(description='包裝容量'),
        'date': fields.Date(required=True, description='日期'),
        'purchase_quantity': fields.Float(description='購入量'),
        'usage_quantity': fields.Float(description='使用量'),
        'remaining_quantity': fields.Float(description='剩餘量')
    })

# 定義 Form12 資料模型
def create_form12_model(api):
    return api.model('Form12', {
        'date_used': fields.Date(required=True, description='使用日期'),
        'field_code': fields.String(required=True, description='田區代號'),
        'crop': fields.String(required=True, description='作物名稱'),
        'material_code_or_name': fields.String(required=True, description='資材代碼或資材名稱'),
        'usage_amount': fields.Float(required=True, description='使用量'),
        'operator': fields.String(required=True, description='操作人員'),
        'notes': fields.String(description='備註')
    })

# 定義 Form13 資料模型
def create_form13_model(api):
    return api.model('Form13', {
        'other_material_code': fields.String(required=True, description='其他資材代碼'),
        'other_material_name': fields.String(required=True, description='其他資材名稱'),
        'notes': fields.String(description='備註')
    })

# 定義 Form14 資料模型
def create_form14_model(api):
    return api.model('Form14', {
        'id': fields.String(required=True, description='編號'),
        'material_name': fields.String(required=True, description='資材名稱'),
        'manufacturer': fields.String(description='廠商'),
        'supplier': fields.String(description='供應商'),
        'packaging_unit': fields.String(required=True, description='包裝單位'),
        'packaging_volume': fields.String(description='包裝容量'),
        'date': fields.Date(required=True, description='日期'),
        'purchase_quantity': fields.Float(required=True, description='購入量'),
        'usage_quantity': fields.Float(required=True, description='使用量'),
        'remaining_quantity': fields.Float(required=True, description='剩餘量'),
        'notes': fields.String(description='備註')
    })

# 定義 Form15 資料模型
def create_form15_model(api):
    return api.model('Form15', {
        'id': fields.String(required=True, description='編號'),
        'date': fields.Date(required=True, description='日期'),
        'item': fields.String(required=True, description='項目'),
        'operation': fields.String(required=True, description='作業內容'),
        'recorder': fields.String(required=True, description='記錄人'),
        'notes': fields.String(description='備註')
    })

# 定義 Form16 資料模型
def create_form16_model(api):
    return api.model('Form16', {
        'id': fields.String(required=True, description='編號'),
        'date': fields.Date(required=True, description='日期'),
        'item': fields.String(required=True, description='項目'),
        'operation': fields.String(required=True, description='作業內容'),
        'recorder': fields.String(required=True, description='記錄人'),
        'notes': fields.String(description='備註')
    })

# 定義 Form17 資料模型
def create_form17_model(api):
    return api.model('Form17', {
        'id': fields.String(required=True, description='編號'),
        'harvest_date': fields.Date(required=True, description='採收日期'),
        'field_code': fields.String(required=True, description='田區代號'),
        'crop_name': fields.String(required=True, description='作物名稱'),
        'batch_or_trace_no': fields.String(description='批次編號或履歷編號'),
        'harvest_weight': fields.Float(required=True, description='採收重量 (處理前)'),
        'process_date': fields.Date(required=True, description='處理日期'),
        'post_harvest_treatment': fields.String(required=True, description='採後處理內容'),
        'post_treatment_weight': fields.Float(required=True, description='處理後重量'),
        'verification_status': fields.String(required=True, description='驗證狀態'),
        'verification_organization': fields.String(description='驗證機構'),
        'notes': fields.String(description='備註')
    })

# 定義 Form18 資料模型
def create_form18_model(api):
    return api.model('Form18', {
        'id': fields.String(required=True, description='編號'),
        'arena': fields.String(required=True, description='處理場所'),
        'process_date': fields.Date(required=True, description='處理日期'),
        'item': fields.String(required=True, description='品項'),
        'batch_number': fields.String(required=True, description='批次編號'),
        'fresh_weight': fields.Float(required=True, description='鮮重 (公斤)'),
        'operation': fields.String(description='作業內容'),
        'dry_weight': fields.Float(required=True, description='乾重 (公斤)'),
        'remarks': fields.String(description='備註')
    })

# 定義 Form19 資料模型
def create_form19_model(api):
    return api.model('Form19', {
        'id': fields.String(required=True, description='編號'),
        'package': fields.String(required=True, description='包裝場所'),
        'sale_date': fields.Date(required=True, description='販售日期'),
        'product_name': fields.String(required=True, description='產品名稱'),
        'sales_target': fields.String(required=True, description='銷售對象'),
        'batch_number': fields.String(required=True, description='批次編號'),
        'shipment_quantity': fields.Float(required=True, description='出貨量 (公斤)'),
        'packaging_spec': fields.String(required=True, description='包裝規格'),
        'label_usage_quantity': fields.Integer(required=True, description='標章使用數量'),
        'label_void_quantity': fields.Integer(required=True, description='標章作廢數量'),
        'verification_status': fields.String(required=True, description='驗證狀態')
    })

# 定義 Form20 資料模型
def create_form20_model(api):
    return api.model('Form20', {
        'id': fields.String(required=True, description='編號'),
        'checkitem': fields.String(required=True, description='檢查項目'),
        'jobdate': fields.Date(required=True, description='作業日期'),
        'operator_name': fields.String(required=True, description='作業人員姓名')
    })

# 定義 Form22 資料模型
def create_form22_model(api):
    return api.model('Form22', {
        'id': fields.String(required=True, description='編號'),
        'date': fields.Date(required=True, description='日期'),
        'customer_name': fields.String(required=True, description='客戶名稱'),
        'customer_phone': fields.String(required=True, description='客戶電話'),
        'complaint': fields.String(required=True, description='客訴內容'),
        'resolution': fields.String(required=True, description='處理結果'),
        'processor': fields.String(required=True, description='處理人簽名/日期')
    })




