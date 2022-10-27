insert into PARTICIPANT values  ("Madison", "Michael",STR_TO_DATE(1, "1962-47-13", '%Y-%m-%d'),"05 51 77 77 22","at.nisi.cum@icloud.ca"),
                                ("Desirae Kent",STR_TO_DATE(2, "1933-18-23", '%Y-%m-%d'),"09 47 69 99 06","vivamus.nibh@protonmail.net"),
                                ("Tashya Hopkins",STR_TO_DATE(3, "1961-11-29", '%Y-%m-%d'),"03 98 52 93 29","eu.tempor@google.net"),
                                ("Sebastian Meadows",STR_TO_DATE(4, "1966-22-10", '%Y-%m-%d'),"04 99 79 35 12","tempor@google.org"),
                                ("Rudyard Blevins",STR_TO_DATE(5, "1974-58-20", '%Y-%m-%d'),"02 62 25 13 41","etiam.ligula@outlook.ca");


INSERT INTO EXPOSANT (idE,numstand) VALUES  (1,1),
                                            (2,2),
                                            (3,3),
                                            (4,4),
                                            (5,5);

INSERT INTO CONSOMMATEUR (idE) VALUES   (100),
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


INSERT INTO RESTAURANT (idE,nomRest) VALUES (1,"Erat Eget Tincidunt Incorporated"),
                                                (2,"A Facilisis Institute"),
                                                (3,"Donec Est Mauris LLP"),
                                                (4,"Cursus Inc."),
                                                (5,"Eget Volutpat Associates"),
                                                (6,"Lacus Vestibulum Lorem Institute"),
                                                (7,"Erat Eget Tincidunt Associates");


INSERT INTO CRENEAU (idCreneau,dateHeureDebut,dateHeureFin) VALUES (1, STR_TO_DATE("17-11-2022 20:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("17-11-2022 22:00", "%d-%m-%Y %H:%i")),
                                                                            (2, STR_TO_DATE("18-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (3, STR_TO_DATE("18-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (4, STR_TO_DATE("18-11-2022 09:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 11:00", "%d-%m-%Y %H:%i")),
                                                                            (5, STR_TO_DATE("19-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (6, STR_TO_DATE("19-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (7, STR_TO_DATE("19-11-2022 14:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 15:30", "%d-%m-%Y %H:%i")),
                                                                            (8, STR_TO_DATE("19-11-2022 20:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 22:00", "%d-%m-%Y %H:%i")),
                                                                            (9, STR_TO_DATE("20-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 11:30", "%d-%m-%Y %H:%i")),
                                                                            (10, STR_TO_DATE("20-11-2022 09:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 10:30", "%d-%m-%Y %H:%i")),
                                                                            (11, STR_TO_DATE("20-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (12, STR_TO_DATE("20-11-2022 20:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 22:00", "%d-%m-%Y %H:%i"));

INSERT INTO REPAS (idRepas,estmidi,idRest,idCreneau) VALUES   (1,true,1,2),
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
                
INSERT INTO REGIME (idRegime,nomRegime) VALUES (1,"Végétarisme"),
                                                    (2,"Pesco-végétarisme"),
                                                    (3,"Flexitarisme"),
                                                    (4,"Véganisme"),
                                                    (5,"Sans gluten"),
                                                    (6,"Sans lactose"),
                                                    (7,"Cétogène");
                                                    
                                                                                                                     
INSERT INTO STAFF (idStaff) VALUES (200),
                                    (201),
                                    (202),
                                    (203);

INSERT INTO HOTEL (idHotel,nomhotel,adressehotel,telhotel,mailhotel,capaciteHotel) VALUES (1,"Ibis","3722 Nisl. Road","07 69 24 88 55","lorem@yahoo.org",128),
                                                                                            (2,"Abba","Ap #258-5002 Eget, St.","06 21 59 29 48","ornare.libero@yahoo.com",55),
                                                                                            (3,"Airotel","693-6863 Ornare Avenue","03 90 57 11 32","curae.phasellus@google.net",64),
                                                                                            (4,"B&B Hotels","440-9129 Rutrum, St.","03 55 26 65 06","feugiat.tellus.lorem@aol.com",127),
                                                                                            (5,"Confort Hotel","P.O. Box 105, 5613 Lacinia Avenue","01 22 50 41 25","mus.aenean@yahoo.couk",181),
                                                                                            (6,"Hitlon","Ap #107-2870 Proin Rd.","04 22 68 85 27","nullam.scelerisque.neque@icloud.edu",87),
                                                                                            (7,"Novotel","Ap #448-6699 Arcu Street","03 88 57 81 57","turpis.egestas.aliquam@outlook.net",153);


INSERT INTO `INTERVENANT` (`idInter`,`arrive`,`depart`) VALUES (300,STR_TO_DATE("19-11-2022 10:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("19-11-2022 19:00", "%d-%m-%Y %H:%i")),
                                                                (301,STR_TO_DATE("19-11-2022 09:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("20-11-2022 19:30", "%d-%m-%Y %H:%i")),
                                                                (302,STR_TO_DATE("17-11-2022 18:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("19-11-2022 10:25", "%d-%m-%Y %H:%i")),
                                                                (303,STR_TO_DATE("20-11-2022 10:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("21-11-2022 10:38", "%d-%m-%Y %H:%i")),
                                                                (304,STR_TO_DATE("19-11-2022 09:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("19-11-2022 10:00", "%d-%m-%Y %H:%i")),
                                                                (400,STR_TO_DATE("20-11-2022 11:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("19-11-2022 10:40", "%d-%m-%Y %H:%i")),
                                                                (401,STR_TO_DATE("18-11-2022 16:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("21-11-2022 8:30", "%d-%m-%Y %H:%i")),
                                                                (500,STR_TO_DATE("18-11-2022 08:30", "%d-%m-%Y %H:%i"),STR_TO_DATE("21-11-2022 10:30", "%d-%m-%Y %H:%i"));                                                                                  