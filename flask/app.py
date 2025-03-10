from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
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

#Database connection settings
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'       #MYSQL 使用者
app.config['MYSQL_PASSWORD'] = 'root'   #MYSQL 密碼
app.config['MYSQL_DB'] = 'new_database' #MYSQL 名稱
mysql = MySQL(app)

# 檢查 MySQL 資料庫連線是否正常。
def test_db_connection():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT 1")
        cur.close()
        print("Database connection successful.")
    except Exception as e:
        print(f"Database connection failed: {str(e)}")

# ----------------------------------------------------------------------------------------------
# 定義資料表模型
from models import db  # 从 models.py 导入 db 实例
from models import users, LandParcel, Form002, Form02, Form03, Form04, Form05, Form06, Form07, Form08, Form09
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
        existing_user.land_parcel_id = data.get('land_parcel_id')
        existing_user.farmer_name = data.get('farmer_name')
        existing_user.phone = data.get('phone')
        existing_user.fax = data.get('fax')
        existing_user.mobile = data.get('mobile')
        existing_user.address = data.get('address')
        existing_user.email = data.get('email')
        existing_user.total_area = data.get('total_area')
        existing_user.notes = data.get('notes')

        db.session.commit()

        return jsonify({'status': '使用者資料更新成功'}), 200
    except Exception as e:
        print(f"Error occurred while updating profile: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 查詢users-all
@app.route('/api/users/get', methods=['GET'])
def get_users():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SHOW TABLES LIKE 'users'")  # 先检查表是否存在
        if not cur.fetchone():
            return jsonify({'error': '資料表 users 不存在'}), 500

        cur.execute("SELECT * FROM users")
        users = cur.fetchall()
        cur.close()
        return jsonify(users)
    except Exception as e:
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
                      'address', 'email', 'total_area', 'notes', 'land_parcel_id']:
            if field in data:
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
@app.route('/api/land_parcels', methods=['POST'])
def add_land_parcel():
    print("Received POST request")  # 新增调试信息
    data = request.get_json()
    if not data:
        return jsonify({'error': '请求的 JSON 格式错误'}), 400

    user_id = data.get('user_id')
    number = data.get('number')
    land_parcel_number = data.get('land_parcel_number')
    area = data.get('area')
    crop = data.get('crop')
    notes = data.get('notes')

    new_land_parcel = LandParcel(
        user_id=user_id,
        number=number,
        land_parcel_number=land_parcel_number,
        area=area,
        crop=crop,
        notes=notes
    )

    db.session.add(new_land_parcel)
    db.session.commit()

    return jsonify({'status': '農地資訊新增成功', 'land_parcel_id': new_land_parcel.id}), 201

# 更新農地資訊 API
@app.route('/api/land_parcels/<int:id>', methods=['PUT'])
def update_land_parcel(id):
    data = request.get_json()
    land_parcel = LandParcel.query.get(id)

    if not land_parcel:
        return jsonify({'error': '農地資訊未找到'}), 404

    land_parcel.number = data.get('number', land_parcel.number)
    land_parcel.land_parcel_number = data.get('land_parcel_number', land_parcel.land_parcel_number)
    land_parcel.area = data.get('area', land_parcel.area)
    land_parcel.crop = data.get('crop', land_parcel.crop)
    land_parcel.notes = data.get('notes', land_parcel.notes)

    db.session.commit()
    return jsonify({'status': '農地資訊更新成功'}), 200

# 删除農地資訊 API
@app.route('/api/land_parcels/<int:id>', methods=['DELETE'])
def delete_land_parcel(id):
    print(f"Attempting to delete ID: {id}")  # 新增调试信息
    land_parcel = LandParcel.query.get(id)
    if not land_parcel:
        print(f"ID {id} not found")  # 新增调试信息
        return jsonify({'error': '農地資訊未找到'}), 404

    db.session.delete(land_parcel)
    db.session.commit()
    return jsonify({'status': '農地資訊已删除'}), 200


# 查詢所有農地資訊 API
@app.route('/api/land_parcels', methods=['GET'])
def get_land_parcels():
    results = db.session.query(
        LandParcel,
        users.farmer_name
    ).join(users).all()

    land_parcels = [
        {
            'id': result.LandParcel.id,
            'user_id': result.LandParcel.user_id,
            'farmer_name': result.farmer_name,
            'number': result.LandParcel.number,
            'land_parcel_number': result.LandParcel.land_parcel_number,
            'area': str(result.LandParcel.area),
            'crop': result.LandParcel.crop,
            'notes': result.LandParcel.notes
        }
        for result in results
    ]

    return jsonify(land_parcels)

