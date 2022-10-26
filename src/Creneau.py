from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Creneau(Base):
    __tablename__ = "CRENEAU"
    idCreneau = Column(Integer, primary_key = True)
    dateDebut = Column(Date)
    dateFin = Column(Date)

    def __init__(self, idCreneau, dateDebut, dateFin) -> None:
        self.idCreneau = idCreneau
        self.dateDebut = dateDebut
        self.dateFin = dateFin

    def __repr__(self) -> str:
        return "ID créneau : " + str(self.idCreneau) + ", date fin : " + str(self.dateDebut)+ ", date début : " + str(self.dateFin)
        