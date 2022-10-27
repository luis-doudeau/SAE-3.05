from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervention(Base):
    __tablename__ = "INTERVENTION"
    idInter = Column(Integer, primary_key = True)
    nomInter = Column(Text)

    def __init__(self, idInter, nomInter) -> None:
        self.idInter = idInter
        self.nomInter = nomInter

    def __repr__(self) -> str:
        return "ID intervention : " + str(self.idInter) + ", nom : " + self.nomInter
        