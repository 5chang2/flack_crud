# /app.py
from flask import Flask, render_template, request, redirect
# flask ORM
from flask_sqlalchemy import SQLAlchemy
# 마이그레이션 관리
from flask_migrate import Migrate

# 모델 설정파일 import
from models import *

app = Flask(__name__)
# DB 설정과 관련된 코드
# 'postgresql:///<pqsl에서 만든 DATABASE이름>'
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///myboard'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return render_template('index.html')
    
