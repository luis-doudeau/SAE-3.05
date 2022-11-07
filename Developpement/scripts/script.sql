-- CREATE DATABASE IF NOT EXISTS BDBOUM DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
-- USE BDBOUM;

drop table if exists INTERVENIR;
drop table if exists TRAVAILLER;
drop table if exists MOBILISER; 
drop table if exists DEPLACER;
drop table if exists LOGER;
drop table if exists TRANSPORTER;
drop table if exists AVOIR;
drop table if exists AUTEUR;
drop table if exists INVITE;
drop table if exists PRESSE;
drop table if exists MANGER;
drop table if exists STAFF;
drop table if exists INTERVENANT;
drop table if exists REPAS;
drop table if exists CONSOMMATEUR;
drop table if exists TRANSPORT;
drop table if exists REGIME;
drop table if exists EXPOSANT;
drop table if exists PARTICIPANT;
drop table if exists VOYAGE;
drop table if exists NAVETTE;
drop table if exists MAISON_EDITION;
drop table if exists LIEU;
drop table if exists HOTEL;
drop table if exists CRENEAU;
drop table if exists RESTAURANT;




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

CREATE TABLE HOTEL (
  idHotel int,
  nomHotel VARCHAR(42),
  adresseHotel VARCHAR(42),
  telHotel VARCHAR(42),
  mailHotel VARCHAR(42),
  capaciteHotel int,
  PRIMARY KEY (idHotel)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE MAISON_EDITION (
  idMe int,
  nomMe VARCHAR(42),
  numStand int,
  PRIMARY KEY (idMe)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE NAVETTE (
  idNavette int,
  nomNavette VARCHAR(42),
  capaciteNavette int,
  PRIMARY KEY (idNavette)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PARTICIPANT (
  idP int,
  prenomP VARCHAR(42),
  nomP VARCHAR(42),
  ddnP DATE,
  telP VARCHAR(42),
  emailP VARCHAR(42),
  mdpP VARCHAR(42),
  invite boolean,
  emailEnvoye boolean,
  remarques VARCHAR(300),
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
  dureeVoy time,
  directionGare boolean,
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
  idP int,
  numStand int,
  PRIMARY KEY (idP),
  FOREIGN KEY EXPOSANT(idP) REFERENCES PARTICIPANT(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE CONSOMMATEUR (
  idP int,
  PRIMARY KEY (idP),
  FOREIGN KEY(idP) REFERENCES PARTICIPANT(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE REPAS (
  idRepas int,
  estMidi boolean,
  idRest int,
  idCreneau int,
  PRIMARY KEY (idRepas),
  FOREIGN KEY(idRest) REFERENCES RESTAURANT(idRest),
  FOREIGN KEY(idCreneau) REFERENCES CRENEAU(idCreneau)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE INTERVENANT (
  idP int,
  dateArrive datetime,
  dateDepart datetime,
  PRIMARY KEY (idP),
  FOREIGN KEY (idP) REFERENCES CONSOMMATEUR(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TRANSPORT (
  idTransport int,
  nomTransport VARCHAR(42),
  PRIMARY KEY (idTransport)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE DEPLACER (
  idP int,
  idTransport int,
  lieuDepart VARCHAR(42),
  lieuArrive VARCHAR(42),
  PRIMARY KEY (idP, idTransport),
  FOREIGN KEY (idP) REFERENCES INTERVENANT(idP),
  FOREIGN KEY (idTransport) REFERENCES TRANSPORT(idTransport)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TRANSPORTER (
  idP int,
  idVoy int,
  PRIMARY KEY (idP, idVoy),
  FOREIGN KEY (idP) REFERENCES INTERVENANT(idP),
  FOREIGN KEY (idVoy) REFERENCES VOYAGE(idVoy)
);

CREATE TABLE LOGER(
  idP int,
  idHotel int,
  dateDeb datetime,
  dateFin datetime,
  PRIMARY KEY (idP, idHotel, dateDeb),
  FOREIGN KEY (idP) REFERENCES INTERVENANT(idP),
  FOREIGN KEY (idHotel) REFERENCES HOTEL(idHotel)
);

CREATE TABLE STAFF (
  idP int,
  PRIMARY KEY (idP),
  FOREIGN KEY (idP) REFERENCES CONSOMMATEUR(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE MANGER (
  idRepas int,
  idP int,
  PRIMARY KEY (idRepas, idP),
  FOREIGN KEY(idRepas) REFERENCES REPAS(idRepas),
  FOREIGN KEY(idP) REFERENCES CONSOMMATEUR(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PRESSE (
  idP int,
  PRIMARY KEY (idP),
  FOREIGN KEY(idP) REFERENCES INTERVENANT(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;


CREATE TABLE INVITE (
  idP int,
  PRIMARY KEY (idP),
  FOREIGN KEY(idP) REFERENCES INTERVENANT(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE AUTEUR (
  idP int,
  idMe int,
  PRIMARY KEY (idP),
  FOREIGN KEY (idP) REFERENCES INTERVENANT(idP),
  FOREIGN KEY (idMe) REFERENCES MAISON_EDITION(idMe)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE AVOIR (
  idP int,
  idregime int,
  PRIMARY KEY (idP, idregime),
  FOREIGN KEY(idP) REFERENCES CONSOMMATEUR(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TRAVAILLER (
  idCreneau int,
  idP int,
  PRIMARY KEY (idCreneau, idP),
  FOREIGN KEY (idCreneau) REFERENCES CRENEAU(idCreneau),
  FOREIGN KEY (idP) REFERENCES STAFF(idP)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE LIEU (
  idLieu int,
  nomLieu VARCHAR(50),
  PRIMARY KEY(idLieu)
)ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE INTERVENIR (
  idP int,
  idCreneau int,
  idLieu int,
  nomIntervention VARCHAR(50),
  descIntervention VARCHAR(500),
  PRIMARY KEY (idP, idCreneau),
  FOREIGN KEY(idP) REFERENCES AUTEUR(idP),
  FOREIGN KEY(idCreneau) REFERENCES CRENEAU(idCreneau),
  FOREIGN KEY(idLieu) REFERENCES LIEU(idLieu)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;







