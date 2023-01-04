import datetime
from operator import inv
from sqlalchemy import DATE, BOOLEAN, ForeignKey
from sqlalchemy import Column , Integer, Text
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin

from .Utilisateur import Utilisateur

Base = declarative_base()

class Participant(Utilisateur, Base):
    __tablename__ = "PARTICIPANT"
    idP = Column(Integer, ForeignKey('UTILISATEUR.idP'), primary_key=True)
    ddnP = Column(DATE)
    telP = Column(Text)
    adresseP = Column(Text)
    invite = Column(BOOLEAN)
    emailEnvoye = Column(BOOLEAN)
    remarques = Column(Text)

    def __init__(self, idP, prenomP, nomP, ddnP, telP, emailP, adresseP, mdpP, remarques, invite = False, emailEnvoye = False) -> None:
        self.idP = idP
        self.prenomP = prenomP
        self.nomP = nomP
        self.ddnP = ddnP
        self.telP = telP
        self.emailP = emailP
        self.adresseP = adresseP
        self.mdpP = mdpP
        self.invite = invite
        self.emailEnvoye = emailEnvoye
        self.remarques = remarques

    def __repr__(self) -> str:
        return str(self.idP) + " - " + self.prenomP + " - " + self.nomP + " - " + self.telP + " - " + self.emailP

    def to_dict(self):
        return {
            "prenomP" : self.prenomP,
            "nomP" : self.nomP,
            "ddnP" : self.ddnP,
            "emailP" : self.emailP
        }
