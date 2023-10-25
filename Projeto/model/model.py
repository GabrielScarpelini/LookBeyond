import mysql.connector
from flask import jsonify
import json
class ConectionSQL:
    def __init__(self):
        self.config = {'user': 'root',
        'password': 'mudar123',
        'host': '172.19.0.2',  # Ou o endereço do servidor MySQL
        'database': 'plataforma_curso'
    }
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()


    def Setar_Erro(self, status, verificacao, msg, valor_inserido):
        d = {"status": status,
             "verificacao": verificacao,
             "msg": msg,
             "valor_inserido": valor_inserido}
        return d
    


    def ChecarId(self, id):
        try:
            comando = f'SELECT COUNT(*) FROM usuario WHERE id={id}'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchone()[0]
            return resultado > 0
        except mysql.connector.Error as err:
            response = self.Setar_Erro(500, False, f"Erro ao verificar existencia de ID: {err}", id)
            return False



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
    
    def findById(self, id):
        try:
            comando = f'SELECT * FROM usuario WHERE id={id}'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchall()
            if not resultado:
                return jsonify(self.Setar_Erro(403, False, "Banco sem dados e registros!", None))
            else:
                data = []
                for resul in resultado:
                    status = 'desativado' if resul[5] == '0' else 'ativado'
                    data.append({
                        "id":resul[0], 
                        "nome": resul[1], 
                        "email": resul[2], 
                        "cpf": resul[3], 
                        "senha": resul[4],
                        "atividade": status
                    })
                return data[0]

        except mysql.connector.Error as err:
            return self.Setar_Erro(403, False, f"Erro de execução SQL", err)
        
        except Exception as e:
            return self.Setar_Erro(404, False, f"Houve um erro na lista de usuários", e)

    def SelectUsers(self):
        try:
            comando = f'SELECT * FROM usuario'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchall()
            if not resultado:
                return jsonify(self.Setar_Erro(403, False, "Banco sem dados e registros!", None))
            else:
                data = []
                for resul in resultado:
                    status = 'desativado' if resul[5] == '0' else 'ativado'
                    data.append({
                        "id":resul[0], 
                        "nome": resul[1], 
                        "email": resul[2], 
                        "cpf": resul[3], 
                        "atividade": status
                    })
                return data

        except mysql.connector.Error as err:
            return self.Setar_Erro(403, False, f"Erro de execução SQL", err)
        
        except Exception as e:
            return self.Setar_Erro(404, False, f"Houve um erro na lista de usuários", e)
        
    
    def  UpdateUser(self, nome, email, senha, id):
        try:
            # Verificar se o usuário com o ID fornecido existe
            comando_verificar_existencia = f'SELECT COUNT(*) FROM usuario WHERE id={id}'
            self.cursor.execute(comando_verificar_existencia)
            total_registros = self.cursor.fetchone()[0]
            if total_registros == 0:
                return self.Setar_Erro(404, False, f"Usuário não encontrado", {"name":nome, "email": email, "senha": senha})
            comando = f'UPDATE usuario SET nome="{nome}", email="{email}", senha={senha} WHERE id={id}'
            self.cursor.execute(comando)
            self.conn.commit()
            return {"status": 200, "msg": "Dados atualizados com sucesso!"}
        except mysql.connector.Error as err:
            return self.Setar_Erro(500, False, f"Erro de execução SQL: {err}", None)
        except Exception as e:
            return self.Setar_Erro(500, False, f"Houve um erro na atualização do cadastro: {e}", None)


    def AtivarUser(self, id):
        try:
            if self.ChecarId(id):
                # Verifique se o usuário já está desativado
                comando_verificacao = f'SELECT atividade FROM usuario WHERE id={id}'
                self.cursor.execute(comando_verificacao)
                resultado_verificacao = self.cursor.fetchone()
                # if resultado_verificacao:
                #     status_atual = resultado_verificacao[0]
                #     if status_atual == "0":
                #         return self.Setar_Erro(304, False, f"Usuário de id {id} já está ativado!", id)
                # Caso o usuário não esteja ativo, ative-o
                comando = f'UPDATE usuario SET atividade="1" WHERE id={id}'
                self.cursor.execute(comando)
                self.conn.commit()
                return {"status": 200, "verificacao": True, "msg": "Usuário Ativado!"}
            else: #Caso não encontre dados
                return self.Setar_Erro(500, False, f"Usuário não encontrado!", id)
        except mysql.connector.Error as err: #Erro de execução do MySQL
            return self.Setar_Erro(500, False, f"Erro de SQL: {err}", id)
        except Exception as e:
            return self.Setar_Erro(500, False, f"Erro ao ativar o usuário: {e}", id)


    def InativarUser(self, id):
        try:
            if self.ChecarId(id):
                # Verifique se o usuário já está desativado
                comando_verificacao = f'SELECT atividade FROM Usuario WHERE id={id}'
                self.cursor.execute(comando_verificacao)
                resultado_verificacao = self.cursor.fetchone()
                if resultado_verificacao:
                    status_atual = resultado_verificacao[0]

                    if status_atual == "0":
                        return self.Setar_Erro(304, False, f"Usuário de id {id} já está desativado!", id)
                # Caso o usuário não esteja desativado, desative-o
                comando = f'UPDATE Usuario SET atividade="0" WHERE id={id}'
                self.cursor.execute(comando)
                self.conn.commit()
                return {"status": 200, "verificacao": True, "msg": "Usuário Desativado!"}
            else: #Caso não tenha dados
                return self.Setar_Erro(500, False, f"Usuário não encontrado!", id)
        except mysql.connector.Error as err:
            return self.Setar_Erro(500, False, f"Erro de SQL: {err}", id)
        except Exception as e:
            return self.Setar_Erro(500, False, f"Erro ao desativar o usuário: {e}", id)


    def desativar(self, id):
        try:
            # Verificar se o usuário com o ID fornecido existe
            comando_verificar_existencia = f'SELECT COUNT(*) FROM usuario WHERE id={id}'
            self.cursor.execute(comando_verificar_existencia)
            total_registros = self.cursor.fetchone()[0]
            if total_registros == 0:
                return self.Setar_Erro(404, False, f"Usuário não encontrado")
            comando = f'UPDATE usuario SET atividade=0 WHERE id={id}'
            self.cursor.execute(comando)
            self.conn.commit()
            return {"status": 200, "msg": "Dados atualizados com sucesso!"}
        except mysql.connector.Error as err:
            return self.Setar_Erro(500, False, f"Erro de execução SQL: {err}", None)
        except Exception as e:
            return self.Setar_Erro(500, False, f"Houve um erro na atualização do cadastro: {e}", None)

    def criarTalelas(self):
        # criarTabelaUsuario = """
        #     CREATE TABLE IF NOT EXISTS usuario (
        #     id INT AUTO_INCREMENT PRIMARY KEY,
        #     nome VARCHAR(255) NOT NULL,
        #     email VARCHAR(255) UNIQUE NOT NULL,
        #     cpf_cnpj VARCHAR(255) UNIQUE NOT NULL,
        #     senha VARCHAR(255) NOT NULL,   
        #     atividade CHAR(4)                                                                                                                                                                                                                                   
        # )
        # """

        criarTabelaCursos = """
            CREATE TABLE IF NOT EXISTS curso (
            id INT AUTO_INCREMENT PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            url VARCHAR(255) NOT NULL,
            descricao VARCHAR(255) NOT NULL,
            imagem VARCHAR(255) NOT NULL                                                                                                                                                                                                            
        )
        """
        self.cursor.execute(criarTabelaCursos)

    def inserirCurso(self, titulo, url, descricao, imagem):
        comando = """INSERT INTO curso (titulo, url, descricao, imagem) VALUES (%s, %s, %s, %s)"""
        values = (titulo, url, descricao, imagem)
        self.cursor.execute(comando, values)
        self.conn.commit()
        return jsonify({"status": 200, "msg": "Usuário cadastrado com sucesso!"})
        
    def todosCursos(self):
        comando = f'SELECT * FROM curso'
        self.cursor.execute(comando)
        resultado = self.cursor.fetchall()
        #return jsonify(resultado)
        if not resultado:
                return False
        else:
            data = []
            for resul in resultado:
                data.append({
                    "id":resul[0], 
                    "titulo": resul[1], 
                    "url": resul[2], 
                    "descricao": resul[3],
                    "imagem": resul[4]
                })

            print(data)
            return (data)
    



if __name__ == "__main__":
    b = ConectionSQL()
   