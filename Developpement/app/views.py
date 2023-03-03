from .app import app

from datetime import datetime
from flask import  render_template, request, redirect, url_for, send_file, session, jsonify, make_response
from flask_login import login_required, login_user, current_user, logout_user
from secrets import token_urlsafe

from .Deplacer import Deplacer
from .Assister import Assister
from .Transport import Transport
from .ConnexionPythonSQL import *
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import pandas as pd
from io import BytesIO
from .constants import *

@app.route('/', methods = ["GET", "POST"])
def connexion():
    """
    Si l'utilisateur s'est bien connecté renvoie vers la bonne page sinon,
    renvoie vers la page login
    :return: la page de connexion.
    """
    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    if request.method == "POST":
        email = request.form["email"]
        mdp = request.form["mdp"]
        utilisateur = get_utilisateur_email_mdp(email, mdp)
        if utilisateur is not None:
            if est_secretaire(utilisateur.idP):
                secretaire = get_secretaire(utilisateur.idP)
                login_user(secretaire)
                return redirect(url_for("page_secretaire_accueil"))
            else:
                participant = get_participant(utilisateur.idP)
                login_user(participant)
                return redirect(url_for('page_inscription'))
        return render_template('login.html', mail = request.form["email"])
    return render_template('login.html', mail = "lenina@gmail.com")


@app.route('/coordonneeForms/', methods = ["GET", "POST"])
@login_required
def page_inscription():
    """
    Il redirige l'utilisateur vers la page où il peut renseigner ses informations personnelles
    :return: le modèle de la page.
    """
    if est_secretaire(current_user.idP):
        return redirect(url_for("page_secretaire_accueil"))
    if request.method == "POST":
        modifier_participant(current_user.idP,request.form["adresse"], request.form["codePostal"], request.form["ville"],request.form["ddn"],request.form["tel"])
        modifier_utilisateur(current_user.idP, request.form["prenom"], request.form["nom"], request.form["email"])
        if est_intervenant(current_user.idP):
            return redirect(url_for('formulaire_auteur_transport', idp = current_user.idP))
        else:
            return redirect(url_for('page_fin', idp = current_user.idP))
    return render_template('coordonneeForms.html')


@app.route('/insereTransportForms/', methods = ["POST"])
@login_required
def insererTransportPersonne():
    """
    Il prend les données du formulaire transport personne et les insère dans la base de données
    :return: Un objet JSON avec un statut de réussite.
    """
    liste_id_box = ["avion", "train", "voiture", "covoiturage", "autre"]
    dico_champs_box = {"avion" : ["lieuDepartAvion", "lieuArriveAvion"], "train": ["lieuDepartTrain", "lieuArriveTrain"],\
                        "voiture": ["lieuDepartVoiture", "lieuArriveVoiture"], "covoiturage": ["lieuDepartCovoiturage", "lieuArriveCovoiturage"],\
                        "autre": ["precision"]}

    currentDateTime = datetime.datetime.now()
    date = currentDateTime.date()
    year = date.strftime("%Y")
    supprime_deplacer_annee(current_user.idP, year)
    for transport in liste_id_box:
        if request.form[transport] == "true" and transport != "autre" :
            lieu_depart = request.form[dico_champs_box[transport][0]]
            lieu_arrive = request.form[dico_champs_box[transport][1]]   
            ajoute_deplacer(current_user.idP, id_transport_with_name(transport), lieu_depart, lieu_arrive, year)
        elif transport == "autre" : 
            modif_participant_remarque(current_user.idP, request.form[dico_champs_box[transport][0]])

    dateArr = request.form["dateArr"].split("-")
    heureArr = request.form["hArrive"].split(":")
    date_arr = datetime.datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(heureArr[0]), int(heureArr[1]))

    dateDep = request.form["dateDep"].replace("-",",").split(",")
    heureDep = request.form["hDep"].replace(":",",").split(",")
    date_dep = datetime.datetime(int(dateDep[0]), int(dateDep[1]), int(dateDep[2]), int(heureDep[0]), int(heureDep[1]))
    ajoute_assister(current_user.idP, date_arr, date_dep)
    supprimer_intervenant_voyage_navette(current_user.idP)
    if request.form["train"] == "true" and "BLOIS" in request.form["lieuArriveTrain"].upper():
        affecter_intervenant_voyage_depart_gare(current_user.idP)
        affecter_intervenant_voyage_depart_festival(current_user.idP)
    return jsonify({"status": "success"})


