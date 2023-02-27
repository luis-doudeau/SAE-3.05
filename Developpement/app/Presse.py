from sqlalchemy import Column , Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from.Intervenant import Intervenant

Base = declarative_base()

class Presse(Intervenant, Base):
    __tablename__ = "PRESSE"
    idP = Column(Integer, ForeignKey('INTERVENANT.idP'), primary_key=True)

    def __init__(self, idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP, remarques, invite = False, emailEnvoye = False) -> None:
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

    def __repr__(self) -> str:
        return "ID presse : " + str(self.idP)
