from xmlrpc.client import Boolean
from sqlalchemy import Date, BOOLEAN, ForeignKey
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Repas(Base):
    __tablename__ = "REPAS"
    idRepas = Column(Integer, primary_key = True)
    estMidi = Column(BOOLEAN)
    idRest = Column(Integer)
    idCreneau = Column(Integer)

    def __init__(self, idRepas, estMidi, idRest, idCreneau) -> None:
        self.idRepas = idRepas
        self.estMidi = estMidi
        self.idRest = idRest
        self.idCreneau = idCreneau

    def __repr__(self) -> str:
        return "ID repas : " + str(self.idRepas) + " il est midi : " + str(self.estMidi) + " au restaurant d'id : " + str(self.idRest) + " du créneau d'id : " + str(self.idCreneau)
