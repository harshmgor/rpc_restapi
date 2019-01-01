#!/usr/bin/env python
import models
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=models.engine)

# update
session = Session()

users = session.query(models.User).filter(models.User.id == '1').first()
users.username = "a"
session.commit()

session.close()
