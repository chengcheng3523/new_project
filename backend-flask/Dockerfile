# 使用官方 Python 映像檔
FROM python:3.10

# 設定工作目錄
WORKDIR /app

# 複製需求檔案
COPY requirements.txt .

# 安裝 Python 套件
RUN pip install --no-cache-dir -r requirements.txt

# 複製專案所有檔案到容器
COPY . .

# 設定 Flask 執行環境變數（可選）
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# 對外開放 5000 port
EXPOSE 5000

# 啟動 Flask
CMD ["flask", "run"]
