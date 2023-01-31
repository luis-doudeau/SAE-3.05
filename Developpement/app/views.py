import json
from .app import app

from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_login import login_required, login_user, LoginManager, current_user, logout_user
from secrets import token_urlsafe

from .Mobiliser import Mobiliser
from .Navette import Navette
from .Transporter import Transporter

from .Consommateur import Consommateur
from .Participant import Participant
from .Avoir import Avoir
from .Manger import Manger
from .Intervenant import Intervenant
from .Loger import Loger
from .Deplacer import Deplacer
from .Assister import Assister
from .Transport import Transport

from .ConnexionPythonSQL import get_info_personne, get_regime,session,get_nom_restaurant,\
get_nom_hotel, get_dormeur, afficher_consommateur, est_intervenant, affiche_participant_trier,\
est_secretaire,modifier_participant, ajoute_assister, ajoute_deplacer, modif_participant_remarque, ajoute_avoir_regime,\
ajoute_regime, get_max_id_regime, get_deb_voyage, get_lieu_depart_voyage, get_nom, get_prenom, load_user, get_utilisateur_email_mdp, get_secretaire,\
get_participant, modifier_utilisateur, get_restaurant, get_creneau, get_date, get_hotel, get_periode_hotel, get_date_dormeur, get_consommateur, get_intervenant, datetime_to_dateFrancais, \
supprimer_utilisateur_role, get_participant, modifier_utilisateur, ajoute_participant_role, ajoute_repas_mangeur, datetime_to_heure, get_role, get_info_all_participants, ajoute_hebergement,\
suppprime_loger, id_transport_with_name, supprime_deplacer_annee


TYPE_PARTICIPANT = ["Auteur", "Consommateur", "Exposant", "Intervenant", "Invite", "Presse", "Staff", "Secretaire"]
TYPE_PARTICIPANT_FINALE = ["Auteur", "Exposant", "Invite", "Presse", "Staff", "Secretaire"]
DATE_FESTIVAL = ["2023-11-16", "2023-11-17", "2023-11-18", "2023-11-19"]
DICO_HORAIRE_RESTAURANT = {"jeudi_soir" : DATE_FESTIVAL[0]+"-19-30-00/"+DATE_FESTIVAL[0]+"-22-00-00", "vendredi_midi": DATE_FESTIVAL[1]+"-11-30-00/"+DATE_FESTIVAL[1]+"-14-00-00", "vendredi_soir": DATE_FESTIVAL[1]+"-19-30-00/"+DATE_FESTIVAL[1]+"-22-00-00", "samedi_midi" : DATE_FESTIVAL[2]+"-11-30-00/"+DATE_FESTIVAL[2]+"-14-00-00", "samedi_soir":DATE_FESTIVAL[2]+"-19-30-00/"+DATE_FESTIVAL[2]+"-22-00-00", "dimanche_midi": DATE_FESTIVAL[3]+"-11-30-00/"+DATE_FESTIVAL[3]+"-14-00-00", "dimanche_soir": DATE_FESTIVAL[3]+"-19-30-00/"+DATE_FESTIVAL[3]+"-22-00-00"}
LISTE_HORAIRE_RESTAURANT = ["jeudi_soir", "vendredi_midi", "vendredi_soir", "samedi_midi" , "samedi_soir", "dimanche_midi", "dimanche_soir"]



LISTE_ROUTE = ["connexion", "page_inscription", "page_secretaire_accueil"]

@app.route('/', methods = ["GET", "POST"])
def connexion():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    if request.method == "POST":
        email = request.form["email"]
        mdp = request.form["mdp"]
        utilisateur = get_utilisateur_email_mdp(session, email, mdp)
        if utilisateur is not None:
            print('l51')
            if est_secretaire(session, utilisateur.idP):
                secretaire = get_secretaire(session, utilisateur.idP)
                login_user(secretaire)
                return redirect(url_for("page_secretaire_accueil"))
            else:
                participant = get_participant(session, utilisateur.idP)
                login_user(participant)
                return redirect(url_for('page_inscription'))
        return render_template('login.html', mail = request.form["email"])
    return render_template('login.html', mail = "ac@icloud.ca")