@app.route('/transportForms/', methods = ["POST", "GET"])
@login_required
def formulaire_auteur_transport():
    """
    Il renvoie une page avec un formulaire pour renseigner les informations de transport de
    l'utilisateur courant
    :return: Un objet de réponse
    """
    if est_secretaire(current_user.idP):
        return redirect(url_for("page_secretaire_accueil"))
    assister = get_assister(current_user.idP, datetime.datetime.now().year)
    dateArr = DATE_FESTIVAL[0]
    dateDep=None
    time_arr = None
    time_dep = None
    if assister is not None :
        dateArr = str(assister.dateArrive.year)+"-"+str(assister.dateArrive.month)+"-"+str(assister.dateArrive.day)
        dateDep = str(assister.dateDepart.year)+"-"+str(assister.dateDepart.month)+"-"+str(assister.dateDepart.day)
        time_arr = assister.dateArrive.strftime("%H:%M")
        time_dep = assister.dateDepart.strftime("%H:%M")
    liste_transport = requete_transport_annee2(current_user.idP, datetime.datetime.now().year)
    print(liste_transport)
    response= make_response(render_template("transportForms.html", date_arr=dateArr,date_dep=dateDep, limite_arr=dateArr, timeArr=time_arr, timeDep=time_dep, limite_dep = DATE_FESTIVAL[-1], listeTransport=liste_transport, liste_lieu_train=get_all_lieu_train(), liste_lieu_avion=get_all_lieu_avion()))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/insererFormulaireReservation/', methods = ["POST"])
@login_required
def inserer_formulaire_reservation():
    """
    Il prend les données du formulaire de réservation et les insère dans la base de
    données
    :return: un objet json avec le statut "success"
    """
    regime = request.form["regime"] # stocker en variable car réutilisé ensuite
    liste_jour_manger = [request.form["jeudi_soir"],request.form["vendredi_midi"],\
    request.form["vendredi_soir"],request.form["samedi_midi"],request.form["samedi_soir"],\
    request.form["dimanche_midi"],request.form["dimanche_soir"]]
    ajoute_repas_mangeur(current_user.idP, liste_jour_manger, LISTE_HORAIRE_RESTAURANT, DICO_HORAIRE_RESTAURANT)

    if not regime.isspace() and not (len(regime)==0): # si le champ 'regime' contient des caractères et n'existe pas déjà
        idRegime = possede_regime(current_user.idP) # verifie si la personne possede un regime et si oui on recupere l'id de ce regime
        if idRegime is not None : # si il possède un regime
            update_regime(idRegime, regime)
        else :
            id_regime = ajoute_regime(regime)
            ajoute_avoir_regime(current_user.idP, id_regime)
    else :
        idRegime = possede_regime(current_user.idP) 
        if idRegime is not None : # si il possède un regime
            supprime_regime(current_user.idP, idRegime)
            
    remarques = request.form["remarque"]
    if remarques.isalpha():  # si le champ 'remarques' contient des caractères
        modif_participant_remarque(current_user.idP, remarques)
    suppprime_loger(current_user.idP)
    if request.form["hebergement"] =="true":
        ajoute_hebergement(current_user.idP)
    print("success")
    return jsonify({"status": "success"})


