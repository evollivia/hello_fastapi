from typing import List, Optional

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.dbfactory import get_db
from app.models.sungjuk import Sungjuk
from app.schema.sungjuk import SungjukModel, NewSungjukModel

sungjuk_router = APIRouter()

# @sungjuk_router.get('/')
# def index():
#     return 'Hello, sungjuk_router'

@sungjuk_router.get('/', response_model=List[SungjukModel])
def read_sungjuk(db: Session = Depends(get_db)):
    sungjuks = db.query(Sungjuk).all()
    return sungjuks

@sungjuk_router.post('/', response_model=NewSungjukModel)
def add_sungjuk(sj: NewSungjukModel, db: Session = Depends(get_db)):
    sj = Sungjuk(**dict(sj))
    db.add(sj)
    db.commit()
    db.refresh(sj)
    return sj

@sungjuk_router.get('/{sjno}', response_model=Optional[SungjukModel])
def readone_sungjuk(sjno: int, db:Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjno == sjno).first()
    return sungjuk


@sungjuk_router.delete('/{sjno}', response_model=Optional[SungjukModel])
def delete_sungjuk(sjno: int, db:Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjno == sjno).first()
    if sungjuk:
        db.delete(sungjuk)
        db.commit()
    return sungjuk


@sungjuk_router.put('/', response_model=Optional[SungjukModel])
def update_sungjuk(sj: SungjukModel, db:Session = Depends(get_db)):
    sungjuk = db.query(Sungjuk).filter(Sungjuk.sjno == sj.sjno).first()
    if sungjuk:
        for key, val in sj.dict().items():
            setattr(sungjuk, key, val)
        db.commit()
        db.refresh(sungjuk)
    return sungjuk
