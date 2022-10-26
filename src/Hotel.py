from sqlalchemy import Date
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Hotel(Base):
    __tablename__ = "HOTEL"
    idHotel = Column(Integer, primary_key = True)
    nomHotel = Column(Text)
    adresseHotel = Column(Text)
    telHotel = Column(Text)
    mailHotel = Column(Text)
    capaciteHotel = Column(Integer)

    def __init__(self, idHotel, nomHotel, adresseHotel, telHotel, mailHotel, capaciteHotel) -> None:
        self.idHotel = idHotel
        self.nomHotel = nomHotel
        self.adresseHotel = adresseHotel
        self.telHotel = telHotel
        self.mailHotel = mailHotel
        self.capaciteHotel = capaciteHotel

    def __repr__(self) -> str:
        return "ID Hotel : " + str(self.idHotel) + ", nom : " + str(self.nomHotel)+ ", adresse : " + str(self.adresseHotel)
        