from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Manger(Base):
    __tablename__ = "MANGER"
    idRepas = Column(Integer, primary_key = True)
    idP = Column(Integer, primary_key = True)

    def __init__(self, idRepas, idP) -> None:
        self.idRepas = idRepas
        self.idP = idP

    def __repr__(self) -> str:
        return "ID repas : " + str(self.idRepas) + ", ID consommateur : " + str(self.idP)
