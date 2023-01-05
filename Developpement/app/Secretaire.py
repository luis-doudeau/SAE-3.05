from sqlalchemy import Column , Integer, Text, ForeignKey
from sqlalchemy . ext . declarative import declarative_base
from .Utilisateur import Utilisateur

Base = declarative_base()

class Secretaire(Utilisateur, Base):
    __tablename__ = "SECRETAIRE"
    idP = Column(Integer, ForeignKey('UTILISATEUR.idP'), primary_key=True)



    def __init__(self, idP, prenomP, nomP, emailP, mdpP) -> None:
        self.idP = idP
        self.prenomP = prenomP
        self.nomP = nomP
        self.emailP = emailP
        self.mdpP = mdpP


    def __repr__(self) -> str:
        return "ID secrétaire : " + str(self.idSecretaire) + " - prenom : " + self.prenomS + " - nom : " + self.nomS + " - email : " + self.emailS +  " - mdp : " + self.mdpS
        
    def est_secretaire(self):
        return True