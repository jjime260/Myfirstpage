#Ambiente virtual
#Direccionamiento de paginas
from flask import Flask, render_template

app=Flask(__name__)

@app.route("/", methods=["get"])
def home():
    return render_template("index.html")

@app.route("/usuario/registro", methods=["get"])
def register():
    return render_template("registro.html")

@app.route("/usuario", methods=["post"])
def usuario():
    return render_template("usuario.html")

app.run(debug=True)


