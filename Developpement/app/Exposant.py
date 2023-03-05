from sqlalchemy import Column , Integer, Text,ForeignKey
from sqlalchemy . ext . declarative import declarative_base
from .Participant import Participant

Base = declarative_base()

class Exposant(Participant, Base):
    __tablename__ = "EXPOSANT"
    idP = Column(Integer, ForeignKey('PARTICIPANT.idP'), primary_key=True)
    numStand = Column(Text)

    def __init__(self,idP, prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP, remarques="", numStand="0", invite = False, emailEnvoye = False) -> None:
        self.idP = idP
        self.prenomP = prenomP
        self.nomP = nomP
        self.emailP = emailP
        self.mdpP = mdpP
        self.ddnP = ddnP
        self.telP = telP
        self.adresseP = adresseP
        self.codePostalP = codePostalP
        self.villeP = villeP
        self.invite = invite
        self.emailEnvoye = emailEnvoye
        self.remarques = remarques
        self.numStand = numStand

    def __repr__(self) -> str:
        return "ID exposant : " + str(self.idP) + ", numéro stand : " + self.numStand
        