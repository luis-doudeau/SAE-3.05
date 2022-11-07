from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Lieu(Base):
    __tablename__ = "LIEU"
    idLieu = Column(Integer, primary_key = True)
    nomLieu = Column(Text)

    def __init__(self, idLieu, nomLieu) -> None:
        self.idLieu = idLieu
        self.nomLieu = nomLieu

    def __repr__(self) -> str:
        return "ID lieu : " + str(self.idLieu) + ", nom du lieu : " + self.nomLieu