@app.route('/coordonneeForms/', methods = ["GET", "POST"])
@login_required
def page_inscription():
    if current_user.est_secretaire():
        return redirect(url_for("page_secretaire_accueil"))
    if request.method == "POST":
        modifier_participant(session, current_user.idP,request.form["adresse"],request.form["ddn"],request.form["tel"])
        modifier_utilisateur(session, current_user.idP, request.form["prenom"], request.form["nom"], request.form["email"])
        if est_intervenant(session, current_user.idP):
            return redirect(url_for('formulaire_auteur_transport', idp = current_user.idP))
        else:
            return redirect(url_for('page_fin'))
    return render_template('coordonneeForms.html')

    

@app.route('/secretaire_consommateur/', methods = ["POST", "GET"])
@login_required
def secretaire_consommateur():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))       
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        liste_consommateur = afficher_consommateur(session,la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaire_consommateur.html', nomsRestau = get_nom_restaurant(), liste_conso = liste_consommateur)
    return render_template('secretaire_consommateur.html', nomsRestau = get_nom_restaurant())
    
@app.route('/dormeurSecretaire/', methods = ["POST", "GET"])
@login_required
def dormeur_secretaire():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    if request.method == "POST":
        return render_template("dormeurSecretaire.html")

    return render_template('dormeurSecretaire.html', nomHotel = get_nom_hotel())

@app.route('/api/dataDormeurs')
@login_required
def dataDormeurs():
    if not current_user.est_secretaire():
        return redirect(url_for('logout')) 
    liste_dormeurs = []
    for intervenants in session.query(Loger).all():
        dormeurs_dico = get_intervenant(session, intervenants.idP).to_dict_sans_ddn()
        dormeurs_dico["hotel"] = get_hotel(session, intervenants.idHotel)
        dormeurs_dico["dateDeb"] = datetime_to_dateFrancais(intervenants.dateDebut)
        dormeurs_dico["dateFin"] = datetime_to_dateFrancais(intervenants.dateFin)
        liste_dormeurs.append(dormeurs_dico)
    return {'data': liste_dormeurs}

@app.route('/api/dataParticipant', methods = ["POST"])
@login_required
def dataParticipant():
    if not current_user.est_secretaire():
        return redirect(url_for('logout')) 
    liste_participants = []
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    adresseEmail = request.form["adresseEmail"]
    naissance = request.form["naissance"]
    role = request.form["role"]
    participants = get_info_all_participants(session, prenom, nom, naissance, adresseEmail, role)
    for participant in participants:
        participant_dico = participant.to_dict()
        participant_dico["role"] = get_role(session, participant.idP)
        liste_participants.append(participant_dico)
    return {'data': liste_participants}

@app.route('/api/dataConsommateurs')
@login_required
def dataConsommateurs():
    if not current_user.est_secretaire():
        return redirect(url_for('logout')) 
    liste_consommateur = []
    for consommateur in session.query(Manger).all():
        consommateur_dico = get_consommateur(session, consommateur.idP).to_dict_sans_ddn()
        consommateur_dico["regime"] = get_regime(session, consommateur.idP)
        consommateur_dico["restaurant"] = get_restaurant(session, consommateur.idRepas)
        consommateur_dico["date"] = get_date(session, consommateur.idRepas)
        consommateur_dico["creneau"] = get_creneau(session, consommateur.idRepas)
        liste_consommateur.append(consommateur_dico)
    return {'data': liste_consommateur}


@app.route('/api/dataNavettes')
@login_required
def dataNavettes():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))
    liste_voyages = []
    for voyages in session.query(Mobiliser).all():
        voyages_dico = voyages.to_dict()
        voyages_dico["heureDeb"] = get_deb_voyage(session, voyages.idVoy)
        voyages_dico["depart"] = get_lieu_depart_voyage(session, voyages.idVoy)
        for elements in session.query(Transporter).filter(Transporter.idVoy == voyages.idVoy).all():
            voyages_dico["prenom"] = get_prenom(session, elements.idP)
            voyages_dico["nom"] = get_nom(session, elements.idP)
            liste_voyages.append(voyages_dico)
    return {'data': liste_voyages}


