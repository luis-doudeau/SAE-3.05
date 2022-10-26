from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Presse(Base):
    __tablename__ = "PRESSE"
    idPresse = Column(Integer, primary_key = True)

    def __init__(self, idPresse) -> None:
        self.idPresse = idPresse

    def __repr__(self) -> str:
        return "ID presse : " + str(self.idPresse)
