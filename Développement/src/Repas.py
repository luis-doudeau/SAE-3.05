from xmlrpc.client import Boolean
from sqlalchemy import Date, BOOLEAN
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Repas(Base):
    __tablename__ = "REPAS"
    idRepas = Column(Integer, primary_key = True)
    estMidi = Column(BOOLEAN)
    idRest = Column(int)
    idCreneauRepas = Column(int)

    def __init__(self, idRepas, estMidi, idRest, idCreneauRepas) -> None:
        self.idRepas = idRepas
        self.estMidi = estMidi
        self.idRest = idRest
        self.idCreneauRepas = idCreneauRepas

    def __repr__(self) -> str:
        return "ID repas : " + str(self.idRepas) + ", il est midi : " + str(self.estMidi) + ", au restaurant d'id : " + str(self.idRest) + ", du créneauRepas d'id : " + str(self.idCreneauRepas)
