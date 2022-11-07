from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Creneau_Repas(Base):
    __tablename__ = "CRENEAU_REPAS"
    idCreneauRepas = Column(Integer, primary_key = True)
    dateDebut = Column(DATETIME)
    dateFin = Column(DATETIME)

    def __init__(self, idCreneauRepas, dateDebut, dateFin) -> None:
        self.idCreneauRepas = idCreneauRepas
        self.dateDebut = dateDebut
        self.dateFin = dateFin

    def __repr__(self) -> str:
        return "ID créneauRepas : " + str(self.idCreneauRepas) + ", date début : " + str(self.dateDebut)+ ", date fin : " + str(self.dateFin)
        