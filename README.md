# Django  learning_log project 部署到 Render
Learning Topic Web
一.準備必要的 Python 套件
pip install gunicorn dj-database-url whitenoise
pip freeze > requirements.txt

二.開啟專案的 settings.py 並調整以下項目：
import os
import dj_database_url

# 允許 Render 產生的網域訪問
ALLOWED_HOSTS = ['.onrender.com', 'localhost', '127.0.0.1']

# 靜態檔案設定 (使用 WhiteNoise)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 必須放在 SecurityMiddleware 下方
    # ... 其他 middleware
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 資料庫設定 (環境變數自動載入 Render PostgreSQL)
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

三.建立部署腳本 build.sh (在專案根目錄新增 build.sh 檔案：) [記得透過 chmod +x build.sh 授予執行權限]
#!/usr/bin/env bash
# 發生錯誤時立即停止
set -o errexit

pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate

四.在 Render 建立 PostgreSQL 資料庫：建立雲端資料庫服務
登入 Render Dashboard，點擊 New + 並選擇 PostgreSQL。
設定 Name，選擇免費方案（Free），然後點擊 Create Database。
建立完成後，複製 Internal Database URL 備用。

五.在 Render 部署 Web Service
點擊 New + 選擇 Web Service，並連結含有 Django 專案的 Repository。
填寫以下基本資訊：
Environment: Python 3
Build Command: pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python manage.py createsuperuser --no-input || true

Start Command: gunicorn <專案名稱>.wsgi (請將 <專案名稱> 替換為包含 wsgi.py 的資料夾名)
在 Environment Variables 區塊新增設定：
DATABASE_URL: 貼上步驟 4 複製的 Internal Database URL
SECRET_KEY: 設定你的 Django 密鑰
PYTHON_VERSION: 例如 3.10.0
點擊 Create Web Service 開始部署。
