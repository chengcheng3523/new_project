``` 
cd backend-flask
flask run
``` 

-p 5000：5000 
第一個5000是你瀏覽器訪問的port
第二個5000是你程式本身的port
第二個一定要跟你程式一樣
第一個不一定要5000 隨便你用 只要別跟別的port衝突到就好

podman build -t backend:V1.0.1 .
podman run -p 5000:5000 -d  backend:V1.

1. 生成 requirements.txt
如果你已经安装了相关库，可以使用以下命令生成：
pip freeze > requirements.txt
这样会自动保存当前 Python 环境中安装的所有依赖。

2. 参考 requirements.txt 内容

3. 依赖说明
依赖库	说明
Flask	Flask 核心框架
Flask-SQLAlchemy	ORM 组件，管理 MySQL 数据库
Flask-Migrate	迁移工具，管理数据库表结构变更
Flask-Cors	允许前端跨域请求
Flask-JWT-Extended	处理用户认证（JWT 方式）
Flask-RESTful	设计 REST API
Flask-Marshmallow	处理数据验证和序列化
marshmallow	数据模式校验
mysql-connector-python	MySQL 连接库
flask-mysqldb	MySQL 适配库
Werkzeug	处理密码哈希等安全操作
python-dotenv	读取 .env 文件中的环境变量
gunicorn	生产环境部署 WSGI 服务器

4. 安装依赖
你可以在新的 Python 环境中运行：
pip install -r requirements.txt
这样 Flask 及所有相关库都会被正确安装。

``` 
pip install -r requirements.txt  # 如果有 requirements.txt 檔案
``` 
