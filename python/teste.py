from flask import jsonify
import conexao_bd
conn = conexao_bd.mySQL_conection()
cursor = conn.cursor()

def listar_aluno_mysql():
    conn = conexao_bd.mySQL_conection()
    cursor = conn.cursor()
    statements = "SELECT * FROM usuario"
    cursor.execute(statements)
    usuarios = cursor.fetchall()
    lista = []

    for tupla in usuarios:
        lista.append({"id":tupla[0], "nome": tupla[1], "email": tupla[2], "cpf": tupla[3]})

    return lista

        

data = listar_aluno_mysql()
print(data[0])

