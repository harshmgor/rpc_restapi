#!/usr/bin/env python
import models
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=models.engine)

# insert
session = Session()

user = models.User()
user.id = 2
user.username = "Name"

session.add(user)
session.commit()

session.close()
