from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_cors import CORS
from model.model import ConectionSQL

app = Flask(__name__)
app.secret_key = "123456"
CORS(app)  # Permite solicitações de diferentes origens (CORS)
user_id = None


@app.route('/')
def entrar():
    return render_template('login.html')
@app.route('/curso')
def cadastroCurso():
    return render_template('cadastro_curso.html')

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
    
@app.route('/cadastrar_curso', methods=['POST'])
def cadastrar_curso():
    url=request.form['url']
    titulo=request.form['titulo']
    descricao=request.form['descricao']
    imagem=request.form['imagem']
    connection = ConectionSQL()
    response = connection.inserirCurso(titulo, url, descricao, imagem)
    if response.status_code == 200:
        flash("curso cadastrado com sucesso")
        return redirect('/cursos')
    return flash("Não foi possivel cadastrar curso tente masi tarde")

@app.route('/cursos', methods=['GET'])
def todosOsCursos():
    connection = ConectionSQL()
    cursos = connection.todosCursos()
    if cursos == False:
        return render_template('error.html')
    return render_template('mostrar_cursos.html', data=cursos)
    


# Rota para autenticar um usuário
@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        email = request.form['email']
        senha = request.form['senha']
        connection = ConectionSQL()
        user = connection.loginUser_mysql(email, senha)
        global user_id
        user_id = user[0]['id']
        checar = connection.ChecarEmail(email)
        if user == False:
            return render_template("login.html")
        elif email != 'admin@teste.com.br':
            return redirect('/curso_user')
        flash("Login realizafdo com sucesso!")
        return redirect('/area_logada')
    #     print(checar)
    #     if checar == 1:
    #         return redirect('/area_logada')
    #     return user
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

@app.route('/curso_user')
def cursos_user():
    connection = ConectionSQL()
    cursos = connection.todosCursos()
    if cursos == False:
        return render_template('error.html')
    return render_template('mostrarCursoUser.html', data=cursos)

@app.route('/meus_cursos')
def meusCursos():
    con = ConectionSQL()
    cursos = con.buscarCursoPeloId()
    if cursos == False:
        return render_template('erroCurso.html')
    return render_template('meusCursos.html', data=cursos)

@app.route('/matriculas/<int:id>')
def matriculasPeloId(id):
    con = ConectionSQL()
    resultado =con.buscarMatricula(id)
    print(resultado)
    return render_template('meusCursos.html')

@app.route('/matricular_curso/<int:id>')
def matricular_curso(id):
    con = ConectionSQL()
    user = con.matricularNoCurso()
    curso = con.cursoId(id)
    return render_template('matricula.html', user=user, curso=curso)

@app.route('/realiza_matricula/', methods=['POST'])
def realizar_matricula():
    id_curso = request.form['id']
    con = ConectionSQL()
    con.matricula(id_curso)
    return redirect('/meus_cursos')

if __name__ == '__main__':
    app.run(debug=True)
