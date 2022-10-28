from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Regime(Base):
    __tablename__ = "REGIME"
    idRegime = Column(Integer, primary_key = True)
    nomRegime = Column(Text)

    def __init__(self, idRegime, nomRegime) -> None:
        self.idRegime = idRegime
        self.nomRegime = nomRegime

    def __repr__(self) -> str:
        return "ID régime : " + str(self.idRegime) + ", nom régime : " + self.nomRegime
        