# /models.py
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Post(db.Model):
    # 데이터베이스 테이블설정(테이블명, 컬럼)
    __tablename__ = 'posts' # class이름의 복수형
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)
    
    # 객체 생성자
    # https://wikidocs.net/1742
    def __init__(self, title, content):
        self.title = title
        self.content = content
        self.created_at = datetime.datetime.now()