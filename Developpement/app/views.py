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
supprimer_utilisateur_role, get_participant, modifier_utilisateur, ajoute_participant_role, ajoute_repas_mangeur


TYPE_PARTICIPANT = ["Auteur", "Consommateur", "Exposant", "Intervenant", "Invite", "Presse", "Staff", "Secretaire"]
TYPE_PARTICIPANT_FINALE = ["Auteur", "Exposant", "Invite", "Presse", "Staff", "Secretaire"]
DATE_FESTIVAL = ["2022-11-17", "2022-11-18", "2022-11-19", "2022-11-20"]
DICO_HORAIRE_RESTAURANT = {"jeudi_soir" : "2022-11-17-19-30-00/2022-11-17-22-00-00", "vendredi_midi": "2022-11-18-11-30-00/2022-11-18-14-00-00", "vendredi_soir":"2022-11-18-19-30-00/2022-11-18-22-00-00", "samedi_midi" : "2022-11-19-11-30-00/2022-11-19-14-00-00", "samedi_soir":"2022-11-19-19-30-00/2022-11-19-22-00-00", "dimanche_midi":"2022-11-20-11-30-00/2022-11-20-14-00-00", "dimanche_soir":"2022-11-20-19-30-00/2022-11-20-22-00-00"}
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

@app.route('/api/dataParticipant')
@login_required
def dataParticipant():
    if not current_user.est_secretaire():
        return redirect(url_for('logout')) 
    return {'data': [participant.to_dict() for participant in session.query(Participant).all()]}

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
        print(transport)
        voyages_dico = {}
        voyages_dico["transport"] = transport[1].nomTransport
        voyages_dico["lieuDepart"] = transport[0].lieuDepart
        voyages_dico["lieuArrive"] = transport[0].lieuArrive
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
    if current_user.est_secretaire():
        return redirect(url_for("page_secretaire_accueil"))
    if request.method == "POST":
        liste_id_box = ["avion", "train", "autre", "voiture", "covoiturage"]
        liste_id_champs = ["aeroport", "gare", "precision"]
        for i in range(len(liste_id_box)-1):
            if request.form.get(liste_id_box[i]) == "option1":
                if i<= 2 : 
                    depart = request.form[liste_id_champs[i]]
                if liste_id_box[i] == "avion":
                    ajoute_deplacer(session, current_user.idP, 1, depart, "Blois")
                elif liste_id_box[i] == "train":
                    depart = request.form[liste_id_champs[i]]
                    ajoute_deplacer(session, current_user.idP, 2, depart, "Blois")
                elif liste_id_box[i] == "voiture": 
                    ajoute_deplacer(session, current_user.idP, 3, current_user.adresseP, "Blois")
                elif liste_id_box[i] == "covoiturage":
                    ajoute_deplacer(session, current_user.idP, 4, current_user.adresseP, "Blois")
                else :
                    modif_participant_remarque(session, current_user.idP, "Moyen de déplacement : "+depart)    
        
        dateArr = request.form["dateArr"].replace("-",",").split(",")
        heureArr = request.form["hArrive"].replace(":",",").split(",")
        date_arr = datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(heureArr[0]), int(heureArr[1]))

        dateDep = request.form["dateDep"].replace("-",",").split(",")
        heureDep = request.form["hDep"].replace(":",",").split(",")
        date_dep = datetime(int(dateDep[0]), int(dateDep[1]), int(dateDep[2]), int(heureDep[0]), int(heureDep[1]))
        print(request.form["hDep"])
        ajoute_assister(session, current_user.idP, date_arr, date_dep)
        return redirect(url_for('formulaire_reservation', idp = current_user.idP))
        
    return render_template("transportForms.html")
    
@app.route('/FormulaireReservation/', methods = ["POST","GET"])
@login_required
def formulaire_reservation():
    print(type(request.method))
    if current_user.est_secretaire():
        return redirect(url_for("page_secretaire_accueil"))
    
    if request.method == "POST":
        regime = request.form["regime"] # stocker en variable car réutilisé ensuite
        liste_jour_manger = [request.form["jeudi_soir"],request.form["vendredi_midi"],\
        request.form["vendredi_soir"],request.form["samedi_midi"],request.form["samedi_soir"],\
        request.form["dimanche_midi"],request.form["dimanche_soir"]]
        ajoute_repas_mangeur(session, current_user.idP, liste_jour_manger, LISTE_HORAIRE_RESTAURANT, DICO_HORAIRE_RESTAURANT)
        
        if regime.isalpha():
            id_regime = ajoute_regime(session, regime)
            ajoute_avoir_regime(session, current_user.idP, id_regime)
        remarques = request.form["remarque"]
        modif_participant_remarque(session, current_user.idP, remarques)
        if request.form["besoinHebergement"] : 
            pass #TODO AJOUTER HOTEL RECUPERER DATE ARRIVE DATE DEPART DE L'HOTEL 
        return redirect(url_for('page_fin')) #TODO                 
        
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
