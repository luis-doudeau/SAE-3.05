INSERT INTO PARTICIPANT (idP,prenomP, nomP,ddnP,telP,emailP,adresseP,mdpP,invite,emailEnvoye,remarques) VALUES
  (1,"Jordan","Latifah","2002-03-21","0867392610","in@protonmail.edu", "5461 Phasellus Street", "M1L13dP-2Wh9qN", false, false, "dolor dapibus gravida. Aliquam tincidunt,"),
  (2,"Caldwell","Delacruz","1970-12-09","0563395678","non.quam.pellentesque@icloud.couk", "P.O. Box 714, 970 Imperdiet Rd.", "I3X56xM-0Vs5tC", false, false,"ac risus. Morbi metus. Vivamus"),
  (3,"Oprah","Hill","1965-12-24","0861673417","facilisi.sed@icloud.com", "2976 Mauris Avenue", "I4M96jI-3Yo8iG", false, false,"egestas lacinia. Sed congue, elit"),
  (4,"Patrick","Gates","1974-12-12","0668301399","fringilla.purus.mauris@outlook.couk", "Ap #970-7190 Ultrices St.", "Q0W07vU-4Fg4yO", false, false,"fermentum risus, at fringilla purus"),
  (5,"Phelan","Fitzpatrick","1939-05-28","0335257324","auctor.vitae.aliquet@protonmail.ca", "Ap #753-3031 Lorem Rd.", "U1T38nY-4Qy4hX", false, false,"eget, dictum placerat, augue. Sed"),
  (100,"Zelda","Sykes","2003-12-18","0434772107","quam.elementum@icloud.ca", "9959 Euismod Ave", "C1M54dJ-4Iu8kI", false, false,"eu, eleifend nec, malesuada ut,"),
  (101,"Arsenio","Hewitt","1988-07-25","0783665556","ultrices.mauris@google.edu", "623-5236 Non St.", "W5F50dE-9Lc2dU", false, false,"nulla. Integer urna. Vivamus molestie"),
  (102,"Lamar","Tran","1943-10-10","0674873608","magna.a.tortor@yahoo.com", "643-2164 Sed Avenue", "L3F52yO-5Md5zH", false, false,"lorem, luctus ut, pellentesque eget,"),
  (200,"Sonya","Petersen","1942-02-25","0950147618","cras@aol.net", "Ap #353-5122 Neque. St.", "G0A15aX-6Jf1wI", false, false,"mattis. Cras eget nisi dictum"),
  (201,"Leilani","Hanson","2004-12-25","0761573559","dis.parturient@aol.org", "Ap #919-1437 Quis Ave", "V8H93dQ-4Lm7eC", false, false,"sociis natoque penatibus et magnis"),
  (202,"Aspen","Murray","1972-03-30","0757524228","morbi.non.sapien@aol.com", "550-8069 Ac Rd.", "Z6O13tU-6Kj7eM", false, false,"imperdiet nec, leo. Morbi neque"),
  (203,"Eric","Villarreal","1969-10-31","0305721353","bibendum.donec.felis@yahoo.couk", "7570 Id, Road", "X2E57mS-3Hp6pY", false, false,"Ut tincidunt vehicula risus. Nulla"),
  (300,"Gail","Valentine","1998-07-10","0647576667","ac@icloud.ca", "994-6410 Magnis Rd.", "J6R53sZ-7By3jO", false, false,"sociis natoque penatibus et magnis"),
  (301,"Plato","Lewis","1982-05-20","0246856015","eleifend.egestas@google.net", "P.O. Street 719, 970 Imperdiet.", "H5S66hD-5Sr8wE", false, false,"erat eget ipsum. Suspendisse sagittis."),
  (302,"Finn","Rowland","1982-11-28","0382746845","libero.donec.consectetuer@aol.edu", "5111 Nonummy. St.", "M6C75mN-2Zt8xX", false, false,"odio semper cursus. Integer mollis."),
  (303,"Dahlia","Barton","1977-08-28","0426439659","volutpat.nulla.dignissim@hotmail.ca", "214-9764 Arcu. Avenue", "S4G35cJ-3Rh9dG", false, false,"sagittis felis. Donec tempor, est"),
  (304,"Igor","Leach","1989-07-28","0710462294","enim@outlook.org", "169-6992 Ligula St.", "A6U48kF-8Dx3eE", false, false,"metus vitae velit egestas lacinia."),
  (400,"Malcolm","Stout","1979-05-01","0328243833","cubilia.curae.donec@outlook.com", "4203 Proin Avenue", "O2W64lW-9Bs2gA", false, false,"velit justo nec ante. Maecenas"),
  (401,"Rashad","Rivas","1943-10-20","0613357729","mauris.sit@protonmail.org", "4422 Ut, Avenue", "E9U74kP-5Il3mY", false, false,"faucibus leo, in lobortis tellus"),
  (500,"Gil","King","1994-07-04","0348483828","eget.metus@hotmail.couk", "895-5679 Faucibus St.", "Q8F62mP-2Cf2bY", false, false,"vitae, erat. Vivamus nisi. Mauris");


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
                                                                            (12, STR_TO_DATE("20-11-2022 20:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 22:00", "%d-%m-%Y %H:%i"));


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
                                                                (13,false,5,12),
                                                                (14,true,5,3),
                                                                (15,true,5,5),
                                                                (16,true,5,6),
                                                                (17,true,6,11),
                                                                (18,false,6,12),
                                                                (19,true,7,11),
                                                                (20,false,7,8);
                                                                
                
