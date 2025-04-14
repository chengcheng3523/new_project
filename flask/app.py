from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token
import re
from decimal import Decimal  # 確保引入 Decimal 類型
from datetime import datetime

app = Flask(__name__)   # 創建 Flask 應用程式實例

CORS( app,resources={r"/api/*": {"origins": "http://localhost:3000"}}) # 針對特定 API 路徑設置 CORS，限制存取路徑
ma = Marshmallow(app)   # 初始化 Marshmallow，提供資料序列化和驗證功能

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/new_database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 設置 JWT 密鑰
app.config['SECRET_KEY'] = 'your_secret_key'  # 設置 Flask 密鑰
jwt = JWTManager(app)  # 初始化 JWTManager 並與 Flask 應用程式關聯
CORS(app)

# 初始化 SQLAlchemy
# db = SQLAlchemy(app)

# 檢查 MySQL 資料庫連線是否正常。
def test_db_connection():
    try:
        with db.engine.connect() as connection:
            connection.execute("SELECT 1")
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

# ----------------------------------------------------------------------------------------------
# 定義資料表模型
from models import db  # 从 models.py 导入 db 实例
from models import users, Lands, Form002, Form02, Form03, Form06, Form07, Form08, Form09
from models import Form10, Form11, Form12, Form13, Form14, Form15, Form16, Form17, Form18, Form19, Form20, Form22

db.init_app(app)  # 初始化 SQLAlchemy 並與 Flask 應用程式關聯

# 建立資料
with app.app_context():
    db.create_all()

