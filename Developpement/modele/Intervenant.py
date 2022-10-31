from sqlalchemy import DATETIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Intervenant(Base):
    __tablename__ = "INTERVENANT"
    idP = Column(Integer, primary_key = True)
    dateArrive = Column(DATETIME)
    dateDepart = Column(DATETIME)

    def __init__(self, idP, dateArrive, dateDepart) -> None:
        self.idP = idP
        self.dateArrive = dateArrive
        self.dateDepart = dateDepart

    def __repr__(self) -> str:
        return "ID intervenant : " + str(self.idP) + ", arrive le " + str(self.dateArrive) + ", part le : " + str(self.dateDepart)