@app.route('/api/dataTransporte')
@login_required
def dataTransport():
    if not current_user.est_secretaire():
        return redirect(url_for('logout')) 
    liste_transport = []
    for transport in session.query(Deplacer, Transport).join(Transport, Deplacer.idTransport==Transport.idTransport).all():
        voyages_dico = {}
        voyages_dico["transport"] = transport[1].nomTransport
        voyages_dico["lieuDepart"] = transport[0].lieuDepart
        voyages_dico["dateDepart"] = datetime_to_heure(transport[0].dateArrive)
        voyages_dico["lieuArrive"] = transport[0].lieuArrive
        voyages_dico["dateArrive"] = datetime_to_heure(transport[0].dateDepart)
        voyages_dico["prenomP"] = get_prenom(session, transport[0].idP)
        voyages_dico["nomP"] = get_nom(session, transport[0].idP)
        liste_transport.append(voyages_dico)
    return {'data': liste_transport}


@app.route('/participantSecretaire/', methods = ["POST", "GET"])
@login_required
def participant_secretaire():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    if request.method == "POST":
        liste_personne = affiche_participant_trier(session, request.form["trier"])
        return render_template('participantSecretaire.html', type_participant = TYPE_PARTICIPANT, liste_personne = liste_personne)
    return render_template('participantSecretaire.html', type_participant = TYPE_PARTICIPANT)


@app.route('/transportForms/', methods = ["POST", "GET"])
@login_required
def formulaire_auteur_transport():
    print(request.form)
    if est_secretaire(session, current_user.idP):
        return redirect(url_for("page_secretaire_accueil"))
    if request.method == "POST":
        
        liste_id_box = ["avion", "train", "voiture", "covoiturage", "autre"]
        dico_champs_box = {"avion" : ["lieuDepartAvion", "lieuArriveAvion"], "train": ["lieuDepartTrain", "lieuArriveTrain"],\
                          "voiture": ["lieuDepartVoiture", "lieuArriveVoiture"], "covoiturage": ["lieuDepartCovoiturage", "lieuArriveCovoiturage"],\
                          "autre": ["precision"]}

        currentDateTime = datetime.now()
        date = currentDateTime.date()
        year = date.strftime("%Y")
        supprime_deplacer_annee(session, current_user.idP, year)
        for transport in liste_id_box:
            if request.form[transport] == "true" and transport != "autre" :
                lieu_depart = request.form[dico_champs_box[transport][0]]
                lieu_arrive = request.form[dico_champs_box[transport][1]]   
                ajoute_deplacer(session, current_user.idP, id_transport_with_name(transport), lieu_depart, lieu_arrive, year)
            elif transport == "autre" : 
                modif_participant_remarque(session, current_user.idP, request.form[dico_champs_box[transport][0]])

        dateArr = request.form["dateArr"].split("-")
        heureArr = request.form["hArrive"].split(":")
        date_arr = datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(heureArr[0]), int(heureArr[1]))

        dateDep = request.form["dateDep"].replace("-",",").split(",")
        heureDep = request.form["hDep"].replace(":",",").split(",")
        date_dep = datetime(int(dateDep[0]), int(dateDep[1]), int(dateDep[2]), int(heureDep[0]), int(heureDep[1]))
        ajoute_assister(session, current_user.idP, date_arr, date_dep)
        print("kdspfkdsfkdsml")
        return render_template("formulaireReservation.html", idp = current_user.idP)
        
    return render_template("transportForms.html")
        
        
    