# ----------------------------------------------------------------------------------------------
# 註冊 API
@app.route('/api/register/post', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        print("Received Data (Register):", data)  # Debug 輸出    

        if not data:
            return jsonify({'error': '請求的 JSON 格式錯誤或 Content-Type 錯誤'}), 400

        username = data.get('username')
        password = data.get('password')
        plain_password = data.get('plain_password')  # 取得原始密碼
        
        if not username or not password or not plain_password:
            return jsonify({'error': '帳號、密碼或原始密碼不能為空'}), 400

        # 檢查密碼與確認密碼是否相同
        if password != plain_password:
            return jsonify({'error': '密碼與確認密碼不一致'}), 400
        
        # 檢查帳號是否已存在
        existing_user = users.query.filter_by(username=username).first()
        if existing_user:
            return jsonify({'error': '帳號已存在'}), 400
        
        # 加密密碼
        password_hash = generate_password_hash(password)

        # 創建使用者（帳號、加密密碼、原始密碼）
        new_user = users(
            username=username,
            password=password_hash,
            plain_password=plain_password  # 存入原始密碼
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'status': '註冊成功', 'user_id': new_user.id}), 201  # 返回使用者 ID
    except Exception as e:
        print(f"Error occurred during registration: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# ----------------------------------------------------------------------------------------------
# 新增/更新基本資料 API
@app.route('/api/users/post', methods=['POST'])
def create_user_profile():
    try:
        data = request.get_json()
        print("Received Data (User Profile):", data)  # Debug 輸出    

        if not data:
            return jsonify({'error': '請求的 JSON 格式錯誤或 Content-Type 錯誤'}), 400

        user_id = data.get('user_id')  # 確保提供 user_id
        if not user_id:
            return jsonify({'error': '缺少 user_id'}), 400

        # 查詢是否有該使用者
        existing_user = users.query.get(user_id)
        if not existing_user:
            return jsonify({'error': '找不到對應的使用者'}), 404

        # 更新使用者的基本資料
        existing_user.unit_name = data.get('unit_name')
        existing_user.farmer_name = data.get('farmer_name')
        existing_user.phone = data.get('phone')
        existing_user.fax = data.get('fax')
        existing_user.mobile = data.get('mobile')
        existing_user.address = data.get('address')
        existing_user.email = data.get('email')
        existing_user.total_area = None if data.get('total_area') in ['', 'None', None] else data.get('total_area')
        existing_user.notes = data.get('notes')

        db.session.commit()

        return jsonify({'status': '使用者資料更新成功'}), 200
    except Exception as e:
        print(f"Error occurred while updating profile: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 查詢所有使用者
@app.route('/api/users/get', methods=['GET'])
def get_users():
    try:
        users_data = users.query.all()  # 使用 SQLAlchemy ORM 获取所有用户
        print(f"Fetched users data: {users_data}")  # 调试输出
        # 构造返回的用户列表
        users_list = [
            {
                'id': user.id,
                'username': user.username,
                'unit_name': user.unit_name,
                'farmer_name': user.farmer_name,
                'phone': user.phone,
                'fax': user.fax,
                'mobile': user.mobile,
                'address': user.address,
                'email': user.email,
                'total_area': str(user.total_area),
                'notes': user.notes
            }
            for user in users_data
        ]
        return jsonify(users_list), 200
    except Exception as e:
        print(f"Error occurred while fetching users: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 修改使用者資料
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_users(id):
    try:
        data = request.get_json()
        user = users.query.get(id)
        if not user:
            return jsonify({'error': '使用者未找到'}), 404

        # 更新密碼
        if data.get('password'):
            user.password = generate_password_hash(data['password'])

        # 更新其他欄位
        for field in ['unit_name', 'farmer_name', 'phone', 'fax', 'mobile', 
                      'address', 'email', 'total_area', 'notes']:
            if field in data:
                if field == 'total_area' and (data[field] == '' or data[field] == 'None'):
                    setattr(user, field, None)  # 如果是空字符串或字符串 'None'，將total_area設為None
                else:
                    setattr(user, field, data[field])

        db.session.commit()
        return jsonify({'status': '使用者資料更新成功'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 刪除users
@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_users(id):
    try:
        user = users.query.get(id) 
        if not user:
            return jsonify({'error': '使用者未找到'}), 404

        db.session.delete(user)  
        db.session.commit()  
        return jsonify({'status': '使用者已刪除'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 登入
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = users.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):

        access_token = create_access_token(identity={
            'userId': user.id, 
            'role': 'user',
            'unitName': user.unit_name  # ✅ 新增 unitName
        })
        return jsonify(token=access_token), 200
    
    return jsonify(error='帳號或密碼錯誤'), 401

# ----------------------------------------------------------------------------------------
# 農地資訊

# 新增農地資訊 API
@app.route('/api/lands', methods=['POST'])
def add_lands():
    print("Received POST request")  # 新增打印資訊
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求的 JSON 格式错误'}), 400

    user_id = data.get('user_id')
    number = data.get('number')
    lands_number = data.get('lands_number')
    area = data.get('area') if data.get('area') not in ['', 'None', None] else None
    crop = data.get('crop')
    notes = data.get('notes')

    new_lands = Lands(
        user_id=user_id,
        number=number,
        lands_number=lands_number,
        area=area,
        crop=crop,
        notes=notes
    )

    db.session.add(new_lands)
    db.session.commit()

    return jsonify({'status': '農地資訊新增成功', 'lands_id': new_lands.id}), 201

# 更新農地資訊 API
@app.route('/api/lands/<int:id>', methods=['PUT'])
def update_lands(id):
    data = request.get_json()
    lands = Lands.query.get(id)

    if not lands:
        return jsonify({'error': '農地資訊未找到'}), 404

    lands.number = data.get('number', lands.number)
    lands.lands_number = data.get('lands_number', lands.lands_number)
    lands.area = data.get('area') if data.get('area') not in ['', 'None', None] else None
    lands.crop = data.get('crop', lands.crop)
    lands.notes = data.get('notes', lands.notes)

    db.session.commit()
    return jsonify({'status': '農地資訊更新成功'}), 200

# 删除農地資訊 API
@app.route('/api/lands/<int:id>', methods=['DELETE'])
def delete_lands(id):
    print(f"Attempting to delete ID: {id}")  # 新增打印資訊
    lands = Lands.query.get(id)
    if not lands:
        print(f"ID {id} not found")  # 新增打印資訊
        return jsonify({'error': '農地資訊未找到'}), 404

    db.session.delete(lands)
    db.session.commit()
    return jsonify({'status': '農地資訊已删除'}), 200

# 查詢所有農地資訊 API
@app.route('/api/lands', methods=['GET'])
def get_lands():
    results = db.session.query(
        Lands,
        users.farmer_name
    ).join(users).all()

    lands = [
        {
            'id': result.Lands.id,
            'user_id': result.Lands.user_id,
            'farmer_name': result.farmer_name,
            'number': result.Lands.number,
            'lands_number': result.Lands.lands_number,
            'area': str(result.Lands.area),
            'crop': result.Lands.crop,
            'notes': result.Lands.notes
        }
        for result in results
    ]
    return jsonify(lands)

# ----------------------------------------------------------------------------------------
# 選擇-場區代號area_codes
# 查詢所有有效的 number
@app.route('/api/valid_area_codes', methods=['GET'])
def get_valid_area_codes():
    try:
        # Lands 是你的資料表模型
        lands = Lands.query.all()  # 查詢所有 lands 資料
        valid_area_codes = [land.number for land in lands]  # 獲取所有有效的 area_code (即 number)
        return jsonify(valid_area_codes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 選擇田區代號field_codes
@app.route('/api/valid_field_codes', methods=['GET'])
def get_valid_field_codes():
    try:
        # Lands 是你的資料表模型
        lands = Lands.query.all()  # 查詢所有 lands 資料
        valid_field_codes = [land.number for land in lands]  # 獲取所有有效的 field_code (即 number)
        return jsonify(valid_field_codes), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 選擇種苗登記的作物
@app.route('/api/valid_crops', methods=['GET'])
def get_valid_crops():
    try:
        # 查詢 Form02.crop，去除 None 並去重
        valid_crops = db.session.query(Lands.crop).filter(Lands.crop.isnot(None)).distinct().all()
        
        # 轉換為純作物列表
        crops_list = [crop[0] for crop in valid_crops]

        return jsonify(crops_list), 200
    except Exception as e:
        print(f"Error in /api/valid_crops: {e}")  # 紀錄錯誤訊息
        return jsonify({'error': str(e)}), 500

# 透過選擇田區代號，顯示該田區的面積
@app.route('/api/lands/<number>', methods=['GET'])
def get_land_area(number):
    land = db.session.query(Lands).filter_by(number=number).first()
    if not land:
        return jsonify({'error': 'Land not found'}), 404

    return jsonify({'number': land.number, 'area': str(land.area)})
# ----------------------------------------------------------------------------------------
# 計算剩餘量的函數

# 肥料
def fertilizer_remaining_quantity(fertilizer_material_name, fertilizer_amount):
    try:
        # 查詢該肥料的最新庫存記錄 Form08
        latest_record = db.session.query(Form08.remaining_quantity).filter(
                Form08.fertilizer_material_name == fertilizer_material_name
        ).order_by(Form08.date.desc(), Form08.id.desc()).first()  # 按日期和ID排序，確保獲取最新記錄

        if latest_record:
            previous_remaining = Decimal(latest_record.remaining_quantity)  # 使用最新剩餘量
            print(f"✅ 找到 {fertilizer_material_name} 的庫存記錄，剩餘量: {previous_remaining}")
        else:
            print(f"⚠️ 沒有找到 {fertilizer_material_name} 的庫存記錄，使用預設庫存500.00")
            previous_remaining = Decimal('500.00')  # 若無記錄，則使用預設庫存

        # 施用量轉換為 Decimal
        fertilizer_amount = Decimal(fertilizer_amount) if fertilizer_amount else Decimal('0.00')

        # 計算新的剩餘量
        new_remaining = previous_remaining - fertilizer_amount
        print(f"🔍 上次剩餘量: {previous_remaining}, 施用量: {fertilizer_amount}, 新的剩餘量: {new_remaining}")

        return new_remaining, previous_remaining, fertilizer_amount
    except Exception as e:
        print(f"❌ 計算剩餘量時發生錯誤: {str(e)}")
        raise

# 藥
def pest_control_remaining_quantity(pest_control_material_name, chemical_usage):
    try:
        # 查詢該藥品的最新庫存記錄 Form11
        latest_record = db.session.query(Form11.remaining_quantity).filter(
                Form11.pest_control_material_name == pest_control_material_name
        ).order_by(Form11.date.desc(), Form11.id.desc()).first()  # 按日期和ID排序，確保獲取最新記錄

        if latest_record:
            previous_remaining = Decimal(latest_record.remaining_quantity)  # 使用最新剩餘量
            print(f"✅ 找到 {pest_control_material_name} 的庫存記錄，剩餘量: {previous_remaining}")
        else:
            print(f"⚠️ 沒有找到 {pest_control_material_name} 的庫存記錄，使用預設庫存500.00")
            previous_remaining = Decimal('500.00')  # 若無記錄，則使用預設庫存

        # 施用量轉換為 Decimal，chemical_usage藥劑使用量（公斤、公升）
        chemical_usage = Decimal(chemical_usage) if chemical_usage else Decimal('0.00')

        # 計算新的剩餘量
        new_remaining = previous_remaining - chemical_usage
        print(f"🔍 上次剩餘量: {previous_remaining}, 施用量: {chemical_usage}, 新的剩餘量: {new_remaining}")

        return new_remaining, previous_remaining, chemical_usage
    except Exception as e:
        print(f"❌ 計算剩餘量時發生錯誤: {str(e)}")
        raise

# 其他
def other_remaining_quantity(other_material_name, usage_amount):
    try:
        # 查詢該資材的最新庫存記錄 Form14
        latest_record = db.session.query(Form14.remaining_quantity).filter(
                Form14.other_material_name == other_material_name
        ).order_by(Form14.date.desc(), Form14.id.desc()).first()  # 按日期和ID排序，確保獲取最新記錄

        if latest_record:
            previous_remaining = Decimal(latest_record.remaining_quantity)  # 使用最新剩餘量
            print(f"✅ 找到 {other_material_name} 的庫存記錄，剩餘量: {previous_remaining}")
        else:
            print(f"⚠️ 沒有找到 {other_material_name} 的庫存記錄，使用預設庫存500.00")
            previous_remaining = Decimal('500.00')

        # 使用量轉換為 Decimal
        usage_amount = Decimal(usage_amount) if usage_amount else Decimal('0.00')

        # 計算新的剩餘量
        new_remaining = previous_remaining - usage_amount
        print(f"🔍 上次剩餘量: {previous_remaining}, 使用量: {usage_amount}, 新的剩餘量: {new_remaining}")

        return new_remaining, previous_remaining, usage_amount
    except Exception as e:
        print(f"❌ 計算剩餘量時發生錯誤: {str(e)}")
        raise

# ----------------------------------------------------------------------------------------
# 生產計畫

#  新增生產計畫
@app.route('/api/form002', methods=['POST'])
def add_form002():
    data = request.get_json()
    print("收到的請求數據:", data)

    user_id = data.get('user_id')
    area_code = data.get('area_code')  # area_code 對應 number
    area_size = data.get('area_size') if data.get('area_size') not in ['', 'None', None] else None
    month = data.get('month')
    crop_info = data.get('crop_info')
    notes = data.get('notes')

    # 使用 `number` 查詢 `lands_id`
    lands = Lands.query.filter_by(number=area_code).first()
    
    if not lands:
        print(f"❌ 錯誤: 找不到 area_code={area_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 area_code={area_code} 對應的農地'}), 400
    
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 area_code={area_code}")

    try:
        new_form = Form002(
            user_id=user_id,
            lands_id=lands_id,  # 自動關聯 lands_id
            area_size=area_size,
            month=month,
            crop_info=crop_info,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '生產計畫新增成功', 'form_id': new_form.id, 'lands_id': lands_id}), 201
    except Exception as e:
        print(f"Error occurred while adding form002: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新生產計畫
@app.route('/api/form002/<int:id>', methods=['PUT'])
def update_form002(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    # 获取要更新的生产计划
    form = Form002.query.get(id)
    if not form:
        return jsonify({'error': '生產計畫未找到'}), 404
    
    # 获取 area_code，如果没有传递就使用原来的 area_code
    area_code = data.get('area_code', form.area_code)
    
    # 如果 area_code 更新了，检查是否存在对应的农地
    if area_code != form.area_code:
        lands = Lands.query.filter_by(number=area_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form.lands_id = lands.id  # 更新关联的 lands_id
    
    # 更新其他字段
    form.area_code = area_code
    form.area_size = data.get('area_size', form.area_size) if data.get('area_size') not in ['', 'None', None] else None
    form.month = data.get('month', form.month)
    form.crop_info = data.get('crop_info', form.crop_info)
    form.notes = data.get('notes', form.notes)
  
    try:
        db.session.commit()
        return jsonify({'status': '生產計畫更新成功'}), 200
    except Exception as e:
        print(f"Error occurred while updating form002: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 刪除生產計畫
@app.route('/api/form002/<int:id>', methods=['DELETE'])
def delete_form002(id):
    form = Form002.query.get(id)
    if not form:
        return jsonify({'error': '生產計畫未找到'}), 404
    
    db.session.delete(form)
    db.session.commit()
    return jsonify({'status': '生產計畫已刪除'}), 200

# 查詢所有生產計劃
@app.route('/api/form002', methods=['GET'])
def get_all_form002(): 
    results = db.session.query(
        Form002,
        users.farmer_name.label("farmer_name"),
        Lands.number.label("land_number")
    ).join(users, Form002.user_id == users.id).join(Lands, Form002.lands_id == Lands.id).all()

    forms = [
        {
            'id': result.Form002.id,
            'user_id': result.Form002.user_id,
            'farmer_name': result.farmer_name,  
            'area_code': result.land_number,  # 修正這裡
            'area_size': float(result.Form002.area_size) if result.Form002.area_size else None,
            'month': result.Form002.month,
            'crop_info': result.Form002.crop_info,
            'notes': result.Form002.notes
        }
        for result in results
    ]
    return jsonify(forms)
# ----------------------------------------------------------------------------------------------
# 種子(苗)登記

#新增種子(苗)登記
@app.route('/api/form02', methods=['POST'])
def add_form02():
    data = request.get_json()
    print("收到的請求數據:", data)

    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400

    user_id = data.get('user_id')
    crop = data.get('crop')

    # 根據 crop 查詢對應的 lands_id
    lands = Lands.query.filter_by(crop=crop).first()
    if not lands:
        return jsonify({'error': f'找不到作物 "{crop}" 對應的農地'}), 400

    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 crop={crop}")

    crop_variety = data.get('crop_variety')
    seed_source = data.get('seed_source')
    seedling_purchase_date = datetime.strptime(data['seedling_purchase_date'], '%Y-%m-%d') if data.get('seedling_purchase_date') else None
    seedling_purchase_type = data.get('seedling_purchase_type')
    notes = data.get('notes')
  
    try:
        new_form = Form02(
            user_id=user_id,
            lands_id=lands_id,
            crop=crop,
            crop_variety=crop_variety,
            seed_source=seed_source,
            seedling_purchase_date=seedling_purchase_date,
            seedling_purchase_type=seedling_purchase_type,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '種苗登記，新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form02: {str(e)}")
        return jsonify({'error': str(e)}), 500

#更新種子(苗)登記
@app.route('/api/form02/<int:id>', methods=['PUT'])
def update_form02(id):
    data = request.get_json()
    form = Form02.query.get(id)
    if not form:
        return jsonify({'error': '種子(苗)登記未找到'}), 404
    
    form.crop = data['crop']
    form.crop_variety = data['crop_variety']
    form.seed_source = data['seed_source']
    form.seedling_purchase_date = datetime.strptime(data['seedling_purchase_date'], '%Y-%m-%d') if data.get('seedling_purchase_date') not in ['', 'None', None] else None
    form.seedling_purchase_type = data['seedling_purchase_type']
    form.notes = data.get('notes') 
    db.session.commit()
    return jsonify({'status': '種子(苗)登記更新成功'}), 200

#刪除種子(苗)登記
@app.route('/api/form02/<int:id>', methods=['DELETE'])
def delete_form02(id):
    record = Form02.query.get(id)
    if not record:
        return jsonify({"error": "Record not found"}), 404

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Record deleted successfully"})

#查詢所有種子(苗)登記
@app.route('/api/form02', methods=['GET'])
def get_all_form02():
    results = db.session.query(Form02, users.farmer_name).\
        join(users, users.id == Form02.user_id).all()

    forms = [
        {
            'id': result.Form02.id,
            'user_id': result.Form02.user_id,
            'farmer_name': result.farmer_name,
            'crop': result.Form02.crop,
            'crop_variety': result.Form02.crop_variety,
            'seed_source': result.Form02.seed_source,
            # 檢查 seedling_purchase_date 是否為 None，如果是，給一個預設值
            'seedling_purchase_date': result.Form02.seedling_purchase_date.strftime('%Y-%m-%d') if result.Form02.seedling_purchase_date else None ,
            'seedling_purchase_type': result.Form02.seedling_purchase_type,
            'notes': result.Form02.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# 栽培工作

# 新增栽培工作
@app.route('/api/form03', methods=['POST'])
def add_form03():
    data = request.get_json()
    print("收到的請求數據:", data)
    
    
    user_id = data.get('user_id')
    operation_date = datetime.strptime(data.get('operation_date'), '%Y-%m-%d') if data.get('operation_date') not in ['', 'None', None] else None
    field_code = data.get('field_code') # field_code 對應 number
    crop = data.get('crop')
    crop_content = data.get('crop_content')
    notes = data.get('notes')

    # 使用 `number` 查詢 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")


    try:
        new_form = Form03(
            user_id=user_id,
            lands_id=lands_id,  # 自動關聯 lands_id
            operation_date=operation_date,
            field_code=field_code,
            crop=crop,
            crop_content=crop_content,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '栽培工作新增成功', 'form_id': new_form.id, 'lands_id': lands_id}), 201
    except Exception as e:
        print(f"Error occurred while adding form03: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新栽培工作
@app.route('/api/form03/<int:id>', methods=['PUT'])
def update_form03(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    form = Form03.query.get(id)
    if not form:
        return jsonify({'error': '栽培工作未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form.lands_id = lands.id  # 更新关联的 lands_id
    
    # 更新其他字段
    form.operation_date = datetime.strptime(data['operation_date'], '%Y-%m-%d') if data.get('operation_date') not in ['', 'None', None] else None
    form.field_code = field_code
    form.crop = data['crop']
    form.crop_content = data['crop_content']
    form.notes = data.get('notes')

    try:
        db.session.commit()
        return jsonify({'message': '栽培工作更新成功'}), 200
    except Exception as e:
        print(f"Error occurred while updating form03: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 刪除栽培工作
@app.route('/api/form03/<int:id>', methods=['DELETE'])
def delete_form03(id):
    form = Form03.query.get(id)
    if not form:
        return jsonify({'error': '栽培工作未找到'}), 404

    db.session.delete(form)
    db.session.commit()
    return jsonify({'message': '栽培工作已刪除'}), 200

# 查詢所有的栽培工作
@app.route('/api/form03', methods=['GET'])
def get_all_form03():
    results = db.session.query(
        Form03,
        users.farmer_name.label("farmer_name"),
        Lands.number.label("land_number")
    ).join(users, Form03.user_id == users.id).join(Lands, Form03.lands_id == Lands.id).all()

    forms = [
        {
            "id": result.Form03.id,
            "user_id": result.Form03.user_id,
            "farmer_name": result.farmer_name,  
            'field_code': result.land_number,  # 修正這裡
            "operation_date": result.Form03.operation_date.strftime('%Y-%m-%d') if result.Form03.operation_date else None,
            "crop": result.Form03.crop,
            "crop_content": result.Form03.crop_content,
            "notes": result.Form03.notes
        }
        for result in results
    ]

    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# 資材選單

# 肥料
@app.route('/api/fertilizer-options', methods=['GET'])
def get_fertilizer_options():
    results = db.session.query(Form07.fertilizer_material_code, Form07.fertilizer_material_name).distinct().all()

    options = [
        {
            "code": result.fertilizer_material_code,
            "name": result.fertilizer_material_name
        }
        for result in results
    ]
    return jsonify(options)

# 藥
@app.route('/api/pest-control-options', methods=['GET'])
def get_pest_control_options():
    results = db.session.query(Form10.pest_control_material_code, Form10.pest_control_material_name).distinct().all()

    options = [
        {
            "code": result.pest_control_material_code,
            "name": result.pest_control_material_name
        }
        for result in results
    ]
    return jsonify(options)

# 其他
@app.route('/api/other-options', methods=['GET'])
def get_other_options():
    results = db.session.query(Form13.other_material_code, Form13.other_material_name).distinct().all()

    options = [
        {
            "code": result.other_material_code,
            "name": result.other_material_name
        }
        for result in results
    ]
    return jsonify(options)

# ----------------------------------------------------------------------------------------------
# 肥料施用

# 新增肥料施用
@app.route('/api/form06', methods=['POST'])
def add_form06():
    data = request.get_json()
    print("收到的請求數據:", data)
    
    # 取得 Form06 欄位
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    field_code = data.get('field_code')
    crop = data.get('crop')
    fertilizer_type = data.get('fertilizer_type')
    fertilizer_material_name = data.get('fertilizer_material_name')
    fertilizer_amount = float(data.get('fertilizer_amount', 0)) if data.get('fertilizer_amount') not in ['', 'None', None] else 0
    dilution_factor = float(data.get('dilution_factor')) if data.get('dilution_factor') not in ['', 'None', None] else None
    operator = data.get('operator')
    process = data.get('process')
    notes = data.get('notes')

    # 使用 `number` 查詢 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")

    try:
        # 新增肥料施用記錄
        new_form = Form06(
            user_id=user_id,
            lands_id=lands_id,
            date_used=date_used,
            field_code=field_code,
            crop=crop,
            fertilizer_type=fertilizer_type,
            fertilizer_material_name=fertilizer_material_name,
            fertilizer_amount=fertilizer_amount,
            dilution_factor=dilution_factor,
            operator=operator,
            process=process,
            notes=notes
        )
        print(f"Form06 : {new_form.__dict__}")  # Debug

        # 先新增 Form06
        db.session.add(new_form)
        db.session.commit()  # 先提交，確保 `new_form.id` 可用
        print(f"Form06 ID: {new_form.id}")

        # 呼叫計算庫存剩餘量的函數
        new_remaining, previous_remaining, fertilizer_amount = fertilizer_remaining_quantity(fertilizer_material_name, fertilizer_amount)

        # 查詢 Form07 資料來獲取肥料的相關資訊
        form07 = Form07.query.filter_by(fertilizer_material_name=fertilizer_material_name).first()
        if not form07:
            print(f"❌ 錯誤: 找不到對應的 Form07 記錄")
            return jsonify({'error': '找不到對應的肥料資料'}), 400
        
        # 新增一筆 Form08 (庫存同步)
        new_form08 = Form08(
            user_id=user_id,
            fertilizer_material_name=fertilizer_material_name,
            manufacturer=form07.manufacturer,  
            supplier=form07.supplier,  
            packaging_volume=form07.packaging_volume,  
            packaging_unit=form07.packaging_unit,  
            date=datetime.now(),
            usage_quantity=fertilizer_amount,
            remaining_quantity=new_remaining,
            notes=f'自動新增，對應 form06 使用記錄，稀釋倍數: {dilution_factor if dilution_factor else "無"}'
        )
        db.session.add(new_form08)
        db.session.commit()
        print(f"✅ 成功新增 Form08，剩餘量: {new_remaining}")

        all_records = db.session.query(Form08).filter(Form08.fertilizer_material_name == fertilizer_material_name).order_by(Form08.date.desc(), Form08.id.desc()).all()
        print(f"所有記錄: {[(r.date, r.remaining_quantity) for r in all_records]}")

        return jsonify({
            'status': '肥料施用新增成功',
            'form_id': new_form.id,
            'remaining_quantity': new_remaining
        }), 201
    
    except Exception as e:
        db.session.rollback()  # 避免資料庫錯誤導致未完成的操作
        print(f"❌ 錯誤: {str(e)}")
        return jsonify({'error': str(e)}), 500


# 更新肥料施用
@app.route('/api/form06/<int:id>', methods=['PUT'])
def update_form06(id):
    data = request.get_json()
    print("收到的更新數據:", data)
    
    # 查詢對應的 Form06 記錄
    form06 = Form06.query.get(id)
    if not form06:
        print(f"❌ 錯誤: 找不到 ID={id} 的肥料施用記錄")
        return jsonify({'error': '肥料施用未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form06.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form06.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form06.lands_id = lands.id  # 更新关联的 lands_id
    
    form06.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    form06.field_code = field_code
    form06.crop = data['crop']
    form06.fertilizer_type = data['fertilizer_type']
    form06.fertilizer_material_name = data['fertilizer_material_name']
    form06.operator = data.get('operator')
    form06.process = data.get('process')
    form06.notes = data.get('notes')

    try:
        # 確保數據類型一致
        old_fertilizer_amount = Decimal(form06.fertilizer_amount)  # 取得舊的使用量
        new_fertilizer_amount = Decimal(data.get('fertilizer_amount', '0'))  # 取得新的使用量
        change_amount = new_fertilizer_amount - old_fertilizer_amount  # 計算變更量

        # 更新 Form06
        form06.fertilizer_amount = new_fertilizer_amount  #更新為新的使用量
        form06.dilution_factor = Decimal(data.get('dilution_factor', '1.00')) if data.get('dilution_factor') else form06.dilution_factor # 稀釋倍數
        db.session.commit()
        print(f"✅ 更新 Form06: {form06.id}，使用量: {old_fertilizer_amount} -> {new_fertilizer_amount}")

        # 查詢最新的 Form08 (庫存)按 date 和 id 由新到舊排序
        form08 = Form08.query.filter_by(fertilizer_material_name=form06.fertilizer_material_name).order_by(Form08.date.desc(), Form08.id.desc()).first()
        if not form08:
            return jsonify({'error': '找不到對應的肥料庫存紀錄'}), 400

        # 更新肥料庫存 (Form08)
        form08.usage_quantity += change_amount
        form08.remaining_quantity -= change_amount
        form08.notes += f" | 更新使用量: {old_fertilizer_amount} -> {new_fertilizer_amount}更新稀釋倍數: {form06.dilution_factor}"

        db.session.commit()

        return jsonify({
            'status': '肥料施用更新成功',
            'form_id': form06.id,
            'new_fertilizer_amount': str(new_fertilizer_amount),  # 返回字串，避免 JSON 無法序列化 Decimal
            'updated_remaining_quantity': str(form08.remaining_quantity)
        }), 200

    except Exception as e:
        db.session.rollback()    # 錯誤時回滾變更 (rollback())
        return jsonify({'error': str(e)}), 500

# 刪除肥料施用
@app.route('/api/form06/<int:id>', methods=['DELETE'])
def delete_form06(id):
    record = Form06.query.get(id)
    if not record:
        return jsonify({'error': '肥料施用未找到'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': '肥料施用已刪除'}), 200

# 查詢所有使用者的肥料施用
@app.route('/api/form06', methods=['GET'])
def get_all_form06():
    results = db.session.query(
        Form06,
        users.farmer_name.label("farmer_name"),
        Lands.number.label("land_number")
    ).join(users, Form06.user_id == users.id).join(Lands, Form06.lands_id == Lands.id).all()

    forms = [
        {
            "id": result.Form06.id,
            "user_id": result.Form06.user_id,
            "farmer_name": result.farmer_name,
            "date_used": result.Form06.date_used.strftime('%Y-%m-%d') if result.Form06.date_used else None,
            'field_code': result.land_number,   # 修正這裡
            "crop": result.Form06.crop,
            "fertilizer_type": result.Form06.fertilizer_type,
            "fertilizer_material_name": result.Form06.fertilizer_material_name,
            "fertilizer_amount": str(result.Form06.fertilizer_amount),
            "dilution_factor": str(result.Form06.dilution_factor),
            "operator": result.Form06.operator,
            "process": result.Form06.process,
            "notes": result.Form06.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------

# form07（肥料資材與代碼）

# 新增肥料資材與代碼
@app.route('/api/form07', methods=['POST'])
def add_form07():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    fertilizer_material_code = data.get('fertilizer_material_code')
    fertilizer_material_name = data.get('fertilizer_material_name')
    manufacturer = data.get('manufacturer')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    notes = data.get('notes')
    
    try:
        new_form = Form07(
            user_id=user_id,
            fertilizer_material_code=fertilizer_material_code,
            fertilizer_material_name=fertilizer_material_name,
            manufacturer=manufacturer,
            supplier=supplier,
            packaging_unit=packaging_unit,
            packaging_volume=packaging_volume,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '肥料資材與代碼新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form07: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新肥料資材與代碼
@app.route('/api/form07/<int:id>', methods=['PUT'])
def update_form07(id):
    data = request.get_json()

    # 查詢 Form07 記錄
    form07 = Form07.query.get(id)
    if not form07:
        return jsonify({'error': '肥料資材與代碼未找到'}), 404
    
    old_fertilizer_material_name = form07.fertilizer_material_name  # 原來的資材名稱
    
    form07.fertilizer_material_code = data['fertilizer_material_code']
    form07.fertilizer_material_name = data['fertilizer_material_name']
    form07.manufacturer = data['manufacturer']            # 廠商
    form07.supplier = data['supplier']                    # 供應商
    form07.packaging_unit = data['packaging_unit']        # 包裝單位
    form07.packaging_volume = data['packaging_volume']    # 包裝容量
    form07.notes = data.get('notes')

    # 更新 Form08 中所有對應的肥料資材名稱
    form08_records = Form08.query.filter_by(fertilizer_material_name=old_fertilizer_material_name).all()
    for record in form08_records:
        record.fertilizer_material_name = data['fertilizer_material_name']
        record.manufacturer = data['manufacturer']  # 更新廠商
        record.supplier = data['supplier']        # 更新供應商
        record.packaging_unit = data['packaging_unit']  # 更新包裝單位
        record.packaging_volume = data['packaging_volume']  # 更新包裝容量
        
    # 提交變更
    db.session.commit()

    return jsonify({
        'message': '肥料資材與代碼更新成功',
        'updated_form08_count': len(form08_records)  # 回傳更新的 Form08 紀錄數量
    }), 200

# 刪除肥料資材與代碼
@app.route('/api/form07/<int:id>', methods=['DELETE'])
def delete_form07(id):
    record = Form07.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的肥料資材與代碼
@app.route('/api/form07', methods=['GET'])
def get_all_form07(): 
    results = db.session.query(Form07, users.farmer_name).\
        join(users, users.id == Form07.user_id).all()
    
    forms = [
        {
            "id": result.Form07.id,
            "user_id": result.Form07.user_id,
            "farmer_name": result.farmer_name,
            "fertilizer_material_code": result.Form07.fertilizer_material_code,
            "fertilizer_material_name": result.Form07.fertilizer_material_name,
            "manufacturer": result.Form07.manufacturer,
            "supplier": result.Form07.supplier,
            "packaging_unit": result.Form07.packaging_unit,
            "packaging_volume": result.Form07.packaging_volume,
            "notes": result.Form07.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form08（肥料入出庫）

# 新增肥料入出庫
@app.route('/api/form08', methods=['POST'])
def add_form08():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    fertilizer_material_name = data.get('fertilizer_material_name')
    manufacturer = data.get('manufacturer')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    purchase_quantity = data.get('purchase_quantity') if data.get('purchase_quantity') not in ['', 'None', None] else None
    usage_quantity = data.get('usage_quantity') if data.get('usage_quantity') not in ['', 'None', None] else None
    remaining_quantity = data.get('remaining_quantity') if data.get('remaining_quantity') not in ['', 'None', None] else None
    notes = data.get('notes')

    # 去除單位，只提取數字部分
    def extract_number(value):
        if value is None:
            return Decimal("0.0")  # 避免 None 造成錯誤
        match = re.match(r"(\d+(\.\d+)?)", value)  # 匹配數字（可包含小數點）
        return float(match.group(1)) if match else 0.0

    try:
        # 提取包裝容量、購入量和使用量的數字部分
        purchase_quantity = extract_number(purchase_quantity) if purchase_quantity else 0.0
        usage_quantity = extract_number(usage_quantity) if usage_quantity else 0.0

        # **確保數據合理**
        if purchase_quantity < 0 or usage_quantity < 0:
            return jsonify({'error': '購入量和使用量不能為負數'}), 400

        # **計算剩餘量**
        numeric_packaging_volume = extract_number(packaging_volume)  # 提取數字部分計算
        remaining_quantity = purchase_quantity * numeric_packaging_volume  - usage_quantity
        remaining_quantity = max(remaining_quantity, Decimal("0.0"))  # 避免負數

        new_form = Form08(
            user_id=user_id,
            fertilizer_material_name=fertilizer_material_name,
            manufacturer=manufacturer,
            supplier=supplier,
            packaging_unit=packaging_unit,
            packaging_volume=packaging_volume,  # **保留原始值（含單位）**
            date=date,
            purchase_quantity=purchase_quantity,
            usage_quantity=usage_quantity,
            remaining_quantity=remaining_quantity,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '肥料入出庫新增成功', 'form_id': new_form.id}), 201
    
    except Exception as e:
        print(f"Error occurred while adding form08: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新肥料入出庫
@app.route('/api/form08/<int:id>', methods=['PUT'])
def update_form08(id):

    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    form08 = Form08.query.get(id)
    if not form08:
        return jsonify({'error': '找不到該入出庫紀錄'}), 404
    
    # **提取數字部分**
    def extract_number(value):
        if value is None:
            return Decimal("0.0")  # 避免 None 造成錯誤
        match = re.search(r"(\d+(\.\d+)?)", str(value))  # 匹配數字（可包含小數點）
        return Decimal(match.group(1)) if match else Decimal("0.0")
    
    try:
        # **保留原始數據**
        form08.fertilizer_material_name = data.get('fertilizer_material_name', form08.fertilizer_material_name)
        form08.manufacturer = data.get('manufacturer', form08.manufacturer)
        form08.supplier = data.get('supplier', form08.supplier)
        form08.packaging_unit = data.get('packaging_unit', form08.packaging_unit)
        form08.packaging_volume = data.get('packaging_volume', form08.packaging_volume)  # **保留完整字串**
        form08.notes = data.get('notes', form08.notes)

        # **提取數字部分進行計算**
        numeric_packaging_volume = extract_number(form08.packaging_volume)

        # 這裡改成 purchase_quantity和 usage_quantity 的更新
        form08.purchase_quantity = extract_number(data.get('purchase_quantity', form08.purchase_quantity))
        form08.usage_quantity = extract_number(data.get('usage_quantity', form08.usage_quantity))

        # **確保數據合理**
        if form08.purchase_quantity < 0 or form08.usage_quantity < 0:
            return jsonify({'error': '購入量和使用量不能為負數'}), 400

        # **計算剩餘量**
        form08.remaining_quantity = form08.purchase_quantity * numeric_packaging_volume - form08.usage_quantity
        form08.remaining_quantity = max(form08.remaining_quantity, Decimal("0.0"))  # 避免負數

        db.session.commit()
        return jsonify({
            'status': '肥料入出庫更新成功',
            'form_id': form08.id,
            'updated_purchase_quantity': str(form08.purchase_quantity),  # ✅ 确保返回正确的购买量
            'updated_remaining_quantity': str(form08.remaining_quantity),
            'packaging_volume': form08.packaging_volume  # **回傳完整格式**
        }), 200

    except Exception as e:
        db.session.rollback()  # **出錯時回滾**
        return jsonify({'error': str(e)}), 500

# 刪除肥料入出庫
@app.route('/api/form08/<int:id>', methods=['DELETE'])
def delete_form08(id):
    record = Form08.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的肥料入出庫
@app.route('/api/form08', methods=['GET'])
def get_all_form08(): 
    results = db.session.query(Form08, users.farmer_name).\
        join(users, users.id == Form08.user_id).all()
    
    forms = [
        {
            "id": result.Form08.id,
            "user_id": result.Form08.user_id,
            "farmer_name": result.farmer_name,
            "fertilizer_material_name": result.Form08.fertilizer_material_name,
            "manufacturer": result.Form08.manufacturer,
            "supplier": result.Form08.supplier,
            "packaging_unit": result.Form08.packaging_unit,
            "packaging_volume": result.Form08.packaging_volume,
            "date": result.Form08.date.strftime('%Y-%m-%d') if result.Form08.date else None,
            "purchase_quantity": str(result.Form08.purchase_quantity),
            "usage_quantity": str(result.Form08.usage_quantity),
            "remaining_quantity": str(result.Form08.remaining_quantity),
            "notes": result.Form08.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form09（有害生物防治或環境消毒資材施用）

# 新增有害生物防治或環境消毒資材施用
@app.route('/api/form09', methods=['POST'])
def add_form09():
    data = request.get_json()
    print("收到的請求數據:", data)
    
    # 取得 Form09 欄位
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    field_code = data.get('field_code')
    crop = data.get('crop')
    pest_target = data.get('pest_target')
    pest_control_material_name = data.get('pest_control_material_name')
    water_volume = data.get('water_volume') if data.get('water_volume') not in ['', 'None', None] else None
    chemical_usage = float(data.get('chemical_usage', 0)) if data.get('chemical_usage') not in ['', 'None', None] else 0
    dilution_factor = data.get('dilution_factor') if data.get('dilution_factor') not in ['', 'None', None] else None
    safety_harvest_period = data.get('safety_harvest_period')
    operator_method = data.get('operator_method')
    operator = data.get('operator')
    notes = data.get('notes')

      # 使用 `number` 查詢 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")

    try:
        new_form = Form09(
            user_id=user_id,
            lands_id=lands_id,
            date_used=date_used,
            field_code=field_code,
            crop=crop,
            pest_target=pest_target,
            pest_control_material_name=pest_control_material_name,
            water_volume=water_volume,
            chemical_usage=chemical_usage,
            dilution_factor=dilution_factor,
            safety_harvest_period=safety_harvest_period,
            operator_method=operator_method,
            operator=operator,
            notes=notes
        )
        print(f"Form09 : {new_form.__dict__}")  # Debug

        # 先新增 Form09
        db.session.add(new_form)
        db.session.commit()  # 先提交，確保 `new_form.id` 可用
        print(f"Form09 ID: {new_form.id}")

        # 呼叫計算庫存剩餘量的函數
        new_remaining, previous_remaining, chemical_usage = pest_control_remaining_quantity(pest_control_material_name, chemical_usage)

        # 查詢 Form10 資料來獲取防治的相關資訊
        form10 = Form10.query.filter_by(pest_control_material_name=pest_control_material_name).first()
        if not form10:
            print(f"❌ 錯誤: 找不到對應的 Form10 記錄")
            return jsonify({'error': '找不到對應的【防治】資料'}), 400

        # 新增一筆 Form11 (庫存同步)
        new_form11 = Form11(
            user_id=user_id,
            pest_control_material_name=pest_control_material_name,

            dosage_form=form10.dosage_form,
            brand_name=form10.brand_name,
            supplier=form10.supplier, 
            packaging_unit=form10.packaging_unit,
            packaging_volume=form10.packaging_volume,

            date=datetime.now(),
            usage_quantity=chemical_usage, #     chemical_usage DECIMAL 藥劑使用量（公斤、公升）
            remaining_quantity=new_remaining, # 剩餘量
            notes=f'自動新增，對應 form09 使用記錄，稀釋倍數: {dilution_factor if dilution_factor else "無"}'
        )
        db.session.add(new_form11)
        db.session.commit()
        print(f"✅ 成功新增 Form11，剩餘量: {new_remaining}")

        all_records = db.session.query(Form11).filter(Form11.pest_control_material_name == pest_control_material_name).order_by(Form11.date.desc(), Form11.id.desc()).all()
        print(f"所有記錄: {[(r.date, r.remaining_quantity) for r in all_records]}")

        return jsonify({
            'status': '有害生物防治或環境消毒資材施用新增成功',
            'form_id': new_form.id,
            'remaining_quantity': new_remaining
        }), 201

    except Exception as e:
        db.session.rollback()  # 避免資料庫錯誤導致未完成的操作
        print(f"❌ 錯誤 Error occurred while adding form09: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新有害生物防治或環境消毒資材施用
@app.route('/api/form09/<int:id>', methods=['PUT'])
def update_form09(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    form09 = Form09.query.get(id)
    if not form09:
        print(f"❌ 錯誤: 找不到 ID={id} 的有害生物防治或環境消毒資材施用記錄")
        return jsonify({'error': '有害生物防治或環境消毒資材施用未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form09.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form09.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form09.lands_id = lands.id  # 更新关联的 lands_id

    form09.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    form09.field_code = field_code
    form09.crop = data['crop']
    form09.pest_target = data['pest_target']# 防治對象
    form09.pest_control_material_name = data['pest_control_material_name']  # 資材代碼或名稱
    form09.water_volume = data['water_volume'] if data.get('water_volume') not in ['', 'None', None] else None          # 用水量（公升）
    form09.safety_harvest_period = data['safety_harvest_period']# 安全採收期（天）
    form09.operator_method = data['operator_method']  # 操作方式
    form09.operator = data['operator'] # 操作人員
    form09.notes = data.get('notes')

    try:
        # 確保數據類型一致
        old_chemical_usage = Decimal(form09.chemical_usage)  # 取得舊的使用量
        new_chemical_usage = Decimal(data.get('chemical_usage', '0'))  # 取得新的使用量
        change_amount = new_chemical_usage - old_chemical_usage  # 計算變更量

        # 更新 Form09
        form09.chemical_usage = new_chemical_usage  # 更新為新的使用量
        form09.dilution_factor = Decimal(data.get('dilution_factor', '1.00')) if data.get('dilution_factor') else form09.dilution_factor  # 稀釋倍數
        db.session.commit()
        print(f"✅ 更新 Form09: {form09.id}，使用量: {old_chemical_usage} -> {new_chemical_usage}")

        # 查詢最新的 Form11 (庫存)按 date 和 id 由新到舊排序
        form11 = Form11.query.filter_by(pest_control_material_name=form09.pest_control_material_name).order_by(Form11.date.desc(), Form11.id.desc()).first()
        if not form11:
            return jsonify({'error': '找不到對應的有害生物防治或環境消毒資材庫存紀錄'}), 400
        
        # 更新有害生物防治或環境消毒資材庫存 (Form11)
        form11.usage_quantity += change_amount
        form11.remaining_quantity -= change_amount
        form11.notes += f" | 更新使用量: {old_chemical_usage} -> {new_chemical_usage} 更新稀釋倍數: {form09.dilution_factor}"

        db.session.commit()
        
        return jsonify({
            'message': '有害生物防治或環境消毒資材施用更新成功',
            'form_id': form09.id,
            'new_chemical_usage': str(new_chemical_usage),  # 返回字串，避免 JSON 無法序列化 Decimal
            'updated_remaining_quantity': str(form11.remaining_quantity)
            }), 200
    
    except Exception as e:
        db.session.rollback()    # 錯誤時回滾變更 (rollback())
        print(f"Error occurred while updating form09: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 刪除有害生物防治或環境消毒資材施用
@app.route('/api/form09/<int:id>', methods=['DELETE'])
def delete_form09(id):
    record = Form09.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的有害生物防治或環境消毒資材施用
@app.route('/api/form09', methods=['GET'])
def get_all_form09():
    results = db.session.query(
        Form09,
        users.farmer_name.label("farmer_name"),
        Lands.number.label("land_number")
    ).join(users, Form09.user_id == users.id).join(Lands, Form09.lands_id == Lands.id).all()
    
    forms = [
        {
            "id": result.Form09.id,
            "user_id": result.Form09.user_id,
            "farmer_name": result.farmer_name,
            "date_used": result.Form09.date_used.strftime('%Y-%m-%d') if result.Form09.date_used else None,
            'field_code': result.land_number,  # 修正這裡
            "crop": result.Form09.crop,
            "pest_target": result.Form09.pest_target,
            "pest_control_material_name": result.Form09.pest_control_material_name,
            "water_volume": str(result.Form09.water_volume),
            "chemical_usage": str(result.Form09.chemical_usage),
            "dilution_factor": str(result.Form09.dilution_factor),
            "safety_harvest_period": result.Form09.safety_harvest_period,
            "operator_method": result.Form09.operator_method,
            "operator": result.Form09.operator,
            "notes": result.Form09.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form10（防治資材與代碼）

# 新增防治資材與代碼
@app.route('/api/form10', methods=['POST'])
def add_form10():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    pest_control_material_code = data.get('pest_control_material_code')
    pest_control_material_name = data.get('pest_control_material_name')
    dosage_form = data.get('dosage_form')
    brand_name = data.get('brand_name')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    notes = data.get('notes')

    try:
        new_form = Form10(
            user_id=user_id,
            pest_control_material_code=pest_control_material_code,
            pest_control_material_name=pest_control_material_name,
            dosage_form=dosage_form,
            brand_name=brand_name,
            supplier=supplier,
            packaging_unit=packaging_unit,
            packaging_volume=packaging_volume,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '防治資材與代碼新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form10: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新防治資材與代碼
@app.route('/api/form10/<int:id>', methods=['PUT'])
def update_form10(id):
    data = request.get_json()

    # 查詢 Form10 記錄
    form10 = Form10.query.get(id)
    if not form10:
        return jsonify({'error': '防治資材與代碼未找到'}), 404
    
    old_pest_control_material_name = form10.pest_control_material_name  # 原來的資材名稱

    form10.pest_control_material_code = data['pest_control_material_code']
    form10.pest_control_material_name = data['pest_control_material_name']
    form10.dosage_form = data['dosage_form']                # 劑型
    form10.brand_name = data['brand_name']                  # 商品名(廠牌)
    form10.supplier = data['supplier']                      # 供應商
    form10.packaging_unit = data['packaging_unit']          # 包裝單位
    form10.packaging_volume = data['packaging_volume']      # 包裝容量
    form10.notes = data.get('notes')

    # 更新 Form09 中所有對應的防治資材名稱
    form09_records = Form09.query.filter_by   (pest_control_material_name=old_pest_control_material_name).all()
    for record in form09_records:
        record.pest_control_material_name = data['pest_control_material_name']
        record.dosage_form = data['dosage_form']  # 更新劑型
        record.brand_name = data['brand_name']  # 更新品牌
        record.supplier = data['supplier']  # 更新供應商
        record.packaging_unit = data['packaging_unit']  # 更新包裝單位
        record.packaging_volume = data['packaging_volume']  # 更新包裝容量

    # 提交變更
    db.session.commit()

    return jsonify({
        'message': '防治資材與代碼更新成功',
        'updated_form09_count': len(form09_records)  # 回傳更新的 Form09 紀錄數量
        }), 200

# 刪除防治資材與代碼
@app.route('/api/form10/<int:id>', methods=['DELETE'])
def delete_form10(id):
    record = Form10.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的防治資材與代碼
@app.route('/api/form10', methods=['GET'])
def get_all_form10(): 
    results = db.session.query(Form10, users.farmer_name).\
        join(users, users.id == Form10.user_id).all()
    
    forms = [
        {
            "id": result.Form10.id,
            "user_id": result.Form10.user_id,
            "farmer_name": result.farmer_name,
            "pest_control_material_code": result.Form10.pest_control_material_code,
            "pest_control_material_name": result.Form10.pest_control_material_name,
            "dosage_form": result.Form10.dosage_form,
            "brand_name": result.Form10.brand_name,
            "supplier": result.Form10.supplier,
            "packaging_unit": result.Form10.packaging_unit,
            "packaging_volume": result.Form10.packaging_volume,
            "notes": result.Form10.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form11（有害生物防治或環境消毒資材入出庫）

# 新增有害生物防治或環境消毒資材入出庫
@app.route('/api/form11', methods=['POST'])
def add_form11():
    data = request.get_json()
    print("接收到資料：", data)
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    pest_control_material_name = data.get('pest_control_material_name')
    dosage_form = data.get('dosage_form')
    brand_name  = data.get('brand_name')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    purchase_quantity = data.get('purchase_quantity') if data.get('purchase_quantity') not in ['', 'None', None] else None
    usage_quantity = data.get('usage_quantity') if data.get('usage_quantity') not in ['', 'None', None] else None
    remaining_quantity = data.get('remaining_quantity') if data.get('remaining_quantity') not in ['', 'None', None] else None
    notes = data.get('notes')

    # 去除單位，只提取數字部分
    def extract_number(value):
        if value is None:
            return Decimal("0.0")  # 避免 None 造成錯誤
        match = re.match(r"(\d+(\.\d+)?)", value)  # 匹配數字（可包含小數點）
        return float(match.group(1)) if match else 0.0

    try:
        # 提取包裝容量、購入量和使用量的數字部分
        purchase_quantity = extract_number(purchase_quantity) if purchase_quantity else 0.0
        usage_quantity = extract_number(usage_quantity) if usage_quantity else 0.0

        # **確保數據合理**
        if purchase_quantity < 0 or usage_quantity < 0:
            return jsonify({'error': '購入量和使用量不能為負數'}), 400

        # **計算剩餘量**
        numeric_packaging_volume = extract_number(packaging_volume)  # 提取數字部分計算
        remaining_quantity = purchase_quantity * numeric_packaging_volume  - usage_quantity
        remaining_quantity = max(remaining_quantity, Decimal("0.0"))  # 避免負數

        new_form = Form11(
            user_id=user_id,
            pest_control_material_name=pest_control_material_name,
            dosage_form=dosage_form,
            brand_name=brand_name,
            supplier=supplier,
            packaging_unit=packaging_unit,
            packaging_volume=packaging_volume,
            date=date,
            purchase_quantity=purchase_quantity,
            usage_quantity=usage_quantity,
            remaining_quantity=remaining_quantity,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '有害生物防治或環境消毒資材入出庫新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form11: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新有害生物防治或環境消毒資材入出庫
@app.route('/api/form11/<int:id>', methods=['PUT'])
def update_form11(id):

    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    form11 = Form11.query.get(id)
    if not form11:
        return jsonify({'error': '有害生物防治或環境消毒資材入出庫未找到'}), 404
    
    # **提取數字部分**
    def extract_number(value):
        if value is None:
            return Decimal("0.0")  # 避免 None 造成錯誤
        match = re.search(r"(\d+(\.\d+)?)", str(value))  # 匹配數字（可包含小數點）
        return Decimal(match.group(1)) if match else Decimal("0.0")
    
    try:
        # **保留原始數據**
        form11.pest_control_material_name = data.get('pest_control_material_name', form11.pest_control_material_name)
        form11.dosage_form = data.get('dosage_form', form11.dosage_form)
        form11.brand_name = data.get('brand_name', form11.brand_name)
        form11.supplier = data.get('supplier', form11.supplier)
        form11.packaging_unit = data.get('packaging_unit', form11.packaging_unit)
        form11.packaging_volume = data.get('packaging_volume', form11.packaging_volume)  # **保留完整字串**
        form11.notes = data.get('notes', form11.notes)
        
        # **提取數字部分進行計算**
        numeric_packaging_volume = extract_number(form11.packaging_volume)
        
        # 這裡改成 purchase_quantity和 usage_quantity 的更新
        form11.purchase_quantity = extract_number(data.get('purchase_quantity', form11.purchase_quantity))
        form11.usage_quantity = extract_number(data.get('usage_quantity', form11.usage_quantity))

        # **確保數據合理**
        if form11.purchase_quantity < 0 or form11.usage_quantity < 0:
            return jsonify({'error': '購入量和使用量不能為負數'}), 400

        # **計算剩餘量**
        form11.remaining_quantity = form11.purchase_quantity * numeric_packaging_volume - form11.usage_quantity
        form11.remaining_quantity = max(form11.remaining_quantity, Decimal("0.0"))  # 避免負數

        db.session.commit()
        db.session.commit()
        return jsonify({
            'status': '有害生物防治或環境消毒資材入出庫更新成功',
            'form_id': form11.id,
            'updated_purchase_quantity': str(form11.purchase_quantity),  # ✅ 确保返回正确的购买量
            'updated_remaining_quantity': str(form11.remaining_quantity),
            'packaging_volume': form11.packaging_volume  # **回傳完整格式**
        }), 200

    except Exception as e:
        db.session.rollback()  # **出錯時回滾**
        return jsonify({'error': str(e)}), 500

# 刪除有害生物防治或環境消毒資材入出庫
@app.route('/api/form11/<int:id>', methods=['DELETE'])
def delete_form11(id):
    record = Form11.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的有害生物防治或環境消毒資材入出庫
@app.route('/api/form11', methods=['GET'])
def get_all_form11():
    results = db.session.query(Form11, users.farmer_name).\
        join(users, users.id == Form11.user_id).all()
    
    forms = [
        {
            "id": result.Form11.id,
            "user_id": result.Form11.user_id,
            "farmer_name": result.farmer_name,
            "pest_control_material_name": result.Form11.pest_control_material_name,
            "dosage_form": result.Form11.dosage_form,
            "brand_name": result.Form11.brand_name,
            "supplier": result.Form11.supplier,
            "packaging_unit": result.Form11.packaging_unit,
            "packaging_volume": result.Form11.packaging_volume,
            "date": result.Form11.date.strftime('%Y-%m-%d') if result.Form11.date else None,
            "purchase_quantity": str(result.Form11.purchase_quantity),
            "usage_quantity": str(result.Form11.usage_quantity),
            "remaining_quantity": str(result.Form11.remaining_quantity),
            "notes": result.Form11.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form12（其他資材使用紀錄）

# 新增其他資材使用紀錄
@app.route('/api/form12', methods=['POST'])
def add_form12():
    data = request.get_json()
    print("收到的請求數據:", data)
    
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    field_code = data.get('field_code')
    crop = data.get('crop')
    other_material_name = data.get('other_material_name')
    usage_amount = data.get('usage_amount') if data.get('usage_amount') not in ['', 'None', None] else None
    operator = data.get('operator')
    notes = data.get('notes')

    # 使用 `number` 查詢 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")

    try:
        new_form = Form12(
            user_id=user_id,
            lands_id=lands_id, 
            date_used=date_used,
            field_code=field_code,
            crop=crop,
            other_material_name=other_material_name,
            usage_amount=usage_amount,
            operator=operator,
            notes=notes
        )
        print(f"Form12 : {new_form.__dict__}")  # Debug

        db.session.add(new_form)
        db.session.commit()
        print(f"Form12: {new_form.id}")

        # 呼叫計算庫存剩餘量的函數
        new_remaining, previous_remaining, usage_amount = other_remaining_quantity(other_material_name, usage_amount)

        # 查詢 Form13 資料來獲取其他的相關資訊
        form13 = Form13.query.filter_by(other_material_name=other_material_name).first()
        if not form13:
            print(f"❌ 錯誤: 找不到對應的 Form13 記錄")
            return jsonify({'error': '找不到對應的其他資材資料'}), 400
        
        # 新增一筆 Form14 (庫存同步)
        new_form14 = Form14(
            user_id=user_id,
            other_material_name=other_material_name,

            manufacturer=form13.manufacturer,
            supplier=form13.supplier,
            packaging_volume=form13.packaging_volume,
            packaging_unit=form13.packaging_unit,

            date=datetime.now(),
            usage_quantity=usage_amount,
            remaining_quantity=new_remaining,
            notes=f'自動新增，對應 form12 使用記錄'
        )
        db.session.add(new_form14)
        db.session.commit()
        print(f"✅ 成功新增 Form14，剩餘量: {new_remaining}")

        all_records = db.session.query(Form14).filter(Form14.other_material_name == other_material_name).order_by(Form14.date.desc(), Form14.id.desc()).all()
        print(f"所有記錄: {[(r.date, r.remaining_quantity) for r in all_records]}")

        return jsonify({
            'status': '其他資材使用紀錄新增成功', 
            'form_id': new_form.id,
            'remaining_quantity': new_remaining
            }), 201
    
    except Exception as e:
        db.session.rollback()  # 避免資料庫錯誤導致未完成的操作
        print(f"❌ 錯誤 Error occurred while adding form12: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新其他資材使用紀錄
@app.route('/api/form12/<int:id>', methods=['PUT'])
def update_form12(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    # 查詢對應的 Form12 記錄
    form12 = Form12.query.get(id)
    if not form12:
        print(f"❌ 錯誤: 找不到 ID={id} 的其他資材使用紀錄")
        return jsonify({'error': '其他資材使用紀錄未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form12.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form12.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form12.lands_id = lands.id  # 更新关联的 lands_id
    
    form12.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    form12.field_code = field_code
    form12.crop = data['crop']
    form12.other_material_name = data['other_material_name']
    form12.usage_amount = data['usage_amount'] if data.get('usage_amount') not in ['', 'None', None] else None
    form12.operator = data['operator']
    form12.notes = data.get('notes')

    try:
        # 確保數據類型一致
        old_usage_amount = Decimal(form12.usage_amount)  # 取得舊的使用量
        new_usage_amount = Decimal(data.get('usage_amount', '0'))  # 取得新的使用量
        change_amount = new_usage_amount - old_usage_amount  # 計算變更量

        # 更新 Form12
        form12.usage_amount = new_usage_amount  # 更新為新的使用量

        db.session.commit()
        print(f"✅ 更新 Form12: {form12.id}，使用量: {old_usage_amount} -> {new_usage_amount}")

        # 查詢最新的 Form14 (庫存)按 date 和 id 由新到舊排序
        form14 = Form14.query.filter_by(other_material_name=form12.other_material_name).order_by(Form14.date.desc(), Form14.id.desc()).first()
        if not form14:
            return jsonify({'error': '找不到對應的其他資材庫存紀錄'}), 400
        
        # 更新其他資材庫存 (Form14)
        form14.usage_amount += change_amount
        form14.remaining_quantity -= change_amount
        form14.notes += f" | 更新使用量: {old_usage_amount} -> {new_usage_amount}"

        db.session.commit()

        return jsonify({''
        'message': '其他資材使用紀錄更新成功',
        'form_id': form12.id,
        'new_usage_amount': str(new_usage_amount),  # 返回字串，避免 JSON 無法序列化 Decimal
        'updated_remaining_quantity': str(form14.remaining_quantity)
        }), 200
    
    except Exception as e:
        db.session.rollback()    # 錯誤時回滾變更 (rollback())
        print(f"Error occurred while updating form12: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 刪除其他資材使用紀錄
@app.route('/api/form12/<int:id>', methods=['DELETE'])
def delete_form12(id):
    record = Form12.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的其他資材使用紀錄
@app.route('/api/form12', methods=['GET'])
def get_all_form12():
    results = db.session.query(
        Form12,
        users.farmer_name.label("farmer_name"),
        Lands.number.label("land_number")
    ).join(users, Form12.user_id == users.id).join(Lands, Form12.lands_id == Lands.id).all()
    
    forms = [
        {
            "id": result.Form12.id,
            "user_id": result.Form12.user_id,
            "farmer_name": result.farmer_name,
            "date_used": result.Form12.date_used.strftime('%Y-%m-%d') if result.Form12.date_used else None,
            'field_code': result.land_number,  # 修正這裡
            "crop": result.Form12.crop,
            "other_material_name": result.Form12.other_material_name,
            "usage_amount": str(result.Form12.usage_amount),
            "operator": result.Form12.operator,
            "notes": result.Form12.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form13（其他資材與代碼）

# 新增其他資材與代碼
@app.route('/api/form13', methods=['POST'])
def add_form13():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    other_material_code = data.get('other_material_code')
    other_material_name = data.get('other_material_name')
    manufacturer = data.get('manufacturer')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    notes = data.get('notes')

    try:
        new_form = Form13(
            user_id=user_id,
            other_material_code=other_material_code,
            other_material_name=other_material_name,
            manufacturer=manufacturer,
            supplier=supplier,
            packaging_unit=packaging_unit,
            packaging_volume=packaging_volume,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '其他資材與代碼新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form13: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新其他資材與代碼
@app.route('/api/form13/<int:id>', methods=['PUT'])
def update_form13(id):
    data = request.get_json()

    # 查詢 Form13 記錄
    form13 = Form13.query.get(id)
    if not form13:
        return jsonify({'error': '其他資材與代碼未找到'}), 404
    
    form13.other_material_code = data['other_material_code']
    form13.other_material_name = data['other_material_name']
    form13.manufacturer = data['manufacturer']
    form13.supplier = data['supplier']
    form13.packaging_unit = data['packaging_unit']
    form13.packaging_volume = data['packaging_volume']
    form13.notes = data.get('notes')

    # 更新 Form12 中所有對應的其他資材名稱
    form12_records = Form12.query.filter_by(other_material_name=form13.other_material_name).all()
    for record in form12_records:
        record.other_material_name = data['other_material_name']
        record.manufacturer = data['manufacturer']  # 更新生產商
        record.supplier = data['supplier']
        record.packaging_unit = data['packaging_unit']
        record.packaging_volume = data['packaging_volume']

    # 提交變更
    db.session.commit()
    
    return jsonify({
        'message': '其他資材與代碼更新成功',
        'updated_form12_count': len(form12_records)  # 回傳更新的 Form12 紀錄數量
        }), 200

# 刪除其他資材與代碼
@app.route('/api/form13/<int:id>', methods=['DELETE'])
def delete_form13(id):
    record = Form13.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的其他資材與代碼
@app.route('/api/form13', methods=['GET'])
def get_all_form13(): 
    results = db.session.query(Form13, users.farmer_name).\
        join(users, users.id == Form13.user_id).all()
    
    forms = [
        {
            "id": result.Form13.id,
            "user_id": result.Form13.user_id,
            "farmer_name": result.farmer_name,
            "other_material_code": result.Form13.other_material_code,
            "other_material_name": result.Form13.other_material_name,
            "manufacturer": result.Form13.manufacturer,
            "supplier": result.Form13.supplier,
            "packaging_unit": result.Form13.packaging_unit,
            "packaging_volume": result.Form13.packaging_volume,
            "notes": result.Form13.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form14（其他資材入出庫紀錄）

# 新增其他資材入出庫紀錄
@app.route('/api/form14', methods=['POST'])
def add_form14():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    other_material_name = data.get('other_material_name')
    manufacturer = data.get('manufacturer')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    purchase_quantity = data.get('purchase_quantity') if data.get('purchase_quantity') not in ['', 'None', None] else None
    usage_quantity = data.get('usage_quantity') if data.get('usage_quantity') not in ['', 'None', None] else None
    remaining_quantity = data.get('remaining_quantity') if data.get('remaining_quantity') not in ['', 'None', None] else None
    notes = data.get('notes')

    # 去除單位，只提取數字部分
    def extract_number(value):
        if value is None:
            return Decimal("0.0")  # 避免 None 造成錯誤
        match = re.match(r"(\d+(\.\d+)?)", value)  # 匹配數字（可包含小數點）
        return float(match.group(1)) if match else 0.0

    try:
        # 提取包裝容量、購入量和使用量的數字部分
        purchase_quantity = extract_number(purchase_quantity) if purchase_quantity else 0.0
        usage_quantity = extract_number(usage_quantity) if usage_quantity else 0.0

        # **確保數據合理**
        if purchase_quantity < 0 or usage_quantity < 0:
            return jsonify({'error': '購入量和使用量不能為負數'}), 400

        # **計算剩餘量**
        numeric_packaging_volume = extract_number(packaging_volume)  # 提取數字部分計算
        remaining_quantity = purchase_quantity * numeric_packaging_volume  - usage_quantity
        remaining_quantity = max(remaining_quantity, Decimal("0.0"))  # 避免負數

        new_form = Form14(
            user_id=user_id,
            other_material_name=other_material_name,
            manufacturer=manufacturer,
            supplier=supplier,
            packaging_unit=packaging_unit,
            packaging_volume=packaging_volume,
            date=date,
            purchase_quantity=purchase_quantity,
            usage_quantity=usage_quantity,
            remaining_quantity=remaining_quantity,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '其他資材入出庫紀錄新增成功', 'form_id': new_form.id}), 201
    
    except Exception as e:
        print(f"Error occurred while adding form14: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新其他資材入出庫紀錄
@app.route('/api/form14/<int:id>', methods=['PUT'])
def update_form14(id):

    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    form14 = Form14.query.get(id)
    if not form14:
        return jsonify({'error': '其他資材入出庫紀錄未找到'}), 404
    
    # **提取數字部分**
    def extract_number(value):
        if value is None:
            return Decimal("0.0")  # 避免 None 造成錯誤
        match = re.search(r"(\d+(\.\d+)?)", str(value))  # 匹配數字（可包含小數點）
        return Decimal(match.group(1)) if match else Decimal("0.0")
    
    try:
        # **保留原始數據**
        form14.other_material_name = data['other_material_name']
        form14.manufacturer = data['manufacturer']
        form14.supplier = data['supplier']
        form14.packaging_unit = data['packaging_unit']
        form14.packaging_volume = data['packaging_volume']
        form14.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
        form14.notes = data.get('notes')
        
        # **提取數字部分進行計算**
        numeric_packaging_volume = extract_number(form14.packaging_volume)

        # 這裡改成 purchase_quantity和 usage_quantity 的更新
        form14.purchase_quantity = extract_number(data.get('purchase_quantity', form14.purchase_quantity))
        form14.usage_quantity = extract_number(data.get('usage_quantity', form14.usage_quantity))

        # **確保數據合理**
        if form14.purchase_quantity < 0 or form14.usage_quantity < 0:
            return jsonify({'error': '購入量和使用量不能為負數'}), 400

        # **計算剩餘量**
        form14.remaining_quantity = form14.purchase_quantity * numeric_packaging_volume - form14.usage_quantity
        form14.remaining_quantity = max(form14.remaining_quantity, Decimal("0.0"))  # 避免負數

        db.session.commit()
        return jsonify({
            'status': '其他資材入出庫紀錄更新成功',
            'form_id': form14.id,
            'updated_purchase_quantity': str(form14.purchase_quantity),  # ✅ 确保返回正确的购买量
            'updated_remaining_quantity': str(form14.remaining_quantity),
            'packaging_volume': form14.packaging_volume  # **回傳完整格式**
        }), 200
    
    except Exception as e:
        db.session.rollback()  # **出錯時回滾**
        return jsonify({'error': str(e)}), 500

# 刪除其他資材入出庫紀錄
@app.route('/api/form14/<int:id>', methods=['DELETE'])
def delete_form14(id):
    record = Form14.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的其他資材入出庫紀錄
@app.route('/api/form14', methods=['GET'])
def get_all_form14():
    results = db.session.query(Form14, users.farmer_name).\
        join(users, users.id == Form14.user_id).all()
    
    forms = [
        {
            "id": result.Form14.id,
            "user_id": result.Form14.user_id,
            "farmer_name": result.farmer_name,
            "other_material_name": result.Form14.other_material_name,
            "manufacturer": result.Form14.manufacturer,
            "supplier": result.Form14.supplier,
            "packaging_unit": result.Form14.packaging_unit,
            "packaging_volume": result.Form14.packaging_volume,
            "date": result.Form14.date.strftime('%Y-%m-%d') if result.Form14.date else None,
            "purchase_quantity": str(result.Form14.purchase_quantity),
            "usage_quantity": str(result.Form14.usage_quantity),
            "remaining_quantity": str(result.Form14.remaining_quantity),
            "notes": result.Form14.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form15（場地設施之保養、維修及清潔管理紀錄）

# 新增場地設施之保養、維修及清潔管理紀錄
@app.route('/api/form15', methods=['POST'])
def add_form15():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    item = data.get('item')
    operation = data.get('operation')
    recorder = data.get('recorder')
    notes = data.get('notes')

    try:
        new_form = Form15(
            user_id=user_id,
            date=date,
            item=item,
            operation=operation,
            recorder=recorder,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '場地設施之保養、維修及清潔管理紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form15: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新場地設施之保養、維修及清潔管理紀錄
@app.route('/api/form15/<int:id>', methods=['PUT'])
def update_form15(id):
    data = request.get_json()
    form = Form15.query.get(id)
    if not form:
        return jsonify({'error': '場地設施之保養、維修及清潔管理紀錄未找到'}), 404
    
    form.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    form.item = data['item']
    form.operation = data['operation']
    form.recorder = data['recorder']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '場地設施之保養、維修及清潔管理紀錄更新成功'}), 200

# 刪除場地設施之保養、維修及清潔管理紀錄
@app.route('/api/form15/<int:id>', methods=['DELETE'])
def delete_form15(id):
    record = Form15.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的場地設施之保養、維修及清潔管理紀錄
@app.route('/api/form15', methods=['GET'])
def get_all_form15():
    results = db.session.query(Form15, users.farmer_name).\
        join(users, users.id == Form15.user_id).all()
    
    forms = [
        {
            "id": result.Form15.id,
            "user_id": result.Form15.user_id,
            "farmer_name": result.farmer_name,
            "date": result.Form15.date.strftime('%Y-%m-%d') if result.Form15.date else None,
            "item": result.Form15.item,
            "operation": result.Form15.operation,
            "recorder": result.Form15.recorder,
            "notes": result.Form15.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form16（器具/機械/設備之保養、維修、校正及清潔管理紀錄）

# 新增器具/機械/設備之保養、維修、校正及清潔管理紀錄
@app.route('/api/form16', methods=['POST'])
def add_form16():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    item = data.get('item')
    operation = data.get('operation')
    recorder = data.get('recorder')
    notes = data.get('notes')

    try:
        new_form = Form16(
            user_id=user_id,
            date=date,
            item=item,
            operation=operation,
            recorder=recorder,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '器具/機械/設備之保養、維修、校正及清潔管理紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form16: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新器具/機械/設備之保養、維修、校正及清潔管理紀錄
@app.route('/api/form16/<int:id>', methods=['PUT'])
def update_form16(id):
    data = request.get_json()
    form = Form16.query.get(id)
    if not form:
        return jsonify({'error': '器具/機械/設備之保養、維修、校正及清潔管理紀錄未找到'}), 404
    
    form.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    form.item = data['item']
    form.operation = data['operation']
    form.recorder = data['recorder']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '器具/機械/設備之保養、維修、校正及清潔管理紀錄更新成功'}), 200

# 刪除器具/機械/設備之保養、維修、校正及清潔管理紀錄
@app.route('/api/form16/<int:id>', methods=['DELETE'])
def delete_form16(id):
    record = Form16.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的器具/機械/設備之保養、維修、校正及清潔管理紀錄
@app.route('/api/form16', methods=['GET'])
def get_all_form16():
    results = db.session.query(Form16, users.farmer_name).\
        join(users, users.id == Form16.user_id).all()
    
    forms = [
        {
            "id": result.Form16.id,
            "user_id": result.Form16.user_id,
            "farmer_name": result.farmer_name,
            "date": result.Form16.date.strftime('%Y-%m-%d') if result.Form16.date else None,
            "item": result.Form16.item,
            "operation": result.Form16.operation,
            "recorder": result.Form16.recorder,
            "notes": result.Form16.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form17（採收及採後處理紀錄）

# 新增採收及採後處理紀錄
@app.route('/api/form17', methods=['POST'])
def add_form17():
    data = request.get_json()
    print("收到的請求數據:", data)
    
    user_id = data.get('user_id')
    harvest_date = datetime.strptime(data.get('harvest_date'), '%Y-%m-%d') if data.get('harvest_date') not in ['', 'None', None] else None
    field_code = data.get('field_code') # field_code 對應 number
    crop_name = data.get('crop_name')
    batch_or_trace_no = data.get('batch_or_trace_no')
    harvest_weight = data.get('harvest_weight') if data.get('harvest_weight') not in ['', 'None', None] else None
    process_date = datetime.strptime(data.get('process_date'), '%Y-%m-%d') if data.get('process_date') not in ['', 'None', None] else None
    post_harvest_treatment = data.get('post_harvest_treatment')
    post_treatment_weight = data.get('post_treatment_weight') if data.get('post_treatment_weight') not in ['', 'None', None] else None
    verification_status = data.get('verification_status') 
    notes = data.get('notes')

    # 使用 `number` 查詢 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")

    try:
        new_form = Form17(
            user_id=user_id,
            lands_id=lands_id,  # 自動關聯 lands_id
            harvest_date=harvest_date,
            field_code=field_code,
            crop_name=crop_name,
            batch_or_trace_no=batch_or_trace_no,
            harvest_weight=harvest_weight,
            process_date=process_date,
            post_harvest_treatment=post_harvest_treatment,
            post_treatment_weight=post_treatment_weight,
            verification_status=verification_status, 
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '採收及採後處理紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form17: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新採收及採後處理紀錄
@app.route('/api/form17/<int:id>', methods=['PUT'])
def update_form17(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    form = Form17.query.get(id)
    if not form:
        return jsonify({'error': '採收及採後處理紀錄未找到'}), 404

    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form.lands_id = lands.id  # 更新关联的 lands_id

    form.harvest_date = datetime.strptime(data['harvest_date'], '%Y-%m-%d') if data.get('harvest_date') not in ['', 'None', None] else None
    form.field_code = field_code
    form.crop_name = data['crop_name']
    form.batch_or_trace_no = data['batch_or_trace_no']
    form.harvest_weight = data['harvest_weight'] if data.get('harvest_weight') not in ['', 'None', None] else None
    form.process_date = datetime.strptime(data['process_date'], '%Y-%m-%d') if data.get('process_date') not in ['', 'None', None] else None
    form.post_harvest_treatment = data['post_harvest_treatment']
    form.post_treatment_weight = data['post_treatment_weight'] if data.get('post_treatment_weight') not in ['', 'None', None] else None
    form.verification_status = data['verification_status'] 
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '採收及採後處理紀錄更新成功'}), 200

# 刪除採收及採後處理紀錄
@app.route('/api/form17/<int:id>', methods=['DELETE'])
def delete_form17(id):
    record = Form17.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的採收及採後處理紀錄
@app.route('/api/form17', methods=['GET'])
def get_all_form17():
    results = db.session.query(
        Form17,
        users.farmer_name.label("farmer_name"),
        Lands.number.label("land_number")
    ).join(users, Form17.user_id == users.id).join(Lands, Form17.lands_id == Lands.id).all()
    
    forms = [
        {
            "id": result.Form17.id,
            "user_id": result.Form17.user_id,
            "farmer_name": result.farmer_name,
            "harvest_date": result.Form17.harvest_date.strftime('%Y-%m-%d') if result.Form17.harvest_date else None,
            'field_code': result.land_number,  # 修正這裡
            "crop_name": result.Form17.crop_name,
            "batch_or_trace_no": result.Form17.batch_or_trace_no,
            "harvest_weight": str(result.Form17.harvest_weight),
            "process_date": result.Form17.process_date.strftime('%Y-%m-%d') if result.Form17.process_date else None,
            "post_harvest_treatment": result.Form17.post_harvest_treatment,
            "post_treatment_weight": str(result.Form17.post_treatment_weight),
            "verification_status": result.Form17.verification_status, 
            "notes": result.Form17.notes
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form18（乾燥作業紀錄）

# 新增乾燥作業紀錄
@app.route('/api/form18', methods=['POST'])
def add_form18():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id') 
    arena = data.get('arena')
    process_date = datetime.strptime(data.get('process_date'), '%Y-%m-%d') if data.get('process_date') not in ['', 'None', None] else None
    item = data.get('item')
    batch_number = data.get('batch_number')
    fresh_weight = data.get('fresh_weight') if data.get('fresh_weight') not in ['', 'None', None] else None
    operation = data.get('operation')
    dry_weight = data.get('dry_weight') if data.get('dry_weight') not in ['', 'None', None] else None
    remarks = data.get('remarks')

    try:
        new_form = Form18(
            user_id=user_id,
            arena=arena,
            process_date=process_date,
            item=item,
            batch_number=batch_number,
            fresh_weight=fresh_weight,
            operation=operation,
            dry_weight=dry_weight,
            remarks=remarks
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '乾燥作業紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form18: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新乾燥作業紀錄
@app.route('/api/form18/<int:id>', methods=['PUT'])
def update_form18(id):
    data = request.get_json()
    form = Form18.query.get(id)
    if not form:
        return jsonify({'error': '乾燥作業紀錄未找到'}), 404
    
    form.arena = data['arena']
    form.process_date = datetime.strptime(data['process_date'], '%Y-%m-%d') if data.get('process_date') not in ['', 'None', None] else None
    form.item = data['item']
    form.batch_number = data['batch_number']
    form.fresh_weight = data['fresh_weight'] if data.get('fresh_weight') not in ['', 'None', None] else None
    form.operation = data['operation']
    form.dry_weight = data['dry_weight'] if data.get('dry_weight') not in ['', 'None', None] else None
    form.remarks = data.get('remarks')
    db.session.commit()
    return jsonify({'message': '乾燥作業紀錄更新成功'}), 200

# 刪除乾燥作業紀錄
@app.route('/api/form18/<int:id>', methods=['DELETE'])
def delete_form18(id):
    record = Form18.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的乾燥作業紀錄
@app.route('/api/form18', methods=['GET'])
def get_all_form18():
    results = db.session.query(Form18, users.farmer_name).\
        join(users, users.id == Form18.user_id).all()
    
    forms = [
        {
            "id": result.Form18.id,
            "user_id": result.Form18.user_id,
            "farmer_name": result.farmer_name,
            "arena": result.Form18.arena,
            "process_date": result.Form18.process_date.strftime('%Y-%m-%d') if result.Form18.process_date else None,
            "item": result.Form18.item,
            "batch_number": result.Form18.batch_number,
            "fresh_weight": str(result.Form18.fresh_weight),
            "operation": result.Form18.operation,
            "dry_weight": str(result.Form18.dry_weight),
            "remarks": result.Form18.remarks
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form19（包裝及出貨紀錄）

# 新增包裝及出貨紀錄
@app.route('/api/form19', methods=['POST'])
def add_form19():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
        
    user_id = data.get('user_id')
    package = data.get('package')
    sale_date = datetime.strptime(data.get('sale_date'), '%Y-%m-%d') if data.get('sale_date') not in ['', 'None', None] else None
    product_name = data.get('product_name')
    sales_target = data.get('sales_target')
    batch_number = data.get('batch_number')
    shipment_quantity = data.get('shipment_quantity') if data.get('shipment_quantity') not in ['', 'None', None] else None
    packaging_spec = data.get('packaging_spec')
    label_usage_quantity = data.get('label_usage_quantity')
    label_void_quantity = data.get('label_void_quantity')
    verification_status = data.get('verification_status')

    try:
        new_form = Form19(
            user_id=user_id,
            package=package,
            sale_date=sale_date,
            product_name=product_name,
            sales_target=sales_target,
            batch_number=batch_number,
            shipment_quantity=shipment_quantity,
            packaging_spec=packaging_spec,
            label_usage_quantity=label_usage_quantity,
            label_void_quantity=label_void_quantity,
            verification_status=verification_status
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '包裝及出貨紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form19: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新包裝及出貨紀錄
@app.route('/api/form19/<int:id>', methods=['PUT'])
def update_form19(id):
    data = request.get_json()
    form = Form19.query.get(id)
    if not form:
        return jsonify({'error': '包裝及出貨紀錄未找到'}), 404
    
    form.package = data['package']
    form.sale_date = datetime.strptime(data['sale_date'], '%Y-%m-%d') if data.get('sale_date') not in ['', 'None', None] else None
    form.product_name = data['product_name']
    form.sales_target = data['sales_target']
    form.batch_number = data['batch_number']
    form.shipment_quantity = data['shipment_quantity'] if data.get('shipment_quantity') not in ['', 'None', None] else None
    form.packaging_spec = data['packaging_spec']
    form.label_usage_quantity = data['label_usage_quantity']
    form.label_void_quantity = data['label_void_quantity']
    form.verification_status = data['verification_status']
    db.session.commit()
    return jsonify({'message': '包裝及出貨紀錄更新成功'}), 200

# 刪除包裝及出貨紀錄
@app.route('/api/form19/<int:id>', methods=['DELETE'])
def delete_form19(id):
    record = Form19.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的包裝及出貨紀錄
@app.route('/api/form19', methods=['GET'])
def get_all_form19():
    results = db.session.query(Form19, users.farmer_name).\
        join(users, users.id == Form19.user_id).all()
    
    forms = [
        {
            "id": result.Form19.id,
            "user_id": result.Form19.user_id,
            "farmer_name": result.farmer_name,
            "package": result.Form19.package,
            "sale_date": result.Form19.sale_date.strftime('%Y-%m-%d') if result.Form19.sale_date else None,
            "product_name": result.Form19.product_name,
            "sales_target": str(result.Form19.sales_target),
            "batch_number": result.Form19.batch_number,
            "shipment_quantity": str(result.Form19.shipment_quantity),
            "packaging_spec": result.Form19.packaging_spec,
            "label_usage_quantity": str(result.Form19.label_usage_quantity),
            "label_void_quantity": str(result.Form19.label_void_quantity),
            "verification_status": result.Form19.verification_status
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form20（作業人員衛生及健康狀態檢查紀錄）

# 新增作業人員衛生及健康狀態檢查紀錄
@app.route('/api/form20', methods=['POST'])
def add_form20():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    checkitem = data.get('checkitem')
    jobdate = datetime.strptime(data.get('jobdate'), '%Y-%m-%d') if data.get('jobdate') not in ['', 'None', None] else None
    operator_name = data.get('temperature')  

    try:
        new_form = Form20(
            user_id=user_id,
            checkitem=checkitem,
            jobdate=jobdate,
            operator_name=operator_name
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '作業人員衛生及健康狀態檢查紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form20: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新作業人員衛生及健康狀態檢查紀錄
@app.route('/api/form20/<int:id>', methods=['PUT'])
def update_form20(id):
    data = request.get_json()
    form = Form20.query.get(id)
    if not form:
        return jsonify({'error': '作業人員衛生及健康狀態檢查紀錄未找到'}), 404
    
    form.checkitem = data['checkitem']
    form.jobdate = datetime.strptime(data['jobdate'], '%Y-%m-%d') if data.get('jobdate') not in ['', 'None', None] else None
    form.operator_name = data['operator_name']
    db.session.commit()
    return jsonify({'message': '作業人員衛生及健康狀態檢查紀錄更新成功'}), 200

# 刪除作業人員衛生及健康狀態檢查紀錄
@app.route('/api/form20/<int:id>', methods=['DELETE'])
def delete_form20(id):
    record = Form20.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit() 
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的作業人員衛生及健康狀態檢查紀錄
@app.route('/api/form20', methods=['GET'])
def get_all_form20():
    results = db.session.query(Form20, users.farmer_name).\
        join(users, users.id == Form20.user_id).all()
    
    forms = [
        {
            "id": result.Form20.id,
            "user_id": result.Form20.user_id,
            "farmer_name": result.farmer_name,
            "checkitem": result.Form20.checkitem,
            "jobdate": result.Form20.jobdate.strftime('%Y-%m-%d') if result.Form20.jobdate else None,
            "operator_name": result.Form20.operator_name
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form22（客戶抱怨/回饋紀錄）

# 新增客戶抱怨/回饋紀錄
@app.route('/api/form22', methods=['POST'])
def add_form22():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    customer_name = data.get('customer_name')
    customer_phone = data.get('customer_phone')
    complaint = data.get('complaint')
    resolution = data.get('resolution')
    processor_name = data.get('processor_name')
    processor_date = datetime.strptime(data.get('processor_date'), '%Y-%m-%d') if data.get('processor_date') not in ['', 'None', None] else None

    try:
        new_form = Form22(
            user_id=user_id,
            date=date,
            customer_name=customer_name,
            customer_phone=customer_phone,
            complaint=complaint,
            resolution=resolution,
            processor_name=processor_name,
            processor_date=processor_date
        )
        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '客戶抱怨/回饋紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form22: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新客戶抱怨/回饋紀錄
@app.route('/api/form22/<int:id>', methods=['PUT'])
def update_form22(id):
    data = request.get_json()
    form = Form22.query.get(id)
    if not form:
        return jsonify({'error': '客戶抱怨/回饋紀錄未找到'}), 404

    form.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    form.customer_name = data['customer_name']
    form.customer_phone = data['customer_phone']
    form.complaint = data['complaint']
    form.resolution = data['resolution']
    form.processor_name = data['processor_name']
    form.processor_date = datetime.strptime(data['processor_date'], '%Y-%m-%d') if data.get('processor_date') not in ['', 'None', None] else None
    db.session.commit()
    return jsonify({'message': '客戶抱怨/回饋紀錄更新成功'}), 200

# 刪除客戶抱怨/回饋紀錄
@app.route('/api/form22/<int:id>', methods=['DELETE'])
def delete_form22(id):
    record = Form22.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的客戶抱怨/回饋紀錄
@app.route('/api/form22', methods=['GET'])
def get_all_form22():
    results = db.session.query(Form22, users.farmer_name).\
        join(users, users.id == Form22.user_id).all()

    forms = [
        {
            "id": result.Form22.id,
            "user_id": result.Form22.user_id,
            "farmer_name": result.farmer_name,
            "date": result.Form22.date.strftime('%Y-%m-%d') if result.Form22.date else None,
            "customer_name": result.Form22.customer_name,
            "customer_phone": result.Form22.customer_phone,
            "complaint": result.Form22.complaint,
            "resolution": result.Form22.resolution,
            "processor_name": result.Form22.processor_name,
            "processor_date": result.Form22.processor_date.strftime('%Y-%m-%d') if result.Form22.processor_date else None
        }
        for result in results
    ]
    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# 根據肥料資材名稱查詢相應資料
@app.route('/api/form07/material/<string:fertilizer_material_name>', methods=['GET'])
def get_material_fertilizer(fertilizer_material_name):
    form = Form07.query.filter_by(fertilizer_material_name=fertilizer_material_name).first()
    if not form:
        return jsonify({'error': '未找到該肥料資材名稱'}), 404
    
    # 回傳相關的欄位資料
    material_fertilizer = {
        "manufacturer": form.manufacturer or '',
        "supplier": form.supplier or '',
        "packaging_unit": form.packaging_unit or '',
        "packaging_volume": form.packaging_volume or ''
    }
    return jsonify(material_fertilizer)

# 根據 藥 資材名稱查詢相應資料
@app.route('/api/form10/material/<string:pest_control_material_name>', methods=['GET'])
def get_material_pest(pest_control_material_name):
    form = Form10.query.filter_by(pest_control_material_name=pest_control_material_name).first()
    if not form:
        return jsonify({'error': '未找到該其他資材名稱'}), 404
    
    # 回傳相關的欄位資料
    material_pest = {
        "dosage_form": form.dosage_form or '',
        "brand_name": form.brand_name or '',
        "supplier": form.supplier or '',
        "packaging_unit": form.packaging_unit or '',
        "packaging_volume": form.packaging_volume or ''
    }
    return jsonify(material_pest)

# 根據其他資材名稱查詢相應資料
@app.route('/api/form13/material/<string:other_material_name>', methods=['GET'])
def get_material_other(other_material_name):
    form = Form13.query.filter_by(other_material_name=other_material_name).first()
    if not form:
        return jsonify({'error': '未找到該其他資材名稱'}), 404
    
    # 回傳相關的欄位資料
    material_other = {
        "manufacturer": form.manufacturer or '',
        "supplier": form.supplier or '',
        "packaging_unit": form.packaging_unit or '',
        "packaging_volume": form.packaging_volume or ''
    }
    return jsonify(material_other)
# ----------------------------------------------------------------------------------------------
@app.route('/api/calc', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        result = eval(data['expression'])
        return jsonify({'result': result})
    except:
        return jsonify({'error': '錯誤的運算式'}), 400

@app.route('/api/convert', methods=['POST'])
def convert_unit():
    data = request.get_json()
    value = float(data['value'])
    from_unit = data['from']
    to_unit = data['to']
    unit_type = data['type']

    conversions = {
    'length': {
        '公尺': 1, '公里': 1000, '公分': 0.01, '英吋': 0.0254, '英尺': 0.3048
    },
    'weight': {
        '公斤': 1, '克': 0.001, '磅': 0.453592, '公噸':1000,'台斤':0.6,'毫克':0.000001
    },
    'area': {
        '平方公尺': 1,
        '平方公里': 1000000,
        '英畝': 4046.86,
        '公畝': 100,
        '公頃': 10000,
        '甲': 9699.2,
        '坪':3.3059
    },
    'CC':{
        '公升':1,'毫升':0.001
    },
    'temperature': None
}


    if not from_unit or not to_unit or unit_type not in conversions:
        return jsonify({'error': '請選擇正確的單位'}), 400

    if unit_type == 'temperature':
        def convert_temp(v, f, t):
            if f == t: return v
            if f == '攝氏':
                return v * 9/5 + 32 if t == '華氏' else v + 273.15
            if f == '華氏':
                return (v - 32) * 5/9 if t == '攝氏' else (v - 32) * 5/9 + 273.15
            if f == '開爾文':
                return v - 273.15 if t == '攝氏' else (v - 273.15) * 9/5 + 32
        result = convert_temp(value, from_unit, to_unit)
    else:
        base = value * conversions[unit_type][from_unit]
        result = base / conversions[unit_type][to_unit]

    return jsonify({'result': round(result, 4)})








# ----------------------------------------------------------------------------------------------
# 在應用程式啟動時測試資料庫連線
if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)