@app.route('/FormulaireReservation/', methods = ["POST","GET"])
@login_required
def formulaire_reservation():
    """
    Il rend le template "formulaireReservation.html" et passe les variables repas, regimes et dormeur au
    template
    :return: un objet de réponse.
    """
    if est_secretaire(current_user.idP):
        return redirect(url_for("page_secretaire_accueil"))
    if get_regime(current_user.idP) == "Pas de régime" :
        regime = ""
    else : 
        regime = get_regime(current_user.idP)
    # Rendering the template "formulaireReservation.html" and passing the variables repas, regimes,
    # and dormeur to the template.
    response = make_response(render_template("formulaireReservation.html",repas=get_repas_present(current_user.idP, datetime.datetime.now().year),regimes=regime, dormeur=get_dormir(current_user.idP, datetime.datetime.now().year)))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

@app.route('/pageFin/', methods = ["GET"])
@login_required
def page_fin():
    """
    Afficher le modèle pageFin.html
    :return: le modèle pageFin.html.
    """
    if est_secretaire(current_user.idP):
        return redirect(url_for("page_secretaire_accueil"))
    return render_template("pageFin.html", idP = current_user.idP)


@app.route('/secretaire_consommateur/', methods = ["POST", "GET"])
@login_required
def secretaire_consommateur():
    """
    Il renvoie vers le modele secretaire consommateur
    :return: Une liste de dictionnaires.
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))       
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        liste_consommateur = afficher_consommateur(la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaire_consommateur.html', nomsRestau = get_liste_nom_restaurant(), liste_conso = liste_consommateur)
    return render_template('secretaire_consommateur.html', nomsRestau = get_liste_nom_restaurant())
    

@app.route('/dormeurSecretaire/', methods = ["POST", "GET"])
@login_required
def dormeur_secretaire():
    """
    Renvoie vers le modele secretaire dormeur
    :return: The dormeur_secretaire function is returning the dormeurSecretaire.html page.
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))   
    if request.method == "POST":
        return render_template("dormeurSecretaire.html")

    return render_template('dormeurSecretaire.html')


@app.route('/api/dataDormeurs', methods = ["POST"])
@login_required
def dataDormeurs():
    """
    Créé la page api dormeurs avec les bonnes informations en fonctions des filtres
    :return: Un dictionnaire avec une clé de 'data' et une valeur de liste_dormeurs
    """
    if not  est_secretaire(current_user.idP):
        return redirect(url_for('logout'))
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    hotel = request.form["hotel"]
    dateDebut = request.form["dateDebut"]
    dateFin = request.form["dateFin"]

    liste_dormeurs = []
    liste_dormeur_sans_info = get_tout_dormeurs_avec_filtre(prenom, nom, hotel, dateDebut, dateFin)
    for intervenants in liste_dormeur_sans_info:
        dormeurs_dico = get_intervenant(intervenants.idP).to_dict()
        dormeurs_dico["hotel"] = get_hotel(intervenants.idHotel)
        dormeurs_dico["idHotel"] = intervenants.idHotel
        dormeurs_dico["dateDeb"] = intervenants.dateDebut.date()
        dormeurs_dico["dateFin"] = intervenants.dateFin.date()
        liste_dormeurs.append(dormeurs_dico)
    session["data"] = {'data': liste_dormeurs}

    return {'data': liste_dormeurs}

  
@app.route("/api/data/nomHotel")
@login_required
def data_nom_hotel():
    """
    Il renvoie un objet JSON contenant les noms de tous les hôtels de la base de données
    :return: Le nom de l'hôtel
    """
    return jsonify(get_nom_hotel())

@app.route("/api/data/nomRestaurant", methods= ["GET"])
@login_required
def data_nom_restaurant():
    """
    Il renvoie un objet JSON contenant la liste des noms de restaurants
    :return: Une liste de tous les restaurants de la base de données
    """
    return jsonify(get_liste_nom_restaurant())

@app.route("/api/data/creneauRepas", methods = ["GET"])
@login_required
def data_creneauRepas():
    """
    Il retourne un objet JSON contenant la liste des créneaux repas
    :return: Une liste de dictionnaires.
    """
    return jsonify(get_liste_creneau_repas())

