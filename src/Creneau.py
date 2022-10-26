from datetime import date
from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Creneau(Base):
    __tablename__ = "CRENEAU"
    idCreneau = Column(Integer, primary_key = True)
    dateDebut = Column(Date)

    def __init__(self, idCreneau, nomRest) -> None:
        self.idCreneau = idCreneau
        self.nomRest = nomRest

    def __repr__(self) -> str:
        return "ID restaurant : " + str(self.idRest) + ", nom restaurant : " + str(self.nomRest)
        