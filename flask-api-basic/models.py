from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Fcuser(db.Model):
    __tablename__ = 'fcuser'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(64))
    userid = db.Column(db.String(32))
    username = db.Column(db.String(8))

    @property   # 함수를 접근할 때 변수처럼 사용 가능해짐
    def serialize(self):    # 모델에 대하여 직렬화 해주는 함수를 생성
        return {
            'id': self.id,
            'userid': self.userid,
            'password': self.password,
            'username': self.username
        }