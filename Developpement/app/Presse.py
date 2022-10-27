from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Presse(Base):
    __tablename__ = "PRESSE"
    idP = Column(Integer, primary_key = True)

    def __init__(self, idP) -> None:
        self.idP = idP

    def __repr__(self) -> str:
        return "ID presse : " + str(self.idP)
