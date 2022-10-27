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
                                        (103),
                                        (104),
                                        (105),
                                        (106),
                                        (107),
                                        (108),
                                        (109),
                                        (110),
                                        (111),
                                        (112),
                                        (113),
                                        (114);


INSERT INTO RESTAURANT (`idE`,`nomRest`) VALUES (1,"Erat Eget Tincidunt Incorporated"),
                                                (2,"A Facilisis Institute"),
                                                (3,"Donec Est Mauris LLP"),
                                                (4,"Cursus Inc."),
                                                (5,"Eget Volutpat Associates"),
                                                (6,"Lacus Vestibulum Lorem Institute"),
                                                (7,"Erat Eget Tincidunt Associates");


INSERT INTO `CRENEAU` (`idCreneau`,`dateHeureDebut`,`dateHeureFin`) VALUES (1, STR_TO_DATE("18-11-2022 09:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 10:00", "%d-%m-%Y %H:%i")),
                                                                            (2, STR_TO_DATE("18-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (3, STR_TO_DATE("18-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("18-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (4, STR_TO_DATE("19-11-2022 09:00", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 16:00", "%d-%m-%Y %H:%i")),
                                                                            (5, STR_TO_DATE("19-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (6, STR_TO_DATE("19-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("19-11-2022 13:30", "%d-%m-%Y %H:%i")),
                                                                            (7, STR_TO_DATE("20-11-2022 11:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 12:30", "%d-%m-%Y %H:%i")),
                                                                            (8, STR_TO_DATE("20-11-2022 12:30", "%d-%m-%Y %H:%i"), STR_TO_DATE("20-11-2022 13:30", "%d-%m-%Y %H:%i"));


INSERT INTO `REPAS` (`idRepas`,`estmidi`,`idRest`,`idCreneau`) VALUES (1,"true",1,2),
                                                                        (2,"true",1,3 ),
                                                                        (3,"true",1,5),
                                                                        (4,"false",2,6),
                                                                        (5,"true",2,7),
                                                                        (6,"false",2,8),
                                                                        (7,"true",3,2),
                                                                        (8,"false",3,3 ),
                                                                        (9,"true",3,5),
                                                                        (10,"true",1,6),
                                                                        (11,"true",1,7),
                                                                        (12,"false",1,8),
                                                                        (13,"false",2,2),
                                                                        (14,"true",2,3 ),
                                                                        (15,"true",2,5),
                                                                        (16,"true",3,6),
                                                                        (17,"true",3,7),
                                                                        (18,"false",3,8),
                                                                        (19,"true",1,2),
                                                                        (20,"false",1,3 );