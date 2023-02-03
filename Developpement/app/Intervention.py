from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervention(Base):
    __tablename__ = "INTERVENTION"
    idIntervention = Column(Integer, primary_key = True)
    nomIntervention = Column(Text)


    def __init__(self, idIntervention, nomIntervention) -> None:
        self.idIntervention = idIntervention
        self.nomIntervention = nomIntervention

    def __repr__(self) -> str:
        return self.nomIntervention
