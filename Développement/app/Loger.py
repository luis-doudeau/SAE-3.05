from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Loger(Base):
    __tablename__ = "LOGER"
    idIntervenant = Column(Integer, primary_key = True)
    idHotel = Column(Integer, primary_key = True)

    def __init__(self, idIntervenant, idHotel) -> None:
        self.idIntervenant = idIntervenant
        self.idHotel = idHotel

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idIntervenant) + ", ID hotel : " + str(self.idHotel)
        