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


# 新增users
@app.route('/api/users/post', methods=['POST'])
def create_users():
    try:
        data = request.get_json()  # 獲取 JSON 數據
        print("Received Data:", data)  # Debug 輸出    
        if not data:
            return jsonify({'error': '請求的 JSON 格式錯誤或 Content-Type 錯誤'}), 400
        
        password = data.get('password')
        if not password:
            return jsonify({'error': '密碼不能為空'}), 400

        password_hash = generate_password_hash(password)  # 加密密碼

        new_users = users(
            username=data.get('username'),
            password=password_hash,  # 使用加密後的密碼
            plain_password=data.get('plain_password'),
            unit_name=data.get('unit_name'),
            land_parcel_id=data.get('land_parcel_id'),
            farmer_name=data.get('farmer_name'),
            phone=data.get('phone'),
            fax=data.get('fax'),
            mobile=data.get('mobile'),
            address=data.get('address'),
            email=data.get('email'),
            total_area=data.get('total_area'),
            notes=data.get('notes')
        )

        db.session.add(new_users)  # 新增使用者資料
        db.session.commit()        # 提交變更
        return jsonify({'status': '使用者創建成功'}), 201  # 回應成功訊息
    except Exception as e:
        print(f"Error occurred: {str(e)}")  # 输出错误信息
        return jsonify({'error': str(e)}), 500  # 返回錯誤訊息

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

# 在應用程式啟動時測試資料庫連線
if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)

# users
