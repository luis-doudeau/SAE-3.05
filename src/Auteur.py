from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Auteur(Base):
    __tablename__ = "AUTEUR"
    idA = Column(Integer, primary_key = True)
    idMe = Column(Integer)

    def __init__(self, idA, idMe) -> None:
        self.idA = idA
        self.idMe = idMe

    def __repr__(self) -> str:
        return "ID auteur : " + str(self.idA) + ", ID maison edition : " + str(self.idMe)
