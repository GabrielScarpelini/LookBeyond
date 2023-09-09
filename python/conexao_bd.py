import mysql.connector

def mySQL_conection():
    config = {
        'user': 'gabriel',
        'password': 'Mudar1234!',
        'host': 'localhost',  # Ou o endereço do servidor MySQL
        'database': 'plataforma_curso',
    }
    conn = mysql.connector.connect(**config)
    return conn