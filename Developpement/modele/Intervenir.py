from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervenir(Base):
    __tablename__ = "INTERVENIR"
    idP = Column(Integer, primary_key = True)
    idCreneau = Column(Integer, primary_key = True)
    nomIntervention = Column(Text)

    def __init__(self, idP, idCreneau, nomIntervention) -> None:
        self.idP = idP
        self.idCreneau = idCreneau
        self.nomIntervention = nomIntervention

    def __repr__(self) -> str:
        return "ID auteur : " + str(self.idP) + ", ID créneau : " + str(self.idCreneau) + ", nom intervention : " + self.nomIntervention