# ----------------------------------------------------------------------------------------
# 生產計畫

# 新增生產計畫
@app.route('/api/form002', methods=['POST'])
def add_form002():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400

    user_id = data.get('user_id')
    area_code = data.get('area_code')
    area_size = data.get('area_size')
    month = data.get('month')
    crop_info = data.get('crop_info')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not area_code:
        return jsonify({'error': '缺少 場區代號'}), 400
    if not area_size:
        return jsonify({'error': '缺少 場區面積(公頃)'}), 400
    if not month:
        return jsonify({'error': '缺少 月份'}), 400
    if not crop_info:
        return jsonify({'error': '缺少 種植作物種類、產期、預估產量（公斤）'}), 400

    try:
        new_form = Form002(
            user_id=user_id,
            area_code=area_code,
            area_size=area_size,
            month=month,
            crop_info=crop_info,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '生產計畫新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form002: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新生產計畫
@app.route('/api/form002/<int:id>', methods=['PUT'])
def update_form002(id):
    data = request.get_json()
    form = Form002.query.get(id)
    if not form:
        return jsonify({'error': '生產計畫未找到'}), 404
    
    form.area_code = data.get('area_code', form.area_code)
    form.area_size = data.get('area_size', form.area_size)
    form.month = data.get('month', form.month)
    form.crop_info = data.get('crop_info', form.crop_info)
    form.notes = data.get('notes', form.notes)
    
    db.session.commit()
    return jsonify({'status': '生產計畫更新成功'}), 200

# 刪除生產計畫
@app.route('/api/form002/<int:id>', methods=['DELETE'])
def delete_form002(id):
    form = Form002.query.get(id)
    if not form:
        return jsonify({'error': '生產計畫未找到'}), 404
    
    db.session.delete(form)
    db.session.commit()
    return jsonify({'status': '生產計畫已刪除'}), 200

# 查詢某使用者的生產計畫
@app.route('/api/form002/user/<int:user_id>', methods=['GET'])
def get_user_form002(user_id):
    results = db.session.query(
        Form002, db.column('users.farmer_name')
    ).join(
        db.table('users'), Form002.user_id == db.column('users.id')
    ).filter(
        Form002.user_id == user_id
    ).all()

    form_list = [
        {
            'id': result.Form002.id,
            'user_id': result.Form002.user_id,
            'area_code': result.Form002.area_code,
            'area_size': str(result.Form002.area_size),
            'month': result.Form002.month,
            'crop_info': result.Form002.crop_info,
            'notes': result.Form002.notes
        }
        for result in results
    ]
    return jsonify(form_list)

# 查詢所有生產計畫 API
@app.route('/api/form002', methods=['GET'])
def get_all_form002():
    results = db.session.query(Form002, users.farmer_name).\
        join(users, users.id == Form002.user_id).all()

    forms = [
        {
            'id': result.Form002.id,
            'user_id': result.Form002.user_id,
            'farmer_name': result.farmer_name,
            'area_code': result.Form002.area_code,
            'area_size': str(result.Form002.area_size),
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
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400

    user_id = data.get('user_id')
    cultivated_crop = data.get('cultivated_crop')
    crop_variety = data.get('crop_variety')
    seed_source = data.get('seed_source')
    seedling_purchase_date = datetime.strptime(data.get('seedling_purchase_date'), '%Y-%m-%d')
    seedling_purchase_type = data.get('seedling_purchase_type')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not cultivated_crop:
        return jsonify({'error': '缺少 栽培作物'}), 400
    if not crop_variety:
        return jsonify({'error': '缺少 栽培品種'}), 400
    if not seed_source:
        return jsonify({'error': '缺少 種子(苗)來源'}), 400
    if not seedling_purchase_date:
        return jsonify({'error': '缺少 育苗(購入)日期'}), 400
    if not seedling_purchase_type:
        return jsonify({'error': '缺少 育苗(購入)種類'}), 400
    
    try:
        new_form = Form02(
            user_id=user_id,
            cultivated_crop=cultivated_crop,
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
    
    form.cultivated_crop = data['cultivated_crop']
    form.crop_variety = data['crop_variety']
    form.seed_source = data['seed_source']
    form.seedling_purchase_date = datetime.strptime(data['seedling_purchase_date'], '%Y-%m-%d')
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
            'cultivated_crop': result.Form02.cultivated_crop,
            'crop_variety': result.Form02.crop_variety,
            'seed_source': result.Form02.seed_source,
            'seedling_purchase_date': result.Form02.seedling_purchase_date.strftime('%Y-%m-%d'),
            'seedling_purchase_type': result.Form02.seedling_purchase_type,
            'notes': result.Form02.notes
        }
        for result in results
    ]

    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# 栽培工作紀錄

# 新增栽培工作紀錄
@app.route('/api/form03', methods=['POST'])
def add_form03():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    operation_date =  datetime.strptime(data.get('operation_date'), '%Y-%m-%d')
    field_code = data.get('field_code')
    crop = data.get('crop')
    crop_content = data.get('crop_content')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not operation_date:
        return jsonify({'error': '缺少 作業日期'}), 400
    if not field_code:
        return jsonify({'error': '缺少 田區代號'}), 400
    if not crop:
        return jsonify({'error': '缺少 crop'}), 400
    if not crop_content:
        return jsonify({'error': '缺少 crop_content'}), 400
    
    try:
        new_form = Form03(
            user_id=user_id,
            operation_date=operation_date,
            field_code=field_code,
            crop=crop,
            crop_content=crop_content,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '栽培工作新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form03: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新栽培工作紀錄
@app.route('/api/form03/<int:id>', methods=['PUT'])
def update_form03(id):
    data = request.get_json()
    form = Form03.query.get(id)
    if not form:
        return jsonify({'error': '栽培工作紀錄 not found未找到'}), 404
    
    form.operation_date = datetime.strptime(data['operation_date'], '%Y-%m-%d')
    form.field_code = data['field_code']
    form.crop = data['crop']
    form.crop_content = data['crop_content']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '栽培工作紀錄更新成功'})

# 刪除栽培工作紀錄
@app.route('/api/form03/<int:id>', methods=['DELETE'])
def delete_form03(id):
    record = Form03.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的栽培紀錄
@app.route('/api/form03', methods=['GET'])
def get_all_form03(): 
    results = db.session.query(Form03, users.farmer_name).\
        join(users, users.id == Form03.user_id).all()
    
    forms = [
        {
            "id": result.Form03.id,
            "user_id": result.Form03.user_id,
            "farmer_name": result.farmer_name,
            "operation_date": result.Form03.operation_date.strftime('%Y-%m-%d'),
            "field_code": result.Form03.field_code,
            "crop": result.Form03.crop,
            "crop_content": result.Form03.crop_content,
            "notes": result.Form03.notes
        }
        for result in results
    ]

    return jsonify(forms)
# ----------------------------------------------------------------------------------------------







# 未測試資料








































# 養液配製紀錄

# 新增養液配製紀錄
@app.route('/api/form04', methods=['POST'])
def add_form04():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    preparation_date =  datetime.strptime(data.get('preparation_date'), '%Y-%m-%d')
    material_code_or_name = data.get('material_code_or_name')
    usage_amount = data.get('usage_amount')
    preparation_process = data.get('preparation_process')
    final_ph_value = data.get('final_ph_value')
    final_ec_value = data.get('final_ec_value')
    preparer_name = data.get('preparer_name')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not preparation_date:
        return jsonify({'error': '缺少 preparation_date'}), 400
    if not usage_amount:
        return jsonify({'error': '缺少 usage_amount'}), 400
    if not preparation_process:
        return jsonify({'error': '缺少 preparation_process'}), 400
    if not final_ph_value:
        return jsonify({'error': '缺少 final_ph_value'}), 400
    if not final_ec_value:
        return jsonify({'error': '缺少 final_ec_value'}), 400
    if not preparer_name:
        return jsonify({'error': '缺少 preparer_name'}), 400
    
    try:
        new_form = Form04(
            user_id=user_id,
            preparation_date=preparation_date,
            material_code_or_name=material_code_or_name,
            usage_amount=usage_amount,
            preparation_process=preparation_process,
            final_ph_value=final_ph_value,
            final_ec_value=final_ec_value,
            preparer_name=preparer_name,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '養液配製紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form04: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新養液配製紀錄
@app.route('/api/form04/<int:id>', methods=['PUT'])
def update_form04(id):
    data = request.get_json()
    form = Form04.query.get(id)
    if not form:
        return jsonify({'error': '養液配製紀錄 未找到'}), 404
    
    form.preparation_date = datetime.strptime(data['preparation_date'], '%Y-%m-%d')
    form.material_code_or_name = data['material_code_or_name']
    form.usage_amount = data['usage_amount']
    form.preparation_process = data['preparation_process']
    form.final_ph_value = data['final_ph_value']
    form.final_ec_value = data['final_ec_value']
    form.preparer_name = data['preparer_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '養液配製紀錄更新成功'})

# 刪除養液配製紀錄
@app.route('/api/form04/<int:id>', methods=['DELETE'])
def delete_form04(id):
    record = Form04.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的養液配製紀錄
@app.route('/api/form04', methods=['GET'])
def get_all_form04(): 
    results = db.session.query(Form04, users.farmer_name).\
        join(users, users.id == Form04.user_id).all()
    
    forms = [
        {
            "id": result.Form04.id,
            "user_id": result.Form04.user_id,
            "farmer_name": result.farmer_name,
            "preparation_date": result.Form04.preparation_date.strftime('%Y-%m-%d'),
            "material_code_or_name": result.Form04.material_code_or_name,
            "usage_amount": str(result.Form04.usage_amount),
            "preparation_process": result.Form04.preparation_process,
            "final_ph_value": str(result.Form04.final_ph_value),
            "final_ec_value": str(result.Form04.final_ec_value),
            "preparer_name": result.Form04.preparer_name,
            "notes": result.Form04.notes
        }
        for result in results
    ]

    return jsonify(forms)

# ----------------------------------------------------------------------------------------------

# 養液配製資材與代碼對照

# 新增養液配製資材與代碼對照
@app.route('/api/form05', methods=['POST'])
def add_form05():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    nutrient_material_code = data.get('nutrient_material_code')
    nutrient_material_name = data.get('nutrient_material_name')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not nutrient_material_code:
        return jsonify({'error': '缺少 nutrient_material_code'}), 400
    if not nutrient_material_name:
        return jsonify({'error': '缺少 nutrient_material_name'}), 400
    
    try:
        new_form = Form05(
            user_id=user_id,
            nutrient_material_code=nutrient_material_code,
            nutrient_material_name=nutrient_material_name,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '養液配製資材與代碼對照新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form05: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新養液配製資材與代碼對照
@app.route('/api/form05/<int:id>', methods=['PUT'])
def update_form05(id):
    data = request.get_json()
    form = Form05.query.get(id)
    if not form:
        return jsonify({'error': '養液配製資材與代碼對照未找到'}), 404
    
    form.nutrient_material_code = data['nutrient_material_code']
    form.nutrient_material_name = data['nutrient_material_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '養液配製資材與代碼對照更新成功'})

# 刪除養液配製資材與代碼對照
@app.route('/api/form05/<int:id>', methods=['DELETE'])
def delete_form05(id):
    record = Form05.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的養液配製資材與代碼對照
@app.route('/api/form05', methods=['GET'])
def get_all_form05(): 
    results = db.session.query(Form05, users.farmer_name).\
        join(users, users.id == Form05.user_id).all()
    
    forms = [
        {
            "id": result.Form05.id,
            "user_id": result.Form05.user_id,
            "farmer_name": result.farmer_name,
            "nutrient_material_code": result.Form05.nutrient_material_code,
            "nutrient_material_name": result.Form05.nutrient_material_name,
            "notes": result.Form05.notes
        }
        for result in results
    ]

    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# 肥料施用紀錄

# 新增肥料施用紀錄
@app.route('/api/form06', methods=['POST'])
def add_form06():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d')
    field_code = data.get('field_code')
    crop = data.get('crop')
    fertilizer_type = data.get('fertilizer_type')
    material_code_or_name = data.get('material_code_or_name')
    fertilizer_amount = data.get('fertilizer_amount')
    dilution_factor = data.get('dilution_factor')
    operator = data.get('operator')
    process = data.get('process')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not date_used:
        return jsonify({'error': '缺少 date_used'}), 400
    if not field_code:
        return jsonify({'error': '缺少 field_code'}), 400
    if not crop:
        return jsonify({'error': '缺少 crop'}), 400
    if not fertilizer_type:
        return jsonify({'error': '缺少 fertilizer_type'}), 400
    if not material_code_or_name:
        return jsonify({'error': '缺少 material_code_or_name'}), 400
    if not fertilizer_amount:
        return jsonify({'error': '缺少 fertilizer_amount'}), 400
    if not dilution_factor:
        return jsonify({'error': '缺少 dilution_factor'}), 400
    if not operator:
        return jsonify({'error': '缺少 operator'}), 400
    if not process:
        return jsonify({'error': '缺少 process'}), 400

    try:
        new_form = Form06(
            user_id=user_id,
            date_used=date_used,
            field_code=field_code,
            crop=crop,
            fertilizer_type=fertilizer_type,
            material_code_or_name=material_code_or_name,
            fertilizer_amount=fertilizer_amount,
            dilution_factor=dilution_factor,
            operator=operator,
            process=process,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '肥料施用紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form06: {str(e)}")
        return jsonify({'error': str(e)}), 500

# 更新肥料施用紀錄
@app.route('/api/form06/<int:id>', methods=['PUT'])
def update_form06(id):
    data = request.get_json()
    form = Form06.query.get(id)
    if not form:
        return jsonify({'error': '肥料施用紀錄未找到'}), 404
    
    form.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d')
    form.field_code = data['field_code']
    form.crop = data['crop']
    form.fertilizer_type = data['fertilizer_type']
    form.material_code_or_name = data['material_code_or_name']
    form.fertilizer_amount = data['fertilizer_amount']
    form.dilution_factor = data['dilution_factor']
    form.operator = data['operator']
    form.process = data['process']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '肥料施用紀錄更新成功'}),200

# 刪除肥料施用紀錄
@app.route('/api/form06/<int:id>', methods=['DELETE'])
def delete_form06(id):
    record = Form06.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的肥料施用紀錄
@app.route('/api/form06', methods=['GET'])
def get_all_form06():
    results = db.session.query(Form06, users.farmer_name).\
        join(users, users.id == Form06.user_id).all()
    
    forms = [
        {
            "id": result.Form06.id,
            "user_id": result.Form06.user_id,
            "farmer_name": result.farmer_name,
            "date_used": result.Form06.date_used.strftime('%Y-%m-%d'),
            "field_code": result.Form06.field_code,
            "crop": result.Form06.crop,
            "fertilizer_type": result.Form06.fertilizer_type,
            "material_code_or_name": result.Form06.material_code_or_name,
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

# form07（肥料資材與代碼對照表）

# 新增肥料資材與代碼對照表
@app.route('/api/form07', methods=['POST'])
def add_form07():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    fertilizer_material_code = data.get('fertilizer_material_code')
    fertilizer_material_name = data.get('fertilizer_material_name')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not fertilizer_material_code:
        return jsonify({'error': '缺少 fertilizer_material_code'}), 400
    if not fertilizer_material_name:
        return jsonify({'error': '缺少 fertilizer_material_name'}), 400
    
    try:
        new_form = Form07(
            user_id=user_id,
            fertilizer_material_code=fertilizer_material_code,
            fertilizer_material_name=fertilizer_material_name,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '肥料資材與代碼對照表新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form07: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新肥料資材與代碼對照表
@app.route('/api/form07/<int:id>', methods=['PUT'])
def update_form07(id):
    data = request.get_json()
    form = Form07.query.get(id)
    if not form:
        return jsonify({'error': '肥料資材與代碼對照表未找到'}), 404
    
    form.fertilizer_material_code = data['fertilizer_material_code']
    form.fertilizer_material_name = data['fertilizer_material_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '肥料資材與代碼對照表更新成功'})

# 刪除肥料資材與代碼對照表
@app.route('/api/form07/<int:id>', methods=['DELETE'])
def delete_form07(id):
    record = Form07.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的肥料資材與代碼對照表
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
# form08（肥料入出庫紀錄）

# 新增肥料入出庫紀錄
@app.route('/api/form08', methods=['POST'])
def add_form08():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    material_name = data.get('material_name')
    manufacturer = data.get('manufacturer')
    supplier = data.get('supplier')
    packaging_unit = data.get('packaging_unit')
    packaging_volume = data.get('packaging_volume')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d')
    purchase_quantity = data.get('purchase_quantity')
    usage_quantity = data.get('usage_quantity')
    remaining_quantity = data.get('remaining_quantity')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not material_name:
        return jsonify({'error': '缺少 material_name'}), 400
    if not manufacturer:
        return jsonify({'error': '缺少 manufacturer'}), 400
    if not supplier:
        return jsonify({'error': '缺少 supplier'}), 400
    if not packaging_unit:
        return jsonify({'error': '缺少 packaging_unit'}), 400
    if not packaging_volume:
        return jsonify({'error': '缺少 packaging_volume'}), 400
    if not date:
        return jsonify({'error': '缺少 date'}), 400
    if not purchase_quantity:
        return jsonify({'error': '缺少 purchase_quantity'}), 400
    if not usage_quantity:
        return jsonify({'error': '缺少 usage_quantity'}), 400
    if not remaining_quantity:
        return jsonify({'error': '缺少 remaining_quantity'}), 400
    

    try:
        new_form = Form08(
            user_id=user_id,
            material_name=material_name,
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
        return jsonify({'status': '肥料入出庫紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form08: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新肥料入出庫紀錄
@app.route('/api/form08/<int:id>', methods=['PUT'])
def update_form08(id):
    data = request.get_json()
    form = Form08.query.get(id)
    if not form:
        return jsonify({'error': '肥料入出庫紀錄未找到'}), 404
    
    form.material_name = data['material_name']
    form.manufacturer = data['manufacturer']
    form.supplier = data['supplier']
    form.packaging_unit = data['packaging_unit']
    form.packaging_volume = data['packaging_volume']
    form.date = datetime.strptime(data['date'], '%Y-%m-%d')
    form.purchase_quantity = data['purchase_quantity']
    form.usage_quantity = data['usage_quantity']
    form.remaining_quantity = data['remaining_quantity']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '肥料入出庫紀錄更新成功'})

# 刪除肥料入出庫紀錄
@app.route('/api/form08/<int:id>', methods=['DELETE'])
def delete_form08(id):
    record = Form08.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的肥料入出庫紀錄
@app.route('/api/form08', methods=['GET'])
def get_all_form08(): 
    results = db.session.query(Form08, users.farmer_name).\
        join(users, users.id == Form08.user_id).all()
    
    forms = [
        {
            "id": result.Form08.id,
            "user_id": result.Form08.user_id,
            "farmer_name": result.farmer_name,
            "material_name": result.Form08.material_name,
            "manufacturer": result.Form08.manufacturer,
            "supplier": result.Form08.supplier,
            "packaging_unit": result.Form08.packaging_unit,
            "packaging_volume": result.Form08.packaging_volume,
            "date": result.Form08.date.strftime('%Y-%m-%d'),
            "purchase_quantity": str(result.Form08.purchase_quantity),
            "usage_quantity": str(result.Form08.usage_quantity),
            "remaining_quantity": str(result.Form08.remaining_quantity),
            "notes": result.Form08.notes
        }
        for result in results
    ]

    return jsonify(forms)

# ----------------------------------------------------------------------------------------------
# form09（有害生物防治或環境消毒資材施用紀錄）

# 新增有害生物防治或環境消毒資材施用紀錄
@app.route('/api/form09', methods=['POST'])
def add_form09():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    date_used =  datetime.strptime(data.get('date_used'), '%Y-%m-%d')
    field_code = data.get('field_code')
    crop = data.get('crop')
    pest_target = data.get('pest_target')
    material_code_or_name = data.get('material_code_or_name')
    water_volume = data.get('water_volume')
    chemical_usage = data.get('chemical_usage')
    dilution_factor = data.get('dilution_factor')
    safety_harvest_period = data.get('safety_harvest_period')
    operator_method = data.get('operator_method')
    operator = data.get('operator')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not date_used:
        return jsonify({'error': '缺少 date_used'}), 400
    if not field_code:  
        return jsonify({'error': '缺少 field_code'}), 400
    if not crop:
        return jsonify({'error': '缺少 crop'}), 400
    if not pest_target:
        return jsonify({'error': '缺少 pest_target'}), 400
    if not material_code_or_name:
        return jsonify({'error': '缺少 material_code_or_name'}), 400
    if not water_volume:
        return jsonify({'error': '缺少 water_volume'}), 400
    if not chemical_usage:
        return jsonify({'error': '缺少 chemical_usage'}), 400
    if not dilution_factor:
        return jsonify({'error': '缺少 dilution_factor'}), 400
    if not safety_harvest_period:
        return jsonify({'error': '缺少 safety_harvest_period'}), 400
    if not operator_method:
        return jsonify({'error': '缺少 operator_method'}), 400
    if not operator:
        return jsonify({'error': '缺少 operator'}), 400
    
    try:
        new_form = Form09(
            user_id=user_id,
            date_used=date_used,
            field_code=field_code,
            crop=crop,
            pest_target=pest_target,
            material_code_or_name=material_code_or_name,
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
        return jsonify({'status': '有害生物防治或環境消毒資材施用紀錄新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form09: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新有害生物防治或環境消毒資材施用紀錄
@app.route('/api/form09/<int:id>', methods=['PUT'])
def update_form09(id):
    data = request.get_json()
    form = Form09.query.get(id)
    if not form:
        return jsonify({'error': '有害生物防治或環境消毒資材施用紀錄未找到'}), 404
    
    form.date_used = datetime.strptime(data['date_used'], '%Y-%m-%d')
    form.field_code = data['field_code']
    form.crop = data['crop']
    form.pest_target = data['pest_target']
    form.material_code_or_name = data['material_code_or_name']
    form.water_volume = data['water_volume']
    form.chemical_usage = data['chemical_usage']
    form.dilution_factor = data['dilution_factor']
    form.safety_harvest_period = data['safety_harvest_period']
    form.operator_method = data['operator_method']
    form.operator = data['operator']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '有害生物防治或環境消毒資材施用紀錄更新成功'})

# 刪除有害生物防治或環境消毒資材施用紀錄
@app.route('/api/form09/<int:id>', methods=['DELETE'])
def delete_form09(id):
    record = Form09.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的有害生物防治或環境消毒資材施用紀錄
@app.route('/api/form09', methods=['GET'])
def get_all_form09():
    results = db.session.query(Form09, users.farmer_name).\
        join(users, users.id == Form09.user_id).all()
    
    forms = [
        {
            "id": result.Form09.id,
            "user_id": result.Form09.user_id,
            "farmer_name": result.farmer_name,
            "date_used": result.Form09.date_used.strftime('%Y-%m-%d'),
            "field_code": result.Form09.field_code,
            "crop": result.Form09.crop,
            "pest_target": result.Form09.pest_target,
            "material_code_or_name": result.Form09.material_code_or_name,
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
# form10（防治資材與代碼對照表）

# 新增防治資材與代碼對照表
@app.route('/api/form10', methods=['POST'])
def add_form10():
    data = request.get_json()
    if not data:
        return jsonify({'error': '請提供 JSON 數據'}), 400
    
    user_id = data.get('user_id')
    pest_control_material_code = data.get('pest_control_material_code')
    pest_control_material_name = data.get('pest_control_material_name')
    notes = data.get('notes')

    # 檢查必要欄位是否存在
    if not user_id:
        return jsonify({'error': '缺少 user_id'}), 400
    if not pest_control_material_code:
        return jsonify({'error': '缺少 pest_control_material_code'}), 400
    if not pest_control_material_name:
        return jsonify({'error': '缺少 pest_control_material_name'}), 400  
    
    try:
        new_form = Form10(
            user_id=user_id,
            pest_control_material_code=pest_control_material_code,
            pest_control_material_name=pest_control_material_name,
            notes=notes
        )

        db.session.add(new_form)
        db.session.commit()
        return jsonify({'status': '防治資材與代碼對照表新增成功', 'form_id': new_form.id}), 201
    except Exception as e:
        print(f"Error occurred while adding form10: {str(e)}")
        return jsonify({'error': str(e)}), 500
    
# 更新防治資材與代碼對照表
@app.route('/api/form10/<int:id>', methods=['PUT'])
def update_form10(id):
    data = request.get_json()
    form = Form10.query.get(id)
    if not form:
        return jsonify({'error': '防治資材與代碼對照表未找到'}), 404
    
    form.pest_control_material_code = data['pest_control_material_code']
    form.pest_control_material_name = data['pest_control_material_name']
    form.notes = data.get('notes')
    db.session.commit()
    return jsonify({'message': '防治資材與代碼對照表更新成功'})

# 刪除防治資材與代碼對照表
@app.route('/api/form10/<int:id>', methods=['DELETE'])
def delete_form10(id):
    record = Form10.query.get(id)
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    
    db.session.delete(record)
    db.session.commit()
    return jsonify({'message': 'Record deleted successfully'})

# 查詢所有使用者的防治資材與代碼對照表
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










































# ----------------------------------------------------------------------------------------------






































































































































# 在應用程式啟動時測試資料庫連線
if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)

# users
