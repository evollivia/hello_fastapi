from typing import List, Optional

from fastapi import FastAPI
from fastapi.params import Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Integer, Column, String, Sequence, func, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

# 회원정보를 이용한 CRUD
# mno, userid, passwd, name, email,regdate

# 데이터베이스 설정
sqlite_url = 'sqlite:///python.db'
engine = create_engine(sqlite_url, connect_args={'check_same_thread': False}, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 데이터베이스 모델 정의
Base = declarative_base()
class Member(Base):
    __tablename__ = 'member'
    mno = Column(Integer, Sequence('seq_member'), primary_key=True, index=True)
    userid = Column(String, index=True)
    passwd = Column(String)
    name = Column(String)
    email = Column(String)
    regdate = Column(DateTime(timezone=True), server_default=func.now())

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# 데이터베이스 세션을 의존성으로 주입하기 위한 함수
def get_db():
    db = SessionLocal()     # 데이터베이스 세션 객체 생성
    try:
        yield db            # yield : 파이썬 제네레이터 객체
        # 함수가 호출될 때 비로소 객체를 반환(넘김)
    finally:
        db.close()          # 데이터베이스 세션 닫음(db연결 해제, 리소스 반환)

# pydantic 모델
class MemberModel(BaseModel):
    mno: int
    userid: str
    passwd: str
    name: str
    email: str
    regdate: str

# FastAPI 메인
app = FastAPI()

@app.get('/')
def index():
    return "Hello SQLAlchemy!! - Member"

# 멤버 조회
@app.get('/member', response_model=List[MemberModel])
def read_member(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

# 멤버 추가
@app.post('/member', response_model=MemberModel)
def madd(m:MemberModel, db: Session = Depends(get_db)):
    m = Member(**dict(m))
    db.add(m)
    db.commit(m)
    db.refresh(m)
    return m

# 멤버 상세 조회
@app.get('/member/{mno}', response_model=List[MemberModel])
def readone_m(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member

# 멤버 삭제
@app.delete('/member/{mno}', response_model=Optional[MemberModel])
def delete_m(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    if member:
        db.delete(member)
        db.commit()
    return member

# 멤버 수정
@app.put('/sj', response_model=Optional[MemberModel])
def update_m(m: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == m.mno).first()
    if member:
        for key, val in m.dict().items():
            setattr(member, key, val)
        db.commit()
        db.refresh(member)
    return member

if __name__ == "__main__":
    import uvicorn
    uvicorn.run('sqlalchemy02:app', reload=True)