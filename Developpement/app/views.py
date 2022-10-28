from flask import Flask, render_template, request

from modele.ConnexionPythonSQL import get_info_personne,session






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
    if personne[0] is True:
        return render_template('pageInscription.html', prenom = personne[1].prenomP)



if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

