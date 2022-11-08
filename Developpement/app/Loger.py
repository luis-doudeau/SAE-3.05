from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Loger(Base):
    __tablename__ = "LOGER"
    idP = Column(Integer, primary_key = True)
    idHotel = Column(Integer, primary_key = True)
    dateArrive = Column(DATETIME)
    dateFin = Column(DATETIME)

    def __init__(self, idP, idHotel, dateArrive, dateFin) -> None:
        self.idP = idP
        self.idHotel = idHotel
        self.dateArrive = dateArrive
        self.dateFin = dateFin

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP) + "- ID hotel : " + str(self.idHotel) + "- date arrivé : " + str(self.dateDebut) + "- date fin : " + str(self.dateFin)
        