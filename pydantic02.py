from datetime import datetime
from typing import List
from fastapi import FastAPI
from pydantic import BaseModel

# 회원정보를 이용한 CRUD
# userid, passwd, name, email,regdate

# 회원관리 모델 정의
class Member(BaseModel):
    userid: str
    passwd: str
    name: str
    email: str
    regdate: datetime

# 회원 데이터 저장용 변수
member_db: List[Member] = []
app = FastAPI()


@app.get('/')
def index():
    return "Hello Pydantic!! - Member"


# 회원 데이터 조회
@app.get('/member', response_model=List[Member])
def member_readall():
    return member_db

# 회원 데이터 추가
# fastapi swagger UI 이용 : http://127.0.0.1:8000/docs
@app.post('/memberadd', response_model=Member)
def member_create(m: Member):
    member_db.append(m)
    return m

# 회원 데이터 추가 : 3건의 기본 데이터
@app.get('/memberadd', response_model=Member)
def member_create3():
    m = Member(userid='abc123', passwd='1q2w3e4r', name='Steve', email='abc123@aabbcc.com', regdate='2024-06-28T03:45:56.123Z')
    member_db.append(m)

    m = Member(userid='def456', passwd='qawsedrf', name='Hellen', email='zxc098@aabbcc.com', regdate='2021-04-09T03:45:56.954Z')
    member_db.append(m)

    m = Member(userid='ghi789', passwd='azsxdcfv', name='Jack', email='mnb765@aabbcc.com', regdate='2023-11-16T03:45:56.855Z')
    member_db.append(m)
    return m

# 회원 데이터 상세 조회 - userid로 조회
@app.get('/memberone/{userid}',response_model=Member)
def memberok(userid: str):
    memberone = Member(userid='----', passwd='****', name='----', email='----', regdate='1970-01-01-T00:00:00.000Z')
    for m in member_db:
        if m.userid == userid:
            memberone = m
    return memberone

# 회원 데이터 삭제 - userid로 삭제
@app.delete('/member/{userid}', response_model=Member)
def memberdel(userid: str):
    memberone = Member(userid='----', passwd='****', name='----', email='----', regdate='1970-01-01-T00:00:00.000Z')
    for idx, m in enumerate(member_db):
        if m.userid == userid:
            memberone = member_db.pop(idx)
    return memberone

# 회원 데이터 수정 - userid로 조회 후 수정
@app.put('/member', response_model=Member)
def memberput(one: Member):
    putone = Member(userid='----', passwd='****', name='----', email='----', regdate='1970-01-01-T00:00:00.000Z')
    for idx, m in enumerate(member_db):
        if m.userid == one.userid:
            member_db[idx] = one
            putone = one
    return putone

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('pydantic02:app', reload=True)
