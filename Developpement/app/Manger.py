from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Manger(Base):
    __tablename__ = "MANGER"
    idP = Column(Integer, primary_key = True)
    idRepas = Column(Integer, primary_key = True)

    def __init__(self, idP, idRepas) -> None:
        self.idP = idP
        self.idRepas = idRepas

    def __repr__(self) -> str:
        return "ID consommateur : " + str(self.idP) + ", ID repas : " + str(self.idRepas)
