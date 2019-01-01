#!/usr/bin/env python
import models
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=models.engine)

# update
session = Session()

session.query(models.User).filter(models.User.id == 1).delete()
session.commit()

session.close()
