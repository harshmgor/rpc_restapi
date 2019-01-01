#!/usr/bin/env python
import models
from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=models.engine)

# select
session = Session()

users = session.query(models.User).all()
for user in users:
    print("ID : %d \t Username : %s" % (user.id, user.username))

session.close()
