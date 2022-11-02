drop trigger if exists ajouteNavette;
drop trigger if exists verifCapaciteHotel;
drop trigger if exists verifCreneauRepasStaff;


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


create trigger verifCreneauRepasStaff before insert on MANGER for each row 
  begin
    declare msg VARCHAR(300);
    if EXISTS(select * from REPAS inner join CRENEAU inner join STAFF
    where new.idP = STAFF.idP and REPAS.idCreneau = CRENEAU.idCreneau and
    TIME("00:00") > TIMEDIFF(TIME(dateDebut), TIME("11:30")) or TIMEDIFF(TIME(dateDebut), TIME("13:30")) > TIME("00:00") or
    TIME("00:00") > TIMEDIFF(TIME(dateFin), TIME("11:30"))  or TIMEDIFF(TIME(dateFin), TIME("14:00")) > TIME("00:00")) then
      set msg = concat("Les membres du staff ne peuvent manger qu'entre 11H30 et 14H00");
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if;
  end |


create trigger verifCreneau before insert on CRENEAU for each row 
  begin
    declare msg VARCHAR(300); 
    if TIMESTAMPDIFF(MINUTE, new.dateDebut, new.dateFin) <= 0 then 
      set msg = concat("Le créneaux n'est pas cohérents");
      signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
    end if;
  end |


create trigger ajouteNavette after insert on DEPLACER for each row  
  begin
    declare idVoyage int default -1;
    declare nbVoyageur int;
    declare idMaxVoy int default 0;
    declare idMaxNav int default 0;
    declare idNav int;
    declare msg varchar(300);
    declare dateArriveP VARCHAR(50);
    declare capaciteVoyage int default -1;
    
    if new.idTransport = 2 and new.lieuArrive = "Gare Blois" then

      select dateArrive into dateArriveP from INTERVENANT where new.idP = idP;
    

      select count(idVoy) as nbVoyageur into nbVoyageur
      from TRANSPORTER natural join VOYAGE
      where not directionGare and TIME("-00:10:00") <= TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(dateArriveP,""), "%Y-%m-%d %H:%i:%s")) and TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(dateArriveP,""), "%Y-%m-%d %H:%i:%s")) <= TIME("00:10:00")
      order by nbVoyageur asc
      limit 1;


      select idVoy as idVoyage into idVoyage
      from TRANSPORTER natural join VOYAGE natural join MOBILISER natural join NAVETTE
      where not directionGare and TIME("-00:10:00") <= TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(dateArriveP,""), "%Y-%m-%d %H:%i:%s")) and TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(dateArriveP,""), "%Y-%m-%d %H:%i:%s")) <= TIME("00:10:00")
      order by idVoyage desc
      limit 1;


      select sum(capaciteNavette) as capaciteVoyage into capaciteVoyage
      from VOYAGE natural join MOBILISER natural join NAVETTE
      where not directionGare and TIME("-00:10:00") <= TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(dateArriveP,""), "%Y-%m-%d %H:%i:%s")) and TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(dateArriveP,""), "%Y-%m-%d %H:%i:%s")) <= TIME("00:10:00")
      limit 1;


      if idVoyage = -1 and 8 <= HOUR(dateArriveP) and HOUR(dateArriveP) <= 20 then   

        select max(idVoy) as idMaxVoy into idMaxVoy from VOYAGE;
        select max(idMaxNav) as idMaxNav into idMaxNav from VOYAGE;
        insert into VOYAGE values(idMaxVoy+1, dateArriveP, TIME("00:10"), false);
        insert into TRANSPORTER values(new.idP, idMaxVoy+1);
        insert into MOBILISER values(idMaxVoy+1, 1);

      elseif capaciteVoyage <= nbVoyageur then  -- vérifier si la navette n'est pas plaine
        select max(idNavette) as idMaxNav into idMaxNav from NAVETTE natural join MOBILISER where idVoy = idVoyage;
        insert into TRANSPORTER values(new.idP, idVoyage);
        insert into MOBILISER values(idVoyage, idMaxNav+1);
      
      elseif idVoyage <> -1 and 8 <= HOUR(dateArriveP) and HOUR(dateArriveP) <= 20 then
          insert into TRANSPORTER values(new.idP, idVoyage); 

      else 
        set msg = concat("Les navettes ne circulent qu'entre 8 heure et 20 heure");
          signal SQLSTATE '45000' set MESSAGE_TEXT = msg;
      
      end if;
    end if;
  end |

delimiter ;


-- select count(*) as nbNavetteRecquise from MOBILISER natural join VOYAGE 
-- where not directionGare and TIME("-00:10:00") <= TIMEDIFF(heureDebVoy, STR_TO_DATE(concat(STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),""), "%Y-%m-%d %H:%i:%s")) and TIMEDIFF(heureDebVoy,
-- STR_TO_DATE(concat(STR_TO_DATE("2022-11-19 10:30", "%Y-%m-%d %H:%i"),""), "%Y-%m-%d %H:%i:%s")) <= TIME("00:10:00");