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
db = SQLAlchemy(app)
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

# 建立資料
with app.app_context():
    db.create_all()


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

# 修改users
@app.route('/api/users/<int:id>', methods=['PUT'])
def update_users(id):
    try:
        data = request.get_json()  # 獲取 JSON 數據
        user = users.query.get(id)  # 查詢指定的使用者

        user_id = data.get('user_id')
        if not user_id:
            return jsonify({'error': '缺少 user_id'}), 400

        existing_user = users.query.get(user_id)
        if not existing_user:
            return jsonify({'error': '找不到對應的使用者'}), 404

        if 'password' in data:
            if data['password']:
                user.password = generate_password_hash(data['password'])


        if not user:
            return jsonify({'error': '使用者未找到'}), 404

        # 更新欄位
        if 'unit_name' in data:
            user.unit_name = data['unit_name']
        if 'farmer_name' in data:
            user.farmer_name = data['farmer_name']
        if 'phone' in data:
            user.phone = data['phone']
        if 'fax' in data:
            user.fax = data['fax']
        if 'mobile' in data:
            user.mobile = data['mobile']
        if 'address' in data:
            user.address = data['address']
        if 'email' in data:
            user.email = data['email']
        if 'total_area' in data:
            user.total_area = data['total_area']
        if 'notes' in data:
            user.notes = data['notes']
        if 'land_parcel_id' in data:
            user.land_parcel_id = data['land_parcel_id']

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
            'unitName': user.unit_name  # ✅ 添加 unitName
        })
        return jsonify(token=access_token), 200
    
    return jsonify(error='帳號或密碼錯誤'), 401

# ----------------------------------------------------------------------------------------
# 農地資訊

# 添加農地資訊 API
@app.route('/api/land_parcels', methods=['POST'])
def add_land_parcel():
    print("Received POST request")  # 添加调试信息
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

    return jsonify({'status': '農地資訊添加成功', 'land_parcel_id': new_land_parcel.id}), 201

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
    print(f"Attempting to delete ID: {id}")  # 添加调试信息
    land_parcel = LandParcel.query.get(id)
    if not land_parcel:
        print(f"ID {id} not found")  # 添加调试信息
        return jsonify({'error': '農地資訊未找到'}), 404

    db.session.delete(land_parcel)
    db.session.commit()
    return jsonify({'status': '農地資訊已删除'}), 200


# 查询所有農地資訊 API
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

# 農地資訊
# ----------------------------------------------------------------------------------------




































































# 添加生產計畫
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
        return jsonify({'error': '缺少 area_code'}), 400
    if not area_size:
        return jsonify({'error': '缺少 area_size'}), 400
    if not month:
        return jsonify({'error': '缺少 month'}), 400
    if not crop_info:
        return jsonify({'error': '缺少 crop_info'}), 400

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
        return jsonify({'status': '生產計畫添加成功', 'form_id': new_form.id}), 201
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

# 查詢某農戶的生產計畫
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

# 查询所有生產計畫 API
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


# 生產計畫


























# 在應用程式啟動時測試資料庫連線
if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)

# users
