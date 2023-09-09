from sqlalchemy import create_engine
import mysql.connector

#arquivo somente para conectar no banco de dados sqlite

def getConexao():
    engine = create_engine('sqlite:///lab.db')
    return engine

def mySQL_conection():
    config = {
        'user': 'gabriel',
        'password': 'Mudar1234!',
        'host': 'localhost',  # Ou o endereço do servidor MySQL
        'database': 'plataforma_curso',
    }
    conn = mysql.connector.connect(**config)
    return conn