@app.route('/FormulaireReservation/', methods = ["POST","GET"])
@login_required
def formulaire_reservation():
    if current_user.est_secretaire():
        return redirect(url_for("page_secretaire_accueil"))

    if request.method == "POST":
        regime = request.form["regime"] # stocker en variable car réutilisé ensuite
        liste_jour_manger = [request.form["jeudi_soir"],request.form["vendredi_midi"],\
        request.form["vendredi_soir"],request.form["samedi_midi"],request.form["samedi_soir"],\
        request.form["dimanche_midi"],request.form["dimanche_soir"]]
        ajoute_repas_mangeur(session, current_user.idP, liste_jour_manger, LISTE_HORAIRE_RESTAURANT, DICO_HORAIRE_RESTAURANT)
        
        if regime.isalpha(): # si le champ 'regime' contient des caractères
            id_regime = ajoute_regime(session, regime)
            ajoute_avoir_regime(session, current_user.idP, id_regime)
        remarques = request.form["remarque"]
        if remarques.isalpha():  # si le champ 'remarques' contient des caractères
            modif_participant_remarque(session, current_user.idP, remarques)
        
        suppprime_loger(session, current_user.idP)
        if request.form["hebergement"] =="true":
            ajoute_hebergement(session, current_user.idP)
        
        return render_template("pageFin.html", idp=current_user.idP) #TODO
        
    return render_template("formulaireReservation.html", idp=current_user.idP)

@app.route('/secretaireNavette/', methods = ["POST","GET"])
@login_required
def page_secretaire_navette():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        liste_navette = afficher_consommateur(session,la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaire_consommateur.html', nomsRestau = get_nom_restaurant(), liste_conso = liste_navette)
    return render_template('secretaireNavette.html', nomsRestau = get_nom_restaurant())



@app.route('/secretaireGererTransport/', methods = ["POST","GET"])
@login_required
def page_secretaire_gerer_participants():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    if request.method == 'POST':
        return render_template('secretaireGererTransport.html')
    return render_template('secretaireGererTransport.html')


@app.route('/pageFin/', methods = ["GET"])
@login_required
def page_fin():
    if current_user.est_secretaire():
        return redirect(url_for("page_secretaire_accueil"))
    return render_template("pageFin.html")

@app.route('/secretaire/', methods = ["GET"])
@login_required
def page_secretaire_accueil():
    if current_user.est_secretaire():
        return render_template("secretaire.html")
    else:
        return redirect(url_for('logout'))

@app.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("connexion"))

@app.route('/inscrireSecretaire/', methods = ["POST","GET"])
@login_required
def page_secretaire_inscrire():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))
    if request.method == 'POST':
        role = request.form["role"]
        print(role)
        prenom = request.form["prenom"]
        print(prenom)
        nom = request.form["nom"]
        email = request.form["email"]
        adresse = request.form["adresse"]
        tel = request.form["tel"]
        ddn = request.form["ddn"]
        ajoute_participant_role(session, prenom, nom, email, adresse, tel, ddn, role)
        return render_template("secretaire.html")
    return render_template("inscrireSecretaire.html", liste_roles=TYPE_PARTICIPANT_FINALE)



@app.route('/delete_utilisateur',methods=['POST'])
def delete_utilisateur():
    print(request.form["id"])
    supprimer_utilisateur_role(session, request.form["id"])
    return ""


#Ne pas effacer test
"""@app.before_request
def before_request():
    if request.endpoint in LISTE_ROUTE:
        print("JE change de page")
        print("path ",request.path)
        print("request ",request)
        print("referrer ",request.referrer)
        print("Ref2:", request.values.get("url"))"""
        

# @app.route('/Participant/<idP>',methods=['POST',"GET"])
# def Participant(id):
#     return render_template("index.html",id=id)#TODO
