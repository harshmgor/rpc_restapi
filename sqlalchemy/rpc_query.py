#!/usr/bin/env python
"""
Four methods to interact with database.
get(), put(), post(), delete()
"""
from models import engine, Data
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


def get():
    """
    The get() will return the all the value from database.
    """
    session = Session()
    _list = []
    values = session.query(Data).all()
    for value in values:
        data = {
            "id": value.id,
            "title": value.title,
            "body": value.body
        }
        _list.append(data)

    _data = {"object": _list}
    session.close()
    return _data


def post(title, body):
    """
        The post() will add a new record in database.
    """
    session = Session()

    data = Data()
    data.title = title
    data.body = body
    session.add(data)
    session.commit()

    session.close()
    return 'Success'


def put(data_id, title, body):
    """
        The put() will will update a record.
        it will take id to find the record,  and title and body values to update
    """
    session = Session()

    data = session.query(Data).filter(Data.id == data_id).first()
    data.title = title
    data.body = body
    session.commit()

    session.close()
    return 'Success'


def delete(data_id):
    """
        The delete() will remove a record from database
    """
    session = Session()

    session.query(Data).filter(Data.id == data_id).delete()
    session.commit()

    session.close()
    return 'Success'
