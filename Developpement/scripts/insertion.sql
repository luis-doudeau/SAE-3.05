INSERT INTO UTILISATEUR (idP,prenomP, nomP,emailP,mdpP) VALUES
  (1,"Jordan","Latifah","in@protonmail.edu", "M1L13dP-2Wh9qN"),
  (2,"Caldwell","Delacruz","non.quam.pellentesque@icloud.couk", "I3X56xM-0Vs5tC"),
  (3,"Oprah","Hill","facilisi.sed@icloud.com", "I4M96jI-3Yo8iG"),
  (4,"Patrick","Gates","fringilla.purus.mauris@outlook.couk", "Q0W07vU-4Fg4yO"),
  (5,"Phelan","Fitzpatrick","auctor.vitae.aliquet@protonmail.ca", "U1T38nY-4Qy4hX"),
  (100,"Zelda","Sykes","quam.elementum@icloud.ca",  "C1M54dJ-4Iu8kI"),
  (101,"Arsenio","Hewitt","ultrices.mauris@google.edu", "W5F50dE-9Lc2dU"),
  (102,"Lamar","Tran","magna.a.tortor@yahoo.com", "L3F52yO-5Md5zH"),
  (200,"Sonya","Petersen","cras@aol.net", "G0A15aX-6Jf1wI"),
  (201,"Leilani","Hanson","dis.parturient@aol.org", "V8H93dQ-4Lm7eC"),
  (202,"Aspen","Murray","morbi.non.sapien@aol.com", "Z6O13tU-6Kj7eM"),
  (203,"Eric","Villarreal","bibendum.donec.felis@yahoo.couk", "X2E57mS-3Hp6pY"),
  (300,"Gail","Valentine","ac@icloud.ca", "J6R53sZ-7By3jO"),
  (301,"Plato","Lewis","eleifend.egestas@google.net", "H5S66hD-5Sr8wE"),
  (302,"Finn","Rowland","libero.donec.consectetuer@aol.edu", "M6C75mN-2Zt8xX"),
  (303,"Dahlia","Barton","volutpat.nulla.dignissim@hotmail.ca", "S4G35cJ-3Rh9dG"),
  (304,"Igor","Leach","enim@outlook.org", "A6U48kF-8Dx3eE"),
  (400,"Malcolm","Stout","cubilia.curae.donec@outlook.com", "O2W64lW-9Bs2gA"),
  (401,"Rashad","Rivas","mauris.sit@protonmail.org", "E9U74kP-5Il3mY"),
  (500,"Gil","King","eget.metus@hotmail.couk", "Q8F62mP-2Cf2bY"),
  (1000,"Lenina","Dadina", "lenina@gmail.com","mdp");


INSERT INTO PARTICIPANT (idP,ddnP,telP,adresseP,invite,emailEnvoye,remarques) VALUES
  (1,"2002-03-21","0867392610", "5461 Phasellus Street", false, false, "dolor dapibus gravida. Aliquam tincidunt"),
  (2,"1970-12-09","0563395678","P.O. Box 714, 970 Imperdiet Rd.",  false, false,"ac risus. Morbi metus. Vivamus"),
  (3,"1965-12-24","0861673417","2976 Mauris Avenue", false, false,"egestas lacinia. Sed congue, elit"),
  (4,"1974-12-12","0668301399","Ap #970-7190 Ultrices St.", false, false,"fermentum risus, at fringilla purus"),
  (5,"1939-05-28","0335257324","Ap #753-3031 Lorem Rd.", false, false,"eget, dictum placerat, augue. Sed"),
  (100,"2003-12-18","0434772107","9959 Euismod Ave", false, false,"eu, eleifend nec, malesuada ut,"),
  (101,"1988-07-25","0783665556","623-5236 Non St.", false, false,"nulla. Integer urna. Vivamus molestie"),
  (102,"1943-10-10","0674873608","643-2164 Sed Avenue", false, false,"lorem, luctus ut, pellentesque eget,"),
  (200,"1942-02-25","0950147618","Ap #353-5122 Neque. St.", false, false,"mattis. Cras eget nisi dictum"),
  (201,"2004-12-25","0761573559","Ap #919-1437 Quis Ave", false, false,"sociis natoque penatibus et magnis"),
  (202,"1972-03-30","0757524228","550-8069 Ac Rd.", false, false,"imperdiet nec, leo. Morbi neque"),
  (203,"1969-10-31","0305721353","7570 Id, Road", false, false,"Ut tincidunt vehicula risus. Nulla"),
  (300,"1998-07-10","0647576667","994-6410 Magnis Rd.", false, false,"sociis natoque penatibus et magnis"),
  (301,"1982-05-20","0246856015","P.O. Street 719, 970 Imperdiet.", false, false,"erat eget ipsum. Suspendisse sagittis."),
  (302,"1982-11-28","0382746845", "5111 Nonummy. St.", false, false,"odio semper cursus. Integer mollis."),
  (303,"1977-08-28","0426439659", "214-9764 Arcu. Avenue", false, false,"sagittis felis. Donec tempor, est"),
  (304,"1989-07-28","0710462294", "169-6992 Ligula St.", false, false,"metus vitae velit egestas lacinia."),
  (400,"1979-05-01","0328243833", "4203 Proin Avenue", false, false,"velit justo nec ante. Maecenas"),
  (401,"1943-10-20","0613357729", "4422 Ut, Avenue", false, false,"faucibus leo, in lobortis tellus"),
  (500,"1994-07-04","0348483828", "895-5679 Faucibus St.", false, false,"vitae, erat. Vivamus nisi. Mauris");


