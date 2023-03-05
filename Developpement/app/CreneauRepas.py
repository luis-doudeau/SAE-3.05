from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class CreneauRepas(Base):
    __tablename__ = "CRENEAUREPAS"
    idCreneau = Column(Integer, primary_key = True)
    dateDebut = Column(DATETIME)
    dateFin = Column(DATETIME)

    def __init__(self, idCreneau, dateDebut, dateFin) -> None:
        self.idCreneau = idCreneau
        self.dateDebut = dateDebut
        self.dateFin = dateFin

    def __repr__(self) -> str:
        return "ID créneau repas : " + str(self.idCreneau) + " date début : " + str(self.dateDebut)+ " date fin : " + str(self.dateFin)
        