# app.py
import os
from flask import Flask
from flask import render_template
from flask_jwt import JWT
from api_v1 import api as api_v1
from models import db, Fcuser

app = Flask(__name__)

# controller 코드들이 app.py에 모여있지 않고, 분리하여 작성할 수 있게 해줌 
# api_v1에서 제공하고 있는 controller 코드들을 url_prefix 뒤에 @api.route 주소를 입력하여 제공함
app.register_blueprint(api_v1, url_prefix='/api/v1')

@app.route('/register')
def register():
    return render_template('register.html')  # GET요청이 왔다면, 화면을 출력, 해당 HTML로 form 전달

@app.route('/login')
def login():
    return render_template('login.html')
# 토큰 방식의 인증
# JWT : Json Web Token
# $ pip install Flask-JWT


# html을 컨트롤러에서 만들어서 View로 전달하는데 컨트롤러와 View를 분리
@app.route('/')     # 해당 Controller로 보내기, 기본적으로 GET요청만 허용
def hello():
    return render_template('home.html')

basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

# sqlalchemy에 필요한 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile   # sqlite DB URI(DB 접속 설정)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True      # TEARDOWN : 사용자 요청의 끝, Auto Commmit
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 수정사항에 대한 track을 하지 않음
app.config['SECRET_KEY'] = 'asdf'   # CSRF의 암호키 설정(임의의 문자열)

db.init_app(app)    # app의 config를 초기화
db.app = app     # db안에 app이란 변수에 app을 넣어주기
db.create_all()     # DB 생성하기

# 인증 함수
def authenticate(username, password):
    user = Fcuser.query.filter(Fcuser.userid == username).first()
    if user.password == password:
        return user

def identify(payload):
    userid = payload['identity']
    return Fcuser.query.filter(Fcuser.id == userid).first()

# JWT 인증
jwt = JWT(app, authenticate, identify)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
