import mysql.connector
from flask import jsonify

class ConectionSQL:
    def __init__(self):
        self.config = {'user': 'root',
        'password': 'Joao$131103',
        'host': 'localhost',  # Ou o endereço do servidor MySQL
        'database': 'plataforma_curso',
    }
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()


    def Setar_Erro(self, status, verificacao, msg, valor_inserido):
        d = {"status": status,
             "verificacao": verificacao,
             "msg": msg,
             "valor_inserido": valor_inserido}
        return d


    def ChecarEmail(self, email):
        try:
            comando_verificar = f'SELECT COUNT(*) FROM usuario WHERE email="{email}"'
            self.cursor.execute(comando_verificar)
            total_registros = self.cursor.fetchone()[0]
            return total_registros > 0
        except mysql.connector.Error as err:
            response = self.Setar_Erro(500, False, f"Erro ao verificar duplicidade: {err}", email)
            return False

    def ChecarDuplicidade(self, nome):
        try:
            comando_verificar = f'SELECT COUNT(*) FROM usuario WHERE nome="{nome}"'
            self.cursor.execute(comando_verificar)
            total_registros = self.cursor.fetchone()[0]
            return total_registros > 0
        except mysql.connector.Error as err:
            response = self.Setar_Erro(500, False, f"Erro ao verificar duplicidade: {err}", nome)
            print(response)
            return response["verificacao"]
    

    def InsertUser(self, name, email, cpf, senha):
        try:
            if not name or not email or not cpf or not senha:
                return jsonify(self.Setar_Erro(403, False, "Erro! Todos os valores de cadastro precisam ser inseridos.", {"nome": name, "email": email, "cpf/cnpj": cpf, "senha": senha}))
            
            if self.ChecarDuplicidade(name):
                return jsonify(self.Setar_Erro(403, False, "Erro! Cadastro já foi realizado!", name))
            
            comando = """INSERT INTO usuario (nome, email, cpf_cnpj, senha) VALUES (%s, %s, %s, %s)"""
            values = (name, email, cpf, senha)
            self.cursor.execute(comando, values)
            self.conn.commit()
            return jsonify({"status": 200, "msg": "Usuário cadastrado com sucesso!"})
        except mysql.connector.Error as err:
            return jsonify(self.Setar_Erro(403, False, f"Erro de execução SQL", err))
        
        except Exception as e:
            return jsonify(self.Setar_Erro(403, False, f"Um erro ocorreu em cadastro!", e))

        
    def loginUser_mysql(self, email, password):
        try:
            comando = "SELECT email FROM usuario WHERE email = %s AND senha = %s"
            values = (email, password)
            print("Comando SQL:", comando, "Valores:", values)  # Adicione esta linha
            self.cursor.execute(comando, values)
            usuario = self.cursor.fetchall()
            print("Resultado da consulta:", usuario)  # Adicione esta linha

            if not usuario:
                return jsonify(self.Setar_Erro(404, False, "Usuário não cadastrado!", {"email": email, "pass": password}))
            return {"status": 200, "msg": "Usuário logado!"}
        
        except mysql.connector.Error as err:
            return jsonify(self.Setar_Erro(500, False, f"Erro ao executar o comando SQL: {err}", None))
    
        except Exception as e:
            return jsonify(self.Setar_Erro(500, False, f"Erro ao executar a consulta do usuário: {e}", None))
    

    def SelectUsers(self):
        try:
            comando = f'SELECT * FROM usuario'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchall()
            if not resultado:
                return self.Setar_Erro(403, False, "Banco sem dados e registros!", None)
            else:
                data = []
                for resul in resultado:
                     data.append({"id":resul[0], "nome": resul[1], "email": resul[2], "documento": resul[3]})
                return data
        except mysql.connector.Error as err:
            return self.Setar_Erro(403, False, f"Erro de execução SQL", err)
        
        except Exception as e:
            return self.Setar_Erro(404, False, f"Houve um erro na lista de usuários", e)


if __name__ == "__main__":
    b = ConectionSQL()
    #print(b.InsertUser("Lucas", "lucas@lucas", "23456789122", "senha"))
    print(b.loginUser_mysql("noa@noa", "123"))
    #print(b.SelectUsers())
