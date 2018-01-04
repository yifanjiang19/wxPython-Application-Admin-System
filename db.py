#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-
import os
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()
# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'user'
    __table_args__ = {'sqlite_autoincrement': True}

    # 表的结构:
    id = Column(Integer, primary_key=True, autoincrement=True)
    index = Column(String(20))
    name = Column(String(20))
    alarm = Column(String(20))
    blood_pressure = Column(String(20))
    breath = Column(String(20))
    temper = Column(String(20))
    time = Column(String(50))

def db_connect():
    basedir = os.path.abspath(os.path.dirname(__file__))

    # 创建对象的基类:
    
    # 初始化数据库连接:
    engine = create_engine('sqlite:///' + os.path.join(basedir, 'test.db'), echo=True)
    # 创建DBSession类型:
    DBsession = sessionmaker(bind=engine)
    session = DBsession()
    Base.metadata.create_all(engine)
    return session
# test_user = User(id=1,
#                 index = '123',
#                 name = '123',
#                 alarm = '123',
#                 blood_pressure = '123',
#                 breath = '123',
#                 temper = '123')
# session.add(test_user)
# session.commit()
# session.close()