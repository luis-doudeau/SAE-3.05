from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Assister(Base):
    __tablename__ = "ASSISTER"
    idP = Column(Integer, primary_key = True)
    dateArrive = Column(datetime, primary_key = True)
    dateDepart = Column(datetime, primary_key = True)

    def __init__(self, idP, dateArrive, dateDepart) -> None:
        self.idP = idP
        self.dateArrive = dateArrive
        self.dateDepart = dateDepart

    def __repr__(self) -> str:
        return "ID participant : " + str(self.idP) + "- date arrivée : " + str(self.dateArrive) + "- date départ : " + str(self.dateDepart) 
