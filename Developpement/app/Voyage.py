from sqlalchemy import DATETIME, BOOLEAN, TIME
from sqlalchemy import Column , Integer, Text
from sqlalchemy . ext . declarative import declarative_base

Base = declarative_base()

class Voyage(Base):
    __tablename__ = "VOYAGE"
    idVoy = Column(Integer, primary_key = True)
    heureDebVoy = Column(DATETIME)
    DureeVoy = Column(TIME)
    directionGare = Column(BOOLEAN)
    idNavette = Column(Integer)

    def __init__(self, idVoy, heureDebVoy, DureeVoy, directionGare, idNavette) -> None:
        self.idVoy = idVoy
        self.heureDebVoy = heureDebVoy
        self.DureeVoy = DureeVoy
        self.directionGare = directionGare 
        self.idNavette = idNavette

    def __repr__(self) -> str:
        return "ID voyage : " + str(self.idVoy) + ", heure début : " + str(self.heureDebVoy) + ", durée : " + str(self.DureeVoy) + ", direction gare : " + str(self.directionGare) +" navette : "+str(self.idNavette)
        
    def to_dict(self):
        return {
            "idVoyage" : self.idVoy,
            "heureDeb" : self.heureDebVoy,
            "DureeVoy" : self.get_duree(),
            "depart" :self.get_direction_gare(),
            "idNavette" : self.idNavette

        }
    def get_direction_gare(self):
        if self.directionGare:
            return "Festival → Gare Blois"
        else:
            return "Gare Blois → Festival"
    def get_duree(self):
<<<<<<< HEAD
        nb_minutes = (self.DureeVoy.second % 3600) // 60
        nb_secondes = self.DureeVoy.second // 3600
        res = str(nb_minutes) +" minutes"
        if nb_secondes != 0:
            res += " "+str(nb_secondes) + " secondes"
        return res
=======
        nb_minutes = (self.DureeVoy.seconds % 3600) // 60
        nb_secondes = self.DureeVoy.seconds // 3600
        res = str(nb_minutes) +" minutes"
        if nb_secondes != 0:
            res += " "+str(nb_secondes) + " secondes"
        return res
>>>>>>> feuille_route
