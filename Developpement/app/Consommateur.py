from sqlalchemy import Date, ForeignKey
from sqlalchemy import Column , Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from Participant import Participant

Base = declarative_base()

class Consommateur(Participant, Base):
    __tablename__ = "CONSOMMATEUR"
    #idP = Column(Integer, primary_key = True)
    idP = Column(Integer, ForeignKey('PARTICIPANT.idP'), primary_key=True)

    def __init__(self, idP) -> None:
        self.idP = idP

    def __repr__(self) -> str:
        return "ID consommateur : " + str(self.idP)