@app.route('/api/dataParticipant', methods = ["POST"])
@login_required
def dataParticipant():
    """
    Créé la page api participant avec les bonnes informations en fonctions des filtres
    :return: Une liste de dictionnaires.
    """
    if not  est_secretaire(current_user.idP):
        return redirect(url_for('logout')) 
    liste_participants = []
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    adresseEmail = request.form["adresseEmail"]
    naissance = request.form["naissance"]
    role = request.form["role"]
    participants = get_info_all_participants(prenom, nom, adresseEmail,naissance, role)
    for participant in participants:
        participant_dico = participant.to_dict()
        participant_dico["role"] = get_role(participant.idP)
        liste_participants.append(participant_dico)
    return {'data': liste_participants}


@app.route('/api/dataConsommateurs', methods = ["POST"])
@login_required
def dataConsommateurs():
    """
    Créé la page api consommateur avec les bonnes informations en fonctions des filtres
    :return: Un dictionnaire avec une clé 'data' et une valeur d'une liste de dictionnaires.
    """
    if not  est_secretaire(current_user.idP):
        return redirect(url_for('logout')) 
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    restaurant = request.form["restaurant"]
    la_date = request.form["la_date"]
    creneau = request.form["creneau"]
    consommateurs = get_info_all_consommateurs(prenom, nom, restaurant, la_date, creneau)
    liste_consommateur = []
    for consommateur in consommateurs:
        consommateur_dico = get_consommateur(consommateur.idP).to_dict_sans_ddn()
        consommateur_dico["regime"] = get_regime(consommateur.idP)
        consommateur_dico["restaurant"] = get_restaurant(consommateur.idRepas)
        consommateur_dico["date"] = get_date_repas(consommateur.idRepas)
        consommateur_dico["creneau"] = get_creneau_repas(consommateur.idRepas)
        consommateur_dico["idRepas"] = consommateur.idRepas
        liste_consommateur.append(consommateur_dico)
    return {'data': liste_consommateur}


@app.route('/api/dataNavettes', methods = ["POST", "GET"])
@login_required
def dataNavettes():
    """
    Créé la page api navette avec les bonnes informations en fonctions des filtres
    :return: Un dictionnaire avec une clé de 'data' et une valeur de liste_voyages
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))
    id_voyage = request.form["idVoyage"]
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    direction = request.form["depart"]
    id_navette = request.form["idNavette"]
    dateDepart = request.form["dateDepart"]
    liste_voyages_sans_info = get_tout_voyage_avec_filtre(id_voyage, direction, id_navette, dateDepart)   
    liste_voyages = []
    for voyages in liste_voyages_sans_info:
        intervenants_navette = get_intervenant_dans_voyage_avec_filtre(voyages.idVoy, prenom, nom)
        for intervenant in intervenants_navette:
            voyages_dico = voyages.to_dict()
            voyages_dico["prenom"] = intervenant.prenomP
            voyages_dico["nom"] = intervenant.nomP
            voyages_dico["idPersonne"] = intervenant.idP
            liste_voyages.append(voyages_dico)
    session["data"] = {'data': liste_voyages}
    return {'data': liste_voyages}


@app.route('/api/dataTransporte')
@login_required
def dataTransport():
    """
    Créé la page api transport avec les bonnes informations en fonctions des filtres
    :return: Un dictionnaire avec une clé 'data' et une valeur d'une liste de dictionnaires.
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout')) 
    liste_transport = []
    res = sessionSQL.query(Deplacer, Transport, Assister).join(Transport, Deplacer.idTransport==Transport.idTransport).join(Assister, Assister.idP == Deplacer.idP).all()
    for transport in res:
        voyages_dico = {}
        voyages_dico["transport"] = transport[1].nomTransport
        voyages_dico["lieuDepart"] = transport[0].lieuDepart
        voyages_dico["dateDepart"] = datetime_to_heure(transport[2].dateArrive)
        voyages_dico["lieuArrive"] = transport[0].lieuArrive
        voyages_dico["date"] = str(transport[2].dateArrive).split(" ")[0]
        voyages_dico["dateArrive"] = datetime_to_heure(transport[2].dateDepart)
        voyages_dico["prenomP"] = get_prenom(transport[0].idP)
        voyages_dico["nomP"] = get_nom(transport[0].idP)
        liste_transport.append(voyages_dico)
    return {'data': liste_transport}


