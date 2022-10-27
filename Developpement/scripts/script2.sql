--CREATE DATABASE IF NOT EXISTS BDBOUM DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8_general_ci;
--USE BDBOUM;


drop table INTERVENIR;
drop table TRAVAILLER;
drop table MOBILISER;
drop table REPRESENTER;
drop table LOGER;
drop table TRANSPORTER;
drop table AVOIR;
drop table AUTEUR;
drop table INVITE;
drop table PRESSE;
drop table MANGER;
drop table STAFF;
drop table INTERVENANT;
drop table REPAS;
drop table CONSOMMATEUR;
drop table REGIME;
drop table EXPOSANT;
drop table PARTICIPANT;
drop table VOYAGE;
drop table NAVETTE;
drop table MAISON_EDITION;
drop table LIEU;
drop table HOTEL;
drop table CRENEAU;
drop table RESTAURANT;



CREATE TABLE PARTICIPANT (
  idP int,
  nomp VARCHAR(42),
  prenomp VARCHAR(42),
  ddnp DATETIME,
  telp VARCHAR(15),
  emailp VARCHAR(50),
  mdpp VARCHAR(42), -- lettre et chiffres générer aléatoirement
  remarques VARCHAR(300),
  moyenlocomotion VARCHAR(42),
  PRIMARY KEY (idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE EXPOSANT (
  idE int,
  numstand int,
  PRIMARY KEY (idE)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE CONSOMMATEUR (
  idConso int,
  PRIMARY KEY (idConso)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE RESTAURANT (
  idRest int,
  nomRest VARCHAR(42),
  PRIMARY KEY (idRest)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE CRENEAU (
  idCreneau int,
  dateHeureDebut DATETIME,
  dateHeureFin DATETIME,
  PRIMARY KEY (idCreneau)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE REPAS (
  idRepas int,
  estmidi boolean,
  idRest int,
  idCreneau int,
  PRIMARY KEY (idRepas)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE REGIME (
  idRegime int,
  nomRegime VARCHAR(42),
  PRIMARY KEY (idRegime)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE STAFF (
  idStaff int,
  PRIMARY KEY (idStaff)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE HOTEL (
  idHotel int,
  nomhotel VARCHAR(42),
  adressehotel VARCHAR(42),
  telhotel VARCHAR(15),
  mailhotel VARCHAR(42),
  capaciteHotel int,
  PRIMARY KEY (idHotel)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE INTERVENANT (
  idInter int,
  arrive DATETIME,
  depart DATETIME,
  PRIMARY KEY (idInter)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE MAISON_EDITION (
  idME int,
  nomME VARCHAR(42),
  numStand int,
  PRIMARY KEY (idME)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE AUTEUR (
  idAuteur int,
  PRIMARY KEY (idAuteur)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE PRESSE (
  idPresse int,
  PRIMARY KEY (idPresse)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE INVITE (
  idInvite int,
  PRIMARY KEY (idInvite)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE VOYAGE (
  idVoy int,
  heureDepart DATETIME,
  duree TIME,
  PRIMARY KEY (idVoy)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE NAVETTE (
  idNav int,
  nomNav VARCHAR(42),
  capaciteNav int,
  PRIMARY KEY (idNav)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE MOBILISER (
  idVoy int,
  idNav int,
  PRIMARY KEY (idVoy, idNav)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE TRANSPORTER (
  idVoy int,
  idInter int,
  PRIMARY KEY (idVoy, idInter)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE LIEU (
  idLieu int,
  nomLieu VARCHAR(42),
  PRIMARY KEY (idLieu)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE AVOIR (
  idConso int,
  idRegime int,
  PRIMARY KEY (idConso, idRegime)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE LOGER (
  idInter int,
  idHotel int,
  dateDebut DATE,
  dateFin DATE,
  PRIMARY KEY (idInter, idHotel, dateDebut)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE REPRESENTER (
  idME int,
  idAuteur int,
  PRIMARY KEY (idME, idAuteur)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE INTERVENIR (
  idAuteur int,
  idCreneau int,
  idLieu int,
  nomIntervention VARCHAR(42),
  descriptionIntervention VARCHAR(300),
  PRIMARY KEY (idAuteur, idCreneau)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE MANGER (
  idRepas int,
  idConso int,
  PRIMARY KEY (idRepas, idConso)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE TRAVAILLER (
  idCreneau int,
  idStaff int,
  PRIMARY KEY (idCreneau, idStaff)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;



ALTER TABLE REPAS ADD FOREIGN KEY (idCreneau) REFERENCES CRENEAU (idCreneau);
ALTER TABLE REPAS ADD FOREIGN KEY (idRest) REFERENCES RESTAURANT (idRest);
ALTER TABLE AUTEUR ADD FOREIGN KEY (idAuteur) REFERENCES INTERVENANT (idInter);
ALTER TABLE PRESSE ADD FOREIGN KEY (idPresse) REFERENCES INTERVENANT (idInter);
ALTER TABLE INVITE ADD FOREIGN KEY (idInvite) REFERENCES INTERVENANT (idInter);
ALTER TABLE AVOIR ADD FOREIGN KEY (idRegime) REFERENCES REGIME (idRegime);
ALTER TABLE AVOIR ADD FOREIGN KEY (idConso) REFERENCES CONSOMMATEUR (idConso);
ALTER TABLE CONSOMMATEUR ADD FOREIGN KEY (idConso) REFERENCES PARTICIPANT(idP);
ALTER TABLE INTERVENIR ADD FOREIGN KEY (idCreneau) REFERENCES CRENEAU (idCreneau);
ALTER TABLE INTERVENIR ADD FOREIGN KEY (idAuteur) REFERENCES AUTEUR (idAuteur);
ALTER TABLE INTERVENIR ADD FOREIGN KEY (idLieu) REFERENCES INTERVENTION (idLieu);
ALTER TABLE EXPOSANT ADD FOREIGN KEY (idE) REFERENCES PARTICIPANT (idP);
ALTER TABLE TRANSPORTER ADD FOREIGN KEY (idVoy) REFERENCES VOYAGE (idVoy);
ALTER TABLE TRANSPORTER ADD FOREIGN KEY (idInter) REFERENCES INTERVENANT (idInter);
ALTER TABLE REPRESENTER ADD FOREIGN KEY (idAuteur) REFERENCES AUTEUR (idAuteur);
ALTER TABLE REPRESENTER ADD FOREIGN KEY (idME) REFERENCES MAISON_EDITION (idME);
ALTER TABLE INTERVENANT ADD FOREIGN KEY (idInter) REFERENCES CONSOMMATEUR (idConso);
ALTER TABLE LOGER ADD FOREIGN KEY (idInter) REFERENCES INTERVENANT (idInter);
ALTER TABLE LOGER ADD FOREIGN KEY (idHotel) REFERENCES HOTEL (idHotel);
ALTER TABLE MANGER ADD FOREIGN KEY (idrepas) REFERENCES REPAS (idrepas);
ALTER TABLE MANGER ADD FOREIGN KEY (idConso) REFERENCES CONSOMMATEUR (idConso);
ALTER TABLE REPAS ADD FOREIGN KEY (idRest) REFERENCES RESTAURANT (idRest);
ALTER TABLE REPAS ADD FOREIGN KEY (idCreneau) REFERENCES CRENEAU (idCreneau);
ALTER TABLE STAFF ADD FOREIGN KEY (idStaff) REFERENCES CONSOMMATEUR (idConso);
ALTER TABLE TRAVAILLER ADD FOREIGN KEY (idStaff) REFERENCES STAFF (idStaff);
ALTER TABLE TRAVAILLER ADD FOREIGN KEY (idCreneau) REFERENCES CRENEAU (idCreneau);
ALTER TABLE MOBILISER ADD FOREIGN KEY (idNav) REFERENCES NAVETTE (idNav);
ALTER TABLE MOBILISER ADD FOREIGN KEY (idVoy) REFERENCES VOYAGE (idVoy);
