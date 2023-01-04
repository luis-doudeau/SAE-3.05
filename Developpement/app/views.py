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

from .ConnexionPythonSQL import get_info_personne, get_regime,session,get_nom_restaurant,\
get_nom_hotel, get_dormeur, afficher_consommateur, est_intervenant, affiche_participant_trier,\
est_secretaire,modifier_participant, ajoute_assister, ajoute_deplacer, modif_participant_remarque, ajoute_avoir_regime,\
ajoute_regime, get_max_id_regime, get_deb_voyage, get_lieu_depart_voyage, get_nom, get_prenom, load_user, get_utilisateur_email_mdp, get_participant, get_secretaire


TYPE_PARTICIPANT = ["Auteur", "Consommateur", "Exposant", "Intervenant", "Invite", "Presse", "Staff", "Secrétaire"]
DATE_FESTIVAL = ["2022-11-17", "2022-11-18", "2022-11-19", "2022-11-20"]
DICO_HORAIRE_RESTAURANT = {"jeudi_soir" : "19:30-22:00", "vendredi_midi": "11:30-14:00", "vendredi_soir":"19:30-22:00", "samedi_midi" : "11:30-14:00", "samedi_soir":"19:30-22:00", "dimanche_midi":"11:30-14:00", "dimanche_soir":"19:30-22:00"}




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
        modifier_participant(session, request.args.get('idp'), request.form["prenom"], request.form["nom"],request.form["ddn"],request.form["tel"],request.form["email"])
        if est_intervenant(session, int(request.args.get('idp'))):
            return redirect(url_for('formulaire_auteur_transport', idp = request.args.get('idp')))
        else:
            return redirect(url_for('page_fin'))
    return render_template('coordonneeForms.html', prenom = request.args.get('prenom'), nom = request.args.get('nom'),
                            ddn = request.args.get('ddn'), tel = request.args.get('tel'), email = request.args.get('email'), adresse = request.args.get("adresse"))

    

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
    
@app.route('/secretaire/dormeur', methods = ["POST", "GET"])
@login_required
def dormeur_secretaire():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    if request.method == "POST":
        la_date = request.form["jours"].split(",")
        print(la_date)
        #liste_dormeur = get_dormeur(session, la_date, request.form["nomH"])
        return render_template("dormeurSecretaire.html",title="TEST")

    return render_template('dormeurSecretaire.html', nomHotel = get_nom_hotel())

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
    for consommateur in session.query(Consommateur).all():
        consommateur_dico = consommateur.to_dict_sans_ddn()
        consommateur_dico["regime"] = get_regime(session, consommateur.idP)
        liste_consommateur.append(consommateur_dico)
    return {'data': liste_consommateur}

@app.route('/api/dataNavettes')
@login_required
def dataNavettes():
    if not current_user.est_secretaire():
        return redirect(url_for('logout')) 
    liste_voyages = []
    print(session.query(Mobiliser).all())
    for voyages in session.query(Mobiliser).all():
        print(voyages)
        voyages_dico = voyages.to_dict()
        voyages_dico["heureDeb"] = get_deb_voyage(session, voyages.idVoy)
        voyages_dico["depart"] = get_lieu_depart_voyage(session, voyages.idVoy)
        for elements in session.query(Transporter).filter(Transporter.idVoy == voyages.idVoy).all():
            voyages_dico["prenom"] = get_prenom(session, elements.idP)
            voyages_dico["nom"] = get_nom(session, elements.idP)
            liste_voyages.append(voyages_dico)
    return {'data': liste_voyages}

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
                    ajoute_deplacer(session, request.args.get('idp'), 1, depart, "Blois")
                elif liste_id_box[i] == "train":
                    depart = request.form[liste_id_champs[i]]
                    ajoute_deplacer(session, request.args.get('idp'), 2, depart, "Blois")
                elif liste_id_box[i] == "voiture": 
                    ajoute_deplacer(session, request.args.get('idp'), 3, str(request.args.get('adresse')), "Blois")
                elif liste_id_box[i] == "covoiturage": 
                    ajoute_deplacer(session, request.args.get('idp'), 4, request.args.get('adresse'), "Blois")
                else :
                    modif_participant_remarque(session, request.args.get('idp'), " / Moyen de déplacement : "+depart)    
        
        dateArr = request.form["dateArr"].replace("-",",").split(",")
        heureArr = request.form["hArrive"].replace(":",",").split(",")
        date_arr = datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(heureArr[0]), int(heureArr[1]))

        dateDep = request.form["dateDep"].replace("-",",").split(",")
        heureDep = request.form["hDep"].replace(":",",").split(",")
        date_dep = datetime(int(dateDep[0]), int(dateDep[1]), int(dateDep[2]), int(heureDep[0]), int(heureDep[1]))
        print(request.form["hDep"])
        ajoute_assister(session, request.args.get('idp'), date_arr, date_dep)
        return redirect(url_for('formulaire_reservation', idp=request.args.get('idp')))
        
    return render_template("transportForms.html", idp=request.args.get('idp'))
    
@app.route('/FormulaireReservation/', methods = ["POST", "GET"])
@login_required
def formulaire_reservation():
    if current_user.est_secretaire():
        return redirect(url_for("page_secretaire_accueil"))
    if request.method == "POST":
        regime = request.form["regime"]
        if regime.isalpha():
            id_regime = ajoute_regime(session, regime)
            ajoute_avoir_regime(session, request.args.get('idp'), id_regime)
        remarques = request.form["remarques"]
        modif_participant_remarque(session, request.args.get('idp'), remarques)
        a = request.form['jeudi_soir']
        for creneau in DICO_HORAIRE_RESTAURANT.keys():
            pass
            #print(request.form["jeud"])  
                
        
    return render_template("formulaireReservation.html", idp=request.args.get('idp'))

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



@app.route('/secretaireGererParticipants/', methods = ["POST","GET"])
@login_required
def page_secretaire_gerer_participants():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    if request.method == 'POST':
        return render_template('secretaireGererParticipants.html')
    return render_template('secretaireGererParticipants.html')


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

@app.route('/inviterSecretaire/', methods = ["GET"])
@login_required
def page_secretaire_inviter():
    if not current_user.est_secretaire():
        return redirect(url_for('logout'))   
    return render_template("inviterSecretaire.html")

#Ne pas effacer test
"""@app.before_request
def before_request():
    if request.endpoint in LISTE_ROUTE:
        print("JE change de page")
        print("path ",request.path)
        print("request ",request)
        print("referrer ",request.referrer)
        print("Ref2:", request.values.get("url"))"""
