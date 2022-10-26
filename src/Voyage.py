from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Voyage(Base):
    __tablename__ = "VOYAGE"
    idVoy = Column(Integer, primary_key = True)
    heureDebVoy = Column(DATETIME)
    DureeVoy = Column(DATETIME)

    def __init__(self, idVoy, heureDebVoy, DureeVoy) -> None:
        self.idVoy = idVoy
        self.heureDebVoy = heureDebVoy
        self.DureeVoy = DureeVoy

    def __repr__(self) -> str:
        return "ID voyage : " + str(self.idVoy) + ", heure début : " + str(self.heureDebVoy) + ", durée : " + str(self.DureeVoy)
        