from sqlalchemy import DATE
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Participant(Base):
    __tablename__ = "PARTICIPANT"
    idP = Column(Integer, primary_key = True)
    nomP = Column(Text)
    prenomP = Column(Text)
    ddnP = Column(DATE)
    telP = Column(Text)
    emailP = Column(Text)
    mdpP = Column(Text)
    remarques = Column(Text)
    moyenLocomotion = Column(Text)

    def __init__(self, idP, nomP, prenomP, ddnP, telP, emailP, mdpP, remarques, moyenLocomotion) -> None:
        self.idP = idP
        self.nomP = nomP
        self.prenomP = prenomP
        self.ddnP = ddnP
        self.telP = telP
        self.emailP = emailP
        self.mdpP = mdpP
        self.remarques = remarques
        self.moyenLocomotion = moyenLocomotion

    def __repr__(self) -> str:
        return self.nomP + " " + self.prenomP + ", id : " + str(self.idP)