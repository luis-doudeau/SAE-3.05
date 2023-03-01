from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class CreneauTravail(Base):
    __tablename__ = "CRENEAUTRAVAIL"
    idCreneau = Column(Integer, primary_key = True)
    dateDebut = Column(DATETIME)
    dateFin = Column(DATETIME)

    def __init__(self, idCreneau, dateDebut, dateFin) -> None:
        self.idCreneau = idCreneau
        self.dateDebut = dateDebut
        self.dateFin = dateFin

    def __repr__(self) -> str:
        return "ID créneau travail : " + str(self.idCreneau) + " date début : " + str(self.dateDebut)+ " date fin : " + str(self.dateFin)
        