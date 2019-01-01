#!/usr/bin/env python
from models import engine, Data
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)


def get():
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
    session = Session()

    data = Data()
    data.title = title
    data.body = body
    session.add(data)
    session.commit()

    session.close()
    return 'Success'


def put(data_id, title, body):
    session = Session()

    data = session.query(Data).filter(Data.id == data_id).first()
    data.title = title
    data.body = body
    session.commit()

    session.close()
    return 'Success'


def delete(data_id):
    session = Session()

    session.query(Data).filter(Data.id == data_id).delete()
    session.commit()

    session.close()
    return 'Success'
