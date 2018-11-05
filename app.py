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
    posts = Post.query.order_by(Post.id.desc()).all()
    # SELECT * FROM posts;
    # SELECT * FROM posts ORDER BY id DESC;
    return render_template("index.html",posts=posts)

@app.route('/new')
def new():
    return render_template('new.html')
    
@app.route('/create')
def create():
    title = request.args.get('title')
    content = request.args.get('content')
    # 여기서 Post는 models.py에 들어있는 클래스 이름
    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()
    # INSERT INTO posts (title, content)
    # VALUES ('1번글', '1번내용');
    return redirect('/')
    
# app.rb
@app.route("/posts/<int:id>")
def read(id):
    post = Post.query.get(id)
    # SELECT * FROM posts WHERE id=1;
    return render_template("read.html", post=post)
    
@app.route("/posts/<int:id>/delete")
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    # DELETE FROM posts WHERE id=2;
    return redirect('/')