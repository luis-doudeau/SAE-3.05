import datetime
from operator import inv
from sqlalchemy import DATE, BOOLEAN
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Participant(Base):
    __tablename__ = "PARTICIPANT"
    idP = Column(Integer, primary_key = True)
    prenomP = Column(Text)
    nomP = Column(Text)
    ddnP = Column(DATE)
    telP = Column(Text)
    emailP = Column(Text)
    adresseP = Column(Text)
    mdpP = Column(Text)
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
    
    def to_dict_sans_ddn(self):
        return {
            "prenomP" : self.prenomP,
            "nomP" : self.nomP,
            "emailP" : self.emailP
        }