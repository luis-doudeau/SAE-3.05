from sqlalchemy import Column , Integer, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .Intervenant import Intervenant

Base = declarative_base()

class Auteur(Intervenant, Base):
    __tablename__ = "AUTEUR"
    idP = Column(Integer, ForeignKey('INTERVENANT.idP'), primary_key=True)
    idMe = Column(Integer)

    def __init__(self, idP,prenomP, nomP, emailP, mdpP, ddnP, telP, adresseP, codePostalP, villeP, remarques="", idMe=1, invite = False, emailEnvoye = False) -> None:
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
        self.idMe = idMe

    def __repr__(self) -> str:
        return self.prenomP + " " + self.nomP
