drop trigger if exists ajouteTransport;



delimiter |
create trigger verifCapaciteHotel before insert on LOGER for each row
  begin
    declare msg varchar(300);
    declare capacite int;
    declare capaciteMax int;

    select IFNULL(count(*),0) into capacite from LOGER where idHotel = new.idHotel and dateFin >= new.dateDeb;
    select capaciteHotel into capaciteMax from HOTEL where idHotel = new.idHotel;


    if capacite >= capaciteMax then
      set msg = concat("L'Hotel n'a plus de place disponible");
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if;
end |
delimiter ;

delimiter |


create trigger ajouteTransport after insert on DEPLACER for each row 
  begin 
    declare heureArriveIntervenant DATETIME;
    declare idVoyage int DEFAULT -1;
    declare nbVoyageur int;
    declare idMax int;
    declare nouveauDepart DATETIME;
    declare msg varchar(300);
    declare idNavetteDispo int;

    
    if EXISTS(select heureArriveIntervenant into moyenloc from DEPLACER natural join MOYEN_TRANSPORT natural join INTERVENANT 
              where idP = new.idP and idTransport = new.idTransport and nomTransport = "Train" and lieuArrive = "Gare Blois") then
      
      select ifnull(count(idVoy),0) as nbV, idVoy into nbVoyageur, idVoyage 
      from TRANSPORTER
      where not directionGare and TIME("-00:15:00") <= TIMEDIFF(heureDebVoy, new.dateArrive) <= TIME("00:15:00");
      
      if idVoyage = -1 and 8 <= HOUR(new.arrive) <= 20 then

        -- Voyage aller
        select IFNULL(max(idVoy)) into idMax from VOYAGE;
        insert into VOYAGE values(idMax+1, new.dateArrive, "00:10", false);
        insert into TRANSPORTER values(new.idP, idMax+1);
        insert into MOBILISER values(idMax+1, 1);
      
      elsif idVoyage != -1 and 8 <= HOUR(new.arrive) <= 20 :
        
        

      else 
        set msg = concat("Les navettes ne circulent qu'entre 8 heure et 20 heure");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      end if;

    end if;

  end |



    

-- -- Voyage retour
--         select IFNULL(max(idVoy)) into idMax from VOYAGE;
--         declare heureDepartNouveauVoyageRetour TIME;
--         set heureDepartNouveauVoyageRetour = TIME(new.arrive + TIME("00:15");
--         set nouveauDepartRetour = STR_TO_DATE(concat(DATE(STR_TO_DATE(new.arrive, "%d-%m-%Y %H:%i"))," ",  heureDepartNouveauVoyageRetour), "%Y-%m-%d %H:%i:%s");
--         insert into VOYAGE values(idMax+2, nouveauDepartRetour, "00:10", false);

-- select idNav into idNavetteDispo from MOBILISER 
--         where idNav not in (select idNav from MOBILISER natural join VOYAGE 
--                             where DATEDIFF(heureDepart, ) < TIME("00:00") and DATEDIFF() and directionGare = False;

-- declare heureDepartNouveauVoyageAller TIME;
--         set heureDepartNouveauVoyageAller = TIME(new.arrive - TIME("00:10");
--         set nouveauDepartAller = STR_TO_DATE(concat(DATE(STR_TO_DATE(new.arrive, "%d-%m-%Y %H:%i"))," ",  heureDepartNouveauVoyageAller), "%Y-%m-%d %H:%i:%s");
--         insert into VOYAGE values(idMax+1, nouveauDepartAller, "00:10", true);
