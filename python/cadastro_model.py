from flask import jsonify
import conexao_bd

conn = conexao_bd.mySQL_conection()
cursor = conn.cursor()
 
def criarTabelaUsuario_mysql():
    create_tabela_usuario = """       
        CREATE TABLE IF NOT EXISTS usuario (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nome VARCHAR(255) NOT NULL,
            email VARCHAR(255) UNIQUE NOT NULL,
            cpf_cnpj VARCHAR(255) UNIQUE NOT NULL,
            senha CHAR(15) NOT NULL                                                                                                                           
        )
        """
    cursor.execute(create_tabela_usuario)
    conn.commit()

def inserirUsuario_mysql(usuario):
    nome = usuario['name']
    email = usuario['email']
    cpf = usuario['cpf']
    senha = usuario['senha']
    statement = """INSERT INTO usuario (nome, email, cpf_cnpj, senha) VALUES (%s, %s, %s, %s)"""
    values = [nome, email, cpf, senha]
    cursor.execute(statement, values)
    conn.commit()

def loginUser_mysql(email, password):
    statement = ("SELECT * FROM Usuario WHERE email = %s AND senha= %s",(email, password)) #esse parenteses aqui está passando os params
    rs = conn.execute(statement)
    usuario = rs.fetchone() 
    print(usuario)
    if usuario == None:
        return None
    # result = [dict(user) for user in usuario]
    return usuario

def listar_bd_mysql():
    conn = conexao_bd.mySQL_conection()
    cursor = conn.cursor()
    statements = "SELECT * FROM usuario"
    cursor.execute(statements)
    usuarios = cursor.fetchall()
    lista = []

    for tupla in usuarios:
        lista.append({"id":tupla[0], "nome": tupla[1], "email": tupla[2], "cpf": tupla[3]})

    return lista

