from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Consommateur(Base):
    __tablename__ = "CONSOMMATEUR"
    idC = Column(Integer, primary_key = True)

    def __init__(self, idC) -> None:
        self.idC = idC

    def __repr__(self) -> str:
        return "ID consommateur : " + str(self.idC)
