drop trigger if exists ajouteTransport;


delimiter |


create trigger ajouteTransport after insert on INTERVENANT for each row 
  begin 
    declare moyenloc varchar(42);
    declare idVoyage int DEFAULT -1;
    declare nbVoyageur int;
    declare idMax int;
    declare nouveauDepart DATETIME;

    select new.moyenlocomotion into moyenloc from INTERVENANT natural join PARTICIPANT;
    if moyenloc == "Train" then
      select ifnull(count(idVoy),0) idVoy into nbVoyageur, idVoyage 
      from INTERVENANT natural join VOYAGE 
      where directionGare and DATEDIFF(minutes, DATEheureDepart, new.arrive) <= 15;
      
      if idVoyage = -1 then

        -- Voyage aller
        select IFNULL(max(idVoy)) into idMax from VOYAGE;
        declare heureDepartNouveauVoyageAller TIME; 
        set heureDepartNouveauVoyage = TIME(arrive - TIME("00:10");
        insert into VOYAGE values(idMax+1, STR_TO_DATE(concat(DATE(heureDepartNouveauVoyage), " ", heureDepartNouveauVoyageAller), ""), "00:15", true));


        -- Voyage retour
        select IFNULL(max(idVoy)) into idMax from VOYAGE;
        declare heureDepartNouveauVoyageRetour TIME;
        set heureDepartNouveauVoyageRetour = TIME(nouveauDepart + TIME("00:15");
        --select TIME(STR_TO_DATE("19-11-2022 09:30", "%d-%m-%Y %H:%i")+ TIME("00:15"));
        --select concat(DATE(STR_TO_DATE("19-11-2022 09:30", "%d-%m-%Y %H:%i"))," ", TIME("00:15", "%H:%i"));
        set heureDepartNouveauVoyageRetour = STR_TO_DATE(concat(DATE(STR_TO_DATE("19-11-2022 09:30", "%d-%m-%Y %H:%i"))," ",  TIME("15:00")), "%Y-%m-%d %H:%i:%s");
        insert into VOYAGE values(idMax+2, heureDepartNouveauVoyageRetour, "00:10", true));
      end if;


