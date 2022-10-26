from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Transporter(Base):
    __tablename__ = "TRANSPORTER"
    idIntervenant = Column(Integer, primary_key = True)
    idVoy = Column(Integer, primary_key = True)

    def __init__(self, idIntervenant, idVoy) -> None:
        self.idIntervenant = idIntervenant
        self.idVoy = idVoy

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idIntervenant) + ", id voyage : " + str(self.idVoy)
        