#!/usr/bin/env python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# a base class that will be shared by all the models
Base = declarative_base()


class User(Base):
    __tablename__ = "person"
    id = Column('id', Integer, primary_key=True)
    username = Column('username', String, unique=True)

# to create in memory data base
# engine = create_engine('sqlite:///:memory:', echo=True)

# to create in data base
engine = create_engine('sqlite:///users.db', echo=False)

# to create table
Base.metadata.create_all(bind=engine)
