from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

from flask_login import UserMixin


Base = declarative_base()

class Intervenant(Base, UserMixin):
    __tablename__ = "INTERVENANT"
    idP = Column(Integer, primary_key = True)

    def __init__(self, idP) -> None:
        self.idP = idP

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP)

    def to_dict(self):
        return {
            'id': self.idP
        }
    def get_id(self):
        return self.idP