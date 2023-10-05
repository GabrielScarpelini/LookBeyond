from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from model.model import ConectionSQL

app = Flask(__name__)
CORS(app)  # Permite solicitações de diferentes origens (CORS)

@app.route('/')
def entrar():
    return render_template('login.html')


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
            return render_template('login.html') # Cadastro bem-sucedido, redireciona para uma nova página
            
        return response
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

# Rota para autenticar um usuário
@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        email = request.form['email']
        senha = request.form['senha']
        connection = ConectionSQL()
        user = connection.loginUser_mysql(email, senha)
        checar = connection.ChecarEmail(email)
        print(checar)
        if checar == 1:
            return redirect('/area_logada')
        return user
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

@app.route('/area_logada')
def homePage():
    return render_template('home.html')

# Rota para listar todos os usuários
@app.route('/show_database', methods=['GET'])
def listar_usuarios():
    try:
        connection = ConectionSQL()
        users = connection.SelectUsers()
        return render_template("listar.html", datas=users)
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

@app.route('/desativar/<int:id>', methods=['PUT'])
def desativarUser(id):
    connection = ConectionSQL()
    checar = connection.InativarUser(id)
    if checar == 1:
        return redirect('#')

@app.route('/atualizar/<int:id>', methods=['PUT'])
def atualizarUser(id):
    return render_template('atualizar.html')
    
@app.route('/tabela')
def criar_tabela():
    con = ConectionSQL()
    con.criarTalelas()
    return 'tabela criada'

if __name__ == '__main__':
    app.run(debug=True)
