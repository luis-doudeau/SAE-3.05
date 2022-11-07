from sqlalchemy import DATETIME, BOOLEAN
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Voyage(Base):
    __tablename__ = "VOYAGE"
    idVoy = Column(Integer, primary_key = True)
    heureDebVoy = Column(DATETIME)
    DureeVoy = Column(DATETIME)
    directionGare = Column(BOOLEAN)

    def __init__(self, idVoy, heureDebVoy, DureeVoy, directionGare) -> None:
        self.idVoy = idVoy
        self.heureDebVoy = heureDebVoy
        self.DureeVoy = DureeVoy
        self.directionGare = directionGare 

    def __repr__(self) -> str:
        return "ID voyage : " + str(self.idVoy) + ", heure début : " + str(self.heureDebVoy) + ", durée : " + str(self.DureeVoy) + ", direction gare : " + str(self.directionGare)
        