INSERT INTO MANGER(idP, idRepas) VALUES (100, 3),
                                        (101, 5),
                                        (102, 6),
                                        (200, 1);


INSERT INTO REGIME (idRegime,nomRegime) VALUES (1,"Végétarisme"),
                                                (2,"Pesco-végétarisme"),
                                                (3,"Flexitarisme"),
                                                (4,"Véganisme"),
                                                (5,"Sans gluten"),
                                                (6,"Sans lactose"),
                                                (7,"Cétogène");
                                                    
                                                                                                                     
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


INSERT INTO LOGER (idP, idHotel, dateDebut, dateFin) VALUES  (300, 1, STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"), STR_TO_DATE("19-11-2022 19:00", "%d-%m-%Y %H:%i")),
                                                             (500, 2, STR_TO_DATE("2022-11-18 16:30", "%Y-%m-%d %H:%i"), STR_TO_DATE("21-11-2022 10:30", "%d-%m-%Y %H:%i")),
                                                            (301, 2, STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i")),
                                                            (303, 3, STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 10:38", "%d-%m-%Y %H:%i"));



INSERT INTO ASSISTER(idP, dateArrive, dateDepart) VALUES  (300,STR_TO_DATE("2022-11-17 17:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i")),
                                                          (301,STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i")),
                                                          (302,STR_TO_DATE("2022-11-19 10:35", "%Y-%m-%d %H:%i"),STR_TO_DATE("19-11-2022 10:25", "%d-%m-%Y %H:%i")),
                                                          (303,STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 10:38", "%d-%m-%Y %H:%i")),
                                                          (304,STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("19-11-2022 10:00", "%d-%m-%Y %H:%i")),
                                                          (400,STR_TO_DATE("2022-11-20 11:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("19-11-2022 10:40", "%d-%m-%Y %H:%i")),
                                                          (401,STR_TO_DATE("2022-11-18 16:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 8:30", "%d-%m-%Y %H:%i")),
                                                          (500,STR_TO_DATE("2022-11-18 16:30", "%Y-%m-%d %H:%i"),STR_TO_DATE("21-11-2022 10:30", "%d-%m-%Y %H:%i"));


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
  (1,STR_TO_DATE("17-11-2022 11:51", "%d-%m-%Y %H:%i"), TIME("00:10"), true);


INSERT INTO NAVETTE (idNavette,nomNavette,capaciteNavette) VALUES (1,"Navette 1",2),
                                                                  (2,"Navette 2",2),
                                                                  (3,"Navette 3",8), 
                                                                  (4,"Navette 4",8),
                                                                  (5,"Navette 5",8),
                                                                  (6,"Navette 6",8);


INSERT INTO TRANSPORT (idTransport, nomTransport) values (1, "Avion"),
                                                          (2, "Train"),
                                                          (3, "Voiture"),
                                                          (4, "Covoiturage");


INSERT INTO DEPLACER VALUES (301, 2, "Paris Gare du Nord", "Gare Blois"),
                            (302, 2, "Gare de Tours", "Gare Blois"),
                            (303, 2, "Gare Orléans", "Gare Blois"),
                            (300, 2, "Aéroport Marseille Provence", "Aéroport d'Orly");