@app.route('/api/dataInvitation', methods = ["POST"])
@login_required
def dataInvitation():
    """
    Créé la page api invitation avec les bonnes informations en fonctions des filtres
    :return: Une liste de dictionnaires.
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))
    liste_participants = []
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    adresseEmail = request.form["adresseEmail"]
    invite = request.form["invite"]
    role = request.form["role"]
    invites = get_info_all_invite(prenom, nom, adresseEmail, invite, role)
    for inv in invites:
        participant_dico = inv.to_dict()
        participant_dico["role"] = get_role(inv.idP)
        participant_dico["invite"] = inv.invite
        liste_participants.append(participant_dico)
    return {'data': liste_participants}


@app.route('/api/dataInterventions', methods = ["POST"])
@login_required
def dataIntervenir():
    """
    Créé la page api interventions avec les bonnes informations en fonctions des filtres
    :return: Un dictionnaire avec une clé 'data' et une valeur d'une liste de dictionnaires.
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout')) 
    liste_intervenir = []
    for intervenir in sessionSQL.query(Intervenir, Intervention, CreneauTravail, Lieu, Auteur).join(
        Intervention, Intervention.idIntervention==Intervenir.idIntervention).join(
        CreneauTravail, CreneauTravail.idCreneau == Intervenir.idCreneau).join(
        Lieu, Lieu.idLieu == Intervenir.idLieu).join(
        Auteur, Auteur.idP == Intervenir.idP).all():
        dico_intervenir = {}
        dico_intervenir["prenom"] = intervenir[4].prenomP
        dico_intervenir["nom"] = intervenir[4].nomP
        dico_intervenir["lieu"] = intervenir[3].nomLieu
        dico_intervenir["typeIntervention"] = intervenir[1].nomIntervention
        dico_intervenir["date"] = str(intervenir[2].dateDebut).split(" ")[0]
        dico_intervenir["dateDebut"] = datetime_to_heure(intervenir[2].dateDebut)
        dico_intervenir["dateArrive"] = datetime_to_heure(intervenir[2].dateFin)
        liste_intervenir.append(dico_intervenir)
    return {'data': liste_intervenir}


@app.route('/interventionsSecretaire/', methods = ["POST", "GET"])
@login_required
def interventions_secretaire():
    """
    Il rend le modèle datatable_interventions.html
    :return: Le modèle datatable_interventions.html est renvoyé.
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))   
    if request.method == "POST":
        return render_template("datatable_interventions.html")
    return render_template('datatable_interventions.html')


@app.route('/participantSecretaire/', methods = ["POST", "GET"])
@login_required
def participant_secretaire():
    """
    Il rend le modèle participantSecretaire.html
    :return: le template de la page participantSecretaire.html
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))   
    if request.method == "POST":
        liste_personne = affiche_participant_trier(request.form["trier"])
        return render_template('participantSecretaire.html', type_participant = TYPE_PARTICIPANT, liste_personne = liste_personne)
    return render_template('participantSecretaire.html', type_participant = TYPE_PARTICIPANT)


