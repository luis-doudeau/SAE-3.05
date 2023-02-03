from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervenir(Base):
    __tablename__ = "INTERVENIR"
    idP = Column(Integer, primary_key = True)
    idCreneau = Column(Integer, primary_key = True)
    idIntervention = Column(Integer, primary_key = True)
    idLieu = Column(Integer)
    descIntervention = Column(Text)

    def __init__(self, idP, idCreneau, idLieu, idIntervention, descIntervention) -> None:
        self.idP = idP
        self.idCreneau = idCreneau
        self.idLieu = idLieu
        self.idIntervention = idIntervention
        self.descIntervention = descIntervention

    def __repr__(self) -> str:
        return "ID auteur : " + str(self.idP) + ", ID créneau : " + str(self.idCreneau) + ", ID lieu : " + str(self.idLieu) +", ID intervention : " + str(self.idIntervention) + ", desc : " + self.descIntervention
