from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Mobiliser(Base):
    __tablename__ = "MOBILISER"
    idVoy = Column(Integer, primary_key = True)
    idNavette = Column(Date)
    DureeVoy = Column(Date)

    def __init__(self, idVoy, idNavette) -> None:
        self.idVoy = idVoy
        self.idNavette = idNavette

    def __repr__(self) -> str:
        return "ID voyage : " + str(self.idVoy) + ", ID navette : " + str(self.idNavette)
        