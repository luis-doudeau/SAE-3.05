from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text, ForeignKey
from sqlalchemy . ext . declarative import declarative_base

from .Consommateur import Consommateur




Base = declarative_base()

class Intervenant(Consommateur, Base):
    __tablename__ = "INTERVENANT"
    idP = Column(Integer, ForeignKey('CONSOMMATEUR.idP'), primary_key=True)

    def __init__(self,idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, remarques, invite = False, emailEnvoye = False) -> None:
        self.idP = idP
        self.prenomP = prenomP
        self.nomP = nomP
        self.emailP = emailP
        self.mdpP = mdpP
        self.ddnP = ddnP
        self.telP = telP
        self.adresseP = adresseP
        self.invite = invite
        self.emailEnvoye = emailEnvoye
        self.remarques = remarques

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP)

    def to_dict(self):
        return {
            "idP" : self.idP,
            "prenomP" : self.prenomP,
            "nomP" : self.nomP,
        }

    def get_id(self):
        return self.idP