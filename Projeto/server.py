from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import mysql.connector
from model.model import ConectionSQL

app = Flask(__name__)
CORS(app)  # Permite solicitações de diferentes origens (CORS)

@app.route('/')
def entrar():
    return render_template('entrada.html')


@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

# Rota para cadastrar um usuário
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    try:
        name = request.form["name"]
        email = request.form["email"]
        cpf = request.form["cpf"]
        senha = request.form["senha"]
        connection = ConectionSQL()
        response = connection.InsertUser(name, email, cpf, senha)
        if response.status_code == 200:  # Verifica se o cadastro foi bem-sucedido
            # Cadastro bem-sucedido, redireciona para uma nova página
            return render_template('acesso.html') 
        return response
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

# Rota para autenticar um usuário
@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        email = request.form['login']
        senha = request.form['senha']
        connection = ConectionSQL()
        user = connection.loginUser_mysql(email, senha)
        checar = connection.ChecarEmail(email)
        print(checar)
        if checar == 1:
            return render_template("acesso.html")
        return user
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

# Rota para listar todos os usuários
@app.route('/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        connection = ConectionSQL()
        users = connection.SelectUsers()
        return render_template("listarBd.html", datas=users)
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

if __name__ == '__main__':
    app.run(debug=True)
