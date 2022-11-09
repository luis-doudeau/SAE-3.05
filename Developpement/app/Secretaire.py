from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Secretaire(Base):
    __tablename__ = "SECRETAIRE"
    idSecretaire = Column(Integer, primary_key = True)
    prenomS = Column(Text)
    nomS = Column(Text)
    emailS = Column(Text)
    mdpS = Column(Text)


    def __init__(self, idSecretaire, prenomS, nomS, emailS, mdpS) -> None:
        self.idSecretaire = idSecretaire
        self.prenomS = prenomS
        self.nomS = nomS
        self.emailS = emailS
        self.mdpS = mdpS


    def __repr__(self) -> str:
        return "ID secrétaire : " + str(self.idSecretaire) + " - prenom : " + self.prenomS + " - nom : " + self.nomS + " - email : " + self.emailS +  " - mdp : " + self.mdpS
        