# app.py

import os
from flask import Flask
from flask import request   # 요청 정보 확인
from flask import redirect
from flask import render_template
from flask import session
from models import db, Fcuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()   # flask-WTF로 작성한 forms를 가져오기
    if form.validate_on_submit():   # 입력받은 값의 유효성 검사(입력, 삭제 등은 무조건 POST요청임)
        # request가 아닌 form으로 입력값에 접근 가능해짐
        fcuser = Fcuser()   # DB의 user테이블을 불러오기, 클래스 변수 생성
        fcuser.userid = form.data.get('userid')   # form으로 입력된 값 가져오기
        fcuser.username = form.data.get('username')
        fcuser.password = form.data.get('password')

        db.session.add(fcuser)  # DB에 값을 추가하기
        db.session.commit()     # 커밋하기

        return redirect('/')    # 입력이 완료되서 이동할 곳


    #### form.validate_on_submit()을 사용하여 아래 내용이 필요 없어짐(주석 처리)
    # if request.method == 'POST':    # POST요청이 왔다면
    #     userid = request.form.get('userid')   # 입력받은 값 가져오기
    #     username = request.form.get('username')
    #     password = request.form.get('password')
    #     re_password = request.form.get('re-password')

    #     # 모든 입력값이 있는지, 비밀번호와 비밀번호 확인이 같은지 체크
    #     if (userid and username and password and re_password) and password == re_password:
    #         fcuser = Fcuser()   # DB의 user테이블을 불러오기, 클래스 변수 생성
    #         fcuser.userid = userid  # 클래스 변수에 입력값 할당하기
    #         fcuser.username = username
    #         fcuser.password = password

    #         db.session.add(fcuser)  # DB에 값을 추가하기
    #         db.session.commit()     # 커밋하기

    #         return redirect('/')    # 입력이 완료되서 이동할 곳

    return render_template('register.html', form=form)  # GET요청이 왔다면, 화면을 출력, 해당 HTML로 form 전달

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')     # 세션에 userid를 추가, 저장하기
        return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET'])
def logout():
        session.pop('userid', None)     # 세션에 저장된 userid를 삭제
        return redirect('/')

# html을 컨트롤러에서 만들어서 View로 전달하는데 컨트롤러와 View를 분리
@app.route('/')     # 해당 Controller로 보내기, 기본적으로 GET요청만 허용
def hello():
    userid = session.get('userid', None)    # 세션에서 userid를 가져오기, userid가 없으면 None
    return render_template('hello.html', userid=userid)    # View 부분으로, 화면 보여줄 파일 전달


basedir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basedir, 'db.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile   # sqlite DB URI(DB 접속 설정)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True      # TEARDOWN : 사용자 요청의 끝
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 수정사항에 대한 track을 하지 않음
app.config['SECRET_KEY'] = 'asdf'   # CSRF의 암호키 설정(임의의 문자열)

csrf = CSRFProtect()
csrf.init_app(app)

db.init_app(app)    # app의 config를 초기화
db.app = app     # db안에 app이란 변수에 app을 넣어주기
db.create_all()     # DB 생성하기


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
