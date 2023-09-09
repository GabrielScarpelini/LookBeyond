from flask import Flask, render_template, redirect, url_for, jsonify
from flask import request, session

import cadastro_model

app = Flask(__name__)
app.secret_key = "123456"

@app.route("/", methods=["GET","POST"]) #laguinho monstro
def principal():
    cadastro_model.criarTabelaUsuario_mysql()
    # cadastro_model.criarTabelaTipo()
    # cadastro_model.criarTabelaUsuario()
    
    if request.method == "POST":
        email = request.form.get("login")
        password = request.form.get("senha")
        cadastrado = cadastro_model.loginUser_mysql(email, password)
        print(cadastrado)
        if cadastrado:
           return cadastrado.email
        else:
            return 'uwu'

    return render_template("entrada.html")

@app.route("/cadastro", methods=["GET","POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("name")
        email = request.form.get("email")
        cpf = request.form.get("cpf")
        senha = request.form.get("senha")


        jsonUser = {}
        jsonUser["name"] = nome
        jsonUser["email"] = email
        jsonUser["cpf"] = cpf
        jsonUser["senha"] = senha

        cadastro_model.inserirUsuario_mysql(jsonUser)

        session["dados"] = jsonUser

        return redirect(url_for("show_database", dados=jsonUser))

    return render_template("formCadastro_flask.html") 

@app.route("/show_database", methods=["GET"])

def show_database():   
    dados = cadastro_model.listar_bd_mysql()
    return render_template("listarBd.html", datas=dados)

app.run(app.run(host = 'localhost', port = 5002, debug = True))