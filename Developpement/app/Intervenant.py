from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervenant(Base):
    __tablename__ = "INTERVENANT"
    idP = Column(Integer, primary_key = True)

    def __init__(self, idP) -> None:
        self.idP = idP

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP)
