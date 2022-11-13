from datetime import date, datetime
from flask import Flask, render_template, request, redirect, url_for

from .ConnexionPythonSQL import get_info_personne,session,get_nom_restaurant,\
get_nom_hotel, get_dormeur, afficher_consommateur, est_intervenant, affiche_participant_trier,\
est_secretaire,modifier_participant, ajoute_assister, ajoute_deplacer, modif_participant_que_id


TYPE_PARTICIPANT = ["Auteur", "Consommateur", "Exposant", "Intervenant", "Invite", "Presse", "Staff", "Secrétaire"]
DATE_FESTIVAL = ["2022-11-17", "2022-11-20"]



app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenny'

@app.route('/', methods = ["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form["email"]
        mdp = request.form["mdp"]
        if est_secretaire(session, email, mdp):
            return redirect(url_for("page_secretaire_accueil"))
        personne = get_info_personne(session, email, mdp)
        print(personne)
        if personne is not None:
            print(personne)
            return redirect(url_for('page_inscription', idp = personne.idP, prenom = personne.prenomP, nom = personne.nomP,adresse = personne.adresseP, ddn = personne.ddnP, tel = personne.telP, email = personne.emailP),code = 302)
        render_template('pageConnexion.html', mail = request.form["email"])
    return render_template('pageConnexion.html', mail = "ac@icloud.ca")


@app.route('/pageInscription/', methods = ["GET", "POST"])
def page_inscription():
    if request.method == "POST":
        print(request.form)
        modifier_participant(session, request.args.get('idp'), request.form["prenom"], request.form["nom"],request.form["ddn"],request.form["tel"],request.form["email"])
        if est_intervenant(session, int(request.args.get('idp'))):
            return redirect(url_for('formulaire_auteur_transport', idp = request.args.get('idp')))
        else:
            return redirect(url_for('page_fin'))
    print(request.args.get("adresse"))
    print(type(request.args.get("adresse")))
    return render_template('pageInscription.html', prenom = request.args.get('prenom'), nom = request.args.get('nom'),
                            ddn = request.args.get('ddn'), tel = request.args.get('tel'), email = request.args.get('email'), adresse = request.args.get("adresse"))

    

@app.route('/secretaire_consommateur/', methods = ["POST", "GET"])
def secretaire_consommateur():        
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        liste_consommateur = afficher_consommateur(session,la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaire_consommateur.html', nomsRestau = get_nom_restaurant(), liste_conso = liste_consommateur)
    return render_template('secretaire_consommateur.html', nomsRestau = get_nom_restaurant())
    
@app.route('/dormeurSecretaire/', methods = ["POST", "GET"])
def dormeur_secretaire():
    if request.method == "POST":
        la_date = request.form["jours"].split(",")
        print(la_date)
        liste_dormeur = get_dormeur(session, la_date, request.form["nomH"])
        return render_template('dormeurSecretaire.html', nomHotel = get_nom_hotel(), liste_dormeur = liste_dormeur)

    return render_template('dormeurSecretaire.html', nomHotel = get_nom_hotel())

@app.route('/participantSecretaire/', methods = ["POST", "GET"])
def participant_secretaire():
    if request.method == "POST":
        print(request.form["trier"])
        liste_personne = affiche_participant_trier(session, request.form["trier"])
        return render_template('participantSecretaire.html', type_participant = TYPE_PARTICIPANT, liste_personne = liste_personne)
        
    return render_template('participantSecretaire.html', type_participant = TYPE_PARTICIPANT)


@app.route('/pageFormulaireAuteurTransport/', methods = ["POST", "GET"] )
def formulaire_auteur_transport():
    if request.method == "POST":
        liste_id_box = ["avion", "train", "autre", "voiture", "covoiturage"]
        liste_id_champs = ["aeroport", "gare", "precision"]
        for i in range(len(liste_id_box)-1):
            if request.form.get(liste_id_box[i]) == "on":
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
                    modif_participant_que_id(session, request.args.get('idp'), " / Moyen de déplacement : "+depart)    
        
        dateArr = request.form["dateArr"].replace("-",",").split(",")
        heureArr = request.form["hArrive"].replace(":",",").split(",")
        date_arr = datetime(int(dateArr[0]), int(dateArr[1]), int(dateArr[2]), int(heureArr[0]), int(heureArr[1]))

        dateDep = request.form["dateDep"].replace("-",",").split(",")
        heureDep = request.form["hDep"].replace(":",",").split(",")
        date_dep = datetime(int(dateDep[0]), int(dateDep[1]), int(dateDep[2]), int(heureDep[0]), int(heureDep[1]))
        
        ajoute_assister(session, request.args.get('idp'), date_arr, date_dep)

    return render_template("pageFormulaireAuteurTransport.html")
    

@app.route('/secretaireNavette/', methods = ["POST","GET"])
def page_secretaire_navette():
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        liste_navette = afficher_consommateur(session,la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaire_consommateur.html', nomsRestau = get_nom_restaurant(), liste_conso = liste_consommateur)
    return render_template('secretaireNavette.html', nomsRestau = get_nom_restaurant())


@app.route('/pageFin/', methods = ["GET"])
def page_fin():
    return render_template("pageFin.html")

@app.route('/secretaire/', methods = ["GET"])
def page_secretaire_accueil():
    return render_template("secretaire.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

