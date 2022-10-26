from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Staff(Base):
    __tablename__ = "STAFF"
    idS = Column(Integer, primary_key = True)

    def __init__(self, idS) -> None:
        self.idS = idS

    def __repr__(self) -> str:
        return "ID staff : " + str(self.idS)
        