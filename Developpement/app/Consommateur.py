from sqlalchemy import Date, ForeignKey
from sqlalchemy import Column , Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from .Participant import Participant

Base = declarative_base()

class Consommateur(Participant, Base):
    __tablename__ = "CONSOMMATEUR"
    idP = Column(Integer, ForeignKey('PARTICIPANT.idP'), primary_key=True)

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
        return "ID consommateur : " + str(self.idP)

    def to_dict_sans_ddn(self):
        return {
            "prenomP" : self.prenomP,
            "nomP" : self.nomP,
            "emailP" : self.emailP
        }
