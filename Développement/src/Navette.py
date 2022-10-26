from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Navette(Base):
    __tablename__ = "NAVETTE"
    idNavette = Column(Integer, primary_key = True)
    capaciteNavette = Column(Integer)

    def __init__(self, idNavette, capaciteNavette) -> None:
        self.idNavette = idNavette
        self.capaciteNavette = capaciteNavette

    def __repr__(self) -> str:
        return "ID navette : " + str(self.idNavette) + ", capacité : " + str(self.capaciteNavette)
        