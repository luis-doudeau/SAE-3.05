from sqlalchemy import Column , Integer, TEXT, DATETIME
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Deplacer(Base):
    __tablename__ = "DEPLACER"
    idP = Column(Integer, primary_key = True)
    idTransport = Column(Integer, primary_key = True)
    lieuDepart = Column(TEXT, primary_key = True)
    lieuArrive = Column(TEXT,  primary_key = True)
    annee = Column(Integer, primary_key = True)


    def __init__(self, idP, idTransport, lieuDepart, lieuArrive, annee) -> None:
        self.idP = idP
        self.idTransport = idTransport
        self.lieuDepart = lieuDepart
        self.lieuArrive = lieuArrive
        self.annee = annee

    def __repr__(self) -> str:
        return str(self.idP) + ","+str(self.idTransport)+ ",\"" + self.lieuDepart + "\",\"" + self.lieuArrive+"\"" # ne pas changé
        