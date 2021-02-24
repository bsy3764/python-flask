from flask import jsonify  # json 형태로 반환할 수 있도록 도와줌
from flask import request
from flask_jwt import jwt_required
from models import Fcuser, db
from . import api  # api는 리소스 또는 데이터 중심

# api는 api_v1/__init__.py 에서 가져옴
@api.route('/users', methods=['GET', 'POST'])
@jwt_required()
def users():
    if request.method == 'POST':  # POST로 요청이 왔을 때
        data = request.get_json()
        userid = data.get('userid')
        username = data.get('username')
        password = data.get('password')
        re_password = data.get('re-password')

        # 입력값이 모두 채워졌는지 체크(입력값중에 하나라도 안 채워져 있다면)
        if not (userid and username and password and re_password):
            return jsonify({'error': 'No arguments'}), 400  # api를 사용하여 json 데이터 형식을 전달

        # 비밀번호와 비밀번호 확인이 다를 경우
        if password != re_password:
            return jsonify({'error': 'Miss Match Password'}), 400

        fcuser = Fcuser()  # DB의 user테이블을 불러오기, 클래스 변수 생성
        fcuser.userid = userid  # 클래스 변수에 입력값 할당하기
        fcuser.username = username
        fcuser.password = password

        db.session.add(fcuser)
        db.session.commit()

        return jsonify(), 201

    users = Fcuser.query.all()  # 해당 모델의 모든 데이터를 가져옴

    # api 의 결과를 list로 전달하기
    # res_users = []
    # for user in users:
    #     res_users.append(user.serialize)

    # 진행형 list를 만들어서 전달하기 
    return jsonify([user.serialize for user in users]), 404  # 데이터 반환(json 형태), 상태코드 작성


@api.route('/users/<uid>', methods=['GET', 'PUT', 'DELETE'])
def user_detail(uid):  # 위의 route의 uid가 매개변수로 들어옴
    if request.method == 'GET':  # 조회
        user = Fcuser.query.filter(Fcuser.id == uid).first()
        return jsonify(user.serialize)

    elif request.method == 'DELETE':  # 삭제
        Fcuser.query.delete(Fcuser.id == uid)
        return jsonify(), 204  # no content 코드

    else:  # 수정,PUT method
        data = request.get_json()

        # userid = data.get('userid') # 입력 받기
        # username = data.get('username')
        # password = data.get('password')

        # updated_data = {}
        # if userid:
        #     updated_data['userid'] = userid
        # if password:
        #     updated_data['password'] = password
        # if username:
        #     updated_data['username'] = username
    # Fcuser.query.filter(Fcuser.id == uid).update(updated_data)

    Fcuser.query.filter(Fcuser.id == uid).update(data)
    user = Fcuser.query.filter(Fcuser.id == uid).first()
    return jsonify(user.serialize)