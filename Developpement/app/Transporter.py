from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Transporter(Base):
    __tablename__ = "TRANSPORTER"
    idP = Column(Integer, primary_key = True)
    idVoy = Column(Integer, primary_key = True)

    def __init__(self, idP, idVoy) -> None:
        self.idP = idP
        self.idVoy = idVoy

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP) + ", id voyage : " + str(self.idVoy)
        