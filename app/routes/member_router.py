from typing import List, Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dbfactory import get_db
from app.models.member import Member
from app.schema.member import MemberModel, NewMemberModel

member_router = APIRouter()

# @member_router.get('/')
# def index():
#     return 'Hello, member_router'

@member_router.get('/', response_model=List[MemberModel])
def list(db: Session = Depends(get_db)):
    members = db.query(Member).all()
    return members

@member_router.post('/', response_model=NewMemberModel)
def add_member(m: NewMemberModel, db: Session = Depends(get_db)):
    m = Member(**dict(m))
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@member_router.get('/{mno}', response_model=Optional[MemberModel])
def readone_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    return member

@member_router.delete('/{mno}', response_model=Optional[MemberModel])
def delete_member(mno: int, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == mno).first()
    if member:
        db.delete(member)
        db.commit()
    return member

@member_router.put('/{mno}', response_model=Optional[MemberModel])
def update_member(m: MemberModel, db: Session = Depends(get_db)):
    member = db.query(Member).filter(Member.mno == m.mno).first()
    if member:
        for key, val in m.dict().items():
            setattr(member, key, val)
        db.commit()
        db.refresh(member)
    return member