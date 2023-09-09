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
    # if usuarios == []:                       #se nao tinha nenhuma linha
    #     return None
    # result = [dict(aluno) for aluno in usuarios]
    lista = []
    cont = 0 
    for tupla in usuarios:
        lista.append({"id":tupla[0], "nome": tupla[1], "email": tupla[2], "cpf": tupla[3]})

    return lista

        

# print(listar_aluno_mysql())
print(listar_aluno_mysql())