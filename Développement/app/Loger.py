from datetime import datetime
from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Loger(Base):
    __tablename__ = "LOGER"
    idIntervenant = Column(Integer, primary_key = True)
    idHotel = Column(Integer, primary_key = True)
    dateDeb = Column(DATETIME, primary_key = True)
    dateFin = Column(DATETIME)

    def __init__(self, idIntervenant, idHotel, dateDeb, dateFin) -> None:
        self.idIntervenant = idIntervenant
        self.idHotel = idHotel
        self.dateDeb = dateDeb
        self.dateFin = dateFin

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idIntervenant) + ", ID hotel : " + str(self.idHotel) + ", date début : " + self.dateDeb + ", date fin : " + self.dateFin
        