from datetime import date
from xmlrpc.client import Boolean
from sqlalchemy import Date, BOOLEAN
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervenant(Base):
    __tablename__ = "INTERVENANT"
    idIntervenant = Column(Integer, primary_key = True)
    dateArrive = Column(Date)
    dateDepart = Column(Date)
    transport = Column(Text)
    intervention = Column(Text)

    def __init__(self, idIntervenant, dateArrive, dateDepart, transport, intervention) -> None:
        self.idIntervenant = idIntervenant
        self.dateArrive = dateArrive
        self.dateDepart = dateDepart
        self.transport = transport
        self.intervention = intervention

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idIntervenant) + ", arrive le " + str(self.dateArrive) + ", part le : " + str(self.dateDepart) + ", prend comme transport : " + str(self.transport) + ", intervient : " + str(self.intervention)
