from datetime import date
from flask import Flask, render_template, request

from .ConnexionPythonSQL import get_info_personne,session,get_nom_restaurant, get_nom_hotel, get_dormeur






app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenny'

@app.route('/')
def hello():
    return render_template('pageConnexion.html')


@app.route('/', methods = ["POST"])
def suite():
    email = request.form["email"]
    mdp = request.form["mdp"]
    personne = get_info_personne(session, email, mdp)
    if personne is not None:
        return render_template('pageInscription.html', prenom = personne.prenomP, nom = personne.nomP, ddn = personne.ddnP, tel = personne.telP)

@app.route('/secretaireConsommateur/', methods = ["POST", "GET"])
def conso():
    if request.method == "GET":
        return render_template('secretaireConsommateur.html', nomsRestau = get_nom_restaurant())

    if request.method == 'POST':
        la_date = request.form["jours"].split(",")
        jour = date(int(la_date[0]),int(la_date[1]),int(la_date[2]))
        print(jour)
        print(request.form["nomR"])
        print(request.form["heureR"])
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

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

