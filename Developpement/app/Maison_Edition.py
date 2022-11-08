from tkinter.tix import INTEGER
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Maison_Edition(Base):
    __tablename__ = "MAISON_EDITION"
    idMe = Column(Integer, primary_key = True)
    nomMe = Column(Text)
    numStand = Column(Text)

    def __init__(self, idMe, nomMe, numStand) -> None:
        self.idMe = idMe
        self.nomMe = nomMe
        self.numStand = numStand

    def __repr__(self) -> str:
        return "ID maison edition : " + str(self.idMe) + ", nom : " + self.nomMe + ", numStand" + self.numStand
        