@app.route('/secretaireIntervention/', methods = ["POST","GET"])
@login_required
def page_secretaire_intervention():
    """
    Il rend le modèle secretaireIntervention.html
    """
    if not  est_secretaire(current_user.idP):
        return redirect(url_for('logout'))   
    if request.method == 'POST':
        idP = request.form["participant"]
        date_intervention = request.form["date"]
        heure_debut = request.form["debut"]
        heure_fin = request.form["fin"]
        id_lieu = request.form["lieu"]
        id_type = request.form["type"]
        desc = request.form["description"]
        year = date_intervention.split("/")[2]
        month = date_intervention.split("/")[0]
        day = date_intervention.split("/")[1]
        heure_debut2 = datetime.datetime(int(year), int(month), int(day),int(get_heure(heure_debut)[0]), int(get_heure(heure_debut)[1]),0)
        heure_fin2 = datetime.datetime(int(year), int(month), int(day),int(get_heure(heure_fin)[0]), int(get_heure(heure_fin)[1]),0)
        idCreneau = ajoute_creneau_travail(heure_debut2, heure_fin2)
        try : 
            ajoute_intervention(int(idP), idCreneau, int(id_lieu), int(id_type), desc)
        except : 
            print("erreur dans l'ajout de l'intervention")
    return render_template('secretaireIntervention.html', lieux=get_all_lieu(), participants=get_all_auteur(), type_inter=get_all_interventions())


