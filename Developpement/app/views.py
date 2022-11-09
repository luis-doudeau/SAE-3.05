from datetime import date
from flask import Flask, render_template, request, redirect, url_for

from .ConnexionPythonSQL import get_info_personne,session,get_nom_restaurant, get_nom_hotel, get_dormeur, afficher_consommateur






app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenny'

@app.route('/', methods = ["GET", "POST"])
def connexion():
    if request.method == "POST":
        email = request.form["email"]
        mdp = request.form["mdp"]
        personne = get_info_personne(session, email, mdp)
        if personne is not None:
            #return render_template('pageInscription.html', prenom = personne.prenomP, nom = personne.nomP, ddn = personne.ddnP, tel = personne.telP)
            return redirect(url_for('pageInscription', idp = personne.idP, prenom = personne.prenomP, nom = personne.nomP, ddn = personne.ddnP, tel = personne.telP, email = personne.emailP))
            #eturn redirect("http://www.example.com", code=302)
        render_template('pageConnexion.html', mail = request.form["email"])
    return render_template('pageConnexion.html', mail = "in@protonmail.edu")


@app.route('/pageInscription/', methods = ["GET", "POST"])
def pageInscription():
    if request.method == "GET":
        return render_template('pageInscription.html', prenom = request.args.get('prenom'), nom = request.args.get('nom'),
                                ddn = request.args.get('ddn'), tel = request.args.get('tel'), email = request.args.get('email'))

    

@app.route('/secretaireConsommateur/', methods = ["POST", "GET"])
def conso():        
    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        print(la_date)
        print(request.form["nomR"])
        print(request.form["heureR"])
        liste_consommateur = afficher_consommateur(session,la_date, request.form["nomR"],request.form["heureR"])
        return render_template('secretaireConsommateur.html', nomsRestau = get_nom_restaurant(), liste_conso = liste_consommateur)
    return render_template('secretaireConsommateur.html', nomsRestau = get_nom_restaurant())
    
@app.route('/dormeurSecretaire/', methods = ["POST", "GET"])
def dormeur_secretaire():
    
    if request.method == "POST":
        la_date = request.form["jours"].replace(",","-")
        print(la_date)
        print(request.form["nomH"])
        liste_dormeur = get_dormeur(session, la_date, int(request.form["nomH"]))
        print(liste_dormeur)
        return render_template('dormeurSecretaire.html', nomHotel = get_nom_hotel())


    return render_template('dormeurSecretaire.html', nomHotel = get_nom_hotel())


@app.route('/pageFormulaireAuteurTransport/', methods = ["POST", "GET"] )
def formulaire_auteur_transport():
    
    if request.method == "POST":
        print(request.form)

    return render_template("pageFormulaireAuteurTransport.html")
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

