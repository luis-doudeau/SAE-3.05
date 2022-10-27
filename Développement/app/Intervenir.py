from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervenir(Base):
    __tablename__ = "INTERVENIR"
    idA = Column(Integer, primary_key = True)
    idCreneau = Column(Integer, primary_key = True)
    idInter = Column(Integer)

    def __init__(self, idA, idCreneau, idInter) -> None:
        self.idA = idA
        self.idCreneau = idCreneau
        self.idInter = idInter

    def __repr__(self) -> str:
        return "ID auteur : " + str(self.idA) + ", ID créneau : " + str(self.idCreneau) + ", ID intervention : " + str(self.idInter)
