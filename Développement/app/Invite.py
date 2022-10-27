from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Invite(Base):
    __tablename__ = "INVITE"
    idInvite = Column(Integer, primary_key = True)

    def __init__(self, idInvite) -> None:
        self.idInvite = idInvite

    def __repr__(self) -> str:
        return "ID invite : " + str(self.idInvite)
