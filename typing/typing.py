import random
import time
import winsound # 소리 출력에 필요한 모듈
import sqlite3
import datetime

# DB 생성 및 Auto Commit
conn = sqlite3.connect('./Python-flask/typing/records.db', isolation_level=None)

# Cursor 연결
cursor = conn.cursor()

cursor.execute("create table if not exists records(\
    id integer primary key autoincrement,\
    cor_cnt integer, record text, regdate text)")

words = []   # 영어 단어 리스트

n = 1   # 게임 시도 횟수
cor_cnt = 0     # 정답 개수

with open('./Python-flask/typing/word.txt') as f:
    for c in f:
        words.append(c.strip()) # strip으로 양쪽 공백 제거

# print(words)

input('Press Enter Key')

start = time.time()   # 게임 시작 시간

while n <= 5:
    random.shuffle(words)   # 리스트으 순서를 섞음
    q = random.choice(words)    # 1개를 임의 선택
    
    print("\n")     # 줄 바꿈

    print("Question# {}".format(n))
    print("Q >", q)    # 문제 출력
    x = input("A > ")  # 입력 받기

    # 입력값과 문제가 같은지 체크
    if str(q).strip() == str(x).strip():   # 정답이라면
        print("Pass")
        # winsound.PlaySound('사운드 파일 경로', winsound.SND_FILENAME)   # SND_FILENAME : 사운드 파일명을 직접 씀
        winsound.PlaySound('./Python-flask/typing/sound/good.wav', winsound.SND_FILENAME)   # SND_FILENAME : 사운드 파일명을 직접 씀
        cor_cnt += 1
    else:   # 틀렸다면
        print("Wrong")
        winsound.PlaySound('./Python-flask/typing/sound/bad.wav', winsound.SND_FILENAME)   # SND_FILENAME : 사운드 파일명을 직접 씀

    n += 1

end = time.time()   # 게임 종료 시간

diff = end - start  # 총 게임 실행 시간
diff = format(diff, ".3f")

if cor_cnt >= 3:
    
    print("합격")
else:
    print("불합격")

# 기록 DB에 삽입
cursor.execute("insert into records('cor_cnt', 'record', 'regdate') values \
    (?, ?, ?)", (cor_cnt, diff, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

print("게임 시간 :", diff, "초,", "정답 개수 : {}".format(cor_cnt))

if __name__ == '__main__':
    pass

