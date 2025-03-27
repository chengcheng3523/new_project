from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token

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

        # 查找是否有該使用者
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
    print("Received POST request")  # 新增调试信息
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
    print(f"Attempting to delete ID: {id}")  # 新增调试信息
    lands = Lands.query.get(id)
    if not lands:
        print(f"ID {id} not found")  # 新增调试信息
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

    # 使用 `number` 查找 `lands_id`
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

    # 根據 crop 查找對應的 lands_id
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

    # 使用 `number` 查找 `lands_id`
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

# 查詢所有使用者的栽培工作
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
    
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    field_code = data.get('field_code')
    crop = data.get('crop')
    fertilizer_type = data.get('fertilizer_type')
    fertilizer_material_name = data.get('fertilizer_material_name')
    fertilizer_amount = float(data.get('fertilizer_amount')) if data.get('fertilizer_amount') not in ['', 'None', None] else None
    dilution_factor = float(data.get('dilution_factor')) if data.get('dilution_factor') not in ['', 'None', None] else None
    operator = data.get('operator')
    process = data.get('process')
    notes = data.get('notes')

    # 使用 `number` 查找 `lands_id`
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
            lands_id=lands_id,  # 自動關聯 lands_id
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

        # 查找該肥料的最新庫存記錄
        latest_inventory = Form08.query.filter_by(
            user_id=user_id,
            fertilizer_material_name=fertilizer_material_name
        ).order_by(Form08.date.desc()).first()

        if latest_inventory:
            # 計算新的剩餘量
            new_remaining = float(latest_inventory.remaining_quantity) - (fertilizer_amount if fertilizer_amount else 0)
            
            # 新增一筆 form08 記錄
            new_form08 = Form08(
                user_id=user_id,
                fertilizer_material_name=fertilizer_material_name,
                date=date_used,
                usage_quantity=fertilizer_amount,
                remaining_quantity=new_remaining,
                notes=f'自動新增，對應 form06 使用記錄，稀釋倍數: {dilution_factor if dilution_factor else "無"}'
            )
            db.session.add(new_form08)

        db.session.add(new_form)
        db.session.commit()

        # 返回成功訊息和剩餘量資訊
        response_data = {
            'status': '肥料施用新增成功',
            'form_id': new_form.id,
            'remaining_quantity': float(latest_inventory.remaining_quantity) if latest_inventory else None
        }
        return jsonify(response_data), 201
    
    except Exception as e:
        print(f"Error occurred while adding form06: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新肥料施用
@app.route('/api/form06/<int:id>', methods=['PUT'])
def update_form06(id):
    data = request.get_json()

    print("收到的更新數據:", data)
    
    form = Form06.query.get(id)
    if not form:
        return jsonify({'error': '肥料施用未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form.field_code)

    # 如果 field_code 更新了，检查是否存在對應的農地
    if field_code != form.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form.lands_id = lands.id  # 更新關聯的 lands_id

    form.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    form.field_code = field_code
    form.crop = data['crop']
    form.fertilizer_type = data['fertilizer_type']
    form.fertilizer_material_name = data['fertilizer_material_name']
    form.fertilizer_amount = data['fertilizer_amount'] if data.get('fertilizer_amount') not in ['', 'None', None] else None
    form.dilution_factor = data['dilution_factor'] if data.get('dilution_factor') not in ['', 'None', None] else None
    form.operator = data['operator']
    form.process = data['process']
    form.notes = data.get('notes')

    try:
        db.session.commit()

        # 自動新增一筆 form08 記錄
        new_form08 = Form08(
            user_id=form.user_id,
            fertilizer_material_name=form.fertilizer_material_name,
            date=form.date_used,
            usage_quantity=form.fertilizer_amount,
            remaining_quantity=(0 - form.fertilizer_amount),  # 假設初始剩餘量為 0
            notes='自動新增，對應 form06 更新'
        )
        db.session.add(new_form08)

        return jsonify({'message': '肥料施用更新成功'}), 200
    except Exception as e:
        print(f"Error occurred while updating form06: {str(e)}")
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
    notes = data.get('notes')
    
    try:
        new_form = Form07(
            user_id=user_id,
            fertilizer_material_code=fertilizer_material_code,
            fertilizer_material_name=fertilizer_material_name,
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
    form = Form07.query.get(id)
    if not form:
        return jsonify({'error': '肥料資材與代碼未找到'}), 404
    
    form.fertilizer_material_code = data['fertilizer_material_code']
    form.fertilizer_material_name = data['fertilizer_material_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '肥料資材與代碼更新成功'})

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

    try:
        new_form = Form08(
            user_id=user_id,
            fertilizer_material_name=fertilizer_material_name,
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
        return jsonify({'status': '肥料入出庫新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form08: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新肥料入出庫
@app.route('/api/form08/<int:id>', methods=['PUT'])
def update_form08(id):
    data = request.get_json()
    form = Form08.query.get(id)
    if not form:
        return jsonify({'error': '肥料入出庫未找到'}), 404
    
    form.fertilizer_material_name = data['fertilizer_material_name']
    form.manufacturer = data['manufacturer']
    form.supplier = data['supplier']
    form.packaging_unit = data['packaging_unit']
    form.packaging_volume = data['packaging_volume']
    form.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None 
    form.purchase_quantity = data['purchase_quantity'] if data.get('purchase_quantity') not in ['', 'None', None] else None
    form.usage_quantity = data['usage_quantity'] if data.get('usage_quantity') not in ['', 'None', None] else None
    form.remaining_quantity = data['remaining_quantity'] if data.get('remaining_quantity') not in ['', 'None', None] else None
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '肥料入出庫更新成功'})

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
    
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    field_code = data.get('field_code')
    crop = data.get('crop')
    pest_target = data.get('pest_target')
    pest_control_material_name = data.get('pest_control_material_name')
    water_volume = data.get('water_volume') if data.get('water_volume') not in ['', 'None', None] else None
    chemical_usage = data.get('chemical_usage') if data.get('chemical_usage') not in ['', 'None', None] else None
    dilution_factor = data.get('dilution_factor') if data.get('dilution_factor') not in ['', 'None', None] else None
    safety_harvest_period = data.get('safety_harvest_period')
    operator_method = data.get('operator_method')
    operator = data.get('operator')
    notes = data.get('notes')

      # 使用 `number` 查找 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")

    try:
        new_form = Form09(
            user_id=user_id,
            lands_id=lands_id,  # 自動關聯 lands_id
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

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '有害生物防治或環境消毒資材施用新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form09: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新有害生物防治或環境消毒資材施用
@app.route('/api/form09/<int:id>', methods=['PUT'])
def update_form09(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    form = Form09.query.get(id)
    if not form:
        return jsonify({'error': '有害生物防治或環境消毒資材施用未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form.lands_id = lands.id  # 更新关联的 lands_id

    form.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    form.field_code = field_code
    form.crop = data['crop']
    form.pest_target = data['pest_target']
    form.pest_control_material_name = data['pest_control_material_name']
    form.water_volume = data['water_volume'] if data.get('water_volume') not in ['', 'None', None] else None
    form.chemical_usage = data['chemical_usage'] if data.get('chemical_usage') not in ['', 'None', None] else None
    form.dilution_factor = data['dilution_factor'] if data.get('dilution_factor') not in ['', 'None', None] else None
    form.safety_harvest_period = data['safety_harvest_period']
    form.operator_method = data['operator_method']
    form.operator = data['operator']
    form.notes = data.get('notes')

    try:
        db.session.commit()
        return jsonify({'message': '有害生物防治或環境消毒資材施用更新成功'})
    except Exception as e:
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
    notes = data.get('notes')

    try:
        new_form = Form10(
            user_id=user_id,
            pest_control_material_code=pest_control_material_code,
            pest_control_material_name=pest_control_material_name,
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
    form = Form10.query.get(id)
    if not form:
        return jsonify({'error': '防治資材與代碼未找到'}), 404
    
    form.pest_control_material_code = data['pest_control_material_code']
    form.pest_control_material_name = data['pest_control_material_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '防治資材與代碼更新成功'})

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

    try:
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
    form = Form11.query.get(id)
    if not form:
        return jsonify({'error': '有害生物防治或環境消毒資材入出庫未找到'}), 404
    
    form.pest_control_material_name = data['pest_control_material_name']
    form.dosage_form = data['dosage_form']
    form.brand_name = data['brand_name']
    form.supplier = data['supplier']
    form.packaging_unit = data['packaging_unit']
    form.packaging_volume = data['packaging_volume']
    form.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    form.purchase_quantity = data['purchase_quantity'] if data.get('purchase_quantity') not in ['', 'None', None] else None
    form.usage_quantity = data['usage_quantity'] if data.get('usage_quantity') not in ['', 'None', None] else None
    form.remaining_quantity = data['remaining_quantity'] if data.get('remaining_quantity') not in ['', 'None', None] else None
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '有害生物防治或環境消毒資材入出庫更新成功'})

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

    # 使用 `number` 查找 `lands_id`
    lands = Lands.query.filter_by(number=field_code).first()
    
    if not lands:
        print(f"❌ 錯誤: 找不到 field_code={field_code} 對應的 lands_id")  # ← 新增錯誤提示
        return jsonify({'error': f'找不到 field_code={field_code} 對應的農地'}), 400
    
    lands_id = lands.id  # 取得 lands_id
    print(f"✅ 成功找到 lands_id={lands_id} 對應的 field_code={field_code}")

    try:
        new_form = Form12(
            user_id=user_id,
            lands_id=lands_id,  # 確保 lands_id 有正確的值
            date_used=date_used,
            field_code=field_code,
            crop=crop,
            other_material_name=other_material_name,
            usage_amount=usage_amount,
            operator=operator,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '其他資材使用紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form12: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新其他資材使用紀錄
@app.route('/api/form12/<int:id>', methods=['PUT'])
def update_form12(id):
    data = request.get_json()
    print("收到的更新數據:", data)

    form = Form12.query.get(id)
    if not form:
        return jsonify({'error': '其他資材使用紀錄未找到'}), 404
    
    # 获取 field_code，如果没有传递就使用原来的 field_code
    field_code = data.get('field_code', form.field_code)

    # 如果 field_code 更新了，检查是否存在对应的农地
    if field_code != form.field_code:
        lands = Lands.query.filter_by(number=field_code).first()
        if not lands:
            return jsonify({'error': '無效的田區代號'}), 400
        form.lands_id = lands.id  # 更新关联的 lands_id
    
    form.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d') if data.get('date_used') not in ['', 'None', None] else None
    form.field_code = field_code
    form.crop = data['crop']
    form.other_material_name = data['other_material_name']
    form.usage_amount = data['usage_amount'] if data.get('usage_amount') not in ['', 'None', None] else None
    form.operator = data['operator']
    form.notes = data.get('notes')

    try:
        db.session.commit()
        return jsonify({'message': '其他資材使用紀錄更新成功'}), 200
    except Exception as e:
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
    notes = data.get('notes')

    try:
        new_form = Form13(
            user_id=user_id,
            other_material_code=other_material_code,
            other_material_name=other_material_name,
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
    form = Form13.query.get(id)
    if not form:
        return jsonify({'error': '其他資材與代碼未找到'}), 404
    
    form.other_material_code = data['other_material_code']
    form.other_material_name = data['other_material_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '其他資材與代碼更新成功'})

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

    try:
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
    form = Form14.query.get(id)
    if not form:
        return jsonify({'error': '其他資材入出庫紀錄未找到'}), 404
    
    form.other_material_name = data['other_material_name']
    form.manufacturer = data['manufacturer']
    form.supplier = data['supplier']
    form.packaging_unit = data['packaging_unit']
    form.packaging_volume = data['packaging_volume']
    form.date = datetime.strptime(data['date'], '%Y-%m-%d') if data.get('date') not in ['', 'None', None] else None
    form.purchase_quantity = data['purchase_quantity'] if data.get('purchase_quantity') not in ['', 'None', None] else None
    form.usage_quantity = data['usage_quantity'] if data.get('usage_quantity') not in ['', 'None', None] else None
    form.remaining_quantity = data['remaining_quantity'] if data.get('remaining_quantity') not in ['', 'None', None] else None
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '其他資材入出庫紀錄更新成功'})

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
    return jsonify({'message': '場地設施之保養、維修及清潔管理紀錄更新成功'})

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
    return jsonify({'message': '器具/機械/設備之保養、維修、校正及清潔管理紀錄更新成功'})

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

    # 使用 `number` 查找 `lands_id`
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
    return jsonify({'message': '採收及採後處理紀錄更新成功'})

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
    return jsonify({'message': '乾燥作業紀錄更新成功'})

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
    return jsonify({'message': '包裝及出貨紀錄更新成功'})

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
    return jsonify({'message': '作業人員衛生及健康狀態檢查紀錄更新成功'})

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
    return jsonify({'message': '客戶抱怨/回饋紀錄更新成功'})

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




















# ----------------------------------------------------------------------------------------------
# 在應用程式啟動時測試資料庫連線
if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)

