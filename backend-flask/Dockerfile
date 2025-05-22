# 使用較輕量但帶有 python 3.12 的官方映像
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 安装编译依赖和 MySQL 开发库
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴清單
COPY requirements.txt ./

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製整個專案
COPY . .

# 避免 Python 緩存與輸出延遲
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 開放 5000 埠口給外部連接 (Flask 預設)
EXPOSE 5000

# 啟動 Flask 應用（假設你有定義 app = Flask(__name__)）
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]

# podman build -t backend:V1.0.1 .
# podman run -p 5000:5000 -d  backend:V1.0.1