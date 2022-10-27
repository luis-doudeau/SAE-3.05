from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Travailler(Base):
    __tablename__ = "TRAVAILLER"
    idCreneau = Column(Integer, primary_key = True)
    idS = Column(Integer)

    def __init__(self, idCreneau, idS) -> None:
        self.idCreneau = idCreneau
        self.idS = idS

    def __repr__(self) -> str:
        return "ID créneau : " + str(self.idCreneau) + ", ID staff : " + str(self.idS)
