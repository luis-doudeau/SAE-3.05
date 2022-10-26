from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Exposant(Base):
    __tablename__ = "EXPOSANT"
    idE = Column(Integer, primary_key = True)
    numStand = Column(Date)

    def __init__(self, idE, numStand) -> None:
        self.idE = idE
        self.numStand = numStand

    def __repr__(self) -> str:
        return "ID exposant : " + str(self.idE) + ", numéro stand : " + str(self.numStand)
        