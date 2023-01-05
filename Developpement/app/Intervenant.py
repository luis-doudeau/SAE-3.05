from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text, ForeignKey
from sqlalchemy . ext . declarative import declarative_base

from .Consommateur import Consommateur




Base = declarative_base()

class Intervenant(Consommateur, Base):
    __tablename__ = "INTERVENANT"
    #idP = Column(Integer, primary_key = True)
    idP = Column(Integer, ForeignKey('CONSOMMATEUR.idP'), primary_key=True)

    def __init__(self, idP) -> None:
        self.idP = idP

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP)

    def to_dict(self):
        return {
            "prenomP" : self.prenomP,
            "nomP" : self.nomP,
        }

    def get_id(self):
        return self.idP