# day3

### check point

- pyenv 환경설정하기 
  - 환경 변수들 bash_profile에서 bashrc로
  - `pyenv local <가상환경이름>`으로 설정하기
- 마크다운 문법 설명
- xd 사용
- 모델 사용전 codecademy sql 해야하나?



### MODEL

- 설정

```bash
# apt-get update
$ sudo apt-get update

# ubuntu에 postgresql 설치하기
$ sudo apt-get install postgresql postgresql-contrib libpq-dev

# python(flask)에서 사용할 수 있도록 도와주는 애들
$ pip install psycopg2 psycopg2-binary 

# flask에서 import 해서 쓸 것들
$ pip install Flask-SQLAlchemy Flask-Migrate
```

- DB 설정
  - postgresql명령어 : http://www.gurubee.net/postgresql/basic
  - postgresql 실행 : `psql`
> 만약에 psql 설치 후에 c에서 could not connect to server: Connection refused 에러가 뜬다면
>
> sudo /etc/init.d/postgresql restart

```bash
$ psql
ubuntu# CREATE DATABASE <databasename> WITH template=template0 encoding='UTF8';
ubuntu# \q
```

- `model.py`

```python
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
```

- `app.py`

```python
# /app.py
from flask import Flask
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
    return "hello world"
```

- 마이그레이션
  1. flask db initialize : `flask db init`
     1. `migrations`폴더생성
  2. models.py 파일의 현재 상태를 반영 : `flask db migrate`
     1. `migrations`폴더에 파일 생성
  3. DB에 반영 : `flask db upgrade`
  4. 실제로 DB에서 확인하기
     1. `psql <이름>`
     2. `ubuntu# \d posts`



### CRUD - index

- `app.py`

```python
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
```

- `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>index!!!</h1>
</body>
</html>
```

- `flask run --host $IP --port $PORT`

### CRUE - C

> route는 RESTful

- `app.py`

```python
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
    return render_template("create.html", post=post)
```

- `index.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>index!!!</h1>
    <h2><a href="/new">글작성하기</a></h2>
</body>
</html>
```

- `new.html`

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>
    <h1>새글쓰기</h1>
    <form action="/create">
        <input type="text" name="title">
        <textarea name="content"></textarea>
        <input type="submit" value="글쓰기!">
    </form>
</body>
</html>
```

- `create.html`

```html
{{post.id}}
{{post.title}}
{{post.content}}
{{post.created_at}}
```

- 실제 DB에 들어갔는지 확인해봅시다.
  - `psql myboard`
  - `SELECT * FROM posts;` 명령어로 실제 데이터 확인



### CRUD - index에서 모두보기

- `app.py`

```python
@app.route('/')
def index():
    posts = Post.query.order_by(Post.id.desc()).all()
    # SELECT * FROM posts;
    # SELECT * FROM posts ORDER BY id DESC;
    return render_template("index.html",posts=posts)
```

- `index.html`

```html
<body>
    <h1>index!!!</h1>
    {% for post in posts %}
      <p>{{post.id}}</p>
      <p>{{post.title}}</p>
      <p>{{post.content}}</p>
      <p>{{post.created_at.strftime("%Y년 %m월 %d일 %H:%M")}}</p>
    {% endfor %}
    <a href="/new">글쓰러 가기!!</a>
</body>
```

- create post방식으로 하기
    - https://github.com/5chang2/flask_crud