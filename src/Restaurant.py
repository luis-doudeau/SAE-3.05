from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = "RESTAURANT"
    idRest = Column(Integer, primary_key = True)
    nomRest = Column(Text)

    def __init__(self, idRest, nomRest) -> None:
        self.idRest = idRest
        self.nomRest = nomRest

    def __repr__(self) -> str:
        return "ID restaurant : " + str(self.idRest) + ", nom restaurant : " + str(self.nomRest)
        