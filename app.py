#Ambiente virtual
#Direccionamiento de paginas
from flask import Flask, render_template, request, session, redirect
import sqlite3
import hashlib
from werkzeug.utils import secure_filename
import os

app=Flask(__name__)
FOLDER_IMAGES = 'static/img/'
app.secret_key=os.urandom(15)

#Api general
@app.route("/", methods=["get"])
def home():
    return render_template("index.html")

@app.route("/usuario/registro", methods=["post"])
def registro():
    return render_template("registro.html")

@app.route("/login", methods=["post"])
def login():
    error=[]
    # Captura los datos enviados
    username = request.form["txtUsername"]
    password = request.form["txtPassword"]

    # Validaciones
    if not username or not password:
        error.append("Username and password are required")

    clave= hashlib.sha256(password.encode())
    pwd = clave.hexdigest()

    with sqlite3.connect("DBJ.db") as con:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        cur.execute("SELECT * FROM asd WHERE username = ? AND password = ?",[username, pwd])
        row =cur.fetchone()
        if row:
            session["usuario"] = row["username"]
            return render_template ("usuario.html")

        else:
            error = "Usuario o password no existe"

    return render_template("index.html", error=error)



@app.route("/usuario", methods=["post"])
def register():
    #Captura los datos del usuario
    nombre= request.form["txtNombre"]
    username=request.form["txtUsername"]
    email=request.form["txtEmail"]
    password=request.form["txtPassword"]
    confirm= request.form["txtConfirm"]
    #Validacion de contraseña
    if (password != confirm ):
        return render_template ("registro.html")
    #Aplica la funcion hash(haslib) al password
    clave= hashlib.sha256(password.encode())
    #Convierte el password a hexadecimal tipo string
    pwd = clave.hexdigest()
    #Se conecta a la BD
    with sqlite3.connect("DBJ.db") as con:
        cur = con.cursor()
        #Consultar si ya existe el usuario
        if siExiste(username):
            return "Username already in use"
        #Crea el nuevo usuario
        #cur.execute("INSERT INTO registro2022 (nombre,username,email,password) VALUES (?,?,?,?)",[nombre,username,email,pwd])
        #sdfsfd
        cur.execute("INSERT INTO asd (nombre,username,email,password)VALUES (?,?,?,?)",[nombre,username,email,pwd])
        #sdsdgf
        con.commit()
        return render_template("usuario.html")



def siExiste(username):
    #se conecta a la BD
    with sqlite3.connect("DBJ.db") as con:
        cur = con.cursor()
        #consultar si ya existe el usuario
        cur.execute("SELECT username from asd WHERE username=?",[username])
        if cur.fetchone():
            return True

    return False

@app.route("/logout")
def logout():
    session.pop("usuario",None)
    return redirect("/")

@app.route("/forgotpass")
def password():
    return render_template("forgotpass.html")

@app.route("/terms")
def terminos():
    return render_template("terms.html")

@app.route("/home", methods=["get"])
def main():
    return render_template("usuario.html")

@app.route("/usuario/myprofile")
def myprofile():
    return render_template("profile.html")




