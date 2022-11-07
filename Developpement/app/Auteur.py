from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Auteur(Base):
    __tablename__ = "AUTEUR"
    idP = Column(Integer, primary_key = True)
    idMe = Column(Integer)

    def __init__(self, idP, idMe) -> None:
        self.idP = idP
        self.idMe = idMe

    def __repr__(self) -> str:
        return "ID auteur : " + str(self.idP) + ", ID maison edition : " + str(self.idMe)
