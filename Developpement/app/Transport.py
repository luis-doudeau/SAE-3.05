from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Transport(Base):
    __tablename__ = "TRANSPORT"
    idTransport = Column(Integer, primary_key = True)
    nomTransport = Column(Text)

    def __init__(self, idTransport, nomTransport) -> None:
        self.idTransport = idTransport
        self.nomTransport = nomTransport

    def __repr__(self) -> str:
        return "\""+str(self.idTransport) + "\"," + self.nomTransport # ne pas changé
        