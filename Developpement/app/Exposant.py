from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Exposant(Base):
    __tablename__ = "EXPOSANT"
    idP = Column(Integer, primary_key = True)
    numStand = Column(Text)

    def __init__(self, idP, numStand) -> None:
        self.idP = idP
        self.numStand = numStand

    def __repr__(self) -> str:
        return "ID exposant : " + str(self.idP) + ", numéro stand : " + self.numStand
        