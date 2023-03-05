from sqlalchemy import Column , Integer, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base

from flask_login import UserMixin
import abc


Base = declarative_base()

class Utilisateur(Base, UserMixin):
    __tablename__ = "UTILISATEUR"
    idP = Column(Integer, primary_key = True)
    prenomP = Column(Text)
    nomP = Column(Text)
    emailP = Column(Text)
    mdpP = Column(Text)
    
    def __init__(self, idP, prenomP, nomP, emailP, mdpP) -> None:
        self.idP = idP
        self.prenomP = prenomP
        self.nomP = nomP
        self.emailP = emailP
        self.mdpP = mdpP

    def __repr__(self) -> str:
        return str(self.idP) + " - " + self.prenomP + " - " + self.nomP + " - " + " - " + self.emailP

    def get_id(self):
        return self.idP

    @abc.abstractmethod
    def est_secretaire(self):
        pass