INSERT INTO EXPOSANT (idP,numStand) VALUES  (1,5),
                                            (2,7),
                                            (3,10),
                                            (4,16),
                                            (5,18);


INSERT INTO CONSOMMATEUR (idP) VALUES   (100),
                                        (101),
                                        (102),
                                        (200),
                                        (201),
                                        (202),
                                        (203),
                                        (300),
                                        (301),
                                        (302),
                                        (303),
                                        (304),
                                        (400),
                                        (401),
                                        (500);


INSERT INTO RESTAURANT (idRest,nomRest) VALUES (1,"Erat Eget Tincidunt Incorporated"),
                                                (2,"A Facilisis Institute"),
                                                (3,"Donec Est Mauris LLP"),
                                                (4,"Cursus Inc."),
                                                (5,"Eget Volutpat Associates"),
                                                (6,"Lacus Vestibulum Lorem Institute"),
                                                (7,"Erat Eget Tincidunt Associates");


INSERT INTO CRENEAU (idCreneau,dateDebut,dateFin) VALUES (1, STR_TO_DATE("17-11-2022 21:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("17-11-2022 22:00", "%d-%m-%Y %H:%i")),
                                                                            (2, STR_TO_DATE("18-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (3, STR_TO_DATE("18-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (4, STR_TO_DATE("18-11-2022 09:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 11:00", "%d-%m-%Y %H:%i")),
                                                                            (5, STR_TO_DATE("19-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (6, STR_TO_DATE("19-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (7, STR_TO_DATE("19-11-2022 14:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 15:30", "%d-%m-%Y %H:%i")),
                                                                            (8, STR_TO_DATE("19-11-2022 20:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 22:00", "%d-%m-%Y %H:%i")),
                                                                            (9, STR_TO_DATE("20-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (10, STR_TO_DATE("20-11-2022 09:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 10:30", "%d-%m-%Y %H:%i")),
                                                                            (11, STR_TO_DATE("20-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 12:31", "%d-%m-%Y %H:%i")),
                                                                            (12, STR_TO_DATE("20-11-2022 08:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 22:00", "%d-%m-%Y %H:%i"));


INSERT INTO REPAS (idRepas,estMidi,idRest,idCreneau) VALUES   (1,true,1,2),
                                                                (2,true,1,3),
                                                                (3,true,1,5),
                                                                (4,false,2,1),
                                                                (5,true,2,6),
                                                                (6,false,2,8),
                                                                (7,true,3,2),
                                                                (8,false,3,8),
                                                                (9,true,3,5),
                                                                (10,true,4,6),
                                                                (11,true,4,9),
                                                                (12,false,4,8),
                                                                (13,false,5,8),
                                                                (14,true,5,3),
                                                                (15,true,5,5),
                                                                (16,true,5,6),
                                                                (17,true,6,11),
                                                                (18,false,6,8),
                                                                (19,true,7,11),
                                                                (20,false,7,8);


INSERT INTO REGIME (idRegime,nomRegime) VALUES (1,"Végétarisme"),
                                                (2,"Pesco-végétarisme"),
                                                (3,"Flexitarisme"),
                                                (4,"Véganisme"),
                                                (5,"Sans gluten"),
                                                (6,"Sans lactose"),
                                                (7,"Cétogène");
                                            
INSERT INTO AVOIR (idP, idRegime) VALUES (100, 1),
                                         (100, 2),
                                         (100, 3),
                                         (102, 5);
                                                    
                                                                                                                     
INSERT INTO STAFF (idP) VALUES (200),
                                (201),
                                (202),
                                (203);


INSERT INTO HOTEL (idHotel,nomHotel,adresseHotel,telHotel,mailHotel,capaciteHotel) VALUES (1,"Ibis","3722 Nisl. Road","07 69 24 88 55","lorem@yahoo.org",128),
                                                                                          (2,"Abba","Ap #258-5002 Eget, St.","06 21 59 29 48","ornare.libero@yahoo.com",55),
                                                                                          (3,"Airotel","693-6863 Ornare Avenue","03 90 57 11 32","curae.phasellus@google.net",64),
                                                                                          (4,"B&B Hotels","440-9129 Rutrum, St.","03 55 26 65 06","feugiat.tellus.lorem@aol.com",127),
                                                                                          (5,"Confort Hotel","P.O. Box 105, 5613 Lacinia Avenue","01 22 50 41 25","mus.aenean@yahoo.couk",181),
                                                                                          (6,"Hitlon","Ap #107-2870 Proin Rd.","04 22 68 85 27","nullam.scelerisque.neque@icloud.edu",87),
                                                                                          (7,"Novotel","Ap #448-6699 Arcu Street","03 88 57 81 57","turpis.egestas.aliquam@outlook.net",153);


INSERT INTO INTERVENANT (idP) VALUES  (300),
                                      (301),
                                      (302),
                                      (303),
                                      (304),
                                      (400),
                                      (401),
                                      (500);


INSERT INTO LOGER (idP, dateDebut, dateFin, idHotel) VALUES  (300, STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"), STR_TO_DATE("19-11-2022 19:00", "%d-%m-%Y %H:%i"), 1),
                                                             (500, STR_TO_DATE("2022-11-18 16:30", "%Y-%m-%d %H:%i"), STR_TO_DATE("21-11-2022 10:30", "%d-%m-%Y %H:%i"), 2),
                                                            (301, STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i"), 2),
                                                            (303, STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 10:38", "%d-%m-%Y %H:%i"), 3);


INSERT INTO MAISON_EDITION (idME, nomME, numStand) values (1, "Dargaud", 4),
                                                          (2, "Dupuis", 5),
                                                          (3, "Glénat", 8),
                                                          (4, "Delcourt", 9),
                                                          (5, "Grand Angle", 10),
                                                          (6, "Soleil", 17),
                                                          (7, "Casterman", 18),
                                                          (8, "Drakoo", 21),
                                                          (9, "Petit à petit", 26);


INSERT INTO AUTEUR (idP, idMe) values (300, 1),
                                      (301, 1),
                                      (302, 2),
                                      (303, 3),
                                      (304, 4);


INSERT INTO PRESSE (idP) values (400),
                                (401);


INSERT INTO INVITE (idP) values (500);


INSERT INTO VOYAGE (idVoy,heureDebVoy, dureeVoy, directionGare) VALUES
  (1,STR_TO_DATE("17-11-2022 11:51", "%d-%m-%Y %H:%i"), TIME("00:10"), true),
  (2,STR_TO_DATE("17-11-2022 13:51", "%d-%m-%Y %H:%i"), TIME("00:10"), false),
  (3,STR_TO_DATE("18-11-2022 15:51", "%d-%m-%Y %H:%i"), TIME("00:10"), true);

INSERT INTO TRANSPORTER(idP, idVoy) VALUES (300, 1),
                                           (300, 2),
                                           (301, 1),
                                           (301, 3);


INSERT INTO NAVETTE (idNavette,nomNavette,capaciteNavette) VALUES (1,"Navette 1",2),
                                                                  (2,"Navette 2",2),
                                                                  (3,"Navette 3",8), 
                                                                  (4,"Navette 4",8),
                                                                  (5,"Navette 5",8),
                                                                  (6,"Navette 6",8);
                                                            
INSERT INTO MOBILISER(idVoy, idNavette) VALUES (1, 1),
                                              (1, 2),
                                              (2, 1);


INSERT INTO TRANSPORT (idTransport, nomTransport) values (1, "Avion"),
                                                          (2, "Train"),
                                                          (3, "Voiture"),
                                                          (4, "Covoiturage");


INSERT INTO DEPLACER (idP, idTransport, lieuDepart, lieuArrive, annee) values (301, 2, "Paris Gare du Nord", "Gare Blois", 2015),
                                                                      (301, 2, "Gare de Tours", "Gare Blois",2019),
                                                                      (303, 2, "Gare Orléans", "Gare Blois", 2022),
                                                                      (300, 2, "Aéroport Marseille Provence", "Aéroport d'Orly", 2022);



INSERT INTO ASSISTER(idP, dateArrive, dateDepart) VALUES  (300,STR_TO_DATE("2022-11-17 17:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i")),
                                                          (301,STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i")),
                                                          (302,STR_TO_DATE("2022-11-19 10:35", "%Y-%m-%d %H:%i"),STR_TO_DATE("19-11-2022 10:25", "%d-%m-%Y %H:%i")),
                                                          (303,STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 10:38", "%d-%m-%Y %H:%i")),
                                                          (304,STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("19-11-2022 10:00", "%d-%m-%Y %H:%i")),
                                                          (400,STR_TO_DATE("2022-11-20 11:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("19-11-2022 10:40", "%d-%m-%Y %H:%i")),
                                                          (401,STR_TO_DATE("2022-11-18 16:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 8:30", "%d-%m-%Y %H:%i")),
                                                          (500,STR_TO_DATE("2022-11-18 16:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 10:30", "%d-%m-%Y %H:%i"));


INSERT INTO SECRETAIRE (idP) VALUES (1000);


INSERT INTO MANGER(idP, idRepas) VALUES (100, 3),
                                        (101, 5),
                                        (102, 6),
                                        (102, 18),
                                        (200, 5);



INSERT INTO INTERVENTION(idIntervention, nomIntervention) VALUES (1, "Conférence de presse"),
                                                                (2, "Dédicace"),
                                                                (3, "Atelier dessin"),
                                                                (4, "Présentation"),
                                                                (5, "Autre");


INSERT INTO LIEU(idLieu, nomLieu) VALUES (1,"Hall 1"),
                                        (2, "Hall 2"),
                                        (3, "Hall 3"),
                                        (4, "Hall 4"),
                                        (5, "Hall 5");