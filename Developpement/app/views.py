from crypt import methods
from flask import Flask, render_template, request



app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenny'

@app.route('/')
def hello():
    return render_template('pageConnexion.html')


@app.route('/', methods = ["POST"])
def suite():
    print(request.form)

    return render_template('pageInscription.html')