@app.route('/secretaireNavette/', methods = ["POST","GET"])
@login_required
def page_secretaire_navette():
    """
    Envoie à la page pour gérer les navettes
    """
    if not  est_secretaire(current_user.idP):
        return redirect(url_for('logout'))
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        liste_navette = afficher_consommateur(la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaire_consommateur.html', nomsRestau = get_liste_nom_restaurant(), liste_conso = liste_navette)
    return render_template('secretaireNavette.html', nomsRestau = get_liste_nom_restaurant())



@app.route('/secretaireGererTransport/', methods = ["POST","GET"])
@login_required
def page_secretaire_gerer_participants():
    """
    Envoie à la page pour gérer les transports
    """
    if not  est_secretaire(current_user.idP):
        return redirect(url_for('logout'))   
    if request.method == 'POST':
        return render_template('secretaireGererTransport.html')
    return render_template('secretaireGererTransport.html')


@app.route('/secretaire/', methods = ["GET"])
@login_required
def page_secretaire_accueil():
    """
    Envoie à la page accueil de la secretaire
    """
    if  est_secretaire(current_user.idP):
        return render_template("secretaire.html")
    else:
        return redirect(url_for('logout'))

@app.route("/logout/")
@login_required
def logout():
    """
    Permet à un utilisateur de se déconnecter
    """
    logout_user()
    return redirect(url_for("connexion"))

@app.route('/inscrireSecretaire/', methods = ["POST","GET"])
@login_required
def page_secretaire_inscrire():
    """
    Permet à la secrétaire d'inscrire une personne
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))
    if request.method == 'POST':
        role = request.form["role"]
        prenom = request.form["prenom"]
        nom = request.form["nom"]
        email = request.form["email"]
        adresse = request.form["adresse"]
        codePostal = request.form["codePostal"]
        ville = request.form["ville"]
        tel = request.form["tel"]
        ddn = request.form["ddn"]
        ajoute_participant_role(prenom, nom, email, adresse, codePostal, ville, tel, ddn,role)
        return render_template("secretaire.html")
    return render_template("inscrireSecretaire.html", liste_roles=TYPE_PARTICIPANT_FINALE)



@app.route('/inviteSecretaire/', methods = ["POST", "GET"])
@login_required
def invite_secretaire():
    """
    Permet à la secrétaire d'inviter une personne
    """
    if not est_secretaire(current_user.idP):
        return redirect(url_for('logout'))   
    if request.method == "POST":
        liste_personne = affiche_participant_trier(request.form["trier"])
        return render_template('secretaireInvite.html', type_participant = TYPE_PARTICIPANT, liste_personne = liste_personne)
    return render_template('secretaireInvite.html', type_participant = TYPE_PARTICIPANT)

@app.route('/resetInvitations/', methods = ["POST"])
@login_required
def reset_invite():
    """
    Réinitialise toutes les invitations des participants
    """
    reiniatilise_invitation()
    return redirect(url_for("invite_secretaire"))

@app.route('/delete_utilisateur',methods=['POST'])
@login_required
def delete_utilisateur():
    """
    Supprime un utilisateur
    """
    supprimer_utilisateur_role(request.form["id"])
    return ""

@app.route('/delete_consommateur',methods=['POST'])
@login_required
def delete_consommateur():
    """
    Supprime un consommateur
    """
    supprimer_repas_consommateur(request.form["idConsommateur"], request.form["idRepas"])
    return ""

@app.route('/delete_dormeur',methods=['POST'])
@login_required
def delete_dormeur():
    """
    Supprime un dormeur
    """
    supprimer_nuit_dormeur(request.form["idDormeur"], request.form["idHotel"], request.form["dateDeb"], request.form["dateFin"])
    return ""

@app.route("/download")
@login_required
def download_file():
    """
    Télécharge un fichier xlsx avec toutes les informations qu'il y a sur la page
    """
    df = pd.DataFrame.from_dict(session["data"]["data"])
    output = BytesIO()
    with pd.ExcelWriter(output) as writer:
        df.to_excel(writer)
    output.seek(0)
    response = send_file(output, download_name='file.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    return response


def envoie_mail(mail_destination, id_participant):
    """
    Envoie un mail à l'id du participant
    """
    message = Mail(
    from_email="bdboum45@gmail.com",
    to_emails=mail_destination,
    subject='Invitation au festival bdBOUM ' + "2023",
    html_content=cree_mail(id_participant))
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
    except Exception as e:
        print(e)

@app.route('/participantSecretaire/<id>',methods=['POST',"GET"])
@login_required
def participant_detail(id):
    """
    Envoie sur la page participantSecretaire avec toutes les informations nécessaires
    """
    return render_template("detail_participant.html", participant=get_participant(id))

@app.route('/consommateurSecretaire/<id>/<idRepas>',methods=["GET", "POST"])
@login_required
def consommateur_detail(id, idRepas):
    """
    Envoie sur la page consommateurSecretaire avec toutes les informations nécessaires
    """
    creneaux = get_all_creneauxRepas()
    restaurant = get_restaurant(idRepas)
    creneauRepas = get_creneau_repas(idRepas)
    return render_template("detail_consommateur.html", consommateur=get_consommateur(id),
    regimes = get_regime(id), nomRestaurant = restaurant,
    creneauRepas = creneauRepas, dateRepas = get_date_repas(idRepas), idR = idRepas, creneaux = creneaux)

@app.route('/navetteSecretaire/<idP>',methods=["GET"])
@login_required
def navette_detail(idP):
    """
    Envoie sur la page navetteSecretaire avec toutes les informations nécessaires
    """
    date_heure_arrive = get_date_heure_arrive_intervenant(idP)
    date_heure_depart = get_date_heure_depart_intervenant(idP)
    dateArrive = date_heure_arrive.date()
    dateDepart = date_heure_depart.date() 
    heureArrive = date_heure_arrive.time()
    heureDepart = date_heure_depart.time()
    return render_template("detail_navette.html", intervenant=get_intervenant(idP), dateArrive = dateArrive, 
                                                  dateDepart = dateDepart, heureArrive=heureArrive, heureDepart=heureDepart)

@app.route('/dormeurSecretaire/<id>/<idHotel>/<dateDeb>/<dateFin>',methods=["GET", "POST"])
@login_required
def dormeur_detail(id, idHotel, dateDeb, dateFin):
    """
    Envoie sur la page dormeurSecretaire
    """
    return render_template("detail_dormeur.html", intervenant = get_intervenant(id), nomHotel = get_hotel(idHotel), idH = idHotel, DateDeb = dateDeb, DateFin = dateFin)

@app.route('/Personne/Update',methods=['POST'])
@login_required
def UpdateParticipant():
    """
    Permet de récupérer les informations sur la page et de modifier un participant
    """
    id = request.form["id"]
    prenom = request.form["prenom"]
    nom = request.form["nom"]
    email = request.form["email"]
    ddn = request.form["ddn"]
    remarques = request.form["remarques"]
    adresse = request.form["adresse"]
    code_postal = int(request.form["code_postal"])
    ville = request.form["ville"]
    tel = request.form["tel"]
    password = request.form["password"]
    save_participant = modifier_participant(id,adresse,code_postal,ville,date_str_datetime(ddn),tel)
    save_remarques = modif_participant_remarque(id, remarques)
    save_user = modifier_utilisateur(id,prenom,nom,email)
    save_pw = modifier_password(id, password)
    res = save_participant and save_user and save_remarques and save_pw
    return "true" if res == True else res

@app.route('/Consommateur/Update',methods=['POST'])
@login_required
def UpdateConsommateur():
    """
    Permet de récupérer les informations sur la page et de modifier le repas d'un consommateur
    """
    id = request.form["id"]
    dateRepas = request.form["dateRepas"]
    creneauRepas = request.form["creneauRepas"]
    restaurant = request.form["restaurant"]
    idRepas = request.form["idRepas"]
    save_repas = modifier_repas(id, restaurant, dateRepas, creneauRepas, idRepas)
    return "true" if save_repas == True else save_repas

@app.route('/navette/intervenant/update',methods=['POST'])
@login_required
def update_navette_intervenant():
    """
    Permet de récupérer les informations sur la page et de modifier les navettes et les voyages d'un intervenant
    """
    id_personne = request.form["idP"]
    dateArrive = request.form["dateArrive"]
    dateDepart = request.form["dateDepart"]
    heureArrive = request.form["heureArrive"]
    heureDepart = request.form["heureDepart"]
    datetime_arrive = datetime_str_to_datetime(dateArrive, heureArrive)
    datetime_depart = datetime_str_to_datetime(dateDepart, heureDepart)
    ajoute_assister(id_personne, datetime_arrive, datetime_depart)
    supprimer_intervenant_voyage_navette(id_personne)
    affecter_intervenant_voyage_depart_gare(id_personne)
    affecter_intervenant_voyage_depart_festival(id_personne)
    return "true"

@app.route('/Dormeur/Update',methods=['POST'])
@login_required
def UpdateDormeur():
    """
    Permet de récupérer les informations sur la page et de modifier l'hébergement
    """
    id = request.form["id"]
    nomHotel = request.form["Hotel"]
    dateFin = request.form["DateFin"]
    dateDeb = request.form["DateDeb"]
    ancienHotel = request.form["ancienHotel"]
    ancienDateDeb = request.form["ancienDateDeb"]
    ancienDateFin = request.form["ancienDateFin"]

    save_hebergement = modifier_hebergement(id, nomHotel, dateDeb, dateFin, ancienHotel, ancienDateDeb, ancienDateFin)
    return "true" if save_hebergement == True else save_hebergement


@app.route('/invite_les_participants', methods=['POST'])
@login_required
def traitement():
    """
    Il invite les particiants où leur id se trouve dans la liste ids
    """
    ids = request.form.getlist('ids[]')
    for id_participant in ids:
        id_participant = int(id_participant)
        invite_un_participant(id_participant)
        email = get_mail(id_participant)
        if email is not None:
            envoie_mail(email, id_participant)
    # Traiter les IDs récupérés
    return jsonify({"status": "success"})


@app.route("/feuille_route/")
@login_required
def feuille_route():
    """
    Il renvoie vers la feuille de route avec toutes les informations nécessaires
    """
    idP = request.args.get('idP')
    annee = datetime.datetime.now().year
    repas = get_repas(idP, annee)
    return render_template("feuille_route.html", infos_perso=get_participant(idP), transports=requete_transport_annee2(idP, annee),\
        periodes=get_assister(idP, annee), navette=get_navette(idP, annee), repas=repas, regime=get_regime(idP),\
        hotels=(get_dormir(idP, annee)), interventions=get_intervenirs(idP))


    
