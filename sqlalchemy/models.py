#!/usr/bin/env python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# a base class that will be shared by all the models
Base = declarative_base()


class Data(Base):
    """
    The Class for table 'data'.
    Columns : id, title & body
    """
    __tablename__ = "data"
    id = Column('id', Integer, primary_key=True, autoincrement=True)
    title = Column('title', String)
    body = Column('body', String)


# to create in data base
engine = create_engine('sqlite:///users.db', echo=False)

# to create table
Base.metadata.create_all(bind=engine)
