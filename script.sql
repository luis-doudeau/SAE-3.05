-- CREATE DATABASE IF NOT EXISTS BDBOUM DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8_general_ci;
-- USE BDBOUM;

drop table INTERVENIR;
drop table TRAVAILLER;
drop table AVOIR;
drop table AUTEUR;
drop table INVITE;
drop table PRESSE;
drop table MANGER;
drop table STAFF;
drop table LOGER;
drop table TRANSPORTER;
drop table INTERVENANT;
drop table REPAS;
drop table CONSOMMATEUR;
drop table REGIME;
drop table EXPOSANT;
drop table MOBILISER;
drop table PERSONNE;
drop table VOYAGE;
drop table NAVETTE;
drop table MAISON_EDITION;
drop table INTERVENTION;
drop table HOTEL;
drop table CRENEAU_REPAS;
drop table CRENEAU;
drop table RESTAURANT;


CREATE TABLE RESTAURANT (
  idRest int,
  nomRest VARCHAR(42),
  PRIMARY KEY (idRest)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE CRENEAU (
  idCreneau int,
  dateDebut datetime,
  dateFin datetime,
  PRIMARY KEY (idCreneau)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE CRENEAU_REPAS (
  idCreneauRepas int,
  dateDeb datetime,
  dateFin datetime,
  PRIMARY KEY (idCreneauRepas)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE HOTEL (
  idHotel int,
  nomHotel VARCHAR(42),
  adresseHotel VARCHAR(42),
  telHotel VARCHAR(42),
  mailHotel VARCHAR(42),
  capaciteHotel int,
  PRIMARY KEY (idHotel)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE INTERVENTION (
  idInter int,
  nomInter VARCHAR(42),
  PRIMARY KEY (idInter)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE MAISON_EDITION (
  idMe int,
  nomMe VARCHAR(42),
  numStand int,
  PRIMARY KEY (idMe)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE NAVETTE (
  idNavette int,
  capaciteNavette int(42),
  PRIMARY KEY (idNavette)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PERSONNE (
  idP int,
  nomP VARCHAR(42),
  prenomP VARCHAR(42),
  ddnP VARCHAR(42),
  telP VARCHAR(42),
  emailP VARCHAR(42),
  mdpP VARCHAR(42),
  remarques VARCHAR(42),
  moyenLocomotion VARCHAR(42),
  PRIMARY KEY (idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE REGIME (
  idRegime int,
  nomRegime VARCHAR(42),
  PRIMARY KEY (idRegime)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE VOYAGE (
  idVoy int,
  heureDebVoy datetime,
  DureeVoy datetime,
  PRIMARY KEY (idVoy)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE MOBILISER(
  idVoy int,
  idNavette int,
  PRIMARY KEY (idVoy, idNavette),
  FOREIGN KEY (idVoy) REFERENCES VOYAGE(idVoy),
  FOREIGN KEY (idNavette) REFERENCES NAVETTE(idNavette)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE EXPOSANT (
  idE int,
  numStand int,
  PRIMARY KEY (idE),
  FOREIGN KEY EXPOSANT(idE) REFERENCES PERSONNE(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE CONSOMMATEUR (
  idC int,
  PRIMARY KEY (idC),
  FOREIGN KEY(idC) REFERENCES PERSONNE(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE REPAS (
  idRepas int,
  estMidi boolean,
  idRest int,
  idCreneauRepas int,
  PRIMARY KEY (idRepas),
  FOREIGN KEY(idRest) REFERENCES RESTAURANT(idRest),
  FOREIGN KEY(idCreneauRepas) REFERENCES CRENEAU_REPAS(idCreneauRepas)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE INTERVENANT (
  idIntervenant int,
  dateArrive datetime,
  dateDepart datetime,
  transport VARCHAR(42),
  intervention VARCHAR(42),
  PRIMARY KEY (idIntervenant),
  FOREIGN KEY (idIntervenant) REFERENCES CONSOMMATEUR(idC)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TRANSPORTER (
  idIntervenant int,
  idVoy int,
  PRIMARY KEY (idIntervenant, idVoy),
  FOREIGN KEY (idIntervenant) REFERENCES INTERVENANT(idIntervenant),
  FOREIGN KEY (idVoy) REFERENCES VOYAGE(idVoy)
);

CREATE TABLE LOGER(
  idIntervenant int,
  idHotel int,
  PRIMARY KEY (idIntervenant, idHotel),
  FOREIGN KEY (idIntervenant) REFERENCES INTERVENANT(idIntervenant),
  FOREIGN KEY (idHotel) REFERENCES HOTEL(idHotel)

);

CREATE TABLE STAFF (
  idS int,
  PRIMARY KEY (idS),
  FOREIGN KEY (idS) REFERENCES CONSOMMATEUR(idC)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE MANGER (
  idRepas int,
  idC int,
  PRIMARY KEY (idRepas, idC),
  FOREIGN KEY(idRepas) REFERENCES REPAS(idRepas),
  FOREIGN KEY(idC) REFERENCES CONSOMMATEUR(idC)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PRESSE (
  idPresse int,
  PRIMARY KEY (idPresse),
  FOREIGN KEY(idPresse) REFERENCES INTERVENANT(idIntervenant)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE INVITE (
  idInvite int,
  PRIMARY KEY (idInvite),
  FOREIGN KEY(idInvite) REFERENCES INTERVENANT(idIntervenant)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE AUTEUR (
  ida int,
  idme int,
  PRIMARY KEY (ida),
  FOREIGN KEY (ida) REFERENCES INTERVENANT(idIntervenant),
  FOREIGN KEY (idme) REFERENCES MAISON_EDITION(idme)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE AVOIR (
  idC int,
  idregime int,
  PRIMARY KEY (idC, idregime),
  FOREIGN KEY(idC) REFERENCES CONSOMMATEUR(idC)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TRAVAILLER (
  idCreneau int,
  idS int,
  PRIMARY KEY (idCreneau, idS),
  FOREIGN KEY (idCreneau) REFERENCES CRENEAU(idCreneau),
  FOREIGN KEY (idS) REFERENCES STAFF(idS)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE INTERVENIR (
  idA int,
  idCreneau int,
  idInter int,
  PRIMARY KEY (idA, idCreneau),
  FOREIGN KEY(idA) REFERENCES AUTEUR(idA),
  FOREIGN KEY(idCreneau) REFERENCES CRENEAU(idCreneau),
  FOREIGN KEY(idInter) REFERENCES INTERVENTION(idInter)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;







