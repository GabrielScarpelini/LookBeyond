from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
#from flask_cors import CORS
from model.model import ConectionSQL

app = Flask(__name__)
app.secret_key = "123456"
#CORS(app)  # Permite solicitações de diferentes origens (CORS)

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
def show_database():
    try:
        connection = ConectionSQL()
        users = connection.SelectUsers()
        return render_template("listar.html", datas=users)
    except Exception as e:
        return jsonify({"status": 500, "msg": f"Erro interno: {str(e)}"})

@app.route('/desativar/<int:id>')
def desativar(id):
    con = ConectionSQL()
    con.desativar(id)
    flash('Usuário desativado com sucesso!')
    return redirect(url_for('show_database'))

@app.route('/editar/<int:id>') 
def editar(id):
    con = ConectionSQL()
    user = con.findById(id)
    return render_template('editar.html', user=user)

    
@app.route('/atualizar', methods=['POST'])
def atualizar():
    id = request.form['id']
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']
    con = ConectionSQL()
    con.UpdateUser(nome, email, senha, id)

    return redirect(url_for('show_database'))
    

@app.route('/ativar/<int:id>')
def ativar(id):
    con = ConectionSQL()
    con.AtivarUser(id)
    return redirect(url_for('show_database'))
    
@app.route('/tabela')
def criar_tabela():
    con = ConectionSQL()
    con.criarTalelas()
    return 'tabela criada'


if __name__ == '__main__':
     app.run(debug=True)
