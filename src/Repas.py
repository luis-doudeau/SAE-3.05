from xmlrpc.client import Boolean
from sqlalchemy import Date, BOOLEAN
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Repas(Base):
    __tablename__ = "REPAS"
    idRepas = Column(Integer, primary_key = True)
    jourR = Column(Date)
    estMidi = Column(BOOLEAN)
    idRest = Column(int)
    idCreneauRepas = Column(int)

    def __init__(self, idRepas, jourR, estMidi, idRest, idCreneauRepas) -> None:
        self.idRepas = idRepas
        self.jourR = jourR
        self.estMidi = estMidi
        self.idRest = idRest
        self.idCreneauRepas = idCreneauRepas

    def __repr__(self) -> str:
        return "ID repas : " + str(self.idRepas) + ", le " + str(self.jourR) + ", midi : " + str(self.estMidi) + ", au restaurant d'id : " + str(self.idRest) + ", du créneauRepas d'id : " + str(self.idCreneauRepas)
