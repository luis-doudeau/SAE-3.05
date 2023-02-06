from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'lenny'


    

@app.route('/secretaire/', methods = ["GET"])
def page_secretaire_accueil():
    return render_template("secretaire2.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

